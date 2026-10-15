from fastapi import FastAPI
from httpx import ASGITransport, AsyncClient


async def test_forbidden_host(app: FastAPI) -> None:
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://evil.test") as client:
        response = await client.get("/health/live")
    assert response.status_code == 400


async def test_cors_preflight(client: AsyncClient) -> None:
    response = await client.options(
        "/health/live",
        headers={
            "Origin": "http://frontend.test",
            "Access-Control-Request-Method": "GET",
        },
    )
    assert response.status_code == 200
    assert response.headers["access-control-allow-origin"] == "http://frontend.test"
