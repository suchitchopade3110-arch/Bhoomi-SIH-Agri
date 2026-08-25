"""Target-type scoping helper for RAG retrieval (PRD §5.7, SIH26131 delta spec §3.1).

Namespaces doc_id matching across the corpus:
- ``target_type="pest"`` -> matches ``kb_p%`` prefix
- ``target_type="disease"`` -> matches ``kb_d%`` prefix (and excludes ``kb_p%``)
- ``target_type=None`` -> unrestricted (searches whole corpus)
"""

from __future__ import annotations

from app.domain.rag.constants import DISEASE_DOC_ID_PREFIX, PEST_DOC_ID_PREFIX


def get_target_type_prefix(target_type: str | None) -> str | None:
    """Return the expected doc_id prefix for a given target_type."""
    if target_type == "pest":
        return PEST_DOC_ID_PREFIX
    if target_type == "disease":
        return DISEASE_DOC_ID_PREFIX
    return None
