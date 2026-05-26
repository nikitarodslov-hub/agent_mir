"""
Miraphone Agent — premium overlay window (PyQt5).

Features:
  • Live session stats (uptime, processed count, queue size)
  • Animated pulsing status dot
  • Color-coded question-type and source badges
  • Response timer with urgency escalation
  • Auto-send countdown for greeting messages (5 s)
  • Clipboard copy with visual confirmation
  • Keyboard shortcuts: Ctrl+Enter=Send  Esc=Skip  Ctrl+Shift+C=Copy

Thread safety: all GUI mutations go through Qt signals emitted from worker threads.
"""
from __future__ import annotations

from datetime import datetime
from typing import Callable, Optional

from PyQt5.QtCore import QObject, QTimer, Qt, pyqtSignal
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QPushButton,
    QShortcut,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)

from .styles import BADGE_COLORS, STYLES, Colors, source_color
from agent.knowledge_base import QUESTION_TYPE_NAMES

C = Colors
AUTO_SEND_SECS = 5  # countdown for greeting auto-send


# ── Signals bridge ────────────────────────────────────────────────── #

class _Signals(QObject):
    status_changed = pyqtSignal(str)
    response_ready = pyqtSignal(dict)
    queue_changed  = pyqtSignal(int)


# ── Helpers ───────────────────────────────────────────────────────── #

def _separator() -> QFrame:
    line = QFrame()
    line.setFrameShape(QFrame.HLine)
    line.setStyleSheet(f"color: {C.BORDER}; max-height: 1px;")
    return line


def _vsep() -> QLabel:
    lbl = QLabel("│")
    lbl.setStyleSheet(f"color: {C.BORDER}; font-size: 10px; padding: 0 3px;")
    return lbl


def _badge(text: str, fg: str, bg: str) -> QLabel:
    lbl = QLabel(text.upper())
    lbl.setStyleSheet(f"""
        QLabel {{
            background-color: {bg};
            color: {fg};
            font-size: 8px;
            font-weight: bold;
            border-radius: 7px;
            padding: 2px 7px;
            border: 1px solid {fg}30;
            font-family: 'Consolas', monospace;
            letter-spacing: 1px;
        }}
    """)
    return lbl


