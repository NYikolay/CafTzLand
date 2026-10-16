from infrastructure.config.settings import Settings
from infrastructure.db import AsyncDatabaseProbe, create_db_engine, create_sessionmaker
from infrastructure.db.base import Base


class ExplodingConnect:
    async def __aenter__(self) -> None:
        raise OSError("connection refused")

    async def __aexit__(self, *args: object) -> bool:
        return False


class ExplodingEngine:
    def connect(self) -> ExplodingConnect:
        return ExplodingConnect()


def test_engine_uses_asyncpg(test_settings: Settings) -> None:
    engine = create_db_engine(test_settings)
    assert engine.url.drivername == "postgresql+asyncpg"


def test_sessionmaker_creates_sessions(test_settings: Settings) -> None:
    sessionmaker = create_sessionmaker(create_db_engine(test_settings))
    session = sessionmaker()
    assert session is not None


def test_naming_convention() -> None:
    convention = Base.metadata.naming_convention
    assert convention["pk"] == "pk_%(table_name)s"
    assert convention["ix"] == "ix_%(column_0_label)s"


async def test_probe_returns_false_on_connection_error() -> None:
    probe = AsyncDatabaseProbe(ExplodingEngine())  # type: ignore[arg-type]
    assert await probe.ping() is False
