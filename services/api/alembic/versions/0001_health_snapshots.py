"""create health_snapshots table

Revision ID: 0001
Revises:
Create Date: 2026-08-21

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "0001"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "health_snapshots",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        # Unconstrained: the Farm aggregate's own table lands in a later
        # phase. Add the FK once app.models.farm.Farm exists.
        sa.Column("farm_id", sa.String(length=36), nullable=False),
        sa.Column("score", sa.Integer(), nullable=True),
        sa.Column("band", sa.String(length=20), nullable=False),
        sa.Column("weights_version", sa.String(length=20), nullable=False),
        sa.Column("computed_at", sa.DateTime(), nullable=False),
        sa.Column("subindices", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("triggering_input", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("missing_fields", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
    )
    op.create_index("ix_health_snapshots_farm_id", "health_snapshots", ["farm_id"])
    op.create_index("ix_health_snapshots_computed_at", "health_snapshots", ["computed_at"])
    op.create_index(
        "ix_health_snapshots_farm_id_computed_at",
        "health_snapshots",
        ["farm_id", "computed_at"],
    )


def downgrade() -> None:
    op.drop_index("ix_health_snapshots_farm_id_computed_at", table_name="health_snapshots")
    op.drop_index("ix_health_snapshots_computed_at", table_name="health_snapshots")
    op.drop_index("ix_health_snapshots_farm_id", table_name="health_snapshots")
    op.drop_table("health_snapshots")
