from typing import Any

import pytest
from pydantic import ValidationError

from app.infrastructure.config.settings import Settings


def make_settings(**overrides: object) -> Settings:
    values: dict[str, Any] = {
        "secret_key": "test-secret-key-0123456789abcdef",
        "admin_password": "test-admin-pass",
    }
    values.update(overrides)
    return Settings(_env_file=None, **values)


def test_database_url_is_asyncpg() -> None:
    settings = make_settings(
        postgres_user="u",
        postgres_password="p",
        postgres_db="d",
        postgres_host="h",
        postgres_port=1234,
    )
    assert settings.database_url == "postgresql+asyncpg://u:p@h:1234/d"


def test_docs_enabled_default_local() -> None:
    assert make_settings().docs_enabled is True


def test_docs_disabled_in_production() -> None:
    assert make_settings(app_env="production").docs_enabled is False


def test_docs_can_be_forced() -> None:
    assert make_settings(app_env="production", enable_docs=True).docs_enabled is True


def test_short_secret_key_rejected() -> None:
    with pytest.raises(ValidationError):
        make_settings(secret_key="short")


def test_short_admin_password_rejected() -> None:
    with pytest.raises(ValidationError):
        make_settings(admin_password="short")


def test_lead_dedup_window_default() -> None:
    assert make_settings().lead_dedup_window_minutes == 10


def test_lead_dedup_window_rejects_zero() -> None:
    with pytest.raises(ValidationError):
        make_settings(lead_dedup_window_minutes=0)


def test_lead_dedup_window_rejects_over_a_day() -> None:
    with pytest.raises(ValidationError):
        make_settings(lead_dedup_window_minutes=1441)


def test_lead_dedup_window_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("LEAD_DEDUP_WINDOW_MINUTES", "5")
    settings = Settings(
        _env_file=None,
        secret_key="test-secret-key-0123456789abcdef",
        admin_password="test-admin-pass",
    )
    assert settings.lead_dedup_window_minutes == 5


def test_telegram_bot_token_defaults_to_none() -> None:
    assert make_settings().telegram_bot_token is None


def test_telegram_bot_token_empty_env_means_disabled(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "")
    settings = Settings(
        _env_file=None,
        secret_key="test-secret-key-0123456789abcdef",
        admin_password="test-admin-pass",
    )
    assert settings.telegram_bot_token is None


def test_telegram_bot_token_from_env(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("TELEGRAM_BOT_TOKEN", "123456:ABC-DEF")
    settings = Settings(
        _env_file=None,
        secret_key="test-secret-key-0123456789abcdef",
        admin_password="test-admin-pass",
    )
    assert settings.telegram_bot_token == "123456:ABC-DEF"