# ── Main window ───────────────────────────────────────────────────── #

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
        self._signals.queue_changed.connect(self._apply_queue)

        self._drag_pos: Optional[object] = None
        self._processed_count = 0
        self._queue_size = 0
        self._session_start = datetime.now()
        self._response_arrived: Optional[datetime] = None
        self._autosend_remaining = 0
        self._is_greeting = False

        # Live-clock / stats tick (every second)
        self._clock_timer = QTimer()
        self._clock_timer.timeout.connect(self._tick_clock)
        self._clock_timer.start(1000)

        # Response-age timer
        self._resp_age_timer = QTimer()
        self._resp_age_timer.timeout.connect(self._tick_resp_age)

        # Auto-send countdown
        self._autosend_timer = QTimer()
        self._autosend_timer.timeout.connect(self._tick_autosend)

        # Pulsing status dot
        self._dot_state = True
        self._dot_timer = QTimer()
        self._dot_timer.timeout.connect(self._toggle_dot)
        self._dot_timer.start(800)

        self._build_ui()
        self.show()

    # ── Thread-safe public API ─────────────────────────────────────── #

    def set_status(self, text: str) -> None:
        self._signals.status_changed.emit(text)

    def show_response(self, data: dict) -> None:
        self._signals.response_ready.emit(data)

    def set_queue_size(self, n: int) -> None:
        self._signals.queue_changed.emit(n)

    # ── UI construction ────────────────────────────────────────────── #

    def _build_ui(self) -> None:
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint | Qt.FramelessWindowHint | Qt.Tool
        )
        self.setMinimumWidth(390)
        self.setMaximumWidth(450)
        self.setStyleSheet(STYLES["window"])

        root = QWidget()
        root.setObjectName("root")
        root.setStyleSheet(STYLES["root"])
        self.setCentralWidget(root)

        layout = QVBoxLayout(root)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        layout.addWidget(self._build_title_bar())
        layout.addWidget(self._build_stats_bar())
        layout.addWidget(self._build_status_bar())

        # Content area (padded)
        content = QWidget()
        cl = QVBoxLayout(content)
        cl.setContentsMargins(12, 8, 12, 8)
        cl.setSpacing(6)

        # ── Client card ──────────────────────────────────────────── #
        self._client_frame = QFrame()
        self._client_frame.setStyleSheet(STYLES["client_frame"])
        cf = QVBoxLayout(self._client_frame)
        cf.setContentsMargins(10, 8, 10, 8)
        cf.setSpacing(5)

        name_row = QHBoxLayout()
        self._lbl_client_name = QLabel()
        self._lbl_client_name.setStyleSheet(STYLES["client_name"])
        name_row.addWidget(self._lbl_client_name)
        name_row.addStretch()
        self._lbl_source_badge = QLabel()
        name_row.addWidget(self._lbl_source_badge)
        cf.addLayout(name_row)

        meta_row = QHBoxLayout()
        self._lbl_type_badge = QLabel()
        meta_row.addWidget(self._lbl_type_badge)
        meta_row.addStretch()
        self._lbl_resp_age = QLabel()
        self._lbl_resp_age.setStyleSheet(STYLES["response_timer"])
        meta_row.addWidget(self._lbl_resp_age)
        cf.addLayout(meta_row)

        cl.addWidget(self._client_frame)
        self._client_frame.hide()

        # ── Client message ───────────────────────────────────────── #
        self._lbl_msg_header = QLabel("СООБЩЕНИЕ КЛИЕНТА")
        self._lbl_msg_header.setStyleSheet(STYLES["section_header"])
        self._lbl_msg_header.hide()
        cl.addWidget(self._lbl_msg_header)

        self._txt_message = QTextEdit()
        self._txt_message.setReadOnly(True)
        self._txt_message.setMaximumHeight(80)
        self._txt_message.setStyleSheet(STYLES["message_box"])
        self._txt_message.hide()
        cl.addWidget(self._txt_message)

        # ── Suggested response ───────────────────────────────────── #
        self._lbl_resp_header = QLabel("ГОТОВЫЙ ОТВЕТ")
        self._lbl_resp_header.setStyleSheet(STYLES["section_header"])
        self._lbl_resp_header.hide()
        cl.addWidget(self._lbl_resp_header)

        self._txt_response = QTextEdit()
        self._txt_response.setMinimumHeight(100)
        self._txt_response.setMaximumHeight(200)
        self._txt_response.setStyleSheet(STYLES["response_box"])
        self._txt_response.textChanged.connect(self._on_response_edited)
        self._txt_response.hide()
        cl.addWidget(self._txt_response)

        # ── Buttons ──────────────────────────────────────────────── #
        btn_row = QHBoxLayout()
        btn_row.setSpacing(6)

        self._btn_send = QPushButton("⚡  ОТПРАВИТЬ")
        self._btn_send.setStyleSheet(STYLES["btn_send"])
        self._btn_send.setMinimumHeight(34)
        self._btn_send.setToolTip("Ctrl+Enter")
        self._btn_send.clicked.connect(self._handle_send)
        self._btn_send.hide()
        btn_row.addWidget(self._btn_send, stretch=2)

        self._btn_skip = QPushButton("ПРОПУСТИТЬ")
        self._btn_skip.setStyleSheet(STYLES["btn_skip"])
        self._btn_skip.setMinimumHeight(34)
        self._btn_skip.setToolTip("Esc")
        self._btn_skip.clicked.connect(self._handle_skip)
        self._btn_skip.hide()
        btn_row.addWidget(self._btn_skip, stretch=1)

        self._btn_copy = QPushButton("КОПИРОВАТЬ")
        self._btn_copy.setStyleSheet(STYLES["btn_copy"])
        self._btn_copy.setMinimumHeight(34)
        self._btn_copy.setToolTip("Ctrl+Shift+C")
        self._btn_copy.clicked.connect(self._handle_copy)
        self._btn_copy.hide()
        btn_row.addWidget(self._btn_copy)

        cl.addLayout(btn_row)

        # ── Idle placeholder ─────────────────────────────────────── #
        self._idle_widget = QWidget()
        idle_l = QVBoxLayout(self._idle_widget)
        idle_l.setContentsMargins(0, 10, 0, 10)
        idle_l.setAlignment(Qt.AlignCenter)

        self._lbl_idle_dot = QLabel("◉")
        self._lbl_idle_dot.setAlignment(Qt.AlignCenter)
        self._lbl_idle_dot.setStyleSheet(STYLES["idle_dot"])
        idle_l.addWidget(self._lbl_idle_dot)

        lbl_idle = QLabel("ожидание сообщений")
        lbl_idle.setAlignment(Qt.AlignCenter)
        lbl_idle.setStyleSheet(STYLES["idle"])
        idle_l.addWidget(lbl_idle)

        cl.addWidget(self._idle_widget)

        layout.addWidget(content)
        layout.addWidget(self._build_footer())

        # ── Keyboard shortcuts ────────────────────────────────────── #
        for seq in ("Ctrl+Return", "Ctrl+Enter"):
            QShortcut(QKeySequence(seq), self).activated.connect(self._handle_send)
        QShortcut(QKeySequence("Escape"), self).activated.connect(self._handle_skip)
        QShortcut(QKeySequence("Ctrl+Shift+C"), self).activated.connect(self._handle_copy)

        self.adjustSize()
        self.move(40, 40)

    def _build_title_bar(self) -> QFrame:
        bar = QFrame()
        bar.setStyleSheet(STYLES["title_bar"])
        layout = QHBoxLayout(bar)
        layout.setContentsMargins(12, 0, 8, 0)
        layout.setSpacing(5)

        dot = QLabel("◆")
        dot.setStyleSheet(STYLES["title_dot"])
        layout.addWidget(dot)

        title = QLabel("MIRAPHONE AGENT")
        title.setStyleSheet(STYLES["title_text"])
        layout.addWidget(title)

        layout.addStretch()

        self._lbl_clock = QLabel(datetime.now().strftime("%H:%M"))
        self._lbl_clock.setStyleSheet(STYLES["title_clock"])
        layout.addWidget(self._lbl_clock)

        btn_min = QPushButton("−")
        btn_min.setFixedSize(22, 22)
        btn_min.setStyleSheet(STYLES["window_btn"])
        btn_min.clicked.connect(self.showMinimized)
        layout.addWidget(btn_min)

        btn_close = QPushButton("×")
        btn_close.setFixedSize(22, 22)
        btn_close.setStyleSheet(STYLES["close_btn"])
        btn_close.clicked.connect(self.close)
        layout.addWidget(btn_close)

        return bar

    def _build_stats_bar(self) -> QFrame:
        bar = QFrame()
        bar.setStyleSheet(STYLES["stats_bar"])
        bar.setFixedHeight(22)
        layout = QHBoxLayout(bar)
        layout.setContentsMargins(12, 0, 12, 0)
        layout.setSpacing(2)

        def _stat(label: str, attr: str) -> None:
            k = QLabel(label)
            k.setStyleSheet(STYLES["stats_key"])
            layout.addWidget(k)
            v = QLabel("00:00:00" if "uptime" in attr else "0")
            v.setStyleSheet(STYLES["stats_val"])
            setattr(self, attr, v)
            layout.addWidget(v)

        _stat("СЕССИЯ", "_lbl_uptime")
        layout.addWidget(_vsep())
        _stat("ОБРАБОТАНО", "_lbl_processed")
        layout.addWidget(_vsep())
        _stat("ОЧЕРЕДЬ", "_lbl_queue")
        layout.addStretch()

        return bar

    def _build_status_bar(self) -> QFrame:
        bar = QFrame()
        bar.setStyleSheet(STYLES["status_frame"])
        bar.setFixedHeight(26)
        layout = QHBoxLayout(bar)
        layout.setContentsMargins(12, 0, 12, 0)
        layout.setSpacing(6)

        self._lbl_dot = QLabel("●")
        self._lbl_dot.setStyleSheet(f"color: {C.CYAN}; font-size: 8px;")
        layout.addWidget(self._lbl_dot)

        self._lbl_status = QLabel("Инициализация…")
        self._lbl_status.setStyleSheet(STYLES["status_text"])
        layout.addWidget(self._lbl_status)
        layout.addStretch()

        return bar

    def _build_footer(self) -> QFrame:
        bar = QFrame()
        bar.setStyleSheet(STYLES["footer"])
        layout = QHBoxLayout(bar)
        layout.setContentsMargins(12, 4, 12, 4)

        hints = QLabel(
            "Ctrl+Enter: отправить  ·  Esc: пропустить  ·  Ctrl⇧C: копировать"
        )
        hints.setStyleSheet(STYLES["shortcut_hints"])
        layout.addWidget(hints)
        layout.addStretch()

        return bar

    # ── Slot handlers ──────────────────────────────────────────────── #

    def _apply_status(self, text: str) -> None:
        self._lbl_status.setText(text)

    def _apply_queue(self, n: int) -> None:
        self._queue_size = n
        self._lbl_queue.setText(str(n))
        style = STYLES["stats_val_warn"] if n > 0 else STYLES["stats_val"]
        self._lbl_queue.setStyleSheet(style)

    def _show_response(self, data: dict) -> None:
        from utils.sound import play_notification
        play_notification()

        self._response_arrived = datetime.now()
        self._is_greeting = (data.get("question_type", "") == "greeting")

        # Client name
        self._lbl_client_name.setText(data.get("client_name", "—"))

        # Source badge
        src = data.get("source", "Битрикс24")
        fg = source_color(src)
        self._lbl_source_badge.setText(src.upper()[:12])
        self._lbl_source_badge.setStyleSheet(f"""
            QLabel {{
                background-color: {fg}18;
                color: {fg};
                font-size: 8px;
                font-weight: bold;
                border-radius: 7px;
                padding: 2px 7px;
                border: 1px solid {fg}30;
                font-family: 'Consolas', monospace;
                letter-spacing: 1px;
            }}
        """)

        # Question type badge
        q_type = data.get("question_type", "other")
        type_name = QUESTION_TYPE_NAMES.get(q_type, q_type).upper()
        bfg, bbg = BADGE_COLORS.get(q_type, ("#4a5c82", "#0c0e1e"))
        self._lbl_type_badge.setText(type_name)
        self._lbl_type_badge.setStyleSheet(f"""
            QLabel {{
                background-color: {bbg};
                color: {bfg};
                font-size: 8px;
                font-weight: bold;
                border-radius: 7px;
                padding: 2px 7px;
                border: 1px solid {bfg}30;
                font-family: 'Consolas', monospace;
                letter-spacing: 1px;
            }}
        """)

        self._client_frame.show()

        # Message
        msgs = data.get("messages", [data.get("last_message", "")])
        self._txt_message.setPlainText("\n".join(msgs))
        self._lbl_msg_header.show()
        self._txt_message.show()

        # Response (set before connecting auto-cancel so initial set doesn't fire it)
        self._txt_response.blockSignals(True)
        self._txt_response.setPlainText(data.get("suggested_response", ""))
        self._txt_response.blockSignals(False)
        self._lbl_resp_header.show()
        self._txt_response.show()

        self._btn_send.show()
        self._btn_skip.show()
        self._btn_copy.show()
        self._idle_widget.hide()

        self._resp_age_timer.start(1000)

        if self._is_greeting:
            self._start_autosend()

        self.adjustSize()
        self._txt_response.setFocus()

    def _handle_send(self) -> None:
        if not self._btn_send.isEnabled():
            return
        text = self._txt_response.toPlainText().strip()
        if not text:
            return
        self._stop_timers()
        self._processed_count += 1
        self._lbl_processed.setText(str(self._processed_count))
        self._btn_send.setEnabled(False)
        self._btn_skip.setEnabled(False)
        self._btn_copy.setEnabled(False)
        self._on_send(text)
        self._reset_to_idle()

    def _handle_skip(self) -> None:
        if not self._btn_skip.isEnabled():
            return
        self._stop_timers()
        self._on_skip()
        self._reset_to_idle()

    def _handle_copy(self) -> None:
        text = self._txt_response.toPlainText().strip()
        if text:
            QApplication.clipboard().setText(text)
            self._btn_copy.setText("✓ СКОПИРОВАНО")
            QTimer.singleShot(1500, lambda: self._btn_copy.setText("КОПИРОВАТЬ"))

    def _reset_to_idle(self) -> None:
        self._client_frame.hide()
        self._lbl_msg_header.hide()
        self._txt_message.hide()
        self._lbl_resp_header.hide()
        self._txt_response.hide()
        for btn, text in (
            (self._btn_send, "⚡  ОТПРАВИТЬ"),
            (self._btn_skip, "ПРОПУСТИТЬ"),
            (self._btn_copy, "КОПИРОВАТЬ"),
        ):
            btn.hide()
            btn.setEnabled(True)
            if btn is self._btn_send:
                btn.setText(text)
                btn.setStyleSheet(STYLES["btn_send"])
            else:
                btn.setText(text)
        self._idle_widget.show()
        self._response_arrived = None
        self._lbl_resp_age.setText("")
        self.adjustSize()

    def _on_response_edited(self) -> None:
        self._cancel_autosend()

    # ── Timer callbacks ────────────────────────────────────────────── #

    def _tick_clock(self) -> None:
        self._lbl_clock.setText(datetime.now().strftime("%H:%M"))
        elapsed = datetime.now() - self._session_start
        total_s = int(elapsed.total_seconds())
        h, rem = divmod(total_s, 3600)
        m, s = divmod(rem, 60)
        self._lbl_uptime.setText(f"{h:02d}:{m:02d}:{s:02d}")
        self._lbl_processed.setText(str(self._processed_count))

    def _tick_resp_age(self) -> None:
        if self._response_arrived is None:
            return
        secs = int((datetime.now() - self._response_arrived).total_seconds())
        m, s = divmod(secs, 60)
        self._lbl_resp_age.setText(f"⏱ {m:02d}:{s:02d}")
        style = STYLES["response_timer_urgent"] if secs > 60 else STYLES["response_timer"]
        self._lbl_resp_age.setStyleSheet(style)

    def _toggle_dot(self) -> None:
        self._dot_state = not self._dot_state
        color = C.CYAN if self._dot_state else C.TEXT_MUTED
        self._lbl_dot.setStyleSheet(f"color: {color}; font-size: 8px;")

    # ── Auto-send ──────────────────────────────────────────────────── #

    def _start_autosend(self) -> None:
        self._autosend_remaining = AUTO_SEND_SECS
        self._btn_send.setStyleSheet(STYLES["btn_send_auto"])
        self._btn_send.setText(f"⚡ АВТО-ОТПРАВКА ({self._autosend_remaining})")
        self._autosend_timer.start(1000)

    def _tick_autosend(self) -> None:
        self._autosend_remaining -= 1
        if self._autosend_remaining <= 0:
            self._autosend_timer.stop()
            self._handle_send()
        else:
            self._btn_send.setText(f"⚡ АВТО-ОТПРАВКА ({self._autosend_remaining})")

    def _cancel_autosend(self) -> None:
        if self._autosend_timer.isActive():
            self._autosend_timer.stop()
            self._btn_send.setStyleSheet(STYLES["btn_send"])
            self._btn_send.setText("⚡  ОТПРАВИТЬ")

    def _stop_timers(self) -> None:
        self._resp_age_timer.stop()
        self._autosend_timer.stop()

    # ── Draggable frameless window ─────────────────────────────────── #

    def mousePressEvent(self, event) -> None:
        if event.button() == Qt.LeftButton:
            self._drag_pos = event.globalPos() - self.frameGeometry().topLeft()

    def mouseMoveEvent(self, event) -> None:
        if event.buttons() == Qt.LeftButton and self._drag_pos is not None:
            self.move(event.globalPos() - self._drag_pos)

    def mouseReleaseEvent(self, event) -> None:
        self._drag_pos = None
