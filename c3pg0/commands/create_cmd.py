from os import mkdir
from pathlib import Path
from typing import Self

from c3pg0.commands.base import BaseCommandResult, Command, SuccessCommandResult, FailCommandResult
from c3pg0.exceptions import CommandError
from c3pg0.queries import IS_VERSION_ALREADY_EXIST
from c3pg0.utils import retrieve_driver
from c3pg0.app_config import application_config


class CreateCommand(Command):
    """Command creates new migrations."""

    def __init__(
        self: Self,
        migration_name: str,
        apply_in_transaction: bool,
        rollback_in_transaction: bool,
    ) -> None:
        """Initialize the create command."""
        # self.version = version
        self.migration_name = migration_name
        self.apply_in_transaction = apply_in_transaction
        self.rollback_in_transaction = rollback_in_transaction
        self.driver = retrieve_driver()

    async def execute_cmd(self: Self) -> BaseCommandResult:
        # is_version_exist = await self.is_version_exist(
        #     version=self.version,
        # )
        # if not is_version_exist:
        #     return FailCommandResult(
        #         f"Version {self.version} is already exist",
        #     )
        
        self.build_new_migration()

        return SuccessCommandResult(
            "New migration successfully created",
        )

    # async def is_version_exist(self: Self, version: str) -> bool:
    #     try:
    #         is_exist = await self.driver.exists(
    #             querystring=IS_VERSION_ALREADY_EXIST,
    #             parameters=[version],
    #         )
    #     except Exception as exc:
    #         raise CommandError("Cannot check version existence") from exc

    #     return is_exist
    
    def build_new_migration(self: Self) -> (BaseCommandResult | None):
        migration_path = self.create_new_migration_folder()
        self.create_migration_file(
            migration_path=migration_path,
            file_name="apply.sql",
        )
        self.create_migration_file(
            migration_path=migration_path,
            file_name="rollback.sql",
        )
        self.create_migration_file(
            migration_path=migration_path,
            file_name="specification.json",
            support_text="",
        )

        return None
    
    def create_new_migration_folder(self) -> str:
        migration_path = f"{application_config.migration_path}/{self.migration_name}"
        try:
            mkdir(path=migration_path)
        except Exception as exc:
            raise CommandError(
                "Cannot create new migration directory",
            ) from exc

        return migration_path

    def create_migration_file(
        self,
        migration_path: str,
        file_name: str,
        support_text: str = "-- File was generated automatically"
    ) -> None:
        try:
            with Path(f"{migration_path}/{file_name}").open("w") as apply_sql:
                apply_sql.write(support_text)
        except Exception as exc:
            raise CommandError(
                "Cannot create new migration file",
            ) from exc

