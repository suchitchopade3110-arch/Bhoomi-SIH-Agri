"""create core aggregates: users, farms, land_parcels, problems, followups, cases, schemes, assets

Revision ID: 0003
Revises: 0002
Create Date: 2026-08-22

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "0003"
down_revision = "0002"
branch_labels = None
depends_on = None


def _base_columns() -> list[sa.Column]:
    """The common id/created_at/updated_at columns every ``models.base.Base``
    subclass carries — factored out so each table below only lists what's
    actually specific to it."""
    return [
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
    ]


def upgrade() -> None:
    op.create_table(
        "users",
        *_base_columns(),
        sa.Column("phone_number", sa.String(length=20), nullable=True),
        sa.Column("email", sa.String(length=255), nullable=True),
        sa.Column("full_name", sa.String(length=255), nullable=False),
        sa.Column("role", sa.String(length=20), nullable=False),
        sa.Column("preferred_language", sa.String(length=10), nullable=False),
        sa.Column("password_hash", sa.String(length=255), nullable=False),
        sa.Column("jurisdiction", sa.String(length=100), nullable=True),
    )
    op.create_index("ix_users_phone_number", "users", ["phone_number"], unique=True)
    op.create_index("ix_users_email", "users", ["email"], unique=True)
    op.create_index("ix_users_role", "users", ["role"])

    op.create_table(
        "farms",
        *_base_columns(),
        sa.Column("farmer_id", sa.String(length=36), nullable=False),
        sa.Column("farm_name", sa.String(length=255), nullable=False),
        sa.Column("village", sa.String(length=255), nullable=False),
        sa.Column("taluk", sa.String(length=255), nullable=False),
        sa.Column("district", sa.String(length=255), nullable=False),
        sa.Column("state", sa.String(length=100), nullable=False),
        sa.Column("latitude", sa.Float(), nullable=False),
        sa.Column("longitude", sa.Float(), nullable=False),
        sa.Column("total_area_acres", sa.Float(), nullable=False),
        sa.Column("survey_number", sa.String(length=100), nullable=True),
        sa.Column("land_status", sa.String(length=30), nullable=False),
        sa.Column("primary_crop", sa.String(length=100), nullable=False),
        sa.Column("growth_stage", sa.String(length=30), nullable=True),
        sa.Column("sowing_date", sa.Date(), nullable=True),
        sa.Column("soil_type", sa.String(length=50), nullable=False),
        sa.Column("irrigation_source", sa.String(length=50), nullable=False),
        sa.Column("soil_moisture_pct", sa.Float(), nullable=True),
        sa.Column("irrigation_delivered_mm", sa.Float(), nullable=True),
        sa.Column("irrigation_required_mm", sa.Float(), nullable=True),
        sa.Column("days_since_planting", sa.Integer(), nullable=True),
        sa.Column("expected_stage_day", sa.Integer(), nullable=True),
        sa.Column("days_since_last_scan", sa.Integer(), nullable=True),
    )
    op.create_index("ix_farms_farmer_id", "farms", ["farmer_id"])

    op.create_table(
        "land_parcels",
        *_base_columns(),
        sa.Column("farm_id", sa.String(length=36), nullable=False),
        sa.Column("survey_number", sa.String(length=100), nullable=False),
        sa.Column("patta_passbook_asset_id", sa.String(length=36), nullable=True),
        sa.Column("status", sa.String(length=30), nullable=False),
        sa.Column("auto_lookup_outcome", sa.String(length=20), nullable=False),
        sa.Column("district", sa.String(length=255), nullable=False),
        sa.Column("suggested_boundary", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("confirmed_boundary", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("submitted_at", sa.DateTime(), nullable=False),
        sa.Column("verified_at", sa.DateTime(), nullable=True),
        sa.Column("verified_by", sa.String(length=255), nullable=True),
        sa.Column("officer_notes", sa.String(length=1000), nullable=True),
    )
    op.create_index("ix_land_parcels_farm_id", "land_parcels", ["farm_id"])
    op.create_index("ix_land_parcels_status", "land_parcels", ["status"])

    op.create_table(
        "problems",
        *_base_columns(),
        sa.Column("farm_id", sa.String(length=36), nullable=False),
        sa.Column("label", sa.String(length=100), nullable=False),
        sa.Column("severity", sa.String(length=20), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("image_asset_id", sa.String(length=36), nullable=True),
        sa.Column("resolved_at", sa.DateTime(), nullable=True),
    )
    op.create_index("ix_problems_farm_id", "problems", ["farm_id"])
    op.create_index("ix_problems_status", "problems", ["status"])

    op.create_table(
        "followups",
        *_base_columns(),
        sa.Column("problem_id", sa.String(length=36), nullable=False),
        sa.Column("farm_id", sa.String(length=36), nullable=False),
        sa.Column("response", sa.String(length=20), nullable=False),
        sa.Column("farmer_notes", sa.String(length=1000), nullable=True),
        sa.Column("photo_asset_id", sa.String(length=36), nullable=True),
    )
    op.create_index("ix_followups_problem_id", "followups", ["problem_id"])
    op.create_index("ix_followups_farm_id", "followups", ["farm_id"])

    op.create_table(
        "cases",
        *_base_columns(),
        sa.Column("farm_id", sa.String(length=36), nullable=False),
        sa.Column("problem_id", sa.String(length=36), nullable=True),
        sa.Column("reason", sa.String(length=500), nullable=True),
        sa.Column("severity", sa.String(length=20), nullable=False),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("assigned_to", sa.String(length=255), nullable=True),
        sa.Column("case_summary", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("resolution", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column("resolved_at", sa.DateTime(), nullable=True),
    )
    op.create_index("ix_cases_farm_id", "cases", ["farm_id"])
    op.create_index("ix_cases_problem_id", "cases", ["problem_id"])
    op.create_index("ix_cases_status", "cases", ["status"])

    op.create_table(
        "schemes",
        *_base_columns(),
        sa.Column("name", sa.String(length=255), nullable=False),
        sa.Column("ministry", sa.String(length=255), nullable=False),
        sa.Column("jurisdiction", sa.String(length=100), nullable=False),
        sa.Column("description", sa.String(length=1000), nullable=False),
        sa.Column("benefits", sa.String(length=1000), nullable=False),
        sa.Column("eligibility_criteria", postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column("subsidy_percentage", sa.Float(), nullable=True),
        sa.Column("max_amount_inr", sa.Float(), nullable=True),
        sa.Column("portal_url", sa.String(length=500), nullable=True),
        sa.Column("status", sa.String(length=20), nullable=False),
        sa.Column("last_verified", sa.Date(), nullable=False),
        sa.Column("crop_filter", sa.String(length=100), nullable=True),
        sa.Column("category_filter", sa.String(length=50), nullable=True),
    )

    op.create_table(
        "assets",
        *_base_columns(),
        sa.Column("asset_kind", sa.String(length=30), nullable=False),
        sa.Column("file_name", sa.String(length=500), nullable=False),
        sa.Column("content_type", sa.String(length=100), nullable=False),
        sa.Column("farm_id", sa.String(length=36), nullable=True),
        sa.Column("storage_key", sa.String(length=500), nullable=False),
    )
    op.create_index("ix_assets_farm_id", "assets", ["farm_id"])


def downgrade() -> None:
    op.drop_index("ix_assets_farm_id", table_name="assets")
    op.drop_table("assets")

    op.drop_table("schemes")

    op.drop_index("ix_cases_status", table_name="cases")
    op.drop_index("ix_cases_problem_id", table_name="cases")
    op.drop_index("ix_cases_farm_id", table_name="cases")
    op.drop_table("cases")

    op.drop_index("ix_followups_farm_id", table_name="followups")
    op.drop_index("ix_followups_problem_id", table_name="followups")
    op.drop_table("followups")

    op.drop_index("ix_problems_status", table_name="problems")
    op.drop_index("ix_problems_farm_id", table_name="problems")
    op.drop_table("problems")

    op.drop_index("ix_land_parcels_status", table_name="land_parcels")
    op.drop_index("ix_land_parcels_farm_id", table_name="land_parcels")
    op.drop_table("land_parcels")

    op.drop_index("ix_farms_farmer_id", table_name="farms")
    op.drop_table("farms")

    op.drop_index("ix_users_role", table_name="users")
    op.drop_index("ix_users_email", table_name="users")
    op.drop_index("ix_users_phone_number", table_name="users")
    op.drop_table("users")
