from typing import Self
from m3p0.commands.base import Command, BaseCommandResult, SuccessCommandResult, FailCommandResult
from m3p0.exceptions import CommandError
from m3p0.queries import CREATE_TABLE_QUERY, IS_TABLE_EXISTS_QUERY
from m3p0.utils import retrieve_driver


class InitCommand(Command):
    """Command to initialize the M3P0 migration system."""

    def __init__(self) -> None:
        self.driver = retrieve_driver()

    async def execute_cmd(self: Self) -> BaseCommandResult:
        is_migration_table_exist = await self.is_already_init()
        if is_migration_table_exist:
            return SuccessCommandResult(
                message="m3p0 is already initialized",
            )

        return await self.create_table()
    
    async def is_already_init(self: Self) -> bool:
        """Check is init was called earlier."""
        is_inited_already = await self.driver.exists(
            querystring=IS_TABLE_EXISTS_QUERY,
        )
        return is_inited_already

    async def create_table(self: Self) -> BaseCommandResult:
        try:
            await self.driver.execute(
                querystring=CREATE_TABLE_QUERY,
            )
        except Exception as exc:
            raise CommandError("Cannot initialize m3p0") from exc

        return SuccessCommandResult(
            message="m3p0 initialized",
        )
