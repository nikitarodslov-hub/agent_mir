"""First-run setup dialog. Saves settings.json next to the executable."""
from __future__ import annotations

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QDialog,
    QDialogButtonBox,
    QFormLayout,
    QLabel,
    QLineEdit,
    QMessageBox,
    QVBoxLayout,
    QWidget,
)

from .styles import Colors

C = Colors

_STYLE = f"""
QDialog {{
    background: qlineargradient(
        x1:0, y1:0, x2:0, y2:1,
        stop:0 #0d0d28, stop:1 {C.BG}
    );
    color: {C.TEXT};
}}
QLabel {{
    color: {C.TEXT};
    font-size: 12px;
    font-family: 'Segoe UI', Arial, sans-serif;
}}
QLabel#hint {{
    color: {C.TEXT_DIM};
    font-size: 10px;
    font-family: 'Consolas', monospace;
}}
QLabel#title {{
    color: {C.CYAN};
    font-size: 15px;
    font-weight: bold;
    font-family: 'Consolas', monospace;
    letter-spacing: 1px;
}}
QLabel#section {{
    color: {C.CYAN};
    font-size: 11px;
    font-weight: bold;
    font-family: 'Consolas', monospace;
    letter-spacing: 1px;
    padding-top: 8px;
}}
QLineEdit {{
    background-color: {C.INPUT_BG};
    color: {C.TEXT};
    border: 1px solid {C.BORDER};
    border-radius: 5px;
    padding: 7px 10px;
    font-size: 12px;
    min-width: 340px;
    font-family: 'Segoe UI', Arial, sans-serif;
}}
QLineEdit:focus {{
    border: 1px solid {C.CYAN};
}}
QDialogButtonBox QPushButton {{
    background: qlineargradient(
        x1:0, y1:0, x2:0, y2:1,
        stop:0 {C.BTN_SEND_H}, stop:1 {C.BTN_SEND}
    );
    color: {C.GREEN};
    font-weight: bold;
    font-size: 12px;
    letter-spacing: 1px;
    border-radius: 5px;
    border: 1px solid {C.GREEN_DIM};
    padding: 8px 22px;
    min-width: 90px;
}}
QDialogButtonBox QPushButton:hover {{
    background: qlineargradient(
        x1:0, y1:0, x2:0, y2:1,
        stop:0 #1a8848, stop:1 {C.BTN_SEND_H}
    );
    color: white;
}}
QDialogButtonBox QPushButton[text="Отмена"] {{
    background: {C.BTN_SKIP};
    color: {C.TEXT_DIM};
    border-color: {C.BORDER};
}}
QDialogButtonBox QPushButton[text="Отмена"]:hover {{
    background: {C.BTN_SKIP_H};
    color: {C.TEXT};
}}
"""


class SetupDialog(QDialog):
    def __init__(self, config, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._config = config
        self.setWindowTitle("Miraphone Agent — Настройка")
        self.setStyleSheet(_STYLE)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self._build_ui()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setSpacing(8)
        layout.setContentsMargins(26, 22, 26, 22)

        title = QLabel("◆ MIRAPHONE AGENT")
        title.setObjectName("title")
        layout.addWidget(title)

        sub = QLabel("Первый запуск — настройте подключения")
        sub.setStyleSheet(f"color: {Colors.TEXT_DIM}; font-size: 11px; padding-bottom: 6px;")
        layout.addWidget(sub)

        form = QFormLayout()
        form.setSpacing(8)
        form.setLabelAlignment(Qt.AlignRight)

        # Claude
        sec1 = QLabel("Claude AI")
        sec1.setObjectName("section")
        form.addRow(sec1)

        self._key_edit = QLineEdit(self._config.CLAUDE_API_KEY)
        self._key_edit.setPlaceholderText("sk-ant-api03-…")
        self._key_edit.setEchoMode(QLineEdit.Password)
        form.addRow("* API Key:", self._key_edit)
        form.addRow("", _hint("console.anthropic.com → API Keys → Create Key"))

        # Bitrix24
        sec2 = QLabel("Битрикс24")
        sec2.setObjectName("section")
        form.addRow(sec2)

        self._bitrix_edit = QLineEdit(self._config.BITRIX_URL)
        self._bitrix_edit.setPlaceholderText("https://b24-xxx.bitrix24.ru")
        form.addRow("* URL:", self._bitrix_edit)
        form.addRow("", _hint(
            "После запуска откроется браузер с Битрикс24.\n"
            "Войдите вручную — сессия сохранится автоматически."
        ))

        # MoySklad
        sec3 = QLabel("МойСклад (необязательно)")
        sec3.setObjectName("section")
        form.addRow(sec3)

        self._ms_login_edit = QLineEdit(self._config.MOYSKLAD_LOGIN)
        self._ms_login_edit.setPlaceholderText("email@example.com")
        form.addRow("Логин:", self._ms_login_edit)

        self._ms_pass_edit = QLineEdit(self._config.MOYSKLAD_PASSWORD)
        self._ms_pass_edit.setEchoMode(QLineEdit.Password)
        self._ms_pass_edit.setPlaceholderText("пароль")
        form.addRow("Пароль:", self._ms_pass_edit)

        layout.addLayout(form)

        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        buttons.button(QDialogButtonBox.Ok).setText("Сохранить и запустить")
        buttons.button(QDialogButtonBox.Cancel).setText("Отмена")
        buttons.accepted.connect(self._on_accept)
        buttons.rejected.connect(self.reject)
        layout.addWidget(buttons)

        self.adjustSize()
        self.setFixedSize(self.sizeHint())

    def _on_accept(self) -> None:
        api_key = self._key_edit.text().strip()
        bitrix_url = self._bitrix_edit.text().strip().rstrip("/")

        if not api_key:
            QMessageBox.warning(self, "Ошибка", "Укажите Claude API Key.")
            return
        if not bitrix_url.startswith("http"):
            QMessageBox.warning(self, "Ошибка", "Укажите URL Битрикс24.")
            return

        self._config.CLAUDE_API_KEY = api_key
        self._config.BITRIX_URL = bitrix_url
        self._config.MOYSKLAD_LOGIN = self._ms_login_edit.text().strip()
        self._config.MOYSKLAD_PASSWORD = self._ms_pass_edit.text().strip()
        self._config.save()
        self.accept()


def _hint(text: str) -> QLabel:
    lbl = QLabel(text)
    lbl.setObjectName("hint")
    lbl.setWordWrap(True)
    return lbl
