import asyncio
import logging
from dataclasses import dataclass
from datetime import UTC, datetime

from app.application.ports.product_repository import ProductRepository
from app.application.ports.telegram_notifier import TelegramNotifier
from app.application.ports.telegram_subscriber_repository import TelegramSubscriberRepository
from app.application.telegram.messages import render_lead_notification
from app.domain.leads import Lead
from app.domain.products import Product
from app.domain.telegram import TelegramBlockedError, TelegramDeliveryError

logger = logging.getLogger(__name__)

SEND_PAUSE_SECONDS = 0.05


@dataclass(frozen=True, slots=True)
class NotifyLeadResult:
    total: int
    sent: int
    failed: int
    deactivated: int


class NotifyNewLead:
    def __init__(
        self,
        subscribers: TelegramSubscriberRepository,
        products: ProductRepository,
        notifier: TelegramNotifier,
        pause_seconds: float = SEND_PAUSE_SECONDS,
    ) -> None:
        self._subscribers = subscribers
        self._products = products
        self._notifier = notifier
        self._pause_seconds = pause_seconds

    async def __call__(self, lead: Lead) -> NotifyLeadResult:
        subscribers = await self._subscribers.list_active()
        if not subscribers:
            logger.info("Lead %s: no active telegram subscribers", lead.id)
            return NotifyLeadResult(total=0, sent=0, failed=0, deactivated=0)
        product: Product | None = None
        if lead.product_id is not None:
            product = await self._products.get(lead.product_id)
        text = render_lead_notification(lead, product, datetime.now(UTC))
        sent = 0
        failed = 0
        deactivated = 0
        for subscriber in subscribers:
            try:
                await self._notifier.send_message(subscriber.telegram_user_id, text)
            except TelegramBlockedError:
                deactivated += 1
                if subscriber.id is not None:
                    try:
                        await self._subscribers.deactivate(subscriber.id)
                    except Exception:
                        logger.exception(
                            "Failed to deactivate telegram subscriber %s",
                            subscriber.telegram_user_id,
                        )
                logger.info("Telegram subscriber %s blocked the bot", subscriber.telegram_user_id)
            except TelegramDeliveryError as exc:
                failed += 1
                logger.warning(
                    "Telegram delivery to %s failed: %s", subscriber.telegram_user_id, exc
                )
            except Exception:
                failed += 1
                logger.exception(
                    "Telegram delivery to %s failed unexpectedly", subscriber.telegram_user_id
                )
            else:
                sent += 1
            await asyncio.sleep(self._pause_seconds)
        logger.info(
            "Lead %s telegram notify: total=%d sent=%d failed=%d deactivated=%d",
            lead.id,
            len(subscribers),
            sent,
            failed,
            deactivated,
        )
        return NotifyLeadResult(
            total=len(subscribers),
            sent=sent,
            failed=failed,
            deactivated=deactivated,
        )
