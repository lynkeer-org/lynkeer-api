"""Add updated_at to owner

Revision ID: 0569a4f91379
Revises: bf650880a0fa
Create Date: 2025-09-09 13:11:58.546495
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "0569a4f91379"
down_revision: Union[str, Sequence[str], None] = "bf650880a0fa"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Only add the column to owner; keep it nullable & timezone-aware
    op.add_column(
        "owner",
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("owner", "updated_at")
