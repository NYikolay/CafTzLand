from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.infrastructure.config.settings import Settings, get_settings
from app.infrastructure.db.session import create_db_engine, create_sessionmaker
from app.infrastructure.logging import configure_logging
from app.presentation.api import health
from app.presentation.api.v1 import router as api_v1_router
from app.presentation.middlewares import register_middlewares


def create_app(settings: Settings | None = None) -> FastAPI:
    app_settings = settings or get_settings()
    configure_logging(app_settings.log_level)

    engine = create_db_engine(app_settings)
    sessionmaker = create_sessionmaker(engine)

    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        yield
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

    register_middlewares(app, app_settings)

    app.include_router(health.router)
    app.include_router(api_v1_router)
    return app
