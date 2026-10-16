from decimal import Decimal

from domain import ProductKind
from infrastructure.db import Product as ProductRow
from infrastructure.db import ProductVariant as VariantRow
from infrastructure.db.repositories.product_repository import to_domain


def make_variant(**overrides: object) -> VariantRow:
    values: dict[str, object] = {
        "id": 11,
        "product_id": 3,
        "packaging_label": "250 Г",
        "price": Decimal("26.00"),
        "weight_grams": 250,
        "units": None,
        "is_active": True,
        "sort_order": 1,
    }
    values.update(overrides)
    return VariantRow(**values)


def make_product(**overrides: object) -> ProductRow:
    values: dict[str, object] = {
        "id": 3,
        "code": "BR",
        "name": "Бразилия Серрадо",
        "kind": "beans",
        "tasting_notes": "Шоколад · орехи · карамель",
        "description": "Плотный и спокойный.",
        "brew_method": "Для эспрессо",
        "is_active": True,
        "sort_order": 1,
    }
    values.update(overrides)
    return ProductRow(**values)


def test_maps_product_with_variants() -> None:
    product = to_domain(make_product(), [make_variant()])

    assert product.id == 3
    assert product.code == "BR"
    assert product.name == "Бразилия Серрадо"
    assert product.kind is ProductKind.BEANS
    assert product.tasting_notes == "Шоколад · орехи · карамель"
    assert len(product.variants) == 1
    variant = product.variants[0]
    assert variant.id == 11
    assert variant.packaging_label == "250 Г"
    assert variant.price == Decimal("26.00")
    assert variant.weight_grams == 250
    assert variant.units is None
