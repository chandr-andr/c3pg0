
from m3p0.commands.base import BaseCommandResult, Command, SuccessCommandResult
from m3p0.queries import IS_VERSION_ALREADY_EXIST
from m3p0.utils import database_revision_history, migrations_revision_history


class ApplyCommand(Command):
    """Command to apply new migrations."""

    def __init__(
        self,
        version: str | None,
        force_no_version: bool
    ) -> None:
        if not version and not force_no_version:
            print(
                "version parameter must be specified, "
                "or set force_no_version",
            )
        self.version = version
        self.force_no_version = force_no_version

    async def execute_cmd(self) -> BaseCommandResult:
        to_run_migrations = [
            migration for migration
            in migrations_revision_history()
            if migration not in await database_revision_history(self.driver)
        ]

        if not to_run_migrations:
            return SuccessCommandResult(
                "There is no migrations to apply! Have fun!",
            )
        
        print(to_run_migrations)

        return SuccessCommandResult(
            "123",
        )
    
    async def is_version_exists(self) -> bool:
        return await self.driver.exists(
            querystring=IS_VERSION_ALREADY_EXIST,
            parameters=[self.version],
        )
