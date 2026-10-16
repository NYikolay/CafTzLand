from datetime import UTC, datetime
from typing import Any

from application.telegram.messages import render_lead_notification
from domain import Interest, Lead, LeadSource, Product, ProductKind

SENT_AT = datetime(2026, 10, 15, 20, 59, tzinfo=UTC)

PRODUCT = Product(
    id=3,
    code="ET",
    name="Эфиопия Иргачеффе",
    kind=ProductKind.BEANS,
    tasting_notes=None,
    description=None,
    brew_method=None,
    variants=[],
)


def make_lead(**overrides: object) -> Lead:
    values: dict[str, Any] = {
        "id": 42,
        "name": "Иван",
        "phone_number": "+375291234567",
        "interest": Interest.SUBSCRIPTION,
        "product_id": None,
        "comment": None,
        "source": None,
    }
    values.update(overrides)
    return Lead(**values)


def test_renders_full_card() -> None:
    lead = make_lead(comment="Хочу на четверг", source=LeadSource(utm_source="yandex"))

    text = render_lead_notification(lead, PRODUCT, SENT_AT)

    assert text == (
        "☕️ <b>Новая заявка · VitaiWorld</b>\n"
        "\n"
        "👤 <b>Иван</b>\n"
        "📞 +375291234567\n"
        "🎯 Подписка\n"
        "📦 Эфиопия Иргачеффе\n"
        "💬 Хочу на четверг\n"
        "🌐 yandex\n"
        "\n"
        "🕒 15.10.2026 23:59 (Минск) · заявка #42"
    )


def test_omits_optional_lines() -> None:
    text = render_lead_notification(make_lead(), None, SENT_AT)

    assert "📦" not in text
    assert "💬" not in text
    assert "🌐" not in text
    assert "🎯 Подписка" in text
    assert "🕒 15.10.2026 23:59 (Минск) · заявка #42" in text


def test_escapes_user_input() -> None:
    lead = make_lead(name="Иван <b>", comment="5 < 6 & 7 > 4")

    text = render_lead_notification(lead, None, SENT_AT)

    assert "👤 <b>Иван &lt;b&gt;</b>" in text
    assert "💬 5 &lt; 6 &amp; 7 &gt; 4" in text
