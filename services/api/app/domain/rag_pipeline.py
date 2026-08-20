"""Pure domain logic for RAG grounding, citation verification, and relevance gating.
Enforces the hard rule: If corpus has nothing relevant, state limits and escalate.
"""

from typing import Any
from app.schemas.advisory import Advisory, Citation


def verify_grounded_citations(
    generated_text: str,
    retrieved_chunks: list[dict[str, Any]],
    relevance_threshold: float = 0.35,
) -> list[Citation]:
    """Verify that every factual claim links to a retrieved chunk with sufficient relevance.

    Args:
        generated_text: Generated advice text.
        retrieved_chunks: Candidate passages from vector search.
        relevance_threshold: Minimum cosine similarity score.

    Returns:
        List of validated Citation objects.

    Raises:
        NotImplementedError: Stubbed for Phase 0.
    """
    raise NotImplementedError("Domain RAG citation verification will be implemented in subsequent phases.")


def format_5point_advisory(
    raw_response: dict[str, Any],
    citations: list[Citation],
    farm_id: str,
) -> Advisory:
    """Format validated output into structured 5-point advisory.

    Args:
        raw_response: Dictionary containing 5-point fields.
        citations: Grounded citations list.
        farm_id: Target farm UUID.

    Returns:
        Structured Advisory object.

    Raises:
        NotImplementedError: Stubbed for Phase 0.
    """
    raise NotImplementedError("Domain 5-point advisory formatting will be implemented in subsequent phases.")
