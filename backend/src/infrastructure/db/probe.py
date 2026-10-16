import asyncio

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncEngine


class AsyncDatabaseProbe:
    def __init__(self, engine: AsyncEngine, *, timeout: float = 2.0) -> None:
        self._engine = engine
        self._timeout = timeout

    async def ping(self) -> bool:
        try:
            async with asyncio.timeout(self._timeout):
                async with self._engine.connect() as connection:
                    await connection.execute(text("SELECT 1"))
        except Exception:
            return False
        return True
