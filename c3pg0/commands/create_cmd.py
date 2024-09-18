import datetime
import json
from os import mkdir
from pathlib import Path
from typing import Self
import uuid

from c3pg0.commands.base import BaseCommandResult, Command, SuccessCommandResult
from c3pg0.consts import MAX_MIGRATION_NAME_LENGTH
from c3pg0.exceptions import CommandError
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
        self.migration_name = migration_name
        self.apply_in_transaction = apply_in_transaction
        self.rollback_in_transaction = rollback_in_transaction
        self.revision = uuid.uuid4().hex

    async def execute_cmd(self: Self) -> BaseCommandResult:
        self.build_new_migration()

        return SuccessCommandResult(
            "New migration successfully created",
        )
    
    def build_new_migration(self: Self) -> None:
        migration_path = self.create_new_migration_folder()
        self.create_migration_file(
            migration_path=migration_path,
            file_name="apply.sql",
        )
        self.create_migration_file(
            migration_path=migration_path,
            file_name="rollback.sql",
        )
        self.create_specification_file(
            specification_path=migration_path,
        )

        return None
    
    def create_new_migration_folder(self) -> str:
        migration_path_name = self.create_migration_folder_name()
        migration_path = (
            f"{application_config.migration_path}"
            f"/{migration_path_name}"
        )
        try:
            mkdir(path=migration_path)
        except Exception as exc:
            raise CommandError(
                "Cannot create new migration directory",
            ) from exc

        return migration_path
    
    def create_migration_folder_name(self) -> str:
        now_time = datetime.datetime.now().strftime(
            application_config.datetime_format,
        )
        migration_name = f"{now_time}_{self.migration_name}"
        return migration_name[:MAX_MIGRATION_NAME_LENGTH]

    def create_migration_file(
        self,
        migration_path: str,
        file_name: str,
        support_text: str | None = "-- File was generated automatically",
    ) -> None:
        try:
            with Path(f"{migration_path}/{file_name}").open("w") as apply_sql:
                if support_text:
                    apply_sql.write(support_text)
        except Exception as exc:
            raise CommandError(
                "Cannot create new migration file",
            ) from exc

    def create_specification_file(
        self,
        specification_path: str,
    ) -> None:
        specification_data = {
            "revision": self.revision,
            "apply_in_transaction": self.apply_in_transaction,
            "rollback_in_transaction": self.rollback_in_transaction,
        }
        try:
            with Path(f"{specification_path}/specification.json").open("w") as apply_sql:
                apply_sql.write(json.dumps(specification_data, indent=2))
        except Exception as exc:
            raise CommandError(
                "Cannot create new migration file",
            ) from exc
