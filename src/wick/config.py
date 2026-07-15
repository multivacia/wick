"""Application settings via pydantic-settings."""

from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    database_url: str = Field(
        default="postgresql+psycopg://wick:wick@localhost:5432/wick",
        alias="DATABASE_URL",
    )
    candle_close_safety_delay_seconds: int = Field(
        default=30,
        alias="CANDLE_CLOSE_SAFETY_DELAY_SECONDS",
    )
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")
    brapi_token: str | None = Field(default=None, alias="BRAPI_TOKEN")
    brapi_base_url: str = Field(
        default="https://brapi.dev/api",
        alias="BRAPI_BASE_URL",
    )
    ingestion_max_retries: int = Field(default=5, alias="INGESTION_MAX_RETRIES")
    ingestion_backoff_base_seconds: float = Field(
        default=1.0,
        alias="INGESTION_BACKOFF_BASE_SECONDS",
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()
