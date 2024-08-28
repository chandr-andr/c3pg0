import os
from typing import Protocol, Self, runtime_checkable

from psqlpy import ConnectionPool

from c3pg0.app_config import application_config


@runtime_checkable
class C3PG0Driver(Protocol):
    
    async def is_version_exists(self: Self, version: str) -> bool:
        """Check is version exists or not."""


class PSQLPyC3PG0Driver:
    """C3PG0 driver based on `PSQLPy`."""

    def __init__(self: Self) -> None:
        """Initialize new driver instance."""

        if application_config.postgres_url:
            self.conn_pool = ConnectionPool(
                dsn=application_config.postgres_url,
            )
            return
        elif application_config.postgres_url_env:
            postgres_url = os.getenv(application_config.postgres_url_env)
            if postgres_url:
                self.conn_pool = ConnectionPool(
                    dsn=application_config.postgres_url,
                )
                return
        
        raise ValueError(
            "Cannot initialize driver to run migrations. "
            "Please provide minimal necessary configuration.",
        )



    async def is_version_exists(self: Self, version: str) -> bool:
        """Check is version exists or not."""
        async with self.conn_pool.acquire() as conn:
            return await conn.fetch_val(
                querystring="SELECT EXISTS (SELECT 1 FROM c3pg0 WHERE version = $1)",
                parameters=[version],
            )
