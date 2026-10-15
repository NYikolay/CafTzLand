from dataclasses import dataclass, field
from enum import StrEnum


class Interest(StrEnum):
    SUBSCRIPTION = "subscription"
    ONE_TIME = "one_time"
    QUESTION = "question"


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
