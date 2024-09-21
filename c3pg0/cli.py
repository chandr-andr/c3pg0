import asyncio
from typing import Optional
from typing_extensions import Annotated

import typer

from c3pg0.app_config import ApplicationConfig
from c3pg0.commands.check_cmd import CheckCommand
from c3pg0.commands.create_cmd import CreateCommand
from c3pg0.commands.init_cmd import InitCommand


app = typer.Typer()


@app.command()
def init() -> None:
    """Initialize the migration tool.
    
    It must be done once at the start.
    """
    result = asyncio.run(InitCommand().execute_cmd())
    result.print_info()


@app.command()
def check_history() -> None:
    """
    Check history of the migrations.

    Local history and database history must be the same.
    """
    result = asyncio.run(CheckCommand().execute_cmd())
    result.print_info()


@app.command()
def apply(
    version: Annotated[
        Optional[str],
        typer.Option(help="New version for the migration."),
    ] = None,
    force_no_version: Annotated[
        bool,
        typer.Option(
            help=(
                "Force apply migrations without setting version. "
                "Without this parameter rolling back "
                "to this version is impossible! "
                "In most cases, it must be used only for local development."
            ),
        ),
    ] = False,
) -> None:
    """Apply new migration."""
    if not version and not force_no_version:
        print(
            "version parameter must be specified, "
            "or set force_no_version",
        )


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
        bool,
        typer.Option(
            help="Execute apply migration in a transaction or not.",
        ),
    ] = True,
    rollback_in_transaction: Annotated[
        bool,
        typer.Option(
            help="Execute rollback migration in a transaction or not.",
        ),
    ] = True,
) -> None:
    """Create new migration."""
    result = asyncio.run(
        CreateCommand(
            migration_name=name,
            apply_in_transaction=apply_in_transaction,
            rollback_in_transaction=rollback_in_transaction,
        ).execute_cmd()
    )
        

if __name__ == "__main__":
    app()
