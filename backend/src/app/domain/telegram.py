from dataclasses import dataclass


class TelegramDeliveryError(Exception):
    pass


class TelegramBlockedError(Exception):
    pass


@dataclass(frozen=True, slots=True)
class TelegramSubscriber:
    telegram_user_id: int
    tg_link: str
    is_active: bool = True
    id: int | None = None
