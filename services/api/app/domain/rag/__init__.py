"""Grounded, cited 5-point advisory — the pure pieces (PRD §5.7, §5.8).

Chunking, prompt construction, output parsing, and similarity math: all
deterministic, all zero I/O. Retrieval (DB) and generation (LLM call) are
orchestration and live in ``services/rag/``.
"""

from app.domain.rag.advisory import FivePointAdvisory, GroundedCitation, ParsedAdvisoryResult, parse_advisory_output
from app.domain.rag.chunking import chunk_text
from app.domain.rag.prompt import build_grounding_prompt
from app.domain.rag.scoping import get_target_type_prefix
from app.domain.rag.similarity import cosine_similarity

__all__ = [
    "FivePointAdvisory",
    "GroundedCitation",
    "ParsedAdvisoryResult",
    "parse_advisory_output",
    "chunk_text",
    "build_grounding_prompt",
    "cosine_similarity",
    "get_target_type_prefix",
]
