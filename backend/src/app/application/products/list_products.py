from app.application.ports.product_repository import ProductRepository
from app.domain.products import Product


class ListProducts:
    def __init__(self, products: ProductRepository) -> None:
        self._products = products

    async def __call__(self) -> list[Product]:
        return await self._products.list_active()
