"""Named constants for the RAG grounding pipeline (PRD §5.7, §5.8)."""

# --------------------------------------------------------------------------
# Chunking (corpus ingestion)
# --------------------------------------------------------------------------
CHUNK_MAX_CHARS = 600
CHUNK_OVERLAP_CHARS = 80

# --------------------------------------------------------------------------
# The fixed 5-point advisory structure (PRD §5.8) — order matters, it's the
# scannable-by-voice structure the farmer hears. ``what_to_avoid`` is first
# and never-cut (SIH26131 feature checklist §4): the harm-prevention point
# must be the one a farmer hears/reads before anything else, ahead of even
# the diagnosis itself.
# --------------------------------------------------------------------------
FIVE_POINT_FIELDS: tuple[str, ...] = (
    "what_to_avoid",
    "possible_issue",
    "what_to_check",
    "what_to_do_next",
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

# ``knowledge_chunks`` carries no ``content_type``/``crop`` column (the
# corpus is single-crop — paddy — for this build, per corpus_data.py's own
# docstring), so target_type-scoped retrieval is done via the existing
# ``doc_id`` prefix convention every pest doc already follows: every pest
# corpus entry is "kb_p3xx" (see services/rag/corpus_data.py's "--- Pest
# entries (kb_p3xx) ---" section); everything else is disease/general.
PEST_DOC_ID_PREFIX = "kb_p"
