from httpx import AsyncClient


async def test_admin_requires_login(client: AsyncClient) -> None:
    response = await client.get("/admin/")
    assert response.status_code == 302
    assert "/admin/login" in response.headers["location"]


async def test_admin_login_rejects_wrong_credentials(client: AsyncClient) -> None:
    response = await client.post(
        "/admin/login",
        data={"username": "admin", "password": "wrong-password"},
    )
    assert response.status_code == 400


async def test_admin_login_and_logout(client: AsyncClient) -> None:
    response = await client.post(
        "/admin/login",
        data={"username": "admin", "password": "test-admin-pass"},
    )
    assert response.status_code == 302
    assert response.headers["location"].endswith("/admin/")

    index = await client.get("/admin/")
    assert index.status_code == 200

    logout = await client.get("/admin/logout")
    assert logout.status_code == 302

    after_logout = await client.get("/admin/")
    assert after_logout.status_code == 302
