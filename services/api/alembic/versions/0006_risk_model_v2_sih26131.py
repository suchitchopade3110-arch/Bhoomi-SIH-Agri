"""realign health_snapshots for SIH26131 risk model v2 (truncate-and-reseed for demo data)

Revision ID: 0006
Revises: 0005
Create Date: 2026-08-24

Strategy chosen: Truncate-and-reseed. Legacy v1 snapshots stored 6-key subindices
in JSONB. Under SIH26131, snapshots are keyed by the 4 v2 sub-indices
('active_problem_severity', 'environmental_risk', 'monitoring_recency', 'treatment_response')
with WEIGHTS_VERSION 'v2-sih26131'.
"""

from alembic import op

# revision identifiers, used by Alembic.
revision = "0006"
down_revision = "0005"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Truncate legacy v1 snapshots so demo history starts fresh with v2 schema
    op.execute("TRUNCATE TABLE health_snapshots")


def downgrade() -> None:
    op.execute("TRUNCATE TABLE health_snapshots")
