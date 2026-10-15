from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from app.application.health.check_readiness import CheckReadiness
from app.infrastructure.config.settings import Settings
from app.main import create_app
from app.presentation.dependencies import get_readiness_check
from tests.conftest import FakeProbe


async def test_security_headers(client: AsyncClient) -> None:
    response = await client.get("/health/live")
    assert response.headers["x-content-type-options"] == "nosniff"
    assert response.headers["x-frame-options"] == "DENY"
    assert response.headers["referrer-policy"] == "strict-origin-when-cross-origin"
    assert "strict-transport-security" not in response.headers


async def test_request_id_generated(client: AsyncClient) -> None:
    response = await client.get("/health/live")
    request_id = response.headers["x-request-id"]
    assert len(request_id) == 32


async def test_request_id_echoed(client: AsyncClient) -> None:
    response = await client.get("/health/live", headers={"X-Request-ID": "abc-123"})
    assert response.headers["x-request-id"] == "abc-123"


async def test_invalid_request_id_replaced(client: AsyncClient) -> None:
    response = await client.get("/health/live", headers={"X-Request-ID": "bad id!!"})
    assert response.headers["x-request-id"] != "bad id!!"
    assert len(response.headers["x-request-id"]) == 32


async def test_gzip_enabled(app: FastAPI, client: AsyncClient) -> None:
    @app.get("/_test/big")
    async def big() -> dict[str, str]:
        return {"data": "x" * 2048}

    response = await client.get("/_test/big", headers={"Accept-Encoding": "gzip"})
    assert response.status_code == 200
    assert response.headers["content-encoding"] == "gzip"


async def test_hsts_when_https_redirect_enabled(test_settings: Settings) -> None:
    settings = test_settings.model_copy(update={"enable_https_redirect": True})
    application = create_app(settings)
    application.dependency_overrides[get_readiness_check] = lambda: CheckReadiness(
        FakeProbe(healthy=True)
    )
    transport = ASGITransport(app=application)
    async with AsyncClient(transport=transport, base_url="https://testserver") as client:
        response = await client.get("/health/live")
    assert response.headers["strict-transport-security"].startswith("max-age=")
