"""
Miraphone Agent — entry point.

Architecture:
  Main thread  → PyQt5 event loop (GUI)
  Worker thread → asyncio event loop (Playwright + Claude API + MoySklad)

Cross-thread communication uses PyQt5 signals (thread-safe).
"""

import asyncio
import logging
import sys
import threading

from PyQt5.QtWidgets import QApplication, QMessageBox

from config import Config
from agent.orchestrator import AgentOrchestrator
from gui.overlay import OverlayWindow

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%H:%M:%S",
)
logger = logging.getLogger("main")


def main() -> None:
    config = Config.load()

    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(True)

    # Validate required settings before starting
    if not config.CLAUDE_API_KEY:
        QMessageBox.critical(
            None,
            "Ошибка конфигурации",
            "CLAUDE_API_KEY не задан.\n\nСоздайте файл .env на основе .env.example\n"
            "и укажите ваш ключ Claude API.",
        )
        sys.exit(1)

    if not config.BITRIX_URL:
        QMessageBox.critical(
            None,
            "Ошибка конфигурации",
            "BITRIX_URL не задан.\n\nДобавьте URL вашего Битрикс24 в файл .env",
        )
        sys.exit(1)

    # async loop lives in a daemon thread
    async_loop = asyncio.new_event_loop()

    # ------------------------------------------------------------------ #
    # Callbacks from orchestrator → GUI  (called in worker thread,
    # bridged to main thread via Qt signals inside OverlayWindow)
    # ------------------------------------------------------------------ #

    orchestrator: AgentOrchestrator | None = None

    def on_send(text: str) -> None:
        if orchestrator is None:
            return
        asyncio.run_coroutine_threadsafe(
            orchestrator.send_and_continue(text), async_loop
        )

    def on_skip() -> None:
        if orchestrator is None:
            return
        orchestrator.skip_current()

    window = OverlayWindow(on_send=on_send, on_skip=on_skip)

    orchestrator = AgentOrchestrator(
        config=config,
        on_status=window.set_status,
        on_response_ready=window.show_response,
    )

    # ------------------------------------------------------------------ #
    # Start the async worker thread
    # ------------------------------------------------------------------ #

    def run_worker() -> None:
        asyncio.set_event_loop(async_loop)
        try:
            async_loop.run_until_complete(orchestrator.start())
        except Exception as exc:
            logger.error("Worker thread crashed: %s", exc)
            window.set_status(f"Ошибка: {exc}")

    worker = threading.Thread(target=run_worker, daemon=True, name="async-worker")
    worker.start()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
