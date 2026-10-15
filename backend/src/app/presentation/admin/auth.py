from hmac import compare_digest

from sqladmin.authentication import AuthenticationBackend
from starlette.requests import Request

from app.infrastructure.config.settings import Settings


class AdminAuthBackend(AuthenticationBackend):
    def __init__(self, settings: Settings) -> None:
        super().__init__(secret_key=settings.secret_key)
        self._username = settings.admin_username
        self._password = settings.admin_password

    async def login(self, request: Request) -> bool:
        form = await request.form()
        username = form.get("username")
        password = form.get("password")
        if not isinstance(username, str) or not isinstance(password, str):
            return False
        username_ok = compare_digest(username, self._username)
        password_ok = compare_digest(password, self._password)
        if username_ok and password_ok:
            request.session.update({"authenticated": True})
            return True
        return False

    async def logout(self, request: Request) -> bool:
        request.session.clear()
        return True

    async def authenticate(self, request: Request) -> bool:
        return bool(request.session.get("authenticated"))
