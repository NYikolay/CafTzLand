from app.domain.leads import (
    INTEREST_BY_NAME,
    INTEREST_NAMES,
    Interest,
    InterestName,
    Lead,
    LeadSource,
)


def test_interest_values() -> None:
    assert [interest.value for interest in Interest] == ["subscription", "one_time", "question"]


def test_interest_name_values() -> None:
    assert [name.value for name in InterestName] == ["Подписка", "Разовый заказ", "Вопрос"]


def test_interest_names_map_codes_to_russian() -> None:
    assert INTEREST_NAMES == {
        Interest.SUBSCRIPTION: InterestName.SUBSCRIPTION,
        Interest.ONE_TIME: InterestName.ONE_TIME,
        Interest.QUESTION: InterestName.QUESTION,
    }


def test_interest_by_name_is_reverse_map() -> None:
    for interest, name in INTEREST_NAMES.items():
        assert INTEREST_BY_NAME[name] is interest


def test_lead_source_defaults_to_nulls() -> None:
    source = LeadSource()
    assert source.utm_source is None
    assert source.utm_medium is None
    assert source.referrer is None
    assert source.page_url is None
    assert source.extra == {}


def test_lead_defaults() -> None:
    lead = Lead(name="Иван", phone_number="+375291234567", interest=Interest.SUBSCRIPTION)
    assert lead.product_id is None
    assert lead.comment is None
    assert lead.source is None
    assert lead.is_handled is False
    assert lead.id is None
