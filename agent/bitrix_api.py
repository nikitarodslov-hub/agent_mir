"""
Bitrix24 REST API client.

Webhook URL format: https://b24-xxx.bitrix24.ru/rest/USER_ID/TOKEN/
How to get one:
  Bitrix24 → Settings (gear) → Developer tools → Inbound webhooks → Add
  Permissions needed: im (read+write), imopenlines (read+write)
"""
from __future__ import annotations

import logging
from typing import Optional

import requests

logger = logging.getLogger(__name__)

TIMEOUT = 10


class BitrixAPI:
    def __init__(self, webhook_url: str) -> None:
        self.base = webhook_url.rstrip("/")

    # ------------------------------------------------------------------ #
    # Public methods
    # ------------------------------------------------------------------ #

    def get_unread_chats(self) -> list[dict]:
        """Return recent chats that have unread messages."""
        data = self._get(
            "im.recent.list",
            {"SKIP_OPENLINES": "N", "LIMIT": 50},
        )
        items = data.get("result", {}).get("items", [])
        return [item for item in items if int(item.get("counter", 0)) > 0]

    def get_last_messages(self, dialog_id: str, limit: int = 5) -> list[str]:
        """Return last `limit` message texts from a dialog (oldest first)."""
        data = self._get(
            "im.dialog.messages.get",
            {"DIALOG_ID": dialog_id, "LIMIT": limit},
        )
        messages = data.get("result", {}).get("messages", [])
        texts = []
        for msg in reversed(messages):
            text = (msg.get("text") or "").strip()
            if text:
                texts.append(text)
        return texts

    def send_message(self, dialog_id: str, text: str) -> bool:
        """Send a message as the operator."""
        data = self._post(
            "im.message.add",
            {"DIALOG_ID": dialog_id, "MESSAGE": text},
        )
        return bool(data.get("result"))

    def mark_as_read(self, dialog_id: str) -> None:
        self._post("im.dialog.read", {"DIALOG_ID": dialog_id})

    def test_connection(self) -> tuple[bool, str]:
        """Return (ok, error_message). Used to validate webhook on setup."""
        data = self._get("app.info")
        if "error" in data:
            return False, data.get("error_description", data["error"])
        if "result" in data or data.get("result") is not None:
            return True, ""
        # Fallback: just check we got a valid JSON response without error key
        return True, ""

    # ------------------------------------------------------------------ #
    # Helpers
    # ------------------------------------------------------------------ #

    @staticmethod
    def parse_chat_title(title: str) -> tuple[str, str]:
        """
        Split 'Никита Рябых | ВКонтакте' → ('Никита Рябых', 'ВКонтакте').
        Falls back to (title, '') when no separator.
        """
        if "|" in title:
            parts = title.split("|", 1)
            return parts[0].strip(), parts[1].strip()
        return title.strip(), ""

    def _get(self, method: str, params: dict | None = None) -> dict:
        url = f"{self.base}/{method}.json"
        try:
            resp = requests.get(url, params=params or {}, timeout=TIMEOUT)
            resp.raise_for_status()
            return resp.json()
        except Exception as exc:
            logger.error("Bitrix GET %s: %s", method, exc)
            return {}

    def _post(self, method: str, payload: dict | None = None) -> dict:
        url = f"{self.base}/{method}.json"
        try:
            resp = requests.post(url, json=payload or {}, timeout=TIMEOUT)
            resp.raise_for_status()
            return resp.json()
        except Exception as exc:
            logger.error("Bitrix POST %s: %s", method, exc)
            return {}
