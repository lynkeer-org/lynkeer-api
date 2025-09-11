"""added updated_at for pass_type

Revision ID: bf650880a0fa
Revises: de4cfb9fd13a
Create Date: 2025-09-09 12:33:34.967640
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "bf650880a0fa"
down_revision: Union[str, Sequence[str], None] = "de4cfb9fd13a"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Make passmodel.updated_at nullable (instead of NOT NULL)
    op.alter_column(
        "passmodel",
        "updated_at",
        existing_type=postgresql.TIMESTAMP(timezone=True),
        nullable=True,
    )

    # Add passtype.updated_at as nullable too
    op.add_column(
        "passtype",
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column("passtype", "updated_at")

    # revert passmodel.updated_at back to NOT NULL
    op.alter_column(
        "passmodel",
        "updated_at",
        existing_type=postgresql.TIMESTAMP(timezone=True),
        nullable=False,
    )
