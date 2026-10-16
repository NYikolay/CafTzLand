from domain import TelegramBlockedError, TelegramDeliveryError, TelegramSubscriber


def test_subscriber_defaults() -> None:
    subscriber = TelegramSubscriber(telegram_user_id=123456789, tg_link="https://t.me/manager")

    assert subscriber.is_active is True
    assert subscriber.id is None


def test_delivery_errors_are_independent() -> None:
    assert not issubclass(TelegramBlockedError, TelegramDeliveryError)
    assert not issubclass(TelegramDeliveryError, TelegramBlockedError)
