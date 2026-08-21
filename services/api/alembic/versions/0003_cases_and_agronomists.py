"""create cases and agronomists tables

Revision ID: 0003
Revises: 0002
Create Date: 2026-08-21

"""

import uuid

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "0003"
down_revision = "0002"
branch_labels = None
depends_on = None

# Matches Settings.DEMO_AGRONOMIST_NAME (core/config.py) — the fixed row
# AGRONOMIST_ROUTING_MODE="demo_fixed" (the default) always assigns cases to.
DEMO_AGRONOMIST_NAME = "Dr. Meena Krishnan"


def upgrade() -> None:
    op.create_table(
        "agronomists",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("name", sa.String(length=120), nullable=False, unique=True),
        sa.Column("kvk_center", sa.String(length=120), nullable=False),
        sa.Column("district", sa.String(length=80), nullable=False),
        sa.Column("is_available", sa.Boolean(), nullable=False, server_default=sa.true()),
    )
    op.create_index("ix_agronomists_name", "agronomists", ["name"])
    op.create_index("ix_agronomists_district", "agronomists", ["district"])

    op.create_table(
        "cases",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        # Unconstrained: the Farm/Problem aggregates don't have their own
        # tables yet (same rationale as health_snapshots.farm_id).
        sa.Column("farm_id", sa.String(length=36), nullable=False),
        sa.Column("problem_id", sa.String(length=36), nullable=True),
        sa.Column("trigger_type", sa.String(length=40), nullable=False),
        sa.Column("reason", sa.Text(), nullable=False),
        sa.Column("severity", sa.String(length=20), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("farmer_name", sa.String(length=120), nullable=True),
        sa.Column("village", sa.String(length=120), nullable=True),
        sa.Column("crop", sa.String(length=80), nullable=True),
        sa.Column("case_summary", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("assigned_to", sa.String(length=36), nullable=True),
        sa.Column("assigned_kvk_center", sa.String(length=120), nullable=True),
        sa.Column("resolution", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("resolved_at", sa.DateTime(), nullable=True),
    )
    op.create_index("ix_cases_farm_id", "cases", ["farm_id"])
    op.create_index("ix_cases_problem_id", "cases", ["problem_id"])
    op.create_index("ix_cases_status", "cases", ["status"])
    op.create_index("ix_cases_assigned_to", "cases", ["assigned_to"])

    # Seed two demo agronomists so both routing modes (core/config.py
    # AGRONOMIST_ROUTING_MODE) have real rows to work against out of the box:
    # the fixed "demo_fixed" name, plus a second one in a different district
    # so "directory" mode's nearest/any-available query has something to pick between.
    agronomists = sa.table(
        "agronomists",
        sa.column("id", sa.String),
        sa.column("created_at", sa.DateTime),
        sa.column("updated_at", sa.DateTime),
        sa.column("name", sa.String),
        sa.column("kvk_center", sa.String),
        sa.column("district", sa.String),
        sa.column("is_available", sa.Boolean),
    )
    now = sa.func.now()
    op.bulk_insert(
        agronomists,
        [
            {
                "id": str(uuid.uuid4()),
                "name": DEMO_AGRONOMIST_NAME,
                "kvk_center": "TNAU KVK - Madurai",
                "district": "Madurai",
                "is_available": True,
            },
            {
                "id": str(uuid.uuid4()),
                "name": "Dr. Karthik Subramaniam",
                "kvk_center": "TNAU KVK - Erode",
                "district": "Erode",
                "is_available": True,
            },
        ],
    )
    # created_at/updated_at have no application-level default on a bulk
    # insert; backfill them explicitly so NOT NULL holds.
    op.execute("UPDATE agronomists SET created_at = NOW(), updated_at = NOW() WHERE created_at IS NULL")


def downgrade() -> None:
    op.drop_index("ix_cases_assigned_to", table_name="cases")
    op.drop_index("ix_cases_status", table_name="cases")
    op.drop_index("ix_cases_problem_id", table_name="cases")
    op.drop_index("ix_cases_farm_id", table_name="cases")
    op.drop_table("cases")

    op.drop_index("ix_agronomists_district", table_name="agronomists")
    op.drop_index("ix_agronomists_name", table_name="agronomists")
    op.drop_table("agronomists")
