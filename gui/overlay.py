"""
Miraphone Agent — always-on-top overlay window (PyQt5).

Thread safety: all GUI mutations happen on the Qt main thread via
Qt signals emitted from worker threads.
"""

from datetime import datetime
from typing import Callable, Optional

from PyQt5.QtCore import QObject, Qt, pyqtSignal
from PyQt5.QtWidgets import (
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from .styles import STYLES, Colors
from agent.knowledge_base import QUESTION_TYPE_NAMES

# ------------------------------------------------------------------ #
# Qt signals bridge (thread → main thread)
# ------------------------------------------------------------------ #


class _Signals(QObject):
    status_changed = pyqtSignal(str)          # status text
    response_ready = pyqtSignal(dict)         # full message data


# ------------------------------------------------------------------ #
# Main overlay window
# ------------------------------------------------------------------ #


class OverlayWindow(QMainWindow):
    def __init__(
        self,
        on_send: Callable[[str], None],
        on_skip: Callable[[], None],
    ):
        super().__init__()
        self._on_send = on_send
        self._on_skip = on_skip
        self._signals = _Signals()
        self._signals.status_changed.connect(self._apply_status)
        self._signals.response_ready.connect(self._show_response)
        self._drag_pos: Optional[object] = None
        self._processed_count = 0

        self._build_ui()
        self.show()

    # ------------------------------------------------------------------ #
    # Thread-safe public API
    # ------------------------------------------------------------------ #

    def set_status(self, text: str) -> None:
        """Call from any thread."""
        self._signals.status_changed.emit(text)

    def show_response(self, data: dict) -> None:
        """Call from any thread."""
        self._signals.response_ready.emit(data)

    # ------------------------------------------------------------------ #
    # UI construction
    # ------------------------------------------------------------------ #

    def _build_ui(self) -> None:
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool
        )
        self.setMinimumWidth(340)
        self.setMaximumWidth(400)
        self.setStyleSheet(STYLES["window"])

        root = QWidget()
        root.setObjectName("root")
        root.setStyleSheet(STYLES["root"])
        self.setCentralWidget(root)

        layout = QVBoxLayout(root)
        layout.setContentsMargins(12, 10, 12, 10)
        layout.setSpacing(7)

        # ── Title bar ──────────────────────────────────────────────── #
        title_bar = QFrame()
        title_bar.setStyleSheet(STYLES["title_bar"])
        tb_layout = QHBoxLayout(title_bar)
        tb_layout.setContentsMargins(10, 6, 8, 6)
        tb_layout.setSpacing(0)

        lbl_title = QLabel("Miraphone Agent")
        lbl_title.setStyleSheet(STYLES["title_text"])
        tb_layout.addWidget(lbl_title)
        tb_layout.addStretch()

        btn_close = QPushButton("×")
        btn_close.setFixedSize(22, 22)
        btn_close.setStyleSheet(STYLES["close_btn"])
        btn_close.clicked.connect(self.close)
        tb_layout.addWidget(btn_close)
        layout.addWidget(title_bar)

        # ── Status line ────────────────────────────────────────────── #
        self._lbl_status = QLabel("Инициализация…")
        self._lbl_status.setStyleSheet(STYLES["status"])
        layout.addWidget(self._lbl_status)

        layout.addWidget(_separator())

        # ── Client info (hidden until response arrives) ────────────── #
        self._client_frame = QFrame()
        self._client_frame.setStyleSheet(STYLES["client_frame"])
        cf_layout = QVBoxLayout(self._client_frame)
        cf_layout.setContentsMargins(10, 7, 10, 7)
        cf_layout.setSpacing(3)

        self._lbl_client_name = QLabel()
        self._lbl_client_name.setStyleSheet(STYLES["client_name"])
        cf_layout.addWidget(self._lbl_client_name)

        meta_row = QHBoxLayout()
        self._lbl_qtype = QLabel()
        self._lbl_qtype.setStyleSheet(STYLES["meta_dim"])
        meta_row.addWidget(self._lbl_qtype)
        meta_row.addStretch()
        self._lbl_source = QLabel()
        self._lbl_source.setStyleSheet(STYLES["meta_accent"])
        meta_row.addWidget(self._lbl_source)
        cf_layout.addLayout(meta_row)

        layout.addWidget(self._client_frame)
        self._client_frame.hide()

        # ── Client message ─────────────────────────────────────────── #
        self._lbl_msg_header = QLabel("СООБЩЕНИЕ КЛИЕНТА:")
        self._lbl_msg_header.setStyleSheet(STYLES["section_header"])
        self._lbl_msg_header.hide()
        layout.addWidget(self._lbl_msg_header)

        self._txt_message = QTextEdit()
        self._txt_message.setReadOnly(True)
        self._txt_message.setMaximumHeight(90)
        self._txt_message.setStyleSheet(STYLES["message_box"])
        self._txt_message.hide()
        layout.addWidget(self._txt_message)

        # ── Suggested response ─────────────────────────────────────── #
        self._lbl_resp_header = QLabel("ГОТОВЫЙ ОТВЕТ:")
        self._lbl_resp_header.setStyleSheet(STYLES["section_header"])
        self._lbl_resp_header.hide()
        layout.addWidget(self._lbl_resp_header)

        self._txt_response = QTextEdit()
        self._txt_response.setMinimumHeight(110)
        self._txt_response.setMaximumHeight(200)
        self._txt_response.setStyleSheet(STYLES["response_box"])
        self._txt_response.hide()
        layout.addWidget(self._txt_response)

        # ── Action buttons ─────────────────────────────────────────── #
        btn_row = QHBoxLayout()
        btn_row.setSpacing(8)

        self._btn_send = QPushButton("ОТПРАВИТЬ")
        self._btn_send.setStyleSheet(STYLES["btn_send"])
        self._btn_send.setMinimumHeight(36)
        self._btn_send.clicked.connect(self._handle_send)
        self._btn_send.hide()
        btn_row.addWidget(self._btn_send)

        self._btn_skip = QPushButton("ПРОПУСТИТЬ")
        self._btn_skip.setStyleSheet(STYLES["btn_skip"])
        self._btn_skip.setMinimumHeight(36)
        self._btn_skip.clicked.connect(self._handle_skip)
        self._btn_skip.hide()
        btn_row.addWidget(self._btn_skip)

        layout.addLayout(btn_row)

        # ── Footer ─────────────────────────────────────────────────── #
        layout.addWidget(_separator())

        self._lbl_counter = QLabel("Обработано сегодня: 0")
        self._lbl_counter.setStyleSheet(STYLES["counter"])
        layout.addWidget(self._lbl_counter)

        self._lbl_idle = QLabel("[нет активных диалогов]")
        self._lbl_idle.setAlignment(Qt.AlignCenter)
        self._lbl_idle.setStyleSheet(STYLES["idle"])
        layout.addWidget(self._lbl_idle)

        self.adjustSize()
        self.move(40, 40)

    # ------------------------------------------------------------------ #
    # Slot handlers (run on main thread)
    # ------------------------------------------------------------------ #

    def _apply_status(self, text: str) -> None:
        time_str = datetime.now().strftime("%H:%M")
        self._lbl_status.setText(f"{text}   {time_str}")

    def _show_response(self, data: dict) -> None:
        from utils.sound import play_notification
        play_notification()

        # Client info block
        self._lbl_client_name.setText(f"Клиент: {data.get('client_name', '—')}")
        q_type = data.get("question_type", "other")
        self._lbl_qtype.setText(f"Тип: {QUESTION_TYPE_NAMES.get(q_type, q_type)}")
        self._lbl_source.setText(data.get("source", ""))
        self._client_frame.show()

        # Message
        self._txt_message.setPlainText(
            "\n".join(data.get("messages", [data.get("last_message", "")]))
        )
        self._lbl_msg_header.show()
        self._txt_message.show()

        # Response (editable)
        self._txt_response.setPlainText(data.get("suggested_response", ""))
        self._lbl_resp_header.show()
        self._txt_response.show()

        # Buttons
        self._btn_send.show()
        self._btn_skip.show()
        self._lbl_idle.hide()

        self.adjustSize()

    def _handle_send(self) -> None:
        text = self._txt_response.toPlainText().strip()
        if not text:
            return
        self._processed_count += 1
        self._lbl_counter.setText(f"Обработано сегодня: {self._processed_count}")
        self._btn_send.setEnabled(False)
        self._btn_skip.setEnabled(False)
        self._on_send(text)
        self._reset_to_idle()

    def _handle_skip(self) -> None:
        self._on_skip()
        self._reset_to_idle()

    def _reset_to_idle(self) -> None:
        self._client_frame.hide()
        self._lbl_msg_header.hide()
        self._txt_message.hide()
        self._lbl_resp_header.hide()
        self._txt_response.hide()
        self._btn_send.hide()
        self._btn_send.setEnabled(True)
        self._btn_skip.hide()
        self._btn_skip.setEnabled(True)
        self._lbl_idle.show()
        self.adjustSize()

    # ------------------------------------------------------------------ #
    # Draggable window (frameless)
    # ------------------------------------------------------------------ #

    def mousePressEvent(self, event) -> None:
        if event.button() == Qt.LeftButton:
            self._drag_pos = event.globalPos() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event) -> None:
        if event.buttons() == Qt.LeftButton and self._drag_pos is not None:
            self.move(event.globalPos() - self._drag_pos)

    def mouseReleaseEvent(self, event) -> None:
        self._drag_pos = None


# ------------------------------------------------------------------ #
# Helpers
# ------------------------------------------------------------------ #


def _separator() -> QFrame:
    line = QFrame()
    line.setFrameShape(QFrame.HLine)
    line.setStyleSheet(f"color: {Colors.BORDER}; max-height: 1px;")
    return line
