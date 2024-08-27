import os
from dataclasses import dataclass

import tomllib


@dataclass
class ApplicationConfig:
    """Main config for the C3PG0 application."""

    # Folder for migrations
    migration_path: str | None = "./migrations"

    # Supported driver
    driver: str | None = None

    # PostgreSQL URL
    postgres_url: str | None = "postgres://postgres:postgres@localhost:5432/postgres"
    postgres_url_env: str | None = "C3PG0_PSQL_URL"

    # PostgresSQL URL separate envs
    postgres_user: str | None = "postgres"
    postgres_user_env: str | None = "C3PG0_PSQL_USER"

    postgres_password: str | None = "postgres"
    postgres_password_env: str | None = "C3PG0_PSQL_PASSWORD"
    
    postgres_host: str | None = "localhost"
    postgres_host_env: str | None = "C3PG0_PSQL_HOST"
    
    postgres_port: int | None = 5432
    postgres_port_env: str | None = "C3PG0_PSQL_PORT"

    postgres_database_name: str | None = "postgres"
    postgres_database_name_env: str | None = "C3PG0_PSQL_DB_NAME"

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
