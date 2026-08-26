"""One-command demo reset script.

Re-seeds the demo database and re-loads the curated RAG corpus that the
rest of this codebase (ingestion, retrieval, the reconciliation e2e test)
actually runs against.

Previously this called ``scripts/load_corpus.py`` (an entirely separate,
SIH25076-era ingestion path reading 8 markdown files from ``corpus/``,
zero pest docs) and ``scripts/seed_demo.py`` + ``scripts/seed_full_demo.py``
(pre-seeding a fake ``82 -> 68 -> 59 -> 86`` snapshot history — the
superseded score walk; the current one, proven live over HTTP in
``tests/e2e/test_runbook.py``, is ``82 -> 73 -> 57 -> 91``). Neither path
was exercised by anything else in the repo, so it silently drifted from
what the app, tests, and every other demo/CI path actually use — and after
``knowledge_chunks`` gained real ``content_type``/``crop`` columns, running
the old path left every chunk with ``content_type=NULL``, invisible to any
disease/pest-scoped retrieval query. A reset via that path meant
``/diagnose`` could never compose a cited advisory again — every diagnosis
above the gate would 404 into "no relevant source" and escalate instead.

Now uses the same two calls ``DEMO_REHEARSAL_RUNBOOK.md``'s own "Quick
Cold-Start Recovery" section documents (corpus ingest + ``scripts.seed``),
just calling the real ingest function directly instead of shelling out.
Seeds only the baseline (farmer/officer/agronomist/farm at health 82,
land unverified) — the demo walkthrough itself, not this script, is what
drives the score through diagnose -> follow-up -> resolve live.

Usage:
    python -m scripts.reset_demo
"""

import asyncio
import logging

from app.adapters.dependencies import get_embedding_adapter
from app.core.db import AsyncSessionLocal
from app.repositories.knowledge_chunk_repository import KnowledgeChunkRepository
from app.services.rag.corpus_data import CORPUS_DOCS
from app.services.rag.ingest import ingest_corpus
from scripts.seed import seed


async def reset() -> None:
    print("==================================================")
    print("  Bhoomi SIH26131 — One-Command Demo Reset")
    print("==================================================")

    print(f"\n1. Ingesting {len(CORPUS_DOCS)} curated corpus documents into pgvector...")
    embedding_port = get_embedding_adapter()
    async with AsyncSessionLocal() as session:
        repo = KnowledgeChunkRepository(session)
        chunk_count = await ingest_corpus(repo, embedding_port)
    print(f"   Ingested {chunk_count} chunks from {len(CORPUS_DOCS)} documents.")

    print("\n2. Seeding demo farmer, officer, agronomist, farm, and schemes...")
    ids = await seed()
    print(f"   {ids}")

    print("\n==================================================")
    print("  Demo Reset Complete — baseline health score is 82.")
    print("  Walk the live demo (diagnose -> follow-up -> resolve) to")
    print("  drive it through 82 -> 73 -> 57 -> 91, same as")
    print("  tests/e2e/test_runbook.py::test_full_runbook_walks_82_73_57_91.")
    print("==================================================")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(reset())
