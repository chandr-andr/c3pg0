import abc
import enum


class CommandResult(enum.Enum):
    """Enum for command result."""

    SUCCESS = enum.auto()
    FAIL = enum.auto()


class Command(abc.ABC):
    """Protocol for every command available."""

    @abc.abstractmethod
    async def execute_cmd(self) -> CommandResult:
        """Execute command and return result in Enum."""

    