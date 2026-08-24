"""add alerts table (SPEC-ALERT-001, Phase 3)

Revision ID: 0005
Revises: 0004
Create Date: 2026-08-24

"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "0005"
down_revision = "0004"
branch_labels = None
depends_on = None


def _base_columns() -> list[sa.Column]:
    """Common id/created_at/updated_at columns from ``models.base.Base``."""
    return [
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    ]


def upgrade() -> None:
    op.create_table(
        "alerts",
        *_base_columns(),
        sa.Column("farm_id", sa.String(length=36), nullable=True),
        sa.Column("district", sa.String(length=255), nullable=False),
        sa.Column("pathogen_name", sa.String(length=255), nullable=False),
        sa.Column("target_crop", sa.String(length=100), nullable=True),
        sa.Column("target", sa.String(length=30), nullable=False),
        sa.Column("severity", sa.String(length=20), nullable=False),
        sa.Column("trigger_reason", sa.String(length=1000), nullable=False),
        sa.Column("preventative_action", sa.String(length=1000), nullable=False),
        sa.Column("spoken_summary", sa.String(length=1000), nullable=False),
        sa.Column("delivery_channels", sa.ARRAY(sa.String()), nullable=False, server_default="{}"),
        sa.Column("cooldown_key", sa.String(length=255), nullable=False),
        sa.Column("expires_at", sa.DateTime(), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False, server_default="active"),
        sa.Column("dismissed_at", sa.DateTime(), nullable=True),
        sa.Column("dismiss_reason", sa.String(length=255), nullable=True),
    )
    op.create_index("ix_alerts_farm_id", "alerts", ["farm_id"])
    op.create_index("ix_alerts_district", "alerts", ["district"])
    op.create_index("ix_alerts_severity", "alerts", ["severity"])
    op.create_index("ix_alerts_cooldown_key", "alerts", ["cooldown_key"])
    op.create_index("ix_alerts_expires_at", "alerts", ["expires_at"])
    op.create_index("ix_alerts_status", "alerts", ["status"])
    # Stage B indexing requirement (spec §5.2) for the regional-broadcast
    # resolve query — a farm's alerts list is (farm_id = X) OR (farm_id IS
    # NULL AND district = Y), so the broadcast half benefits from its own
    # partial index rather than sharing the per-farm one.
    op.execute(
        """
        CREATE INDEX IF NOT EXISTS ix_alerts_broadcast
        ON alerts (district, target_crop, expires_at)
        WHERE farm_id IS NULL
        """
    )


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS ix_alerts_broadcast")
    op.drop_index("ix_alerts_status", table_name="alerts")
    op.drop_index("ix_alerts_expires_at", table_name="alerts")
    op.drop_index("ix_alerts_cooldown_key", table_name="alerts")
    op.drop_index("ix_alerts_severity", table_name="alerts")
    op.drop_index("ix_alerts_district", table_name="alerts")
    op.drop_index("ix_alerts_farm_id", table_name="alerts")
    op.drop_table("alerts")
