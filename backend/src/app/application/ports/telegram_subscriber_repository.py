from typing import Protocol

from app.domain.telegram import TelegramSubscriber


class TelegramSubscriberRepository(Protocol):
    async def list_active(self) -> list[TelegramSubscriber]: ...

    async def deactivate(self, subscriber_id: int) -> None: ...
