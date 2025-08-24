"""citext + partial unique index

Revision ID: c2f10424a415
Revises: 1b3aea183f0c
Create Date: 2025-08-21 08:59:16.316103
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "c2f10424a415"
down_revision: Union[str, Sequence[str], None] = "1b3aea183f0c"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Ensure citext exists (idempotent)
    op.execute("CREATE EXTENSION IF NOT EXISTS citext;")

    # If an older unique constraint exists, drop it safely (idempotent)
    op.execute(
        """
        DO $$
        BEGIN
            IF EXISTS (
                SELECT 1
                FROM pg_constraint
                WHERE conname = 'uq_title_owner_pass_type'
            ) THEN
                ALTER TABLE passmodel DROP CONSTRAINT uq_title_owner_pass_type;
            END IF;
        END$$;
        """
    )

    # Enforce NOT NULL as per your model (keep if intended)
    op.alter_column("owner", "active", existing_type=sa.BOOLEAN(), nullable=False)

    # Convert title to CITEXT (case-insensitive)
    op.alter_column(
        "passmodel",
        "title",
        existing_type=sa.VARCHAR(),
        type_=postgresql.CITEXT(),
        existing_nullable=False,
    )

    # Ensure active is NOT NULL (predicate depends on it)
    op.alter_column("passmodel", "active", existing_type=sa.BOOLEAN(), nullable=False)

    # Create partial unique index on active rows
    op.create_index(
        "uq_active_title_owner_type",
        "passmodel",
        ["title", "owner_id", "pass_type_id"],
        unique=True,
        postgresql_where=sa.text("active = true"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Drop the partial unique index
    op.drop_index("uq_active_title_owner_type", table_name="passmodel")

    # Revert passmodel.title back to VARCHAR
    op.alter_column(
        "passmodel",
        "title",
        existing_type=postgresql.CITEXT(),
        type_=sa.VARCHAR(),
        existing_nullable=False,
    )

    # Revert NOT NULL if you changed it in upgrade
    op.alter_column("passmodel", "active", existing_type=sa.BOOLEAN(), nullable=True)
    op.alter_column("owner", "active", existing_type=sa.BOOLEAN(), nullable=True)
