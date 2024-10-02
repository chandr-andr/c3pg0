import asyncio
from contextlib import contextmanager
from dataclasses import dataclass
from importlib import import_module
import inspect
import json
import os
from pathlib import Path
import sys
import types
from typing import Any, Generator

from m3p0.driver import M3P0Driver, PSQLPyM3P0Driver
from m3p0.app_config import application_config
from m3p0.queries import RETRIEVE_SORTED_REVISIONS


@dataclass
class MigrationSpec:
    revision: str
    back_revision: str | None
    apply_in_transaction: bool
    rollback_in_transaction: bool


@contextmanager
def add_cwd_in_path() -> Generator[None, None, None]:
    """
    Adds current directory in python path.

    This context manager adds current directory in sys.path,
    so all python files are discoverable now, without installing
    current project.

    :yield: none
    """
    cwd = Path.cwd()
    if str(cwd) in sys.path:
        yield
    else:
        # logger.debug(f"Inserting {cwd} in sys.path")
        sys.path.insert(0, str(cwd))
        try:
            yield
        finally:
            try:
                sys.path.remove(str(cwd))
            except ValueError:
                # logger.warning(f"Cannot remove '{cwd}' from sys.path")
                pass


def import_object(object_spec: str) -> Any:
    """
    It parses python object spec and imports it.

    :param object_spec: string in format like `package.module:variable`
    :raises ValueError: if spec has unknown format.
    :returns: imported broker.
    """
    import_spec = object_spec.split(":")

    if len(import_spec) != 2:
        raise ValueError("You should provide object path in `module:variable` format.")

    with add_cwd_in_path():
        module = import_module(import_spec[0])

    return getattr(module, import_spec[1])


def retrieve_driver() -> M3P0Driver:
    """Retrieve driver.

    If config file has driver path, try to import it and initialize.
    It could be func, async func or subclass of `M3P0Driver`.

    ### Returns:
    subclass of `M3P0Driver`.
    """
    if not application_config.driver:
        return PSQLPyM3P0Driver()

    driver_or_builder = import_object(application_config.driver)

    if inspect.iscoroutinefunction(driver_or_builder):
        return _retrieve_driver(asyncio.run(driver_or_builder()))
    elif isinstance(driver_or_builder, types.FunctionType):
        return _retrieve_driver(driver_or_builder())
    else:
        return _retrieve_driver(driver_or_builder)


def _retrieve_driver(possible_driver: Any) -> M3P0Driver:
    """Check that driver has a correct type."""
    if isinstance(possible_driver, M3P0Driver):
        return possible_driver
    
    raise ValueError("NOT")


def migrations_revision_history() -> list[str]:
    """Retrieve migration history by revisions locally.
    
    ### Returns:
    list of sorted revisions.
    """
    migrations_data: dict[str | None, MigrationSpec] = {}

    all_migrations = [
        migration[0] for migration 
        in os.walk(application_config.migration_path)
    ][1:]
    
    while all_migrations:
        migration = all_migrations.pop()
        with open(f"{migration}/specification.json") as migration_spec_json:
            migration_spec = MigrationSpec(**json.load(migration_spec_json))

            migrations_data[migration_spec.back_revision] = migration_spec

    # sort
    sorted_migrations_revisions: list[str] = []

    revision_back_revision = None
    while len(sorted_migrations_revisions) != len(migrations_data):
        migration_spec = migrations_data[revision_back_revision]
        sorted_migrations_revisions.append(migration_spec.revision)

        revision_back_revision = migration_spec.revision

    return sorted_migrations_revisions


async def database_revision_history(
    driver: M3P0Driver,
) -> list[str]:
    """Retrieve migration history by revisions with database."""
    result = await driver.fetch(
        querystring=RETRIEVE_SORTED_REVISIONS,
    )

    return (
        [db_record["revision"] for db_record in result]
        if result
        else []
    )