"""Corpus ingestion (PRD §5.7, execution plan item 1): chunk the curated
corpus, embed each chunk via EmbeddingPort, and write it into the pgvector
``knowledge_chunks`` table.

Run as a script:

    python -m app.services.rag.ingest

Idempotent — each run replaces the corpus wholesale (``delete_all`` then
re-insert), so re-running after editing ``corpus_data.py`` is always safe.
"""

import asyncio
import logging

from app.ports.embeddings import EmbeddingPort
from app.core.db import AsyncSessionLocal
from app.domain.rag.chunking import chunk_text
from app.repositories.knowledge_chunk_repository import KnowledgeChunkRepository
from app.services.rag.corpus_data import CORPUS_DOCS, CorpusDoc

logger = logging.getLogger("bhoomi.rag.ingest")


async def ingest_corpus(
    repo: KnowledgeChunkRepository,
    embedding_port: EmbeddingPort,
    docs: list[CorpusDoc] = CORPUS_DOCS,
) -> int:
    """Chunk, embed, and write ``docs`` into the corpus table.

    Args:
        repo: The (real, pgvector-backed) knowledge chunk repository.
        embedding_port: The EmbeddingPort to embed each chunk with — the
            same one the app uses at query time, so ingestion and retrieval
            always agree on embedding space.
        docs: The curated corpus documents to ingest.

    Returns:
        The total number of chunks written.
    """
    await repo.delete_all()

    total_chunks = 0
    for doc in docs:
        chunks = chunk_text(doc["body"])
        if not chunks:
            logger.warning("Document %s produced zero chunks — skipping.", doc["doc_id"])
            continue

        embeddings = await embedding_port.embed_batch(chunks)
        for index, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            await repo.add_chunk(
                doc_id=doc["doc_id"],
                title=doc["title"],
                reviewed_on=doc["reviewed_on"],
                chunk_index=index,
                chunk_text=chunk,
                embedding=embedding,
                content_type=doc["content_type"],
                crop=doc["crop"],
                distinguishing_cues=doc.get("distinguishing_cues"),
            )
            total_chunks += 1

    await repo.commit()
    logger.info("Ingested %d chunks from %d documents.", total_chunks, len(docs))
    return total_chunks


async def main() -> None:
    """Entrypoint for ``python -m app.services.rag.ingest``.

    Uses the real embedding adapter selected by config (falls back to the
    stub — see ``adapters/dependencies.py``) and a real DB session.
    """
    from app.adapters.dependencies import get_embedding_adapter

    logging.basicConfig(level=logging.INFO)
    embedding_port = get_embedding_adapter()

    async with AsyncSessionLocal() as session:
        repo = KnowledgeChunkRepository(session)
        count = await ingest_corpus(repo, embedding_port)
        print(f"Ingested {count} chunks from {len(CORPUS_DOCS)} documents into knowledge_chunks.")


if __name__ == "__main__":
    asyncio.run(main())
