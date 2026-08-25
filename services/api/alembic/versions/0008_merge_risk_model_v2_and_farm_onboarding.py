"""merge risk_model_v2 and farm_simplified_onboarding branches

Revision ID: b37a2db9c0ca
Revises: 0006b, 0007
Create Date: 2026-08-24 23:49:59.516609

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b37a2db9c0ca'
down_revision: Union[str, None] = ('0006b', '0007')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    pass


def downgrade() -> None:
    pass
