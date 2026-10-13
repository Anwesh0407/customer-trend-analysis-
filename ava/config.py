"""
AVA Core Configuration
Settings management via environment variables and .env file.
"""

import os
from typing import Optional, List
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="allow")

    APP_NAME: str = "Amazon Vendor Assist"
    APP_VERSION: str = "0.2.0"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")

    # Server
    HOST: str = os.getenv("APP_HOST", "0.0.0.0")
    PORT: int = int(os.getenv("APP_PORT", "8000"))

    # Database
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./ava.db")
    DB_USER: str = os.getenv("DB_USER", "postgres")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "")
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_PORT: str = os.getenv("DB_PORT", "5432")
    DB_NAME: str = os.getenv("DB_NAME", "amazon_vendor_assist")

    # CORS
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:5173")

    # Compliance & HTTP Client
    BLOCKED_DOMAINS: List[str] = [
        "amazon.in",
        "amazon.com",
        "media-amazon.com",
        "images-amazon.com",
        "ssl-images-amazon.com",
        "m.media-amazon.com"
    ]
    USER_AGENT: str = os.getenv("USER_AGENT", "AVA-Vendor-Assist-Research-Bot/1.0 (+http://example.com/bot)")
    RATE_LIMIT_DELAY: float = float(os.getenv("RATE_LIMIT_DELAY", "1.0"))
    REQUEST_TIMEOUT: float = float(os.getenv("REQUEST_TIMEOUT", "10.0"))

    # Creators API (Conditional)
    AMAZON_CREATORS_API_KEY: Optional[str] = os.getenv("AMAZON_CREATORS_API_KEY")
    AMAZON_CREATORS_API_SECRET: Optional[str] = os.getenv("AMAZON_CREATORS_API_SECRET")
    AMAZON_ASSOCIATE_TAG: Optional[str] = os.getenv("AMAZON_ASSOCIATE_TAG")

    # Ask AVA (Gemini & Fallback)
    GEMINI_API_KEY: Optional[str] = os.getenv("GEMINI_API_KEY")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-1.5-flash")
    ASK_AVA_MODE: str = os.getenv("ASK_AVA_MODE", "auto")  # auto | demo | gemini

    # Analytics Guardrails
    MIN_SAMPLE_SIZE: int = int(os.getenv("MIN_SAMPLE_SIZE", "30"))
    MIN_GROUP_SIZE: int = int(os.getenv("MIN_GROUP_SIZE", "5"))
    MAX_PRICE_CAP_INR: float = float(os.getenv("MAX_PRICE_CAP_INR", "50000.0"))

    @property
    def database_url(self) -> str:
        return self.DATABASE_URL

settings = Settings()

def get_settings() -> Settings:
    return settings
