"""init tables

Revision ID: 5fab3eade2a6
Revises:
Create Date: 2025-09-27 08:41:04.783590

"""

from collections.abc import Sequence

# revision identifiers, used by Alembic.
revision: str = "5fab3eade2a6"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
