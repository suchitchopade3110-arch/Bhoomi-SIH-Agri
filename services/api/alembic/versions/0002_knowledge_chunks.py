"""create knowledge_chunks table (pgvector corpus)

Revision ID: 0002
Revises: 0001
Create Date: 2026-08-21

"""

from alembic import op
import sqlalchemy as sa
from pgvector.sqlalchemy import Vector

# revision identifiers, used by Alembic.
revision = "0002"
down_revision = "0001"
branch_labels = None
depends_on = None

EMBEDDING_DIM = 1024


def upgrade() -> None:
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")

    op.create_table(
        "knowledge_chunks",
        sa.Column("id", sa.String(length=36), primary_key=True),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.Column("updated_at", sa.DateTime(), nullable=False),
        sa.Column("doc_id", sa.String(length=64), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("reviewed_on", sa.Date(), nullable=False),
        sa.Column("chunk_index", sa.Integer(), nullable=False),
        sa.Column("chunk_text", sa.Text(), nullable=False),
        sa.Column("embedding", Vector(EMBEDDING_DIM), nullable=False),
    )
    op.create_index("ix_knowledge_chunks_doc_id", "knowledge_chunks", ["doc_id"])

    # HNSW needs no training data (unlike IVFFlat), so it's safe to create
    # against an empty table right after migration, before the corpus is
    # ingested. Requires pgvector >= 0.5.0.
    op.execute(
        "CREATE INDEX ix_knowledge_chunks_embedding_cosine "
        "ON knowledge_chunks USING hnsw (embedding vector_cosine_ops)"
    )


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS ix_knowledge_chunks_embedding_cosine")
    op.drop_index("ix_knowledge_chunks_doc_id", table_name="knowledge_chunks")
    op.drop_table("knowledge_chunks")
