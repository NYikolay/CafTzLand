from dataclasses import dataclass
from datetime import timedelta

from app.application.ports.lead_repository import LeadRepository
from app.application.ports.product_repository import ProductRepository
from app.domain.exceptions import ValidationError
from app.domain.leads import Lead

PRODUCT_UNAVAILABLE_MESSAGE = (
    "Выбранный кофе больше недоступен — выберите другой или оставьте поле пустым"
)


@dataclass(frozen=True, slots=True)
class CreateLeadResult:
    lead: Lead
    duplicate: bool


class CreateLead:
    def __init__(
        self,
        leads: LeadRepository,
        products: ProductRepository,
        window: timedelta,
    ) -> None:
        self._leads = leads
        self._products = products
        self._window = window

    async def __call__(self, lead: Lead) -> CreateLeadResult:
        if lead.product_id is not None:
            product = await self._products.get_active(lead.product_id)
            if product is None:
                raise ValidationError(PRODUCT_UNAVAILABLE_MESSAGE)
        stored, duplicate = await self._leads.add_if_not_recent(lead, self._window)
        return CreateLeadResult(lead=stored, duplicate=duplicate)
