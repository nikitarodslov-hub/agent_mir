"""
Bitrix24 Open Lines browser monitor using Playwright.

Selectors are written for a typical Bitrix24 cloud installation.
If your version differs, adjust SELECTORS below to match actual DOM.
"""

import asyncio
import json
import logging
import os
from datetime import date
from typing import Callable, Optional

from playwright.async_api import (
    Browser,
    BrowserContext,
    Page,
    Playwright,
    async_playwright,
)

logger = logging.getLogger(__name__)

# CSS selectors for Bitrix24 Open Lines interface.
# These cover common Bitrix24 cloud and self-hosted versions.
SELECTORS = {
    # Login page
    "login_input": "input[name='LOGIN'], input[type='text'][autocomplete='username']",
    "password_input": "input[name='PASSWORD'], input[type='password']",
    "login_button": "button[type='submit'], input[type='submit']",
    # Open lines navigation
    "openlines_link": "a[href*='crm/chats'], a[href*='open-lines'], a[href*='openlines']",
    # Tab "Неотвеченные" (Unanswered)
    "unanswered_tab": (
        "span:has-text('Неотвеченные'), "
        "a:has-text('Неотвеченные'), "
        "div[data-type='unread']:has-text('Неотвеченные')"
    ),
    # Dialog list items in the sidebar
    "dialog_items": (
        ".bx-im-recent-item, "
        ".bx-im-list-item, "
        ".bx-messenger-item, "
        "[class*='recent-item'], "
        "[class*='chat-item']"
    ),
    # Unread counter badge on a dialog item
    "unread_badge": (
        ".bx-im-recent-item-counter, "
        ".bx-im-counter, "
        "[class*='counter']:not([class*='total']), "
        ".bx-messenger-item-unread-counter"
    ),
    # Client name in open dialog header
    "client_name": (
        ".bx-im-dialog-header-name, "
        ".bx-im-chat-title, "
        ".bx-imsettings-profile-name, "
        "[class*='header-name'], "
        "[class*='chat-name']"
    ),
    # Source channel (VK, Avito, etc.)
    "source_channel": (
        ".bx-im-open-line-source, "
        "[class*='open-line-source'], "
        "[class*='channel-name'], "
        ".bx-im-dialog-header-desc"
    ),
    # Message text items in conversation
    "message_items": (
        ".bx-im-message-text, "
        "[class*='message-text'], "
        ".bx-messenger-content-message-text"
    ),
    # Message input field
    "message_input": (
        ".bx-im-message-form-input-container textarea, "
        ".bx-im-textarea, "
        "[contenteditable='true'][class*='input'], "
        "textarea[class*='message']"
    ),
    # Send button
    "send_button": (
        ".bx-im-message-form-button-send, "
        "button[class*='send'], "
        "[class*='send-button']"
    ),
}

# How long to wait for selectors (ms)
TIMEOUT_SHORT = 3_000
TIMEOUT_LONG = 10_000


