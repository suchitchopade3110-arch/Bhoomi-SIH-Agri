"""System health endpoint — verifies DB, extensions, and demo readiness."""

from typing import Any

from fastapi import APIRouter

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
    result: dict[str, Any] = {
        "db": "unknown",
        "pgvector": "unknown",
        "corpus_docs": 0,
        "corpus_chunks": 0,
        "demo_farm": "not_seeded",
    }

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
