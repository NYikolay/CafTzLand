import logging
from decimal import Decimal
from typing import Any

from pydantic import BaseModel, ConfigDict, Field, field_validator
from pydantic_core import PydanticCustomError

from app.domain.leads import Interest, InterestName, Lead, LeadSource
from app.domain.products import ProductKind
from app.infrastructure.phone import normalize_belarus_phone

logger = logging.getLogger(__name__)

PHONE_INVALID_MESSAGE = "Пожалуйста, введите корректный номер телефона"
SOURCE_INVALID_MESSAGE = "Некорректный параметр источника"
MAX_SOURCE_VALUE_LENGTH = 1024
SOURCE_KEY_MAX_LENGTHS: dict[str, int] = {
    "utm_source": 255,
    "utm_medium": 255,
    "utm_campaign": 255,
    "utm_content": 255,
    "utm_term": 255,
    "referrer": 1024,
    "page_url": 1024,
}
KNOWN_SOURCE_KEYS = frozenset(SOURCE_KEY_MAX_LENGTHS)


class LeadCreateRequest(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)

    name: str = Field(min_length=1, max_length=200)
    phone_number: str = Field(min_length=1, max_length=32)
    interest: Interest
    product_id: int | None = Field(default=None, ge=1)
    comment: str | None = Field(default=None, max_length=2000)
    source: dict[str, str] | None = None

    @field_validator("phone_number")
    @classmethod
    def _normalize_phone(cls, value: str) -> str:
        try:
            return normalize_belarus_phone(value)
        except ValueError as exc:
            raise PydanticCustomError("phone_invalid", PHONE_INVALID_MESSAGE) from exc

    @field_validator("source", mode="before")
    @classmethod
    def _clean_source(cls, value: Any) -> Any:
        if value is None:
            return None
        if not isinstance(value, dict):
            raise PydanticCustomError("source_invalid", SOURCE_INVALID_MESSAGE)
        cleaned: dict[str, str] = {}
        for key, raw in value.items():
            if not isinstance(key, str) or not isinstance(raw, str):
                raise PydanticCustomError("source_invalid", SOURCE_INVALID_MESSAGE)
            stripped = raw.strip()
            if not stripped:
                continue
            limit = SOURCE_KEY_MAX_LENGTHS.get(key, MAX_SOURCE_VALUE_LENGTH)
            if len(stripped) > limit:
                logger.warning("Source value for %r truncated to %d chars", key, limit)
                stripped = stripped[:limit]
            cleaned[key] = stripped
        return cleaned

    def to_lead(self) -> Lead:
        return Lead(
            name=self.name,
            phone_number=self.phone_number,
            interest=self.interest,
            product_id=self.product_id,
            comment=self.comment,
            source=to_domain_source(self.source),
        )


def to_domain_source(raw: dict[str, str] | None) -> LeadSource | None:
    if raw is None:
        return None
    extra = {key: value for key, value in raw.items() if key not in KNOWN_SOURCE_KEYS}
    return LeadSource(
        utm_source=raw.get("utm_source"),
        utm_medium=raw.get("utm_medium"),
        utm_campaign=raw.get("utm_campaign"),
        utm_content=raw.get("utm_content"),
        utm_term=raw.get("utm_term"),
        referrer=raw.get("referrer"),
        page_url=raw.get("page_url"),
        extra=extra,
    )


class LeadCreateResponse(BaseModel):
    id: int
    duplicate: bool


class InterestOptionOut(BaseModel):
    value: Interest
    label: InterestName


class ProductVariantOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    packaging_label: str
    price: Decimal
    weight_grams: int | None
    units: int | None


class ProductOut(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    code: str
    name: str
    kind: ProductKind
    tasting_notes: str | None
    description: str | None
    brew_method: str | None
    variants: list[ProductVariantOut]
