from app.infrastructure.db.models.telegram_subscriber import (
    TelegramSubscriber as TelegramSubscriberRow,
)
from app.infrastructure.db.repositories.telegram_subscriber_repository import to_domain


def make_row(**overrides: object) -> TelegramSubscriberRow:
    values: dict[str, object] = {
        "id": 1,
        "telegram_user_id": 123456789,
        "tg_link": "https://t.me/manager",
        "is_active": True,
    }
    values.update(overrides)
    return TelegramSubscriberRow(**values)


def test_maps_row_to_domain() -> None:
    subscriber = to_domain(make_row())

    assert subscriber.id == 1
    assert subscriber.telegram_user_id == 123456789
    assert subscriber.tg_link == "https://t.me/manager"
    assert subscriber.is_active is True


def test_maps_inactive_subscriber() -> None:
    subscriber = to_domain(make_row(is_active=False))

    assert subscriber.is_active is False
