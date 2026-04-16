"""
First-run setup dialog.

Shown automatically when required settings are missing.
Saves to settings.json next to the executable.
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
    padding-bottom: 4px;
}}
QLabel#section {{
    color: {Colors.ACCENT_GREEN};
    font-size: 11px;
    font-weight: bold;
    padding-top: 6px;
}}
QLineEdit {{
    background-color: {Colors.PANEL};
    color: {Colors.TEXT};
    border: 1px solid {Colors.BORDER};
    border-radius: 4px;
    padding: 6px 8px;
    font-size: 12px;
    min-width: 340px;
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
        layout.setContentsMargins(24, 20, 24, 20)

        title = QLabel("Miraphone Agent — первый запуск")
        title.setObjectName("title")
        layout.addWidget(title)

        desc = QLabel("Заполните поля (отмечены *). Настройки сохранятся автоматически.")
        desc.setObjectName("hint")
        layout.addWidget(desc)

        form = QFormLayout()
        form.setSpacing(8)
        form.setLabelAlignment(Qt.AlignRight)

        # ── Claude API Key ────────────────────────────────────────── #
        sec1 = QLabel("Claude AI")
        sec1.setObjectName("section")
        form.addRow(sec1)

        self._key_edit = QLineEdit(self._config.CLAUDE_API_KEY)
        self._key_edit.setPlaceholderText("sk-ant-api03-...")
        self._key_edit.setEchoMode(QLineEdit.Password)
        form.addRow("* API Key:", self._key_edit)

        key_hint = QLabel("console.anthropic.com → API Keys → Create Key")
        key_hint.setObjectName("hint")
        form.addRow("", key_hint)

        # ── Bitrix24 ─────────────────────────────────────────────── #
        sec2 = QLabel("Битрикс24")
        sec2.setObjectName("section")
        form.addRow(sec2)

        self._bitrix_edit = QLineEdit(self._config.BITRIX_URL)
        self._bitrix_edit.setPlaceholderText("https://b24-xxx.bitrix24.ru")
        form.addRow("* URL сайта:", self._bitrix_edit)

        self._webhook_edit = QLineEdit(self._config.BITRIX_WEBHOOK)
        self._webhook_edit.setPlaceholderText(
            "https://b24-xxx.bitrix24.ru/rest/1/TOKEN/"
        )
        form.addRow("* Webhook URL:", self._webhook_edit)

        wh_hint = QLabel(
            "Как получить: Настройки (шестерёнка) → Разработчикам\n"
            "→ Входящий вебхук → Добавить\n"
            "Права: IM (чтение+запись), Открытые линии (чтение+запись)\n"
            "Скопируйте URL вида: .../rest/1/abc123xyz/"
        )
        wh_hint.setObjectName("hint")
        form.addRow("", wh_hint)

        # ── MoySklad ──────────────────────────────────────────────── #
        sec3 = QLabel("МойСклад (необязательно — для проверки склада)")
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
        webhook = self._webhook_edit.text().strip().rstrip("/") + "/"

        if not api_key:
            QMessageBox.warning(self, "Ошибка", "Укажите Claude API Key.")
            return
        if not bitrix_url.startswith("http"):
            QMessageBox.warning(self, "Ошибка", "Укажите URL Битрикс24 (начинается с https://).")
            return
        if "rest/" not in webhook:
            QMessageBox.warning(
                self,
                "Ошибка",
                "Webhook URL должен выглядеть так:\n"
                "https://b24-xxx.bitrix24.ru/rest/1/TOKEN/",
            )
            return

        self._config.CLAUDE_API_KEY = api_key
        self._config.BITRIX_URL = bitrix_url
        self._config.BITRIX_WEBHOOK = webhook
        self._config.MOYSKLAD_LOGIN = self._ms_login_edit.text().strip()
        self._config.MOYSKLAD_PASSWORD = self._ms_pass_edit.text().strip()
        self._config.save()
        self.accept()
