"""add distinguishing_cues column to knowledge_chunks (checklist §4.7)

Persists optional diagnostic cues for knowledge chunks so identification cues
are queryable directly on the chunk aggregate.

Revision ID: 0011
Revises: 0010
Create Date: 2026-08-26

"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "0011"
down_revision = "0010"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column("knowledge_chunks", sa.Column("distinguishing_cues", sa.Text(), nullable=True))


def downgrade() -> None:
    op.drop_column("knowledge_chunks", "distinguishing_cues")
