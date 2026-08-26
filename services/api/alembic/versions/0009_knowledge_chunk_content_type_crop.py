"""add content_type/crop columns to knowledge_chunks (checklist §4.1)

Replaces the doc_id-prefix retrieval-scoping convention (``kb_p*`` = pest)
with real, indexed metadata columns. Backfills existing rows from the same
prefix convention they were relying on, so no data is lost — new ingests
populate both columns directly from ``corpus_data.CorpusDoc``.

Revision ID: 0009
Revises: 268cf03f8c62
Create Date: 2026-08-26

"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = "0009"
down_revision = "268cf03f8c62"
branch_labels = None
depends_on = None

PEST_DOC_ID_PREFIX = "kb_p"


def upgrade() -> None:
    op.add_column("knowledge_chunks", sa.Column("content_type", sa.String(length=20), nullable=True))
    op.add_column("knowledge_chunks", sa.Column("crop", sa.String(length=50), nullable=True))

    # Backfill existing rows from the doc_id prefix convention they were
    # implicitly relying on — every current corpus doc is paddy.
    op.execute(
        f"""
        UPDATE knowledge_chunks
        SET content_type = CASE WHEN doc_id LIKE '{PEST_DOC_ID_PREFIX}%' THEN 'pest' ELSE 'disease' END,
            crop = 'paddy'
        WHERE content_type IS NULL
        """
    )

    op.create_index("ix_knowledge_chunks_content_type", "knowledge_chunks", ["content_type"])
    op.create_index("ix_knowledge_chunks_crop", "knowledge_chunks", ["crop"])


def downgrade() -> None:
    op.drop_index("ix_knowledge_chunks_crop", table_name="knowledge_chunks")
    op.drop_index("ix_knowledge_chunks_content_type", table_name="knowledge_chunks")
    op.drop_column("knowledge_chunks", "crop")
    op.drop_column("knowledge_chunks", "content_type")
