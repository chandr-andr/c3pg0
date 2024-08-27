from argparse import ArgumentDefaultsHelpFormatter, ArgumentParser
from dataclasses import dataclass
from typing import Optional, Sequence, Type, Union
from typing_extensions import Annotated

import typer

from c3pg0.app_config import ApplicationConfig


app = typer.Typer()


@app.command()
def init() -> None:
    """Initialize the migration tool.
    
    It must be done once at the start.
    """


@app.command()
def apply(
    version: Annotated[
        str,
        typer.Option(help="New version for the migration."),
    ],
) -> None:
    """Apply new migration."""


@app.command()
def rollback(
    version: Annotated[
        str,
        typer.Option(help="Version for rollback."),
    ],
) -> None:
    """Rollback database to specified version."""


@app.command()
def create(
    name: Annotated[
        str,
        typer.Argument(help="Name for the revision."),
    ],
    apply_in_transaction: Annotated[
        Optional[bool],
        typer.Option(help="Execute in transaction or not."),
    ] = True,
    rollback_in_transaction: Annotated[
        Optional[bool],
        typer.Option(help="Execute in transaction or not."),
    ] = True,
    is_python: Annotated[
        Optional[bool],
        typer.Option(help="Is it .py file of not?"),
    ] = False,
) -> None:
    """Create new migration."""
        

if __name__ == "__main__":
    app()
