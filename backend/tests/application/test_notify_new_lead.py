from application.telegram.notify_new_lead import NotifyLeadResult, NotifyNewLead
from domain import (
    Interest,
    Lead,
    Product,
    ProductKind,
    TelegramBlockedError,
    TelegramDeliveryError,
    TelegramSubscriber,
)

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


class FakeSubscriberRepository:
    def __init__(
        self,
        subscribers: list[TelegramSubscriber],
        deactivate_raises: Exception | None = None,
    ) -> None:
        self._subscribers = subscribers
        self._deactivate_raises = deactivate_raises
        self.deactivated: list[int] = []

    async def list_active(self) -> list[TelegramSubscriber]:
        return list(self._subscribers)

    async def deactivate(self, subscriber_id: int) -> None:
        if self._deactivate_raises is not None:
            raise self._deactivate_raises
        self.deactivated.append(subscriber_id)


class FakeNotifier:
    def __init__(self, errors: dict[int, Exception] | None = None) -> None:
        self._errors = errors or {}
        self.sent: list[tuple[int, str]] = []

    async def send_message(self, chat_id: int, text: str) -> None:
        error = self._errors.get(chat_id)
        if error is not None:
            raise error
        self.sent.append((chat_id, text))


class FakeProductRepository:
    def __init__(self, product: Product | None = None) -> None:
        self._product = product
        self.calls: list[int] = []

    async def get(self, product_id: int) -> Product | None:
        self.calls.append(product_id)
        return self._product

    async def get_active(self, product_id: int) -> Product | None:
        return self._product

    async def list_active(self) -> list[Product]:
        return []


def make_lead(product_id: int | None = None) -> Lead:
    return Lead(
        name="Иван",
        phone_number="+375291234567",
        interest=Interest.SUBSCRIPTION,
        product_id=product_id,
        id=42,
    )


def make_subscriber(subscriber_id: int, chat_id: int) -> TelegramSubscriber:
    return TelegramSubscriber(
        id=subscriber_id,
        telegram_user_id=chat_id,
        tg_link=f"https://t.me/user{subscriber_id}",
    )


def make_use_case(
    subscribers: list[TelegramSubscriber],
    *,
    notifier: FakeNotifier | None = None,
    products: FakeProductRepository | None = None,
    deactivate_raises: Exception | None = None,
) -> tuple[NotifyNewLead, FakeSubscriberRepository, FakeNotifier]:
    repository = FakeSubscriberRepository(subscribers, deactivate_raises=deactivate_raises)
    fake_notifier = notifier if notifier is not None else FakeNotifier()
    use_case = NotifyNewLead(
        subscribers=repository,
        products=products if products is not None else FakeProductRepository(),
        notifier=fake_notifier,
        pause_seconds=0,
    )
    return use_case, repository, fake_notifier


async def test_sends_to_all_active_subscribers() -> None:
    use_case, _, notifier = make_use_case([make_subscriber(1, 111), make_subscriber(2, 222)])

    result = await use_case(make_lead())

    assert result == NotifyLeadResult(total=2, sent=2, failed=0, deactivated=0)
    assert [chat_id for chat_id, _ in notifier.sent] == [111, 222]
    assert "🎯 Подписка" in notifier.sent[0][1]
    assert "заявка #42" in notifier.sent[0][1]


async def test_skips_everything_without_subscribers() -> None:
    products = FakeProductRepository()
    use_case, _, notifier = make_use_case([], products=products)

    result = await use_case(make_lead(product_id=3))

    assert result == NotifyLeadResult(total=0, sent=0, failed=0, deactivated=0)
    assert products.calls == []
    assert notifier.sent == []


async def test_includes_product_name() -> None:
    products = FakeProductRepository(PRODUCT)
    use_case, _, notifier = make_use_case([make_subscriber(1, 111)], products=products)

    await use_case(make_lead(product_id=3))

    assert products.calls == [3]
    assert "📦 Эфиопия Иргачеффе" in notifier.sent[0][1]


async def test_deactivates_blocked_subscriber() -> None:
    use_case, repository, notifier = make_use_case(
        [make_subscriber(1, 111), make_subscriber(2, 222)],
        notifier=FakeNotifier(errors={111: TelegramBlockedError()}),
    )

    result = await use_case(make_lead())

    assert result.deactivated == 1
    assert result.failed == 0
    assert result.sent == 1
    assert repository.deactivated == [1]
    assert [chat_id for chat_id, _ in notifier.sent] == [222]


async def test_counts_delivery_errors() -> None:
    use_case, repository, notifier = make_use_case(
        [make_subscriber(1, 111), make_subscriber(2, 222)],
        notifier=FakeNotifier(errors={111: TelegramDeliveryError("timeout")}),
    )

    result = await use_case(make_lead())

    assert result.failed == 1
    assert result.sent == 1
    assert result.deactivated == 0
    assert repository.deactivated == []
    assert [chat_id for chat_id, _ in notifier.sent] == [222]


async def test_unexpected_notifier_error_does_not_abort_broadcast() -> None:
    use_case, repository, notifier = make_use_case(
        [make_subscriber(1, 111), make_subscriber(2, 222)],
        notifier=FakeNotifier(errors={111: RuntimeError("boom")}),
    )

    result = await use_case(make_lead())

    assert result == NotifyLeadResult(total=2, sent=1, failed=1, deactivated=0)
    assert repository.deactivated == []
    assert [chat_id for chat_id, _ in notifier.sent] == [222]


async def test_failed_deactivation_does_not_abort_broadcast() -> None:
    use_case, _, notifier = make_use_case(
        [make_subscriber(1, 111), make_subscriber(2, 222)],
        notifier=FakeNotifier(errors={111: TelegramBlockedError()}),
        deactivate_raises=RuntimeError("db down"),
    )

    result = await use_case(make_lead())

    assert result == NotifyLeadResult(total=2, sent=1, failed=0, deactivated=1)
    assert [chat_id for chat_id, _ in notifier.sent] == [222]
