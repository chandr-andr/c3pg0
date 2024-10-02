

from m3p0.driver import M3P0Driver
from m3p0.utils import database_revision_history, migrations_revision_history


async def check_migration_history(
    driver: M3P0Driver,
) -> tuple[bool, str]:
    local_revisions_history = migrations_revision_history()
    database_revisions_history = await database_revision_history(
        driver=driver,
    )

    if local_revisions_history == database_revisions_history:
        return (
            True,
            "Migration history and actual database state is synchronized.",
        )
    elif len(database_revisions_history) < len(local_revisions_history):
        migrations_to_apply = [
            revision for revision in local_revisions_history
            if revision not in set(database_revisions_history)
        ]
        return (
            False,
            f"There are some unapplied migrations - {migrations_to_apply}",
        )
    elif len(local_revisions_history) < len(database_revisions_history):
        unrecognized_migrations = [
            revision for revision in database_revisions_history
            if revision not in set(local_revisions_history)
        ]
        return (
            False,
            f"Database has migrations not presented "
            f"locally - {unrecognized_migrations}",
        )
    
    return (
        True,
        "Migration history and actual database state is synchronized.",
    )