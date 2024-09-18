import abc
import enum
from typing import Self
from colorama import Fore

from c3pg0.utils import retrieve_driver


class BaseCommandResult(abc.ABC):
    """Base command result class."""

    def __init__(self: Self, message: str) -> None:
        self.message = message
    
    @abc.abstractmethod
    def print_info(self: Self) -> None:
        """Print information about command in correct way."""


class SuccessCommandResult(BaseCommandResult):
    """Result for successful command execution."""

    def print_info(self: Self) -> None:
        """Print success information in green color."""
        print(Fore.GREEN + self.message)


class FailCommandResult(BaseCommandResult):
    """Result for successful command execution."""

    def print_info(self: Self) -> None:
        """Print failure information in red color."""
        print(Fore.RED + self.message)


class Command(abc.ABC):
    """Protocol for every command available."""

    driver = retrieve_driver()

    @abc.abstractmethod
    async def execute_cmd(self) -> BaseCommandResult:
        """Execute command and return result in Enum."""
