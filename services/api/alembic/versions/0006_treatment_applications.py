"""create treatment_applications table, treatment_application_id FK on followups, efficacy compound index

Revision ID: 0006
Revises: 0005
Create Date: 2026-08-24

"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "0006"
down_revision = "0005"
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
    # -- 1. treatment_applications table --
    op.create_table(
        "treatment_applications",
        *_base_columns(),
        sa.Column(
            "problem_id",
            sa.String(length=36),
            sa.ForeignKey("problems.id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column(
            "farm_id",
            sa.String(length=36),
            sa.ForeignKey("farms.id", ondelete="RESTRICT"),
            nullable=False,
        ),
        sa.Column("pathogen_type", sa.String(length=100), nullable=False),
        sa.Column("treatment_name", sa.String(length=255), nullable=False),
        sa.Column("treatment_category", sa.String(length=50), nullable=False),
        sa.Column("applied_on", sa.Date(), nullable=False),
        sa.Column("crop", sa.String(length=100), nullable=False),
        sa.Column("district", sa.String(length=255), nullable=False),
        sa.Column("final_outcome", sa.String(length=50), nullable=True),
        sa.Column("followups_to_resolution", sa.Integer(), nullable=True),
        sa.Column("days_to_resolution", sa.Integer(), nullable=True),
        sa.Column("failed_on_got_worse", sa.Boolean(), nullable=False, server_default=sa.text("false")),
        sa.Column("escalated_for_expert", sa.Boolean(), nullable=False, server_default=sa.text("false")),
    )
    op.create_index("ix_treatment_applications_problem_id", "treatment_applications", ["problem_id"])
    op.create_index("ix_treatment_applications_farm_id", "treatment_applications", ["farm_id"])
    op.create_index("ix_treatment_applications_pathogen_type", "treatment_applications", ["pathogen_type"])
    op.create_index("ix_treatment_applications_treatment_name", "treatment_applications", ["treatment_name"])
    op.create_index("ix_treatment_applications_applied_on", "treatment_applications", ["applied_on"])
    op.create_index("ix_treatment_applications_district", "treatment_applications", ["district"])

    # Composite index for regional trailing efficacy aggregation (spec §3.5)
    op.create_index(
        "idx_treatment_apps_efficacy",
        "treatment_applications",
        ["pathogen_type", "treatment_name", "crop", "district", "applied_on"],
    )

    # -- 2. Add treatment_application_id FK to followups --
    op.add_column(
        "followups",
        sa.Column(
            "treatment_application_id",
            sa.String(length=36),
            sa.ForeignKey("treatment_applications.id", ondelete="SET NULL"),
            nullable=True,
        ),
    )
    op.create_index("ix_followups_treatment_application_id", "followups", ["treatment_application_id"])


def downgrade() -> None:
    # Revert followups column & index
    op.drop_index("ix_followups_treatment_application_id", table_name="followups")
    op.drop_column("followups", "treatment_application_id")

    # Revert treatment_applications indexes & table
    op.drop_index("idx_treatment_apps_efficacy", table_name="treatment_applications")
    op.drop_index("ix_treatment_applications_district", table_name="treatment_applications")
    op.drop_index("ix_treatment_applications_applied_on", table_name="treatment_applications")
    op.drop_index("ix_treatment_applications_treatment_name", table_name="treatment_applications")
    op.drop_index("ix_treatment_applications_pathogen_type", table_name="treatment_applications")
    op.drop_index("ix_treatment_applications_farm_id", table_name="treatment_applications")
    op.drop_index("ix_treatment_applications_problem_id", table_name="treatment_applications")
    op.drop_table("treatment_applications")
