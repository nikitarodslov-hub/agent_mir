import os
from dataclasses import dataclass
from dotenv import load_dotenv


@dataclass
class Config:
    CLAUDE_API_KEY: str
    BITRIX_URL: str
    BITRIX_OPENLINES_PATH: str
    MOYSKLAD_LOGIN: str
    MOYSKLAD_PASSWORD: str
    SESSION_FILE: str = "bitrix_session.json"
    PROCESSED_FILE: str = "processed_dialogs.json"

    @classmethod
    def load(cls) -> "Config":
        load_dotenv()
        return cls(
            CLAUDE_API_KEY=os.getenv("CLAUDE_API_KEY", ""),
            BITRIX_URL=os.getenv("BITRIX_URL", "").rstrip("/"),
            BITRIX_OPENLINES_PATH=os.getenv("BITRIX_OPENLINES_PATH", "/crm/chats/"),
            MOYSKLAD_LOGIN=os.getenv("MOYSKLAD_LOGIN", ""),
            MOYSKLAD_PASSWORD=os.getenv("MOYSKLAD_PASSWORD", ""),
        )
