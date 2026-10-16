from collections.abc import AsyncIterator
from datetime import timedelta

from fastapi import Request
from sqlalchemy.ext.asyncio import AsyncSession

from application.health.check_readiness import CheckReadiness
from application.leads.create_lead import CreateLead
from application.leads.list_interest_options import ListInterestOptions
from application.products.list_products import ListProducts
from application.telegram.notify_new_lead import NotifyNewLead
from infrastructure.db.probe import AsyncDatabaseProbe
from infrastructure.db.repositories.lead_repository import SqlAlchemyLeadRepository
from infrastructure.db.repositories.product_repository import SqlAlchemyProductRepository
from infrastructure.db.repositories.telegram_subscriber_repository import (
    SqlAlchemyTelegramSubscriberRepository,
)
from infrastructure.telegram.notifier import AiogramTelegramNotifier


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


def get_list_interest_options() -> ListInterestOptions:
    return ListInterestOptions()


def get_notify_new_lead(request: Request) -> NotifyNewLead | None:
    bot = request.app.state.telegram_bot
    if bot is None:
        return None
    sessionmaker = request.app.state.sessionmaker
    return NotifyNewLead(
        subscribers=SqlAlchemyTelegramSubscriberRepository(sessionmaker),
        products=SqlAlchemyProductRepository(sessionmaker),
        notifier=AiogramTelegramNotifier(bot),
    )
