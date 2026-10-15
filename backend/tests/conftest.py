from collections.abc import AsyncIterator

import pytest
from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from app.application.health.check_readiness import CheckReadiness
from app.infrastructure.config.settings import Settings
from app.main import create_app
from app.presentation.dependencies import get_readiness_check

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
    "LEAD_DEDUP_WINDOW_MINUTES",
]


class FakeProbe:
    def __init__(self, *, healthy: bool) -> None:
        self._healthy = healthy

    async def ping(self) -> bool:
        return self._healthy


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


@pytest.fixture
def app(test_settings: Settings) -> FastAPI:
    application = create_app(test_settings)
    application.dependency_overrides[get_readiness_check] = lambda: CheckReadiness(
        FakeProbe(healthy=True)
    )
    return application


@pytest.fixture
async def client(app: FastAPI) -> AsyncIterator[AsyncClient]:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        yield client
