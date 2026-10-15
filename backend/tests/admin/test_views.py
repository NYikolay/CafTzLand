import pytest
from httpx import AsyncClient

ADMIN_LISTS = [
    "/admin/order/list",
    "/admin/product/list",
    "/admin/product-variant/list",
    "/admin/telegram-subscriber/list",
]


async def log_in(client: AsyncClient) -> None:
    response = await client.post(
        "/admin/login",
        data={"username": "admin", "password": "test-admin-pass"},
    )
    assert response.status_code == 302


@pytest.mark.parametrize("path", ADMIN_LISTS)
async def test_admin_list_requires_login(path: str, client: AsyncClient) -> None:
    response = await client.get(path)
    assert response.status_code == 302
    assert "/admin/login" in response.headers["location"]


async def test_admin_order_create_forbidden_when_authenticated(client: AsyncClient) -> None:
    await log_in(client)
    response = await client.get("/admin/order/create")
    assert response.status_code == 403


async def test_admin_unknown_identity_not_found_when_authenticated(client: AsyncClient) -> None:
    await log_in(client)
    response = await client.get("/admin/nonexistent/list")
    assert response.status_code == 404
