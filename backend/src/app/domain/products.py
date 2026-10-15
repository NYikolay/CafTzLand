from dataclasses import dataclass
from decimal import Decimal
from enum import StrEnum


class ProductKind(StrEnum):
    BEANS = "beans"
    ASSORTED = "assorted"
    SET = "set"


@dataclass(frozen=True, slots=True)
class ProductVariant:
    id: int
    packaging_label: str
    price: Decimal
    weight_grams: int | None = None
    units: int | None = None


@dataclass(frozen=True, slots=True)
class Product:
    id: int
    code: str
    name: str
    kind: ProductKind
    tasting_notes: str | None
    description: str | None
    brew_method: str | None
    variants: list[ProductVariant]
