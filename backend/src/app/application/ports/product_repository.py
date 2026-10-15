from typing import Protocol

from app.domain.products import Product


class ProductRepository(Protocol):
    async def get_active(self, product_id: int) -> Product | None: ...

    async def list_active(self) -> list[Product]: ...
