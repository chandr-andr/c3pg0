import os
from dataclasses import dataclass

import tomllib
from typing import Self


@dataclass
class ApplicationConfig:
    """Main config for the C3PG0 application."""

    # Folder for migrations
    migration_path: str = "./migrations"

    # Supported driver
    driver: str | None = None

    # PostgreSQL URL
    postgres_url: str | None = None
    postgres_url_env: str | None = "C3PG0_PSQL_URL"

    # Other custom settings
    datetime_format: str = "%d-%m-%Y|%H:%M:%S"

    @classmethod
    def construct(cls: type["ApplicationConfig"]) -> "ApplicationConfig":
        """Create new ApplicationConfig from pyproject.toml configuration.

        ### Returns:
        New `ApplicationConfig`.
        """
        path = f"{os.getcwd()}/pyproject.toml"
        with open(path, mode="rb") as pyproject:
            pyconfig = tomllib.load(pyproject)

        c3pg0_config = pyconfig["tool"].get("c3pg0")

        return ApplicationConfig(**c3pg0_config if c3pg0_config else {})


application_config = ApplicationConfig.construct()
