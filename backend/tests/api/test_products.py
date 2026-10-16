from decimal import Decimal

from fastapi import FastAPI
from httpx import AsyncClient

from domain import Product, ProductKind, ProductVariant
from presentation import get_list_products

PRODUCTS = [
    Product(
        id=1,
        code="BR",
        name="Бразилия Серрадо",
        kind=ProductKind.BEANS,
        tasting_notes="Шоколад · орехи · карамель",
        description="Плотный и спокойный. Понятный кофе на каждый день.",
        brew_method="Для эспрессо, турки и молочных напитков",
        variants=[
            ProductVariant(
                id=1,
                packaging_label="250 Г",
                price=Decimal("26.00"),
                weight_grams=250,
                units=None,
            ),
        ],
    ),
]


class FakeListProducts:
    async def __call__(self) -> list[Product]:
        return PRODUCTS


async def test_lists_products_with_variants(app: FastAPI, client: AsyncClient) -> None:
    app.dependency_overrides[get_list_products] = lambda: FakeListProducts()

    response = await client.get("/api/v1/products")

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "code": "BR",
            "name": "Бразилия Серрадо",
            "kind": "beans",
            "tasting_notes": "Шоколад · орехи · карамель",
            "description": "Плотный и спокойный. Понятный кофе на каждый день.",
            "brew_method": "Для эспрессо, турки и молочных напитков",
            "variants": [
                {
                    "id": 1,
                    "packaging_label": "250 Г",
                    "price": "26.00",
                    "weight_grams": 250,
                    "units": None,
                }
            ],
        }
    ]
