"""Retrieval (execution plan item 2): embed the query, run pgvector cosine
similarity search, return top-k chunks with scores. The top score becomes
``retrieval_relevance`` for the Phase-2 confidence gate.
"""

from typing import Annotated

from fastapi import Depends

from app.adapters.dependencies import get_embedding_adapter
from app.ports.embeddings import EmbeddingPort
from app.domain.rag.constants import DEFAULT_TOP_K
from app.repositories.dependencies import get_knowledge_chunk_reader
from app.repositories.interfaces import KnowledgeChunkReader, RetrievedChunk


class RetrievalService:
    """Embeds a query and returns the top-k most relevant corpus chunks."""

    def __init__(self, reader: KnowledgeChunkReader, embedding_port: EmbeddingPort) -> None:
        self._reader = reader
        self._embedding_port = embedding_port

    async def retrieve(self, query_text: str, top_k: int = DEFAULT_TOP_K) -> list[RetrievedChunk]:
        """Embed ``query_text`` and return the top-``k`` chunks, highest score first.

        Returns an empty list if the corpus has nothing to offer — callers
        must treat that as zero relevance (escalate), never skip the check.
        """
        query_embedding = await self._embedding_port.embed_text(query_text)
        return await self._reader.similarity_search(query_embedding, top_k)

    @staticmethod
    def top_relevance(chunks: list[RetrievedChunk]) -> float:
        """The score to feed the confidence gate as ``retrieval_relevance``.

        Deliberately ``0.0`` — not ``None`` — when nothing was retrieved:
        retrieval is always attempted for advisory/diagnose calls, so an
        empty result is a real zero-relevance signal the gate must act on,
        not a "signal not applicable" skip (contrast with the image
        confidence signal, which genuinely can be absent for a text-only
        query).
        """
        return chunks[0].score if chunks else 0.0


def get_retrieval_service(
    reader: Annotated[KnowledgeChunkReader, Depends(get_knowledge_chunk_reader)],
    embedding_port: Annotated[EmbeddingPort, Depends(get_embedding_adapter)],
) -> RetrievalService:
    """FastAPI dependency provider assembling ``RetrievalService`` from its ports."""
    return RetrievalService(reader, embedding_port)
