from dataclasses import dataclass, field
from enum import StrEnum


class Interest(StrEnum):
    SUBSCRIPTION = "subscription"
    ONE_TIME = "one_time"
    QUESTION = "question"


class InterestName(StrEnum):
    SUBSCRIPTION = "Подписка"
    ONE_TIME = "Разовый заказ"
    QUESTION = "Вопрос"


INTEREST_NAMES: dict[Interest, InterestName] = {
    Interest.SUBSCRIPTION: InterestName.SUBSCRIPTION,
    Interest.ONE_TIME: InterestName.ONE_TIME,
    Interest.QUESTION: InterestName.QUESTION,
}

INTEREST_BY_NAME: dict[InterestName, Interest] = {
    name: interest for interest, name in INTEREST_NAMES.items()
}


@dataclass(frozen=True, slots=True)
class LeadSource:
    utm_source: str | None = None
    utm_medium: str | None = None
    utm_campaign: str | None = None
    utm_content: str | None = None
    utm_term: str | None = None
    referrer: str | None = None
    page_url: str | None = None
    extra: dict[str, str] = field(default_factory=dict)


@dataclass(frozen=True, slots=True)
class Lead:
    name: str
    phone_number: str
    interest: Interest
    product_id: int | None = None
    comment: str | None = None
    source: LeadSource | None = None
    is_handled: bool = False
    id: int | None = None
