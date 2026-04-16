"""
Bitrix24 Open Lines browser monitor.

Strategy:
  - Open a visible browser at Bitrix24 (manager can see and interact).
  - Navigate to the Open Lines / Contact Center interface.
  - Scan for chat items with unread counters every POLL_INTERVAL seconds.
  - Click each unread chat, extract the message text, yield to orchestrator.
  - Send replies by typing into the chat input and clicking Send.

Selector customisation:
  If the defaults do not match your Bitrix24 version, create a file
  `selectors.json` next to the executable with any keys you want to
  override (see DEFAULT_SELECTORS below for key names).
  The file is hot-reloaded on each poll so you can tune it live.

Debug screenshots:
  Saved to `debug_screenshot.png` in the app directory whenever the
  monitor cannot find expected elements.  Share this file when reporting
  issues so the selectors can be adjusted.
"""
from __future__ import annotations

import asyncio
import json
import logging
import os
from datetime import date
from pathlib import Path
from typing import Callable, Optional

from playwright.async_api import (
    Browser,
    BrowserContext,
    ElementHandle,
    Page,
    Playwright,
    async_playwright,
)

logger = logging.getLogger(__name__)

POLL_INTERVAL = 4          # seconds between full scans
NAV_TIMEOUT   = 8_000      # ms – navigation timeout
FIND_TIMEOUT  = 3_000      # ms – element lookup timeout

# ------------------------------------------------------------------ #
# Default CSS / text selectors.
# Key names must stay stable (referenced in code below).
# ------------------------------------------------------------------ #
DEFAULT_SELECTORS: dict[str, str | list[str]] = {
    # ── Navigation ───────────────────────────────────────────────── #

    # URLs to try for the Open Lines page (relative to BITRIX_URL)
    "openlines_urls": [
        "/contact-center/",
        "/crm/configs/list/open-line/",
        "/crm/chats/",
        "/online/",
    ],

    # Text that appears on / near the "Open Lines" section link
    "openlines_nav_texts": [
        "Открытые линии",
        "Контакт-центр",
        "Contact Center",
        "Open Lines",
    ],

    # Selector for the messenger/chat icon in the top or side navigation
    "chat_icon": (
        ".bx-header-btn-messenger, "
        "[class*='messenger-btn'], "
        "[class*='im-btn'], "
        "a[href*='/online/'], "
        "a[href*='/im/']"
    ),

    # ── Dialog / chat list ────────────────────────────────────────── #

    # Each row in the chat list
    "dialog_items": [
        ".bx-im-recent-item",
        ".bx-im-list-item",
        ".im-open-lines-item",
        "[class*='recent-item']",
        "[class*='openlines-item']",
        "[class*='im-item']",
        "[class*='dialog-item']",
        ".bx-messenger-item",
    ],

    # Unread-counter badge inside a dialog item
    "unread_badge": [
        ".bx-im-recent-item-counter",
        ".bx-im-counter",
        "[class*='unread-counter']",
        "[class*='counter']:not([class*='total'])",
        ".bx-messenger-item-unread-counter",
    ],

    # ── Opened chat ───────────────────────────────────────────────── #

    # Client name in the chat header
    "client_name": [
        ".bx-im-dialog-header-name",
        ".bx-im-chat-title",
        "[class*='header-name']",
        "[class*='chat-title']",
        ".bx-imsettings-profile-name",
    ],

    # Source label (ВКонтакте, Авито, …)
    "source_label": [
        ".bx-im-open-line-source",
        "[class*='open-line-source']",
        "[class*='channel-name']",
        ".bx-im-dialog-header-desc",
    ],

    # Individual message text bubbles
    "message_text": [
        ".bx-im-message-text",
        "[class*='message-text']",
        ".bx-messenger-content-message-text",
    ],

    # ── Reply input & send ────────────────────────────────────────── #

    "message_input": [
        ".bx-im-message-form-input-container textarea",
        ".bx-im-textarea",
        "[contenteditable='true'][class*='input']",
        "textarea[class*='message']",
        ".bx-im-input-box textarea",
    ],

    "send_button": [
        ".bx-im-message-form-button-send",
        "button[class*='send']",
        "[class*='send-button']",
        "[class*='submit-btn']",
    ],
}

