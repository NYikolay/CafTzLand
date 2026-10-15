import pytest
from httpx import AsyncClient

ADMIN_LISTS = [
    "/admin/order/list",
    "/admin/product/list",
    "/admin/product-variant/list",
]


@pytest.mark.parametrize("path", ADMIN_LISTS)
async def test_admin_list_requires_login(path: str, client: AsyncClient) -> None:
    response = await client.get(path)
    assert response.status_code == 302
    assert "/admin/login" in response.headers["location"]
