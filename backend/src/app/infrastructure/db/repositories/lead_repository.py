from datetime import UTC, datetime, timedelta

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.domain.leads import Interest, Lead, LeadSource
from app.infrastructure.db.models.order import Order


class SqlAlchemyLeadRepository:
    def __init__(self, sessionmaker: async_sessionmaker[AsyncSession]) -> None:
        self._sessionmaker = sessionmaker

    async def add_if_not_recent(self, lead: Lead, window: timedelta) -> tuple[Lead, bool]:
        async with self._sessionmaker() as session, session.begin():
            await session.execute(
                select(func.pg_advisory_xact_lock(func.hashtextextended(lead.phone_number, 0)))
            )
            since = datetime.now(UTC) - window
            recent = await session.scalar(
                select(Order)
                .where(Order.phone_number == lead.phone_number, Order.created_at >= since)
                .order_by(Order.created_at.desc())
                .limit(1)
            )
            if recent is not None:
                return to_domain(recent), True
            row = Order(
                name=lead.name,
                interest=lead.interest.value,
                phone_number=lead.phone_number,
                product_id=lead.product_id,
                comment=lead.comment,
                is_handled=lead.is_handled,
                utm_source=lead.source.utm_source if lead.source else None,
                utm_medium=lead.source.utm_medium if lead.source else None,
                utm_campaign=lead.source.utm_campaign if lead.source else None,
                utm_content=lead.source.utm_content if lead.source else None,
                utm_term=lead.source.utm_term if lead.source else None,
                referrer=lead.source.referrer if lead.source else None,
                page_url=lead.source.page_url if lead.source else None,
                source_extra=(lead.source.extra or None) if lead.source else None,
            )
            session.add(row)
            await session.flush()
            return to_domain(row), False


def to_domain(order: Order) -> Lead:
    return Lead(
        name=order.name,
        phone_number=order.phone_number,
        interest=Interest(order.interest),
        product_id=order.product_id,
        comment=order.comment,
        source=_source_to_domain(order),
        is_handled=order.is_handled,
        id=order.id,
    )


def _source_to_domain(order: Order) -> LeadSource | None:
    extra = dict(order.source_extra or {})
    values = (
        order.utm_source,
        order.utm_medium,
        order.utm_campaign,
        order.utm_content,
        order.utm_term,
        order.referrer,
        order.page_url,
    )
    if all(value is None for value in values) and not extra:
        return None
    return LeadSource(
        utm_source=order.utm_source,
        utm_medium=order.utm_medium,
        utm_campaign=order.utm_campaign,
        utm_content=order.utm_content,
        utm_term=order.utm_term,
        referrer=order.referrer,
        page_url=order.page_url,
        extra=extra,
    )
