"""
Central coordinator: ties together Bitrix24 monitor, MoySklad API,
and Claude AI. Communicates results back to the GUI via callbacks.
"""
from __future__ import annotations

import asyncio
import logging
from typing import Callable, Optional

from .bitrix_monitor import BitrixMonitor
from .claude_ai import ClaudeAI
from .knowledge_base import QUESTION_CATEGORIES
from .moysklad_api import MoySkladAPI

logger = logging.getLogger(__name__)


def classify_question(text: str) -> str:
    text_lower = text.lower()
    for category, keywords in QUESTION_CATEGORIES.items():
        for kw in keywords:
            if kw in text_lower:
                return category
    return "other"


class AgentOrchestrator:
    def __init__(
        self,
        config,
        on_status: Callable[[str], None],
        on_response_ready: Callable[[dict], None],
        on_queue_update: Optional[Callable[[int], None]] = None,
    ) -> None:
        self._config = config
        self._on_status = on_status
        self._on_response_ready = on_response_ready
        self._on_queue_update = on_queue_update

        self._monitor = BitrixMonitor(
            bitrix_url=config.BITRIX_URL,
            session_file=config.SESSION_FILE,
            processed_file=config.PROCESSED_FILE,
            selectors_file=config.SELECTORS_FILE,
            debug_screenshot=config.DEBUG_SCREENSHOT,
        )
        self._moysklad = MoySkladAPI(config.MOYSKLAD_LOGIN, config.MOYSKLAD_PASSWORD)
        self._claude = ClaudeAI(config.CLAUDE_API_KEY)

        self._processed_today = 0
        self._busy = False
        self._pending_queue: asyncio.Queue = asyncio.Queue()

    # ── Public API ─────────────────────────────────────────────────── #

    async def start(self) -> None:
        self._on_status("Запуск браузера…")
        asyncio.ensure_future(self._process_queue())
        await self._monitor.start(on_new_message=self._enqueue_message)

    async def send_and_continue(self, text: str) -> None:
        self._on_status("Отправляю…")
        ok = await self._monitor.send_message(text)
        if ok:
            self._processed_today += 1
            self._on_status(f"Отправлено ✓  (сегодня: {self._processed_today})")
        else:
            self._on_status("Ошибка отправки — проверьте браузер")
        self._busy = False

    def skip_current(self) -> None:
        self._busy = False
        self._on_status("Пропущено")

    @property
    def processed_today(self) -> int:
        return self._processed_today

    # ── Internal pipeline ──────────────────────────────────────────── #

    def _notify_queue(self) -> None:
        if self._on_queue_update:
            self._on_queue_update(self._pending_queue.qsize())

    async def _enqueue_message(self, data: dict) -> None:
        await self._pending_queue.put(data)
        self._notify_queue()

    async def _process_queue(self) -> None:
        while True:
            data = await self._pending_queue.get()
            self._notify_queue()
            while self._busy:
                await asyncio.sleep(0.5)
            self._busy = True
            await self._handle_message(data)

    async def _handle_message(self, data: dict) -> None:
        client = data.get("client_name", "Клиент")
        self._on_status(f"Новое сообщение от {client}!")
        await asyncio.sleep(0.3)

        last_msg = data.get("last_message", "")
        q_type = classify_question(last_msg)
        data["question_type"] = q_type

        inventory_info: Optional[str] = None
        if q_type in ("availability", "technical") and self._moysklad.is_enabled():
            self._on_status("Проверяю склад…")
            device = self._moysklad.parse_device_from_message(last_msg)
            if device:
                inventory_info = self._moysklad.search_inventory(device)

        self._on_status("Готовлю ответ…")
        try:
            response = self._claude.generate_response(
                client_name=client,
                source=data.get("source", ""),
                messages=data.get("messages", [last_msg]),
                inventory_info=inventory_info,
                question_type=q_type,
            )
        except Exception as exc:
            logger.error("Claude error: %s", exc)
            response = f"(Ошибка AI: {exc})\nНапишите ответ вручную."

        data["suggested_response"] = response
        self._on_status("Проверьте ответ")
        self._on_response_ready(data)
