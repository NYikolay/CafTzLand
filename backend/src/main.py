import logging
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqladmin import Admin

from infrastructure.config.settings import AppEnv, Settings, get_settings
from infrastructure.db.session import create_db_engine, create_sessionmaker
from infrastructure.logging import configure_logging
from infrastructure.telegram.notifier import create_telegram_bot
from presentation.admin.auth import AdminAuthBackend
from presentation.admin.orders import OrderAdmin
from presentation.admin.products import ProductAdmin, ProductVariantAdmin
from presentation.admin.subscribers import TelegramSubscriberAdmin
from presentation.api import health
from presentation.api.v1 import router as api_v1_router
from presentation.errors import register_exception_handlers
from presentation.middlewares import register_middlewares

logger = logging.getLogger(__name__)


def create_app(settings: Settings | None = None) -> FastAPI:
    app_settings = settings or get_settings()
    configure_logging(app_settings.log_level)

    engine = create_db_engine(app_settings)
    sessionmaker = create_sessionmaker(engine)
    telegram_bot = create_telegram_bot(app_settings.telegram_bot_token)

    if telegram_bot is None:
        logger.warning("TELEGRAM_BOT_TOKEN is not set — telegram lead notifications are disabled")

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        try:
            yield
        finally:
            if telegram_bot is not None:
                await telegram_bot.session.close()
            await engine.dispose()

    app = FastAPI(
        title=app_settings.app_name,
        docs_url="/docs" if app_settings.docs_enabled else None,
        redoc_url="/redoc" if app_settings.docs_enabled else None,
        openapi_url="/openapi.json" if app_settings.docs_enabled else None,
        lifespan=lifespan,
    )
    app.state.settings = app_settings
    app.state.db_engine = engine
    app.state.sessionmaker = sessionmaker
    app.state.telegram_bot = telegram_bot

    register_middlewares(app, app_settings)

    register_exception_handlers(
        app,
        expose_details=app_settings.app_env is not AppEnv.PRODUCTION,
    )

    admin = Admin(
        app=app,
        engine=engine,
        authentication_backend=AdminAuthBackend(app_settings),
        title=app_settings.app_name,
        base_url=app_settings.admin_password
    )
    admin.add_view(OrderAdmin)
    admin.add_view(ProductAdmin)
    admin.add_view(ProductVariantAdmin)
    admin.add_view(TelegramSubscriberAdmin)

    app.include_router(health.router)
    app.include_router(api_v1_router)
    return app
