import os
from typing import Any, Protocol, Self, runtime_checkable

from psqlpy import ConnectionPool

from c3pg0.app_config import application_config


@runtime_checkable
class C3PG0Driver(Protocol):
    
    async def exists(
        self: Self,
        querystring: str,
        parameters: list[Any] | None = None,
    ) -> bool:
        """Check is version exists or not."""
    
    async def fetch(
        self: Self,
        querystring: str,
        parameters: list[Any] | None = None,
    ) -> list[dict[str, Any]] | None:
        """Execute query and fetch data from response."""
    
    async def execute(
        self: Self,
        querystring: str,
        parameters: list[Any] | None = None,
    ) -> None:
        """Execute query.
        
        Don't return anything, just run the query.
        """


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

    async def exists(self: Self, querystring: str, parameters: list[Any] | None = None) -> bool:
        """Check is version exists or not."""
        async with self.conn_pool.acquire() as conn:
            return await conn.fetch_val(
                querystring=querystring,
                parameters=parameters,
            )

    async def fetch(
        self: Self,
        querystring: str,
        parameters: list[Any] | None = None,
    ) -> list[dict[str, Any]] | None:
        """Execute query and fetch data from response."""
        async with self.conn_pool.acquire() as conn:
            response = await conn.fetch(
                querystring=querystring,
                parameters=parameters,
            )
        
        result = response.result()
        return result if result else None

    async def execute(
        self: Self,
        querystring: str,
        parameters: list[Any] | None = None,
    ) -> None:
        """Execute query.
        
        Don't return anything, just run the query.
        """
        async with self.conn_pool.acquire() as conn:
            await conn.execute(
                querystring=querystring,
                parameters=parameters,
            )

