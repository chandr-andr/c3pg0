from m3p0.checks import check_migration_history
from m3p0.commands.base import BaseCommandResult, Command, FailCommandResult, SuccessCommandResult


class CheckCommand(Command):
    """Command creates new migrations."""

    async def execute_cmd(self) -> BaseCommandResult:
        result, message = await check_migration_history(
            driver=self.driver,
        )

        return SuccessCommandResult(
            message=message
        ) if result else FailCommandResult(
            message=message,
        )
