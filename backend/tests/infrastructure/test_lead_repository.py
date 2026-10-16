import pytest

from domain import Interest
from infrastructure.db.models.order import Order
from infrastructure.db.repositories import to_domain


def make_order(**overrides: object) -> Order:
    values: dict[str, object] = {
        "id": 7,
        "name": "Иван",
        "interest": "Подписка",
        "phone_number": "+375291234567",
        "product_id": 3,
        "comment": "Хочу на четверг",
        "is_handled": False,
        "utm_source": None,
        "utm_medium": None,
        "utm_campaign": None,
        "utm_content": None,
        "utm_term": None,
        "referrer": None,
        "page_url": None,
        "source_extra": None,
    }
    values.update(overrides)
    return Order(**values)


def test_maps_order_to_lead() -> None:
    lead = to_domain(make_order())

    assert lead.id == 7
    assert lead.name == "Иван"
    assert lead.phone_number == "+375291234567"
    assert lead.interest is Interest.SUBSCRIPTION
    assert lead.product_id == 3
    assert lead.comment == "Хочу на четверг"
    assert lead.is_handled is False
    assert lead.source is None


def test_maps_russian_interest_to_code() -> None:
    lead = to_domain(make_order(interest="Разовый заказ"))

    assert lead.interest is Interest.ONE_TIME


def test_maps_question_interest_to_code() -> None:
    lead = to_domain(make_order(interest="Вопрос"))

    assert lead.interest is Interest.QUESTION


def test_rejects_unknown_stored_interest() -> None:
    with pytest.raises(ValueError, match="unknown"):
        to_domain(make_order(interest="unknown"))


def test_maps_full_source() -> None:
    order = make_order(
        utm_source="yandex",
        utm_content="ad_32",
        page_url="https://kvarta.by/",
        source_extra={"gclid": "CjcK"},
    )

    lead = to_domain(order)

    assert lead.source is not None
    assert lead.source.utm_source == "yandex"
    assert lead.source.utm_medium is None
    assert lead.source.utm_content == "ad_32"
    assert lead.source.page_url == "https://kvarta.by/"
    assert lead.source.extra == {"gclid": "CjcK"}


def test_source_with_only_extra_is_kept() -> None:
    lead = to_domain(make_order(source_extra={"gclid": "CjcK"}))

    assert lead.source is not None
    assert lead.source.utm_source is None
    assert lead.source.extra == {"gclid": "CjcK"}
