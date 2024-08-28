from typing import Self

from c3pg0.commands.base import Command, CommandResult


class CreateCommand(Command):
    """Command creates new migrations."""

    def __init__(
        self: Self,
        version: str,
    ) -> None:
        """Initialize the create command."""
        self.version = version

    async def execute_cmd(self: Self) -> CommandResult:
        return CommandResult.SUCCESS