class BitrixMonitor:
    def __init__(
        self,
        bitrix_url: str,
        openlines_path: str = "/crm/chats/",
        session_file: str = "bitrix_session.json",
        processed_file: str = "processed_dialogs.json",
    ):
        self.bitrix_url = bitrix_url.rstrip("/")
        self.openlines_url = self.bitrix_url + openlines_path
        self.session_file = session_file
        self.processed_file = processed_file

        self._playwright: Optional[Playwright] = None
        self._browser: Optional[Browser] = None
        self._context: Optional[BrowserContext] = None
        self._page: Optional[Page] = None
        self._running = False
        self._current_dialog_id: Optional[str] = None

        self._processed: set[str] = self._load_processed()

    # ------------------------------------------------------------------ #
    # Public API
    # ------------------------------------------------------------------ #

    async def start(self, on_new_message: Callable) -> None:
        self._playwright = await async_playwright().start()
        storage = self.session_file if os.path.exists(self.session_file) else None

        self._browser = await self._launch_browser()

        ctx_kwargs: dict = {"viewport": {"width": 1280, "height": 900}}
        if storage:
            ctx_kwargs["storage_state"] = storage

        self._context = await self._browser.new_context(**ctx_kwargs)
        self._page = await self._context.new_page()

        await self._page.goto(self.openlines_url, wait_until="domcontentloaded")
        await self._ensure_logged_in()
        await self._save_session()
        await self._navigate_to_unanswered()

        self._running = True
        await self._monitor_loop(on_new_message)

    async def _launch_browser(self) -> Browser:
        """Try Edge → Chrome → downloaded Chromium, return first that works."""
        launch_attempts = [
            # Microsoft Edge — pre-installed on every Windows 10/11 machine
            dict(channel="msedge", headless=False),
            # Google Chrome — most common browser
            dict(channel="chrome", headless=False),
            # Playwright's own Chromium (requires `playwright install chromium`)
            dict(headless=False, args=["--no-sandbox", "--disable-setuid-sandbox"]),
        ]
        last_exc: Exception = RuntimeError("No browser available")
        for kwargs in launch_attempts:
            try:
                browser = await self._playwright.chromium.launch(**kwargs)
                logger.info("Browser launched with: %s", kwargs)
                return browser
            except Exception as exc:
                last_exc = exc
                logger.debug("Browser launch failed (%s): %s", kwargs, exc)
        raise RuntimeError(
            "Не удалось запустить браузер.\n"
            "Установите Microsoft Edge или Google Chrome,\n"
            "либо выполните: playwright install chromium"
        ) from last_exc

    async def send_message(self, text: str) -> bool:
        """Type and send a message in the currently open dialog."""
        if not self._page:
            return False
        try:
            input_el = await self._page.wait_for_selector(
                SELECTORS["message_input"], timeout=TIMEOUT_LONG
            )
            await input_el.click()
            await input_el.fill("")
            await input_el.type(text, delay=10)
            await asyncio.sleep(0.3)

            send_btn = await self._page.query_selector(SELECTORS["send_button"])
            if send_btn:
                await send_btn.click()
            else:
                await input_el.press("Enter")

            logger.info("Message sent successfully")
            return True
        except Exception as exc:
            logger.error("send_message failed: %s", exc)
            return False

    async def stop(self) -> None:
        self._running = False
        if self._browser:
            await self._browser.close()
        if self._playwright:
            await self._playwright.stop()

    # ------------------------------------------------------------------ #
    # Internal helpers
    # ------------------------------------------------------------------ #

    async def _ensure_logged_in(self) -> None:
        """If on login page, wait until user logs in manually."""
        try:
            await self._page.wait_for_selector(
                SELECTORS["login_input"], timeout=TIMEOUT_SHORT
            )
            logger.info("Login page detected — waiting for manual login…")
            # Wait until URL changes away from login page (up to 5 min)
            await self._page.wait_for_url(
                lambda url: "login" not in url.lower(), timeout=300_000
            )
            await asyncio.sleep(2)
        except Exception:
            # Not on login page — already authenticated
            pass

    async def _navigate_to_unanswered(self) -> None:
        """Open Open Lines and click the 'Неотвеченные' tab."""
        try:
            await self._page.goto(self.openlines_url, wait_until="domcontentloaded")
            await asyncio.sleep(2)
            tab = await self._page.query_selector(SELECTORS["unanswered_tab"])
            if tab:
                await tab.click()
                await asyncio.sleep(1)
        except Exception as exc:
            logger.warning("Could not navigate to unanswered tab: %s", exc)

    async def _monitor_loop(self, on_new_message: Callable) -> None:
        consecutive_errors = 0
        while self._running:
            try:
                dialogs = await self._find_unread_dialogs()
                for dialog_id, element in dialogs:
                    if dialog_id in self._processed:
                        continue
                    # Mark immediately to avoid double-processing
                    self._processed.add(dialog_id)
                    self._save_processed()

                    data = await self._extract_dialog(dialog_id, element)
                    if data:
                        await on_new_message(data)
                        # Pause to let manager respond before next dialog
                        await asyncio.sleep(2)

                consecutive_errors = 0
                await asyncio.sleep(5)
            except Exception as exc:
                logger.error("Monitor loop error: %s", exc)
                consecutive_errors += 1
                wait = min(60, 5 * consecutive_errors)
                await asyncio.sleep(wait)
                await self._try_recover()

    async def _find_unread_dialogs(self) -> list[tuple[str, object]]:
        """Return (dialog_id, element) pairs that have unread messages."""
        result = []
        try:
            items = await self._page.query_selector_all(SELECTORS["dialog_items"])
            for item in items:
                badge = await item.query_selector(SELECTORS["unread_badge"])
                if not badge:
                    continue
                badge_text = (await badge.inner_text()).strip()
                if not badge_text or badge_text == "0":
                    continue
                # Derive a stable ID from element attribute or position
                dialog_id = (
                    await item.get_attribute("data-id")
                    or await item.get_attribute("data-cid")
                    or await item.get_attribute("id")
                )
                if not dialog_id:
                    # Fallback: use inner text hash as id
                    inner = await item.inner_text()
                    dialog_id = str(hash(inner[:80]))
                result.append((dialog_id, item))
        except Exception as exc:
            logger.debug("_find_unread_dialogs error: %s", exc)
        return result

    async def _extract_dialog(self, dialog_id: str, element) -> Optional[dict]:
        """Click on dialog and extract all relevant data."""
        try:
            await element.click()
            await asyncio.sleep(1.2)

            # Client name
            name_el = await self._page.query_selector(SELECTORS["client_name"])
            client_name = (
                (await name_el.inner_text()).strip() if name_el else "Клиент"
            )

            # Source channel
            source_el = await self._page.query_selector(SELECTORS["source_channel"])
            source = (
                (await source_el.inner_text()).strip()
                if source_el
                else "Не определён"
            )

            # Last messages (up to 5)
            msg_els = await self._page.query_selector_all(SELECTORS["message_items"])
            messages = []
            for el in msg_els[-5:]:
                txt = (await el.inner_text()).strip()
                if txt:
                    messages.append(txt)

            if not messages:
                logger.debug("No messages found in dialog %s", dialog_id)
                return None

            self._current_dialog_id = dialog_id
            return {
                "id": dialog_id,
                "client_name": client_name,
                "source": source,
                "messages": messages,
                "last_message": messages[-1],
            }
        except Exception as exc:
            logger.error("_extract_dialog error: %s", exc)
            return None

    async def _try_recover(self) -> None:
        """Attempt to recover from errors by reloading the page."""
        try:
            await self._page.reload(wait_until="domcontentloaded", timeout=30_000)
            await asyncio.sleep(3)
            await self._navigate_to_unanswered()
        except Exception as exc:
            logger.error("Recovery failed: %s", exc)

    async def _save_session(self) -> None:
        try:
            await self._context.storage_state(path=self.session_file)
        except Exception as exc:
            logger.warning("Could not save session: %s", exc)

    # ------------------------------------------------------------------ #
    # Processed dialogs persistence (daily reset)
    # ------------------------------------------------------------------ #

    def _load_processed(self) -> set[str]:
        try:
            if os.path.exists(self.processed_file):
                with open(self.processed_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                # Reset if saved on a different date
                if data.get("date") == str(date.today()):
                    return set(data.get("ids", []))
        except Exception:
            pass
        return set()

    def _save_processed(self) -> None:
        try:
            with open(self.processed_file, "w", encoding="utf-8") as f:
                json.dump(
                    {"date": str(date.today()), "ids": list(self._processed)},
                    f,
                    ensure_ascii=False,
                )
        except Exception as exc:
            logger.warning("Could not save processed list: %s", exc)
