from fastapi import FastAPI
from httpx import AsyncClient

from application import CheckReadiness
from presentation import get_readiness_check
from tests.conftest import FakeProbe


async def test_live(client: AsyncClient) -> None:
    response = await client.get("/health/live")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


async def test_ready_when_database_up(client: AsyncClient) -> None:
    response = await client.get("/health/ready")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "database": "ok"}


async def test_ready_when_database_down(app: FastAPI, client: AsyncClient) -> None:
    app.dependency_overrides[get_readiness_check] = lambda: CheckReadiness(FakeProbe(healthy=False))
    response = await client.get("/health/ready")
    assert response.status_code == 503
    assert response.json() == {"status": "unavailable", "database": "down"}
