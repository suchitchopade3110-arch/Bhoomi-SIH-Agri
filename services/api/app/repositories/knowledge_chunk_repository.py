"""All DB access for the curated RAG corpus (PRD §5.7). Real, pgvector-backed."""

from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.knowledge_chunk import KnowledgeChunk
from app.repositories.interfaces import RetrievedChunk


class KnowledgeChunkRepository:
    """Corpus ingestion (write) and similarity search (read) over ``knowledge_chunks``."""

    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def delete_all(self) -> None:
        """Clear the corpus — ingestion is idempotent, re-running replaces it wholesale."""
        await self._session.execute(delete(KnowledgeChunk))

    async def add_chunk(
        self,
        doc_id: str,
        title: str,
        reviewed_on,
        chunk_index: int,
        chunk_text: str,
        embedding: list[float],
        content_type: str | None = None,
        crop: str | None = None,
        distinguishing_cues: str | None = None,
    ) -> None:
        self._session.add(
            KnowledgeChunk(
                doc_id=doc_id,
                title=title,
                reviewed_on=reviewed_on,
                chunk_index=chunk_index,
                chunk_text=chunk_text,
                embedding=embedding,
                content_type=content_type,
                crop=crop,
                distinguishing_cues=distinguishing_cues,
            )
        )

    async def commit(self) -> None:
        await self._session.commit()

    async def similarity_search(
        self, query_embedding: list[float], top_k: int, content_type: str | None = None
    ) -> list[RetrievedChunk]:
        """Top-``k`` chunks by cosine similarity to ``query_embedding``, highest first.

        pgvector's ``cosine_distance`` is ``1 - cosine_similarity`` for
        normalized vectors; we convert back to a similarity score in
        ``[0.0, 1.0]`` so callers (the confidence gate) work with the same
        "higher is more relevant" convention everywhere.

        ``content_type``: ``"pest"`` or ``"disease"`` restricts to chunks
        with that ``content_type`` column value (checklist §4.1 — a real,
        indexed column, not a ``doc_id`` prefix inference); ``None``
        (default) searches the whole corpus.
        """
        distance = KnowledgeChunk.embedding.cosine_distance(query_embedding)
        stmt = select(KnowledgeChunk, distance.label("distance"))
        if content_type is not None:
            stmt = stmt.where(KnowledgeChunk.content_type == content_type)
        stmt = stmt.order_by(distance).limit(top_k)
        result = await self._session.execute(stmt)

        return [
            RetrievedChunk(
                doc_id=row.doc_id,
                title=row.title,
                reviewed_on=row.reviewed_on,
                chunk_text=row.chunk_text,
                score=max(0.0, min(1.0, 1.0 - distance_value)),
            )
            for row, distance_value in result.all()
        ]
