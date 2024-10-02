

from dataclasses import dataclass
from uuid import UUID


@dataclass
class MigrationModel:
    """Represent revision model in database."""
    id: int
    version: str
    revision: UUID
    is_applied: bool | None
