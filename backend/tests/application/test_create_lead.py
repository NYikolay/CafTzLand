from dataclasses import replace
from datetime import timedelta

import pytest

from application.leads import (
    PRODUCT_UNAVAILABLE_MESSAGE,
    CreateLead,
    CreateLeadResult,
)
from domain.exceptions import ValidationError
from domain import Interest, Lead
from domain import Product, ProductKind

WINDOW = timedelta(minutes=10)


class FakeLeadRepository:
    def __init__(self, existing: Lead | None = None) -> None:
        self._existing = existing
        self.windows: list[timedelta] = []
        self.saved: list[Lead] = []

    async def add_if_not_recent(self, lead: Lead, window: timedelta) -> tuple[Lead, bool]:
        self.windows.append(window)
        if self._existing is not None:
            return self._existing, True
        stored = replace(lead, id=1)
        self.saved.append(stored)
        return stored, False


class FakeProductRepository:
    def __init__(self, active_ids: set[int]) -> None:
        self._active_ids = active_ids
        self.calls: list[int] = []

    async def get_active(self, product_id: int) -> Product | None:
        self.calls.append(product_id)
        if product_id not in self._active_ids:
            return None
        return Product(
            id=product_id,
            code="BR",
            name="Бразилия Серрадо",
            kind=ProductKind.BEANS,
            tasting_notes=None,
            description=None,
            brew_method=None,
            variants=[],
        )

    async def get(self, product_id: int) -> Product | None:
        return None

    async def list_active(self) -> list[Product]:
        return []


def make_lead(product_id: int | None = None) -> Lead:
    return Lead(
        name="Иван",
        phone_number="+375291234567",
        interest=Interest.SUBSCRIPTION,
        product_id=product_id,
    )


async def test_creates_new_lead() -> None:
    leads = FakeLeadRepository()
    use_case = CreateLead(leads=leads, products=FakeProductRepository(set()), window=WINDOW)

    result = await use_case(make_lead())

    assert isinstance(result, CreateLeadResult)
    assert result.duplicate is False
    assert result.lead.id == 1
    assert result.lead.name == "Иван"
    assert result.lead.phone_number == "+375291234567"
    assert leads.windows == [WINDOW]


async def test_returns_existing_lead_within_window() -> None:
    existing = Lead(
        name="Иван",
        phone_number="+375291234567",
        interest=Interest.SUBSCRIPTION,
        id=7,
    )
    leads = FakeLeadRepository(existing=existing)
    use_case = CreateLead(leads=leads, products=FakeProductRepository(set()), window=WINDOW)

    result = await use_case(make_lead())

    assert result.duplicate is True
    assert result.lead.id == 7
    assert leads.saved == []


async def test_rejects_unknown_product() -> None:
    use_case = CreateLead(
        leads=FakeLeadRepository(),
        products=FakeProductRepository(active_ids={5}),
        window=WINDOW,
    )

    with pytest.raises(ValidationError) as exc_info:
        await use_case(make_lead(product_id=3))

    assert exc_info.value.message == PRODUCT_UNAVAILABLE_MESSAGE
    assert exc_info.value.status_code == 422


async def test_skips_product_lookup_without_product_id() -> None:
    products = FakeProductRepository(active_ids={1})
    use_case = CreateLead(leads=FakeLeadRepository(), products=products, window=WINDOW)

    await use_case(make_lead())

    assert products.calls == []
