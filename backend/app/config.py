import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database
    DATABASE_URL: str = "postgresql://user:password@localhost/family_roots"
    NEO4J_URI: str = "bolt://localhost:7687"
    NEO4J_USER: str = "neo4j"
    NEO4J_PASSWORD: str = "password"

    # JWT
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # API
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Семейные корни"

    # Telegram Bot
    TELEGRAM_TOKEN: str = os.getenv("TELEGRAM_TOKEN", "")
    TELEGRAM_WEBHOOK_URL: str = "https://api.familyroots.ru/telegram"

    # VK Bot
    VK_TOKEN: str = os.getenv("VK_TOKEN", "")
    VK_GROUP_ID: str = os.getenv("VK_GROUP_ID", "")

    # Redis
    REDIS_URL: str = "redis://localhost:6379"

    # Email
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = os.getenv("SMTP_USER", "")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")

    # Frontend
    FRONTEND_URL: str = "http://localhost:3000"

    # Subscription prices (in kopecks)
    BASIC_PRICE: int = 0
    RESEARCHER_PRICE: int = 249000  # 2490 RUB
    PROFESSIONAL_PRICE: int = 3000000  # 30000 RUB

    class Config:
        env_file = ".env"

settings = Settings()
