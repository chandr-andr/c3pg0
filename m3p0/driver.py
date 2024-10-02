import os
from typing import Any, Protocol, Self, runtime_checkable

from psqlpy import ConnectionPool

from m3p0.app_config import application_config


@runtime_checkable
class M3P0Driver(Protocol):
    
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
    
    async def fetch_val(
        self: Self,
        querystring: str,
        parameters: list[Any] | None = None,
    ) -> Any:
        """
        Execute a query and return one value.

        Querystring must return exactly one value,
        otherwise exception will be raised.
        """
    
    async def execute(
        self: Self,
        querystring: str,
        parameters: list[Any] | None = None,
    ) -> None:
        """Execute query.
        
        Don't return anything, just run the query.
        """
    
    async def execute_migration(
        self,
        querystring: str,
        in_transaction: bool = True,
    ) -> None:
        """Execute query from migration file.

        This method must be able to execute many queries in one string:
        `SELECT 1; SELECT 2; SELECT 3; ...`.

        ### Parameters:
        - `querystring`: migration query to execute.
        - `in_transaction`: flag execute migration in transaction or not.
        """


class PSQLPyM3P0Driver:
    """M3P0 driver based on `PSQLPy`."""

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
                prepared=False,
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
                prepared=False,
            )
        
        result = response.result()
        return result if result else None

    async def fetch_val(
        self: Self,
        querystring: str,
        parameters: list[Any] | None = None,
    ) -> Any:
        """
        Execute a query and return one value.

        Querystring must return exactly one value,
        otherwise exception will be raised.
        """
        async with self.conn_pool.acquire() as conn:
            return await conn.fetch_val(
                querystring=querystring,
                parameters=parameters,
                prepared=False,
            )

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
                prepared=False,
            )

    async def execute_migration(
        self,
        querystring: str,
        in_transaction: bool = True,
    ) -> None:
        """Execute query from migration file.

        ### Parameters:
        - `querystring`: migration query to execute.
        - `in_transaction`: flag execute migration in transaction or not.
        """
        async with self.conn_pool.acquire() as conn:
            if in_transaction:
                async with conn.transaction() as transaction:
                    await transaction.execute_batch(
                        querystring=querystring,
                    )
            else:
                await conn.execute_many(querystring=querystring)
