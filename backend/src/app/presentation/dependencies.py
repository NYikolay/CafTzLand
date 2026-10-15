from collections.abc import AsyncIterator

from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.health.check_readiness import CheckReadiness
from app.infrastructure.db.probe import AsyncDatabaseProbe


async def get_session(request: Request) -> AsyncIterator[AsyncSession]:
    sessionmaker = request.app.state.sessionmaker
    async with sessionmaker() as session:
        yield session


def get_readiness_check(request: Request) -> CheckReadiness:
    return CheckReadiness(AsyncDatabaseProbe(request.app.state.db_engine))
