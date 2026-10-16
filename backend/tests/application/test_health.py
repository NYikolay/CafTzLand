from application import CheckReadiness


class StubProbe:
    def __init__(self, *, healthy: bool) -> None:
        self._healthy = healthy

    async def ping(self) -> bool:
        return self._healthy


async def test_ready_when_probe_healthy() -> None:
    result = await CheckReadiness(StubProbe(healthy=True))()
    assert result.healthy is True
    assert result.database is True


async def test_not_ready_when_probe_down() -> None:
    result = await CheckReadiness(StubProbe(healthy=False))()
    assert result.healthy is False
    assert result.database is False
