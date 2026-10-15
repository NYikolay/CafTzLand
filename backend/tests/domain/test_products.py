from decimal import Decimal

from app.domain.products import ProductKind, ProductVariant


def test_product_kind_values() -> None:
    assert [kind.value for kind in ProductKind] == ["beans", "assorted", "set"]


def test_product_variant_holds_price() -> None:
    variant = ProductVariant(
        id=1,
        packaging_label="250 Г",
        price=Decimal("26.00"),
        weight_grams=250,
        units=None,
    )
    assert variant.price == Decimal("26.00")
    assert variant.units is None
