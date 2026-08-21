"""create cases and agronomists tables

Revision ID: 0003
Revises: 0002
Create Date: 2026-08-21

"""

import uuid
from datetime import datetime

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "0003"
down_revision = "0002"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "agronomists",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("identifier", sa.String(length=64), nullable=False, unique=True),
        sa.Column("name", sa.String(length=120), nullable=False),
        sa.Column("kvk_center", sa.String(length=120), nullable=False),
        sa.Column("jurisdiction", sa.String(length=80), nullable=False),
        sa.Column("is_available", sa.Boolean(), nullable=False, server_default=sa.true()),
        sa.Column("active_case_count", sa.Integer(), nullable=False, server_default="0"),
    )
    op.create_index("ix_agronomists_identifier", "agronomists", ["identifier"], unique=True)
    op.create_index("ix_agronomists_jurisdiction", "agronomists", ["jurisdiction"])

    op.create_table(
        "cases",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("farm_id", sa.String(length=36), nullable=False),
        sa.Column("problem_id", sa.String(length=36), nullable=True),
        sa.Column("status", sa.String(length=20), nullable=False, server_default="open"),
        sa.Column("reason", sa.Text(), nullable=False),
        sa.Column("trigger", sa.String(length=40), nullable=False),
        sa.Column("assigned_to", sa.String(length=64), nullable=True),
        sa.Column("summary", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("diagnosis", sa.Text(), nullable=True),
        sa.Column("treatment", sa.Text(), nullable=True),
        sa.Column("notes", sa.Text(), nullable=True),
        sa.Column("resolved_at", sa.DateTime(), nullable=True),
    )
    op.create_index("ix_cases_farm_id", "cases", ["farm_id"])
    op.create_index("ix_cases_problem_id", "cases", ["problem_id"])

    # Seed a small demo roster (execution plan item 3): two available
    # agronomists in different jurisdictions plus one unavailable one, so
    # "nearest available, else next available, else OFFICER_UNAVAILABLE"
    # routing has something real to exercise out of the box.
    now = datetime.utcnow()
    agronomists_table = sa.table(
        "agronomists",
        sa.column("id", sa.String),
        sa.column("created_at", sa.DateTime),
        sa.column("updated_at", sa.DateTime),
        sa.column("identifier", sa.String),
        sa.column("name", sa.String),
        sa.column("kvk_center", sa.String),
        sa.column("jurisdiction", sa.String),
        sa.column("is_available", sa.Boolean),
        sa.column("active_case_count", sa.Integer),
    )
    op.bulk_insert(
        agronomists_table,
        [
            {
                "id": str(uuid.uuid4()),
                "created_at": now,
                "updated_at": now,
                "identifier": "agronomist:kvk_erode",
                "name": "Dr. Kavitha Selvam",
                "kvk_center": "KVK Erode",
                "jurisdiction": "erode",
                "is_available": True,
                "active_case_count": 0,
            },
            {
                "id": str(uuid.uuid4()),
                "created_at": now,
                "updated_at": now,
                "identifier": "agronomist:kvk_madurai",
                "name": "Dr. Ramesh Iyer",
                "kvk_center": "KVK Madurai",
                "jurisdiction": "madurai",
                "is_available": True,
                "active_case_count": 0,
            },
            {
                "id": str(uuid.uuid4()),
                "created_at": now,
                "updated_at": now,
                "identifier": "agronomist:kvk_trichy",
                "name": "Dr. Priya Natarajan",
                "kvk_center": "KVK Trichy",
                "jurisdiction": "trichy",
                "is_available": False,
                "active_case_count": 5,
            },
        ],
    )


def downgrade() -> None:
    op.drop_index("ix_cases_problem_id", table_name="cases")
    op.drop_index("ix_cases_farm_id", table_name="cases")
    op.drop_table("cases")
    op.drop_index("ix_agronomists_jurisdiction", table_name="agronomists")
    op.drop_index("ix_agronomists_identifier", table_name="agronomists")
    op.drop_table("agronomists")
