from dataclasses import dataclass

from app.application.ports.database_probe import DatabaseProbe


@dataclass(frozen=True, slots=True)
class Readiness:
    database: bool

    @property
    def healthy(self) -> bool:
        return self.database


class CheckReadiness:
    def __init__(self, probe: DatabaseProbe) -> None:
        self._probe = probe

    async def __call__(self) -> Readiness:
        return Readiness(database=await self._probe.ping())
