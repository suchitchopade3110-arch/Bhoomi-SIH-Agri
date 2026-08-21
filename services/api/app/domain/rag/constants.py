"""Named constants for the RAG grounding pipeline (PRD §5.7, §5.8)."""

# --------------------------------------------------------------------------
# Chunking (corpus ingestion)
# --------------------------------------------------------------------------
CHUNK_MAX_CHARS = 600
CHUNK_OVERLAP_CHARS = 80

# --------------------------------------------------------------------------
# The fixed 5-point advisory structure (PRD §5.8) — order matters, it's the
# scannable-by-voice structure the farmer hears.
# --------------------------------------------------------------------------
FIVE_POINT_FIELDS: tuple[str, ...] = (
    "possible_issue",
    "what_to_check",
    "what_to_do_next",
    "what_to_avoid",
    "expert_triggers",
)

# --------------------------------------------------------------------------
# The stable sentinel key an LLMPort implementation must set to true when the
# retrieved chunks don't support a grounded answer, instead of guessing
# (PRD §5.7's "no-retrieval fallback", tech stack §1.3's confidence gate).
# --------------------------------------------------------------------------
INSUFFICIENT_CONTEXT_KEY = "insufficient_context"

REQUIRED_CITATION_FIELDS: tuple[str, ...] = ("doc_id", "title", "reviewed_on")

# --------------------------------------------------------------------------
# Retrieval
# --------------------------------------------------------------------------
DEFAULT_TOP_K = 5
