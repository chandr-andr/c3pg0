
from m3p0.commands.base import BaseCommandResult, Command, SuccessCommandResult
from m3p0.queries import IS_VERSION_ALREADY_EXIST


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
        return SuccessCommandResult(
            "123",
        )
    
    async def is_version_exists(self) -> bool:
        return await self.driver.exists(
            querystring=IS_VERSION_ALREADY_EXIST,
            parameters=[self.version],
        )
