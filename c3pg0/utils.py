import asyncio
from contextlib import contextmanager
from importlib import import_module
import inspect
from pathlib import Path
import sys
import types
from typing import Any, Generator

from c3pg0.driver import C3PG0Driver, PSQLPyC3PG0Driver
from c3pg0.app_config import application_config


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


def retrieve_driver() -> C3PG0Driver:
    """Retrieve driver.

    If config file has driver path, try to import it and initialize.
    It could be func, async func or subclass of `C3PG0Driver`.

    ### Returns:
    subclass of `C3PG0Driver`.
    """
    if not application_config.driver:
        return PSQLPyC3PG0Driver()

    driver_or_builder = import_object(application_config.driver)

    if inspect.iscoroutinefunction(driver_or_builder):
        return _retrieve_driver(asyncio.run(driver_or_builder()))
    elif isinstance(driver_or_builder, types.FunctionType):
        return _retrieve_driver(driver_or_builder())
    else:
        return _retrieve_driver(driver_or_builder)


def _retrieve_driver(possible_driver: Any) -> C3PG0Driver:
    """Check that driver has a correct type."""
    if isinstance(possible_driver, C3PG0Driver):
        return possible_driver
    
    raise ValueError("NOT")
