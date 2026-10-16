from collections.abc import Sequence

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from sqlalchemy.orm import selectinload

from domain.products import Product, ProductKind, ProductVariant
from infrastructure.db.models.product import Product as ProductRow
from infrastructure.db.models.product import ProductVariant as ProductVariantRow


class SqlAlchemyProductRepository:
    def __init__(self, sessionmaker: async_sessionmaker[AsyncSession]) -> None:
        self._sessionmaker = sessionmaker

    async def get(self, product_id: int) -> Product | None:
        async with self._sessionmaker() as session:
            row = await session.get(ProductRow, product_id)
            if row is None:
                return None
            return to_domain(row, [])

    async def get_active(self, product_id: int) -> Product | None:
        async with self._sessionmaker() as session:
            row = await session.get(ProductRow, product_id)
            if row is None or not row.is_active:
                return None
            return to_domain(row, [])

    async def list_active(self) -> list[Product]:
        statement = (
            select(ProductRow)
            .where(ProductRow.is_active.is_(True))
            .options(selectinload(ProductRow.variants))
            .order_by(ProductRow.sort_order, ProductRow.id)
        )
        async with self._sessionmaker() as session:
            rows = (await session.scalars(statement)).all()
        return [
            to_domain(
                row,
                sorted(
                    (variant for variant in row.variants if variant.is_active),
                    key=lambda variant: (variant.sort_order, variant.id),
                ),
            )
            for row in rows
        ]


def to_domain(row: ProductRow, variants: Sequence[ProductVariantRow]) -> Product:
    return Product(
        id=row.id,
        code=row.code,
        name=row.name,
        kind=ProductKind(row.kind),
        tasting_notes=row.tasting_notes,
        description=row.description,
        brew_method=row.brew_method,
        variants=[
            ProductVariant(
                id=variant.id,
                packaging_label=variant.packaging_label,
                price=variant.price,
                weight_grams=variant.weight_grams,
                units=variant.units,
            )
            for variant in variants
        ],
    )
