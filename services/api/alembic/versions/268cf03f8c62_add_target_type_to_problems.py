"""add target_type to problems

Revision ID: 268cf03f8c62
Revises: b37a2db9c0ca
Create Date: 2026-08-25 09:04:56.413137

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '268cf03f8c62'
down_revision: Union[str, None] = 'b37a2db9c0ca'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("problems", sa.Column("target_type", sa.String(length=20), nullable=True))


def downgrade() -> None:
    op.drop_column("problems", "target_type")
