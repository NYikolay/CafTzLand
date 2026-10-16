from dataclasses import replace
from typing import Any

from fastapi import FastAPI
from httpx import AsyncClient

from application.leads import PRODUCT_UNAVAILABLE_MESSAGE, CreateLeadResult
from application.telegram.notify_new_lead import NotifyLeadResult
from domain import Interest, Lead, LeadSource
from domain.exceptions import ValidationError
from presentation import get_create_lead, get_notify_new_lead

VALID_PAYLOAD: dict[str, Any] = {
    "name": "Иван",
    "phone_number": "+375 (29) 123-45-67",
    "interest": "subscription",
    "product_id": 3,
    "comment": "Хочу на четверг",
    "source": {
        "utm_source": "yandex",
        "utm_medium": "cpc",
        "utm_content": "ad_32",
        "page_url": "https://kvarta.by/",
        "gclid": "CjcK",
    },
}


class FakeCreateLead:
    def __init__(self, *, duplicate: bool = False, error: ValidationError | None = None) -> None:
        self._duplicate = duplicate
        self._error = error
        self.calls: list[Lead] = []

    async def __call__(self, lead: Lead) -> CreateLeadResult:
        self.calls.append(lead)
        if self._error is not None:
            raise self._error
        return CreateLeadResult(lead=replace(lead, id=42), duplicate=self._duplicate)


class FakeNotifyNewLead:
    def __init__(self) -> None:
        self.calls: list[Lead] = []

    async def __call__(self, lead: Lead) -> NotifyLeadResult:
        self.calls.append(lead)
        return NotifyLeadResult(total=0, sent=0, failed=0, deactivated=0)


def override(app: FastAPI, use_case: FakeCreateLead) -> None:
    app.dependency_overrides[get_create_lead] = lambda: use_case


async def test_creates_lead(app: FastAPI, client: AsyncClient) -> None:
    use_case = FakeCreateLead()
    override(app, use_case)

    response = await client.post("/api/v1/lead", json=VALID_PAYLOAD)

    assert response.status_code == 201
    assert response.json() == {"id": 42, "duplicate": False}
    lead = use_case.calls[0]
    assert lead.name == "Иван"
    assert lead.phone_number == "+375291234567"
    assert lead.interest is Interest.SUBSCRIPTION
    assert lead.product_id == 3
    assert lead.comment == "Хочу на четверг"
    assert lead.source == LeadSource(
        utm_source="yandex",
        utm_medium="cpc",
        utm_content="ad_32",
        page_url="https://kvarta.by/",
        extra={"gclid": "CjcK"},
    )


async def test_duplicate_returns_200(app: FastAPI, client: AsyncClient) -> None:
    override(app, FakeCreateLead(duplicate=True))

    response = await client.post("/api/v1/lead", json=VALID_PAYLOAD)

    assert response.status_code == 200
    assert response.json() == {"id": 42, "duplicate": True}


async def test_invalid_phone_shows_russian_hint(app: FastAPI, client: AsyncClient) -> None:
    override(app, FakeCreateLead())
    payload = {**VALID_PAYLOAD, "phone_number": "залупа"}

    response = await client.post("/api/v1/lead", json=payload)

    assert response.status_code == 422
    error = response.json()["error"]
    assert error["code"] == "validation_error"
    detail = error["details"][0]
    assert detail["loc"] == ["body", "phone_number"]
    assert detail["msg"] == "Пожалуйста, введите корректный номер телефона"
    assert detail["type"] == "phone_invalid"


async def test_missing_name_rejected(app: FastAPI, client: AsyncClient) -> None:
    override(app, FakeCreateLead())
    payload = {key: value for key, value in VALID_PAYLOAD.items() if key != "name"}

    response = await client.post("/api/v1/lead", json=payload)

    assert response.status_code == 422


async def test_source_with_non_string_value_rejected(app: FastAPI, client: AsyncClient) -> None:
    override(app, FakeCreateLead())
    payload = {**VALID_PAYLOAD, "source": {"utm_source": 5}}

    response = await client.post("/api/v1/lead", json=payload)

    assert response.status_code == 422
    assert response.json()["error"]["details"][0]["msg"] == "Некорректный параметр источника"


async def test_source_empty_values_are_dropped(app: FastAPI, client: AsyncClient) -> None:
    use_case = FakeCreateLead()
    override(app, use_case)
    payload = {**VALID_PAYLOAD, "source": {"utm_source": "  ", "utm_medium": "cpc"}}

    response = await client.post("/api/v1/lead", json=payload)

    assert response.status_code == 201
    assert use_case.calls[0].source == LeadSource(utm_medium="cpc")


async def test_source_value_truncated_to_column_width(app: FastAPI, client: AsyncClient) -> None:
    use_case = FakeCreateLead()
    override(app, use_case)
    payload = {**VALID_PAYLOAD, "source": {"utm_source": "x" * 300}}

    response = await client.post("/api/v1/lead", json=payload)

    assert response.status_code == 201
    source = use_case.calls[0].source
    assert source is not None
    assert source.utm_source == "x" * 255


async def test_extra_source_value_keeps_default_limit(app: FastAPI, client: AsyncClient) -> None:
    use_case = FakeCreateLead()
    override(app, use_case)
    payload = {**VALID_PAYLOAD, "source": {"gclid": "y" * 1100}}

    response = await client.post("/api/v1/lead", json=payload)

    assert response.status_code == 201
    source = use_case.calls[0].source
    assert source is not None
    assert source.extra["gclid"] == "y" * 1024


async def test_source_with_non_dict_value_rejected(app: FastAPI, client: AsyncClient) -> None:
    override(app, FakeCreateLead())
    payload = {**VALID_PAYLOAD, "source": 5}

    response = await client.post("/api/v1/lead", json=payload)

    assert response.status_code == 422
    assert response.json()["error"]["details"][0]["msg"] == "Некорректный параметр источника"


async def test_unavailable_product_returns_validation_error(
    app: FastAPI, client: AsyncClient
) -> None:
    override(app, FakeCreateLead(error=ValidationError(PRODUCT_UNAVAILABLE_MESSAGE)))

    response = await client.post("/api/v1/lead", json=VALID_PAYLOAD)

    assert response.status_code == 422
    error = response.json()["error"]
    assert error["code"] == "validation_error"
    assert error["message"] == PRODUCT_UNAVAILABLE_MESSAGE


async def test_new_lead_schedules_notification(app: FastAPI, client: AsyncClient) -> None:
    override(app, FakeCreateLead())
    notify = FakeNotifyNewLead()
    app.dependency_overrides[get_notify_new_lead] = lambda: notify

    response = await client.post("/api/v1/lead", json=VALID_PAYLOAD)

    assert response.status_code == 201
    assert [lead.id for lead in notify.calls] == [42]


async def test_duplicate_lead_does_not_notify(app: FastAPI, client: AsyncClient) -> None:
    override(app, FakeCreateLead(duplicate=True))
    notify = FakeNotifyNewLead()
    app.dependency_overrides[get_notify_new_lead] = lambda: notify

    response = await client.post("/api/v1/lead", json=VALID_PAYLOAD)

    assert response.status_code == 200
    assert notify.calls == []
