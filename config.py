"""
Configuration loader.

Priority (highest → lowest):
  1. settings.json  (written by the GUI setup dialog, lives next to the exe)
  2. .env file      (developer convenience)
  3. environment variables

APP_DIR always points to the directory that contains the running
executable (PyInstaller) or this source file (plain Python).
"""
from __future__ import annotations

import json
import os
import sys
from dataclasses import dataclass, field
from pathlib import Path

from dotenv import load_dotenv


def _app_dir() -> Path:
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    return Path(__file__).parent


APP_DIR = _app_dir()
SETTINGS_FILE = APP_DIR / "settings.json"


def _load_settings_json() -> dict:
    try:
        if SETTINGS_FILE.exists():
            return json.loads(SETTINGS_FILE.read_text(encoding="utf-8"))
    except Exception:
        pass
    return {}


def save_settings(data: dict) -> None:
    SETTINGS_FILE.write_text(
        json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8"
    )


@dataclass
class Config:
    CLAUDE_API_KEY: str
    BITRIX_URL: str
    BITRIX_WEBHOOK: str           # REST API webhook URL
    BITRIX_OPENLINES_PATH: str
    MOYSKLAD_LOGIN: str
    MOYSKLAD_PASSWORD: str
    SESSION_FILE: str = field(default="")
    PROCESSED_FILE: str = field(default="")

    def __post_init__(self) -> None:
        if not self.SESSION_FILE:
            self.SESSION_FILE = str(APP_DIR / "bitrix_session.json")
        if not self.PROCESSED_FILE:
            self.PROCESSED_FILE = str(APP_DIR / "processed_dialogs.json")

    def is_complete(self) -> bool:
        return bool(self.CLAUDE_API_KEY and self.BITRIX_URL and self.BITRIX_WEBHOOK)

    def to_dict(self) -> dict:
        return {
            "CLAUDE_API_KEY": self.CLAUDE_API_KEY,
            "BITRIX_URL": self.BITRIX_URL,
            "BITRIX_WEBHOOK": self.BITRIX_WEBHOOK,
            "BITRIX_OPENLINES_PATH": self.BITRIX_OPENLINES_PATH,
            "MOYSKLAD_LOGIN": self.MOYSKLAD_LOGIN,
            "MOYSKLAD_PASSWORD": self.MOYSKLAD_PASSWORD,
        }

    def save(self) -> None:
        save_settings(self.to_dict())

    @classmethod
    def load(cls) -> Config:
        load_dotenv(APP_DIR / ".env")
        js = _load_settings_json()

        def get(key: str, default: str = "") -> str:
            return js.get(key) or os.getenv(key, default) or default

        return cls(
            CLAUDE_API_KEY=get("CLAUDE_API_KEY"),
            BITRIX_URL=get("BITRIX_URL", "https://b24-g1b864.bitrix24.ru").rstrip("/"),
            BITRIX_WEBHOOK=get("BITRIX_WEBHOOK"),
            BITRIX_OPENLINES_PATH=get("BITRIX_OPENLINES_PATH", "/crm/chats/"),
            MOYSKLAD_LOGIN=get("MOYSKLAD_LOGIN"),
            MOYSKLAD_PASSWORD=get("MOYSKLAD_PASSWORD"),
        )
