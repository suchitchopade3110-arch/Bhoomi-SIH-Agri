"""db/models.py — SQLAlchemy 2.0 ORM tables for Bhoomi (spec-mandated path).

The canonical ORM model definitions live in ``app/models/``. This module
re-exports them at the spec-mandated ``db/models.py`` path so Alembic and
any tooling that follows the spec can locate them.

Tables in scope for Phase 0 (the intelligence-layer tables):
  - health_snapshots  — one row per HealthSnapshot computation
  - knowledge_chunks  — RAG corpus chunks with pgvector embedding column

Farm, LandRecord, Problem, Case, Scheme tables are shared with teammates
and will be added to Alembic once their schemas are finalised.
"""

# Re-export ORM base and intelligence-layer models at the spec path.
from app.models.base import Base  # noqa: F401
from app.models.health_snapshot import HealthSnapshot  # noqa: F401
from app.models.knowledge_chunk import KnowledgeChunk  # noqa: F401

__all__ = ["Base", "HealthSnapshot", "KnowledgeChunk"]
