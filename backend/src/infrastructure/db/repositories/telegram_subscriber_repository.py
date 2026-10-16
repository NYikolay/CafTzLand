from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from domain.telegram import TelegramSubscriber
from infrastructure.db.models.telegram_subscriber import (
    TelegramSubscriber as TelegramSubscriberRow,
)


class SqlAlchemyTelegramSubscriberRepository:
    def __init__(self, sessionmaker: async_sessionmaker[AsyncSession]) -> None:
        self._sessionmaker = sessionmaker

    async def list_active(self) -> list[TelegramSubscriber]:
        statement = (
            select(TelegramSubscriberRow)
            .where(TelegramSubscriberRow.is_active.is_(True))
            .order_by(TelegramSubscriberRow.id)
        )
        async with self._sessionmaker() as session:
            rows = (await session.scalars(statement)).all()
        return [to_domain(row) for row in rows]

    async def deactivate(self, subscriber_id: int) -> None:
        async with self._sessionmaker() as session, session.begin():
            await session.execute(
                update(TelegramSubscriberRow)
                .where(TelegramSubscriberRow.id == subscriber_id)
                .values(is_active=False)
            )


def to_domain(row: TelegramSubscriberRow) -> TelegramSubscriber:
    return TelegramSubscriber(
        id=row.id,
        telegram_user_id=row.telegram_user_id,
        tg_link=row.tg_link,
        is_active=row.is_active,
    )
