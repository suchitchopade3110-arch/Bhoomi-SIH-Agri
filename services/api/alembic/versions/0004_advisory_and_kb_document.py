"""add advisories and kb_documents tables, knowledge_chunks.document_id FK, HNSW index

Revision ID: 0004
Revises: 0003
Create Date: 2026-08-22

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "0004"
down_revision = "0003"
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
    # -- kb_documents: parent table for curated corpus docs --
    op.create_table(
        "kb_documents",
        *_base_columns(),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("source", sa.String(length=255), nullable=False),
        sa.Column("curator", sa.String(length=100), nullable=False),
        sa.Column("reviewed_on", sa.Date(), nullable=False),
        sa.Column("content", sa.Text(), nullable=False),
        sa.Column("lang", sa.String(length=10), nullable=False, server_default="en"),
    )

    # -- advisories: RAG-generated 5-point structured advice --
    op.create_table(
        "advisories",
        *_base_columns(),
        sa.Column("farm_id", sa.String(length=36), nullable=False),
        sa.Column("problem_id", sa.String(length=36), nullable=True),
        sa.Column("possible_issue", sa.Text(), nullable=False),
        sa.Column("what_to_check", sa.Text(), nullable=False),
        sa.Column("what_to_do_next", sa.Text(), nullable=False),
        sa.Column("what_to_avoid", sa.Text(), nullable=False),
        sa.Column("expert_triggers", sa.Text(), nullable=False),
        sa.Column("citations", postgresql.JSONB(), nullable=False, server_default="[]"),
        sa.Column("confidence", sa.Float(), nullable=True),
        sa.Column("model_version", sa.String(length=50), nullable=True),
        sa.Column("query_text", sa.Text(), nullable=True),
        sa.Column("lang", sa.String(length=10), nullable=False, server_default="ta-IN"),
    )
    op.create_index("ix_advisories_farm_id", "advisories", ["farm_id"])
    op.create_index("ix_advisories_problem_id", "advisories", ["problem_id"])

    # -- Add document_id FK column to knowledge_chunks --
    op.add_column(
        "knowledge_chunks",
        sa.Column("document_id", sa.String(length=36), nullable=True),
    )
    op.create_index("ix_knowledge_chunks_document_id", "knowledge_chunks", ["document_id"])

    # -- HNSW index for cosine similarity on embeddings --
    # This uses pgvector's HNSW index type for approximate nearest-neighbor search.
    op.execute(
        """
        CREATE INDEX IF NOT EXISTS ix_kb_chunk_embedding_cosine
        ON knowledge_chunks
        USING hnsw (embedding vector_cosine_ops)
        WITH (m = 16, ef_construction = 64)
        """
    )


def downgrade() -> None:
    op.execute("DROP INDEX IF EXISTS ix_kb_chunk_embedding_cosine")
    op.drop_index("ix_knowledge_chunks_document_id", table_name="knowledge_chunks")
    op.drop_column("knowledge_chunks", "document_id")
    op.drop_index("ix_advisories_problem_id", table_name="advisories")
    op.drop_index("ix_advisories_farm_id", table_name="advisories")
    op.drop_table("advisories")
    op.drop_table("kb_documents")
