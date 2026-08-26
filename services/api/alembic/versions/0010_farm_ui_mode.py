"""add ui_mode column to farms (checklist §1.5)

Persists the veteran/novice UI density toggle on the farm profile so it
survives across sessions and devices instead of only living as client-local
state.

Revision ID: 0010
Revises: 0009
Create Date: 2026-08-26

"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "0010"
down_revision = "0009"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        "farms",
        sa.Column("ui_mode", sa.String(length=20), nullable=False, server_default="novice"),
    )


def downgrade() -> None:
    op.drop_column("farms", "ui_mode")
