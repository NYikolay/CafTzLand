from aiogram import Bot
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.exceptions import TelegramAPIError, TelegramForbiddenError, TelegramNotFound

from domain.telegram import TelegramBlockedError, TelegramDeliveryError


def create_telegram_bot(token: str | None) -> Bot | None:
    if token is None:
        return None
    return Bot(token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


class AiogramTelegramNotifier:
    def __init__(self, bot: Bot) -> None:
        self._bot = bot

    async def send_message(self, chat_id: int, text: str) -> None:
        try:
            await self._bot.send_message(chat_id=chat_id, text=text)
        except (TelegramForbiddenError, TelegramNotFound) as exc:
            raise TelegramBlockedError(str(exc)) from exc
        except TelegramAPIError as exc:
            raise TelegramDeliveryError(str(exc)) from exc
