"""Pure domain logic for confidence gate decision boundary.
Enforces the hard rule: Below threshold -> escalate, never guess.
"""

from app.schemas.gate import Decision


def evaluate_confidence_gate(
    confidence_score: float,
    threshold: float = 0.70,
    context_type: str = "diagnosis",
    advisory_id: str | None = None,
    escalation_id: str | None = None,
) -> Decision:
    """Evaluate whether model confidence satisfies the decision gate.

    Args:
        confidence_score: Raw model or retrieval confidence (0.0 - 1.0).
        threshold: Minimum confidence required to answer directly.
        context_type: Type of evaluation ('diagnosis' or 'rag_retrieval').
        advisory_id: Optional ID of advisory if answered.
        escalation_id: Optional ID of escalation if below gate.

    Returns:
        Decision object with outcome (ANSWER | ESCALATE) and rationale.

    Raises:
        NotImplementedError: Stubbed for Phase 0.
    """
    raise NotImplementedError("Domain confidence_gate evaluation will be implemented in subsequent phases.")
