"""services/rag/pipeline.py — spec-mandated RAG pipeline entry point.

The full grounded-advisory pipeline (PRD §5.7, contract §2.11):
  1. Embed the query via ``EmbeddingPort``
  2. Similarity-search pgvector; apply ``RAG_RELEVANCE_THRESHOLD``
  3. If nothing above threshold → ``{retrieved: False, reason: no_relevant_source}``
  4. Ground the answer through ``LLMPort`` (ONLY from retrieved chunks)
  5. Parse/validate: 5-point schema + ≥1 citation required; reject otherwise
  6. Return ``Advisory`` + ``citations[]``, or escalate

Hard rule (never-fabricate): if retrieval is empty, the function returns the
no-retrieval object before any LLM generation call is made. This is enforced
in code, not in a prompt.

The concrete orchestration lives in ``app.services.rag.advisory_service``
(``AdvisoryService``).  ``pipeline`` is the spec-path re-export of its
``answer_query`` coroutine signature and the ``AdvisoryQueryOutcome`` type,
so Phase 3 and later phases can import via:
    from app.services.rag.pipeline import AdvisoryQueryOutcome, AdvisoryService
"""

from app.services.rag.advisory_service import (  # noqa: F401
    AdvisoryQueryOutcome,
    AdvisoryService,
    get_advisory_service,
)

__all__ = ["AdvisoryService", "AdvisoryQueryOutcome", "get_advisory_service"]
