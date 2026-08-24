"""simplify farm onboarding: add region column, make legacy profile columns nullable

Revision ID: 0007
Revises: 0006
Create Date: 2026-08-24

"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "0007"
down_revision = "0006"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # 1. Add region column + index
    op.add_column("farms", sa.Column("region", sa.String(length=255), nullable=True))
    op.create_index("ix_farms_region", "farms", ["region"])

    # 2. Make legacy profile columns nullable
    op.alter_column("farms", "farm_name", existing_type=sa.String(length=255), nullable=True)
    op.alter_column("farms", "village", existing_type=sa.String(length=255), nullable=True)
    op.alter_column("farms", "taluk", existing_type=sa.String(length=255), nullable=True)
    op.alter_column("farms", "district", existing_type=sa.String(length=255), nullable=True)
    op.alter_column("farms", "latitude", existing_type=sa.Float(), nullable=True)
    op.alter_column("farms", "longitude", existing_type=sa.Float(), nullable=True)
    op.alter_column("farms", "total_area_acres", existing_type=sa.Float(), nullable=True)


def downgrade() -> None:
    # 1. Revert legacy profile columns to NOT NULL (note: will fail if NULL rows exist)
    op.alter_column("farms", "total_area_acres", existing_type=sa.Float(), nullable=False)
    op.alter_column("farms", "longitude", existing_type=sa.Float(), nullable=False)
    op.alter_column("farms", "latitude", existing_type=sa.Float(), nullable=False)
    op.alter_column("farms", "district", existing_type=sa.String(length=255), nullable=False)
    op.alter_column("farms", "taluk", existing_type=sa.String(length=255), nullable=False)
    op.alter_column("farms", "village", existing_type=sa.String(length=255), nullable=False)
    op.alter_column("farms", "farm_name", existing_type=sa.String(length=255), nullable=False)

    # 2. Revert region column + index
    op.drop_index("ix_farms_region", table_name="farms")
    op.drop_column("farms", "region")
