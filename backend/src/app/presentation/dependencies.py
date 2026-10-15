from collections.abc import AsyncIterator
from datetime import timedelta

from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.application.health.check_readiness import CheckReadiness
from app.application.leads.create_lead import CreateLead
from app.application.products.list_products import ListProducts
from app.infrastructure.db.probe import AsyncDatabaseProbe
from app.infrastructure.db.repositories.lead_repository import SqlAlchemyLeadRepository
from app.infrastructure.db.repositories.product_repository import SqlAlchemyProductRepository


async def get_session(request: Request) -> AsyncIterator[AsyncSession]:
    sessionmaker = request.app.state.sessionmaker
    async with sessionmaker() as session:
        yield session


def get_readiness_check(request: Request) -> CheckReadiness:
    return CheckReadiness(AsyncDatabaseProbe(request.app.state.db_engine))


def get_create_lead(request: Request) -> CreateLead:
    sessionmaker = request.app.state.sessionmaker
    return CreateLead(
        leads=SqlAlchemyLeadRepository(sessionmaker),
        products=SqlAlchemyProductRepository(sessionmaker),
        window=timedelta(minutes=request.app.state.settings.lead_dedup_window_minutes),
    )


def get_list_products(request: Request) -> ListProducts:
    return ListProducts(SqlAlchemyProductRepository(request.app.state.sessionmaker))
