from app.domain.leads import Interest, Lead, LeadSource


def test_interest_values() -> None:
    assert [interest.value for interest in Interest] == ["subscription", "one_time", "question"]


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
