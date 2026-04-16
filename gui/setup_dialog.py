"""
First-run setup dialog.

Shown automatically when Claude API key is not configured.
Saves settings to settings.json next to the executable.
"""
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

_STYLE = f"""
QDialog {{
    background-color: {Colors.BG};
    color: {Colors.TEXT};
}}
QLabel {{
    color: {Colors.TEXT};
    font-size: 12px;
}}
QLabel#hint {{
    color: {Colors.TEXT_DIM};
    font-size: 10px;
}}
QLabel#title {{
    color: {Colors.ACCENT_GREEN};
    font-size: 14px;
    font-weight: bold;
}}
QLineEdit {{
    background-color: {Colors.PANEL};
    color: {Colors.TEXT};
    border: 1px solid {Colors.BORDER};
    border-radius: 4px;
    padding: 6px 8px;
    font-size: 12px;
    min-width: 320px;
}}
QLineEdit:focus {{
    border: 1px solid {Colors.ACCENT_GREEN};
}}
QDialogButtonBox QPushButton {{
    background-color: {Colors.BTN_SEND};
    color: white;
    font-weight: bold;
    border-radius: 4px;
    padding: 7px 20px;
    border: none;
    min-width: 80px;
}}
QDialogButtonBox QPushButton:hover {{
    background-color: {Colors.BTN_SEND_HOVER};
}}
QDialogButtonBox QPushButton[text="Отмена"] {{
    background-color: {Colors.ACCENT_BLUE};
    color: {Colors.TEXT_DIM};
}}
"""


class SetupDialog(QDialog):
    """Collect required settings on first run."""

    def __init__(self, config, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self._config = config
        self.setWindowTitle("Miraphone Agent — Настройка")
        self.setStyleSheet(_STYLE)
        self.setWindowFlags(self.windowFlags() & ~Qt.WindowContextHelpButtonHint)
        self._build_ui()

    def _build_ui(self) -> None:
        layout = QVBoxLayout(self)
        layout.setSpacing(12)
        layout.setContentsMargins(24, 20, 24, 20)

        title = QLabel("Miraphone Agent — первый запуск")
        title.setObjectName("title")
        layout.addWidget(title)

        desc = QLabel(
            "Заполните обязательные поля (отмечены *).\n"
            "Настройки сохранятся — при следующем запуске вводить не нужно."
        )
        desc.setObjectName("hint")
        desc.setWordWrap(True)
        layout.addWidget(desc)

        form = QFormLayout()
        form.setSpacing(10)
        form.setLabelAlignment(Qt.AlignRight)

        # ── Claude API Key ──────────────────────────────────────────── #
        self._key_edit = QLineEdit(self._config.CLAUDE_API_KEY)
        self._key_edit.setPlaceholderText("sk-ant-api03-...")
        self._key_edit.setEchoMode(QLineEdit.Password)
        form.addRow("* Claude API Key:", self._key_edit)

        key_hint = QLabel(
            "Получить: console.anthropic.com → API Keys → Create Key"
        )
        key_hint.setObjectName("hint")
        form.addRow("", key_hint)

        # ── Bitrix24 URL ────────────────────────────────────────────── #
        self._bitrix_edit = QLineEdit(self._config.BITRIX_URL)
        self._bitrix_edit.setPlaceholderText("https://company.bitrix24.ru")
        form.addRow("* Bitrix24 URL:", self._bitrix_edit)

        # ── MoySklad (optional) ─────────────────────────────────────── #
        ms_label = QLabel("МойСклад (необязательно):")
        ms_label.setObjectName("hint")
        layout.addWidget(ms_label)

        self._ms_login_edit = QLineEdit(self._config.MOYSKLAD_LOGIN)
        self._ms_login_edit.setPlaceholderText("email@example.com")
        form.addRow("Логин:", self._ms_login_edit)

        self._ms_pass_edit = QLineEdit(self._config.MOYSKLAD_PASSWORD)
        self._ms_pass_edit.setEchoMode(QLineEdit.Password)
        self._ms_pass_edit.setPlaceholderText("пароль")
        form.addRow("Пароль:", self._ms_pass_edit)

        layout.addLayout(form)

        # ── Buttons ─────────────────────────────────────────────────── #
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
            QMessageBox.warning(self, "Ошибка", "Укажите корректный URL Битрикс24.")
            return

        self._config.CLAUDE_API_KEY = api_key
        self._config.BITRIX_URL = bitrix_url
        self._config.MOYSKLAD_LOGIN = self._ms_login_edit.text().strip()
        self._config.MOYSKLAD_PASSWORD = self._ms_pass_edit.text().strip()
        self._config.save()
        self.accept()
