"""
Miraphone Agent — entry point.

Architecture:
  Main thread  → PyQt5 event loop (GUI)
  Worker thread → asyncio event loop (Playwright + Claude API + MoySklad)

Cross-thread communication uses PyQt5 signals (thread-safe).
"""
from __future__ import annotations

import asyncio
import logging
import sys
import threading

from PyQt5.QtWidgets import QApplication, QMessageBox

from config import Config
from agent.orchestrator import AgentOrchestrator
from gui.overlay import OverlayWindow
from gui.setup_dialog import SetupDialog

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("main")


def main() -> None:
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(True)

    config = Config.load()

    # ── First-run setup dialog ──────────────────────────────────────── #
    if not config.is_complete():
        dlg = SetupDialog(config)
        if dlg.exec_() != SetupDialog.Accepted:
            sys.exit(0)
        # config is mutated & saved inside SetupDialog._on_accept

    # ── Sanity check (should not happen after dialog) ───────────────── #
    if not config.is_complete():
        QMessageBox.critical(
            None,
            "Ошибка конфигурации",
            "CLAUDE_API_KEY или BITRIX_URL не заданы.\n"
            "Перезапустите программу и заполните настройки.",
        )
        sys.exit(1)

    # ── Build GUI ────────────────────────────────────────────────────── #
    async_loop = asyncio.new_event_loop()
    orchestrator: AgentOrchestrator | None = None

    def on_send(text: str) -> None:
        if orchestrator is not None:
            asyncio.run_coroutine_threadsafe(
                orchestrator.send_and_continue(text), async_loop
            )

    def on_skip() -> None:
        if orchestrator is not None:
            orchestrator.skip_current()

    window = OverlayWindow(on_send=on_send, on_skip=on_skip)

    orchestrator = AgentOrchestrator(
        config=config,
        on_status=window.set_status,
        on_response_ready=window.show_response,
    )

    # ── Async worker thread ──────────────────────────────────────────── #
    def run_worker() -> None:
        asyncio.set_event_loop(async_loop)
        try:
            async_loop.run_until_complete(orchestrator.start())
        except Exception as exc:
            logger.error("Worker thread crashed: %s", exc)
            window.set_status(f"Ошибка: {exc}")

    threading.Thread(target=run_worker, daemon=True, name="async-worker").start()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
