from enum import StrEnum
from functools import lru_cache
from typing import Any

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import URL


class AppEnv(StrEnum):
    LOCAL = "local"
    DEV = "dev"
    PRODUCTION = "production"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    app_env: AppEnv = AppEnv.LOCAL
    app_name: str = "VitaiWorld API"

    postgres_user: str = "vitai"
    postgres_password: str = "vitai"
    postgres_db: str = "vitai"
    postgres_host: str = "localhost"
    postgres_port: int = 5432

    secret_key: str = Field(min_length=32)
    admin_username: str = "admin"
    admin_password: str = Field(min_length=8)
    admin_url: str = "/admin"

    allowed_hosts: list[str] = Field(default_factory=lambda: ["localhost", "127.0.0.1"])
    cors_origins: list[str] = Field(default_factory=list)
    enable_https_redirect: bool = False
    enable_docs: bool | None = None
    log_level: str = "INFO"
    sql_echo: bool = False
    lead_dedup_window_minutes: int = Field(default=10, ge=1, le=1440)
    telegram_bot_token: str | None = None

    @field_validator("telegram_bot_token", mode="before")
    @classmethod
    def _blank_telegram_token_to_none(cls, value: Any) -> Any:
        if isinstance(value, str) and not value.strip():
            return None
        return value

    @property
    def database_url(self) -> str:
        return URL.create(
            "postgresql+asyncpg",
            username=self.postgres_user,
            password=self.postgres_password,
            host=self.postgres_host,
            port=self.postgres_port,
            database=self.postgres_db,
        ).render_as_string(hide_password=False)

    @property
    def docs_enabled(self) -> bool:
        if self.enable_docs is not None:
            return self.enable_docs
        return self.app_env is not AppEnv.PRODUCTION


@lru_cache
def get_settings() -> Settings:
    return Settings()
