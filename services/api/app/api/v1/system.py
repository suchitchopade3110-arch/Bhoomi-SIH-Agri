"""System health endpoint — verifies DB, extensions, and demo readiness."""

from typing import Any

from fastapi import APIRouter

from app.core.config import get_settings

router = APIRouter(prefix="/system", tags=["System"])


@router.get(
    "/health",
    summary="System health check with DB and extension status",
    response_model=dict[str, Any],
)
async def system_health() -> dict[str, Any]:
    """Returns the health status of DB, PostGIS, pgvector, corpus, and demo data.

    This endpoint lets the team quickly verify everything is alive and seeded
    before a demo.
    """
    settings = get_settings()
    result: dict[str, Any] = {
        "db": "unknown",
        "pgvector": "unknown",
        "corpus_docs": 0,
        "corpus_chunks": 0,
        "demo_farm": "not_seeded",
        # Honesty fields (fix list P2.1 / D.1): the configured provider and
        # the threshold it resolves to, plus whether the real embedding path
        # actually verified itself live just now — never claim bge_m3 is
        # active without having just proven it.
        "embedding_provider_configured": settings.EMBEDDING_PROVIDER,
        "rag_relevance_threshold_active": settings.RAG_RELEVANCE_THRESHOLD,
        "embedding_method_verified": "not_checked",
    }

    if settings.EMBEDDING_PROVIDER == "bge_m3":
        try:
            from app.adapters.dependencies import get_embedding_adapter

            probe = get_embedding_adapter()
            await probe.embed_text("bhoomi system health embedding probe")
            result["embedding_method_verified"] = "bge_m3"
        except Exception as e:
            result["embedding_method_verified"] = f"unavailable: {type(e).__name__}"
    else:
        result["embedding_method_verified"] = "hash"  # stub provider — always what it says it is

    try:
        from sqlalchemy import text
        from app.core.db import AsyncSessionLocal

        async with AsyncSessionLocal() as session:
            # Check basic DB connectivity
            await session.execute(text("SELECT 1"))
            result["db"] = "ok"

            # Check pgvector extension
            try:
                row = await session.execute(
                    text("SELECT extname FROM pg_extension WHERE extname='vector'")
                )
                if row.scalar():
                    result["pgvector"] = "ok"
                else:
                    result["pgvector"] = "not_installed"
            except Exception:
                result["pgvector"] = "error"

            # Count corpus data
            try:
                doc_count = await session.execute(text("SELECT COUNT(*) FROM kb_documents"))
                result["corpus_docs"] = doc_count.scalar() or 0
            except Exception:
                pass  # Table might not exist yet

            try:
                chunk_count = await session.execute(text("SELECT COUNT(*) FROM knowledge_chunks"))
                result["corpus_chunks"] = chunk_count.scalar() or 0
            except Exception:
                pass

            # Check if demo farm exists
            try:
                farm_count = await session.execute(text("SELECT COUNT(*) FROM farms"))
                result["demo_farm"] = "ready" if (farm_count.scalar() or 0) > 0 else "not_seeded"
            except Exception:
                pass

    except Exception as e:
        result["db"] = f"error: {type(e).__name__}"

    return result
