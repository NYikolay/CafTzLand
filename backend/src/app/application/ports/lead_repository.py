from datetime import timedelta
from typing import Protocol

from app.domain.leads import Lead


class LeadRepository(Protocol):
    async def add_if_not_recent(self, lead: Lead, window: timedelta) -> tuple[Lead, bool]: ...
