import pytest

from app.infrastructure.config.settings import Settings

ENV_NAMES = [
    "APP_ENV",
    "APP_NAME",
    "POSTGRES_USER",
    "POSTGRES_PASSWORD",
    "POSTGRES_DB",
    "POSTGRES_HOST",
    "POSTGRES_PORT",
    "SECRET_KEY",
    "ADMIN_USERNAME",
    "ADMIN_PASSWORD",
    "ALLOWED_HOSTS",
    "CORS_ORIGINS",
    "ENABLE_HTTPS_REDIRECT",
    "ENABLE_DOCS",
    "LOG_LEVEL",
    "SQL_ECHO",
]


@pytest.fixture(autouse=True)
def clean_env(monkeypatch: pytest.MonkeyPatch) -> None:
    for name in ENV_NAMES:
        monkeypatch.delenv(name, raising=False)


@pytest.fixture
def test_settings() -> Settings:
    return Settings(
        _env_file=None,
        secret_key="test-secret-key-0123456789abcdef",
        admin_username="admin",
        admin_password="test-admin-pass",
        allowed_hosts=["testserver", "localhost"],
        cors_origins=["http://frontend.test"],
    )
