"""
Bitrix24 Open Lines monitor.

Two responsibilities:
  1. Open a VISIBLE browser so the manager can see conversations.
  2. Poll the REST API every N seconds for unread dialogs; yield each one
     to the orchestrator via the on_new_message callback.

Sending replies is done entirely via REST API — no browser DOM needed.
"""
from __future__ import annotations

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

from .bitrix_api import BitrixAPI

logger = logging.getLogger(__name__)

POLL_INTERVAL = 5  # seconds between API polls


class BitrixMonitor:
    def __init__(
        self,
        bitrix_url: str,
        webhook_url: str,
        session_file: str = "bitrix_session.json",
        processed_file: str = "processed_dialogs.json",
    ) -> None:
        self.bitrix_url = bitrix_url.rstrip("/")
        self.api = BitrixAPI(webhook_url)
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
        await self._open_browser()
        self._running = True
        await self._poll_loop(on_new_message)

    async def send_message(self, text: str) -> bool:
        """Send reply to the current dialog via REST API."""
        if not self._current_dialog_id:
            logger.warning("send_message called but no current_dialog_id")
            return False
        loop = asyncio.get_running_loop()
        ok = await loop.run_in_executor(
            None, lambda: self.api.send_message(self._current_dialog_id, text)
        )
        if ok:
            await loop.run_in_executor(
                None, lambda: self.api.mark_as_read(self._current_dialog_id)
            )
        return ok

    async def stop(self) -> None:
        self._running = False
        if self._browser:
            await self._browser.close()
        if self._playwright:
            await self._playwright.stop()

    # ------------------------------------------------------------------ #
    # Browser — display only
    # ------------------------------------------------------------------ #

    async def _open_browser(self) -> None:
        self._playwright = await async_playwright().start()
        self._browser = await self._launch_browser()

        storage = self.session_file if os.path.exists(self.session_file) else None
        ctx_kwargs: dict = {"viewport": {"width": 1280, "height": 900}}
        if storage:
            ctx_kwargs["storage_state"] = storage

        self._context = await self._browser.new_context(**ctx_kwargs)
        self._page = await self._context.new_page()

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
        for _ in range(150):          # 150 × 2 s = 5 minutes
            await asyncio.sleep(2)
            current = self._page.url
            if "login" not in current.lower() and current != start_url:
                await asyncio.sleep(2)
                return

    async def _navigate_to_chat(self, dialog_id: str) -> None:
        """Best-effort: navigate browser to the specific chat."""
        try:
            url = f"{self.bitrix_url}/online/{dialog_id}/"
            await self._page.goto(url, wait_until="domcontentloaded", timeout=6_000)
        except Exception:
            pass  # Non-critical; the manager can navigate manually

    async def _save_session(self) -> None:
        try:
            await self._context.storage_state(path=self.session_file)
        except Exception as exc:
            logger.warning("Could not save session: %s", exc)

    async def _launch_browser(self) -> Browser:
        """Try Edge → Chrome → downloaded Chromium, return first that works."""
        attempts = [
            {"channel": "msedge", "headless": False},
            {"channel": "chrome", "headless": False},
            {"headless": False, "args": ["--no-sandbox", "--disable-setuid-sandbox"]},
        ]
        last_exc: Exception = RuntimeError("No browser available")
        for kwargs in attempts:
            try:
                b = await self._playwright.chromium.launch(**kwargs)
                logger.info("Browser launched: %s", kwargs.get("channel", "chromium"))
                return b
            except Exception as exc:
                last_exc = exc
        raise RuntimeError(
            "Could not start any browser.\n"
            "Install Microsoft Edge or Google Chrome, "
            "or run: playwright install chromium"
        ) from last_exc

    # ------------------------------------------------------------------ #
    # REST API polling loop
    # ------------------------------------------------------------------ #

    async def _poll_loop(self, on_new_message: Callable) -> None:
        consecutive_errors = 0
        while self._running:
            try:
                loop = asyncio.get_running_loop()
                chats = await loop.run_in_executor(None, self.api.get_unread_chats)

                for chat in chats:
                    dialog_id = str(chat.get("id", "")).strip()
                    if not dialog_id or dialog_id in self._processed:
                        continue

                    self._processed.add(dialog_id)
                    self._save_processed()

                    data = await self._build_message_data(chat, dialog_id)
                    if data:
                        await on_new_message(data)
                        await asyncio.sleep(1)

                consecutive_errors = 0
            except Exception as exc:
                consecutive_errors += 1
                logger.error("Poll error: %s", exc)
                await asyncio.sleep(min(60, 5 * consecutive_errors))
                continue

            await asyncio.sleep(POLL_INTERVAL)

    async def _build_message_data(
        self, chat: dict, dialog_id: str
    ) -> Optional[dict]:
        try:
            title = chat.get("title") or "Клиент"
            client_name, source = BitrixAPI.parse_chat_title(title)

            loop = asyncio.get_running_loop()
            messages = await loop.run_in_executor(
                None, lambda: self.api.get_last_messages(dialog_id, 5)
            )
            # Fallback to the text snippet already in the recent-list item
            if not messages:
                snippet = (chat.get("message") or {}).get("text", "").strip()
                if snippet:
                    messages = [snippet]
            if not messages:
                return None

            self._current_dialog_id = dialog_id

            # Navigate the visible browser to this chat (best-effort)
            asyncio.ensure_future(self._navigate_to_chat(dialog_id))

            return {
                "id": dialog_id,
                "client_name": client_name,
                "source": source or "Битрикс24",
                "messages": messages,
                "last_message": messages[-1],
            }
        except Exception as exc:
            logger.error("_build_message_data: %s", exc)
            return None

    # ------------------------------------------------------------------ #
    # Processed dialogs — daily reset
    # ------------------------------------------------------------------ #

    def _load_processed(self) -> set:
        try:
            if os.path.exists(self.processed_file):
                with open(self.processed_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
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
            logger.warning("Could not save processed: %s", exc)
