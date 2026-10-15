from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient

from app.domain.exceptions import NotFoundError
from app.infrastructure.config.settings import AppEnv, Settings
from app.main import create_app


async def test_domain_error_envelope(app: FastAPI, client: AsyncClient) -> None:
    @app.get("/_test/not-found")
    async def not_found() -> None:
        raise NotFoundError("Item not found")

    response = await client.get("/_test/not-found")
    assert response.status_code == 404
    assert response.json() == {"error": {"code": "not_found", "message": "Item not found"}}


async def test_validation_error_envelope(app: FastAPI, client: AsyncClient) -> None:
    @app.get("/_test/validate")
    async def validate(q: int) -> dict[str, int]:
        return {"q": q}

    response = await client.get("/_test/validate", params={"q": "abc"})
    assert response.status_code == 422
    body = response.json()
    assert body["error"]["code"] == "validation_error"
    assert isinstance(body["error"]["details"], list)


async def test_unknown_route_envelope(client: AsyncClient) -> None:
    response = await client.get("/missing")
    assert response.status_code == 404
    body = response.json()
    assert body["error"]["code"] == "http_404"
    assert body["error"]["message"] == "Not Found"


async def test_internal_error_exposes_details_locally(app: FastAPI) -> None:
    @app.get("/_test/boom")
    async def boom() -> None:
        raise RuntimeError("secret detail")

    transport = ASGITransport(app=app, raise_app_exceptions=False)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.get("/_test/boom")
    assert response.status_code == 500
    assert response.json()["error"]["details"] == "secret detail"


async def test_internal_error_hides_details_in_production(
    test_settings: Settings,
) -> None:
    settings = test_settings.model_copy(update={"app_env": AppEnv.PRODUCTION, "enable_docs": False})
    application = create_app(settings)

    @application.get("/_test/boom")
    async def boom() -> None:
        raise RuntimeError("secret detail")

    transport = ASGITransport(app=application, raise_app_exceptions=False)
    async with AsyncClient(transport=transport, base_url="http://testserver") as client:
        response = await client.get("/_test/boom")
    assert response.status_code == 500
    body = response.json()
    assert body["error"]["code"] == "internal_error"
    assert "details" not in body["error"]
