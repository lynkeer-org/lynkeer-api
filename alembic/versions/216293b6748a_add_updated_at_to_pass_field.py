"""Add updated_at to pass_field

Revision ID: 216293b6748a
Revises: 0569a4f91379
Create Date: 2025-09-10 09:39:18.242632
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "216293b6748a"
down_revision: Union[str, Sequence[str], None] = "0569a4f91379"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "passfield",
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
    )


def downgrade() -> None:
    op.drop_column("passfield", "updated_at")
