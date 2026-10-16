from application.products.list_products import ListProducts
from domain import Product, ProductKind


class FakeProductRepository:
    def __init__(self, products: list[Product]) -> None:
        self._products = products

    async def get_active(self, product_id: int) -> Product | None:
        return None

    async def get(self, product_id: int) -> Product | None:
        return None

    async def list_active(self) -> list[Product]:
        return self._products


async def test_returns_active_products() -> None:
    product = Product(
        id=1,
        code="BR",
        name="Бразилия Серрадо",
        kind=ProductKind.BEANS,
        tasting_notes=None,
        description=None,
        brew_method=None,
        variants=[],
    )

    assert await ListProducts(FakeProductRepository([product]))() == [product]