# ------------------------------------------------------------------ #
# Helpers
# ------------------------------------------------------------------ #

def _load_selectors_override(selectors_file: str) -> dict:
    try:
        p = Path(selectors_file)
        if p.exists():
            return json.loads(p.read_text(encoding="utf-8"))
    except Exception as exc:
        logger.warning("Could not load selectors.json: %s", exc)
    return {}


def _merged_selectors(selectors_file: str) -> dict:
    sel = dict(DEFAULT_SELECTORS)
    sel.update(_load_selectors_override(selectors_file))
    return sel


def _as_list(val: str | list[str]) -> list[str]:
    return val if isinstance(val, list) else [val]


# ------------------------------------------------------------------ #
# Monitor
# ------------------------------------------------------------------ #

class BitrixMonitor:
    def __init__(
        self,
        bitrix_url: str,
        session_file: str = "bitrix_session.json",
        processed_file: str = "processed_dialogs.json",
        selectors_file: str = "selectors.json",
        debug_screenshot: str = "debug_screenshot.png",
    ) -> None:
        self.bitrix_url    = bitrix_url.rstrip("/")
        self.session_file  = session_file
        self.processed_file = processed_file
        self.selectors_file = selectors_file
        self.debug_screenshot = debug_screenshot

        self._playwright: Optional[Playwright] = None
        self._browser:    Optional[Browser]    = None
        self._context:    Optional[BrowserContext] = None
        self._page:       Optional[Page]       = None
        self._running = False
        self._current_dialog_id: Optional[str] = None
        self._processed: set[str] = self._load_processed()

    # ── Public API ─────────────────────────────────────────────────── #

    async def start(self, on_new_message: Callable) -> None:
        await self._open_browser()
        self._running = True
        await self._navigate_to_open_lines()
        await self._poll_loop(on_new_message)

    async def send_message(self, text: str) -> bool:
        if not self._page:
            return False
        sel = _merged_selectors(self.selectors_file)
        try:
            # Try each input selector
            input_el = None
            for s in _as_list(sel["message_input"]):
                try:
                    input_el = await self._page.wait_for_selector(
                        s, timeout=4_000
                    )
                    if input_el:
                        break
                except Exception:
                    continue

            if not input_el:
                logger.error("send_message: could not find input")
                await self._save_debug_screenshot()
                return False

            await input_el.click()
            await input_el.fill("")
            await input_el.type(text, delay=8)
            await asyncio.sleep(0.3)

            # Try send button, fallback to Enter
            sent = False
            for s in _as_list(sel["send_button"]):
                btn = await self._page.query_selector(s)
                if btn:
                    await btn.click()
                    sent = True
                    break
            if not sent:
                await input_el.press("Enter")

            logger.info("Message sent.")
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

    # ── Browser setup ─────────────────────────────────────────────── #

    async def _open_browser(self) -> None:
        self._playwright = await async_playwright().start()
        self._browser = await self._launch_browser()

        storage = self.session_file if os.path.exists(self.session_file) else None
        ctx = {"viewport": {"width": 1280, "height": 900}}
        if storage:
            ctx["storage_state"] = storage

        self._context = await self._browser.new_context(**ctx)
        self._page    = await self._context.new_page()

        await self._page.goto(self.bitrix_url, wait_until="domcontentloaded")

        if await self._is_login_page():
            logger.info("Waiting for manual login (up to 5 min)…")
            await self._wait_for_login()

        await self._save_session()

    async def _is_login_page(self) -> bool:
        try:
            await self._page.wait_for_selector(
                "input[name='LOGIN'], input[autocomplete='username']",
                timeout=3_000,
            )
            return True
        except Exception:
            return False

    async def _wait_for_login(self) -> None:
        start_url = self._page.url
        for _ in range(150):
            await asyncio.sleep(2)
            if "login" not in self._page.url.lower() and self._page.url != start_url:
                await asyncio.sleep(2)
                return

    async def _save_session(self) -> None:
        try:
            await self._context.storage_state(path=self.session_file)
        except Exception as exc:
            logger.warning("Could not save session: %s", exc)

    async def _launch_browser(self) -> Browser:
        for kwargs in [
            {"channel": "msedge", "headless": False},
            {"channel": "chrome",  "headless": False},
            {"headless": False, "args": ["--no-sandbox"]},
        ]:
            try:
                b = await self._playwright.chromium.launch(**kwargs)
                logger.info("Browser: %s", kwargs.get("channel", "chromium"))
                return b
            except Exception:
                continue
        raise RuntimeError(
            "No browser found. Install Edge/Chrome or run: playwright install chromium"
        )

    # ── Navigation ─────────────────────────────────────────────────── #

    async def _navigate_to_open_lines(self) -> bool:
        """Try several strategies to reach the Open Lines interface."""
        sel = _merged_selectors(self.selectors_file)

        # 1. Try direct URLs
        for path in _as_list(sel["openlines_urls"]):
            if await self._try_goto(path):
                logger.info("Navigated to open lines via URL: %s", path)
                return True

        # 2. Try clicking navigation text links
        for text in _as_list(sel["openlines_nav_texts"]):
            if await self._try_click_text(text):
                logger.info("Navigated to open lines via text: %s", text)
                return True

        # 3. Try clicking the chat/messenger icon first, then text
        icon_sel = sel.get("chat_icon", "")
        try:
            icon = await self._page.query_selector(icon_sel)
            if icon:
                await icon.click()
                await asyncio.sleep(1.5)
                for text in _as_list(sel["openlines_nav_texts"]):
                    if await self._try_click_text(text):
                        logger.info("Navigated via chat icon + text: %s", text)
                        return True
        except Exception:
            pass

        logger.warning(
            "Could not navigate to Open Lines automatically. "
            "Please navigate manually in the browser. "
            "Screenshot saved: %s", self.debug_screenshot
        )
        await self._save_debug_screenshot()
        return False

    async def _try_goto(self, path: str) -> bool:
        """Navigate to a URL and return True if chat items are found."""
        try:
            url = self.bitrix_url + path
            await self._page.goto(url, wait_until="domcontentloaded", timeout=NAV_TIMEOUT)
            await asyncio.sleep(2)
            items = await self._find_dialog_items()
            return len(items) > 0
        except Exception:
            return False

    async def _try_click_text(self, text: str) -> bool:
        """Click a visible element containing `text`. Return True on success."""
        try:
            loc = self._page.get_by_text(text, exact=False).first
            await loc.click(timeout=FIND_TIMEOUT)
            await asyncio.sleep(1.5)
            return True
        except Exception:
            return False

    # ── Polling loop ───────────────────────────────────────────────── #

    async def _poll_loop(self, on_new_message: Callable) -> None:
        errors = 0
        while self._running:
            try:
                items = await self._find_unread_items()
                for dialog_id, element in items:
                    if dialog_id in self._processed:
                        continue
                    self._processed.add(dialog_id)
                    self._save_processed()

                    data = await self._extract_dialog(dialog_id, element)
                    if data:
                        await on_new_message(data)
                        await asyncio.sleep(1)

                errors = 0
            except Exception as exc:
                errors += 1
                logger.error("Poll error: %s", exc)
                await asyncio.sleep(min(60, 5 * errors))
                # Try to recover by re-navigating
                if errors % 3 == 0:
                    await self._recover()
                continue

            await asyncio.sleep(POLL_INTERVAL)

    async def _recover(self) -> None:
        """Reload the page and re-navigate after repeated errors."""
        try:
            await self._page.reload(wait_until="domcontentloaded", timeout=15_000)
            await asyncio.sleep(2)
            await self._navigate_to_open_lines()
        except Exception as exc:
            logger.error("Recovery failed: %s", exc)

    # ── Finding unread items ───────────────────────────────────────── #

    async def _find_dialog_items(self) -> list[ElementHandle]:
        """Return all visible dialog/chat list items."""
        sel = _merged_selectors(self.selectors_file)
        for s in _as_list(sel["dialog_items"]):
            try:
                items = await self._page.query_selector_all(s)
                if items:
                    return items
            except Exception:
                continue
        return []

    async def _find_unread_items(self) -> list[tuple[str, ElementHandle]]:
        """Return (dialog_id, element) pairs for items with unread messages."""
        sel = _merged_selectors(self.selectors_file)
        result = []
        items = await self._find_dialog_items()

        for item in items:
            try:
                # Check for a visible unread badge with a number
                badge = None
                for bs in _as_list(sel["unread_badge"]):
                    badge = await item.query_selector(bs)
                    if badge:
                        break
                if not badge:
                    continue

                badge_text = (await badge.inner_text()).strip()
                if not badge_text or badge_text == "0":
                    continue

                # Derive a stable id
                dialog_id = (
                    await item.get_attribute("data-id")
                    or await item.get_attribute("data-cid")
                    or await item.get_attribute("data-entity-id")
                    or await item.get_attribute("id")
                )
                if not dialog_id:
                    inner = (await item.inner_text())[:60]
                    dialog_id = f"hash_{hash(inner)}"

                result.append((dialog_id, item))
            except Exception:
                continue

        return result

    # ── Extracting dialog content ──────────────────────────────────── #

    async def _extract_dialog(
        self, dialog_id: str, element: ElementHandle
    ) -> Optional[dict]:
        sel = _merged_selectors(self.selectors_file)
        try:
            await element.click()
            await asyncio.sleep(1.2)

            # Client name
            client_name = "Клиент"
            for s in _as_list(sel["client_name"]):
                el = await self._page.query_selector(s)
                if el:
                    client_name = (await el.inner_text()).strip()
                    break

            # Source channel
            source = ""
            for s in _as_list(sel["source_label"]):
                el = await self._page.query_selector(s)
                if el:
                    source = (await el.inner_text()).strip()
                    break

            # Message texts (last 5)
            messages: list[str] = []
            for s in _as_list(sel["message_text"]):
                els = await self._page.query_selector_all(s)
                if els:
                    for el in els[-5:]:
                        txt = (await el.inner_text()).strip()
                        if txt:
                            messages.append(txt)
                    break

            if not messages:
                # Fallback: grab text from the item row itself
                row_text = (await element.inner_text()).strip()
                if row_text:
                    messages = [row_text]

            if not messages:
                await self._save_debug_screenshot()
                return None

            self._current_dialog_id = dialog_id
            return {
                "id": dialog_id,
                "client_name": client_name,
                "source": source or "Битрикс24",
                "messages": messages,
                "last_message": messages[-1],
            }
        except Exception as exc:
            logger.error("_extract_dialog: %s", exc)
            await self._save_debug_screenshot()
            return None

    # ── Debug & persistence ────────────────────────────────────────── #

    async def _save_debug_screenshot(self) -> None:
        """Save a screenshot so the user/developer can inspect the page."""
        try:
            await self._page.screenshot(path=self.debug_screenshot, full_page=False)
            logger.info("Debug screenshot saved: %s", self.debug_screenshot)
        except Exception:
            pass

    def _load_processed(self) -> set:
        try:
            if os.path.exists(self.processed_file):
                data = json.loads(
                    open(self.processed_file, encoding="utf-8").read()
                )
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
                    f, ensure_ascii=False,
                )
        except Exception as exc:
            logger.warning("Could not save processed: %s", exc)
