from typing import cast

import pytest
from aiogram import Bot
from aiogram.enums import ParseMode
from aiogram.exceptions import (
    TelegramBadRequest,
    TelegramForbiddenError,
    TelegramNetworkError,
    TelegramNotFound,
)
from aiogram.methods import SendMessage

from domain import TelegramBlockedError, TelegramDeliveryError
from infrastructure.telegram.notifier import AiogramTelegramNotifier, create_telegram_bot

METHOD = SendMessage(chat_id=1, text="test")


class FakeBot:
    def __init__(self, error: Exception | None = None) -> None:
        self._error = error
        self.messages: list[tuple[int, str]] = []

    async def send_message(self, chat_id: int, text: str) -> None:
        if self._error is not None:
            raise self._error
        self.messages.append((chat_id, text))


def make_notifier(bot: FakeBot) -> AiogramTelegramNotifier:
    return AiogramTelegramNotifier(cast(Bot, bot))


async def test_sends_message_through_bot() -> None:
    bot = FakeBot()

    await make_notifier(bot).send_message(123, "текст")

    assert bot.messages == [(123, "текст")]


async def test_forbidden_error_becomes_blocked() -> None:
    bot = FakeBot(TelegramForbiddenError(METHOD, "bot was blocked by the user"))

    with pytest.raises(TelegramBlockedError):
        await make_notifier(bot).send_message(123, "текст")


async def test_not_found_error_becomes_blocked() -> None:
    bot = FakeBot(TelegramNotFound(METHOD, "chat not found"))

    with pytest.raises(TelegramBlockedError):
        await make_notifier(bot).send_message(123, "текст")


async def test_bad_request_becomes_delivery_error() -> None:
    bot = FakeBot(TelegramBadRequest(METHOD, "chat_id is empty"))

    with pytest.raises(TelegramDeliveryError):
        await make_notifier(bot).send_message(123, "текст")


async def test_network_error_becomes_delivery_error() -> None:
    bot = FakeBot(TelegramNetworkError(METHOD, "connection failed"))

    with pytest.raises(TelegramDeliveryError):
        await make_notifier(bot).send_message(123, "текст")


def test_bot_is_not_created_without_token() -> None:
    assert create_telegram_bot(None) is None


async def test_bot_created_with_html_parse_mode() -> None:
    bot = create_telegram_bot("123456:TEST-TOKEN")

    assert bot is not None
    assert bot.default.parse_mode == ParseMode.HTML
    await bot.session.close()
