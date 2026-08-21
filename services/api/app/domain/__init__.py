"""Domain logic modules for Bhoomi."""

from app.domain.confidence_gate import evaluate_confidence_gate
from app.domain.escalation import build_case_summary
from app.domain.fao56 import calculate_fao56_irrigation
from app.domain.health import compute_health
from app.domain.rag_pipeline import format_5point_advisory, verify_grounded_citations

__all__ = [
    "compute_health",
    "evaluate_confidence_gate",
    "verify_grounded_citations",
    "format_5point_advisory",
    "build_case_summary",
    "calculate_fao56_irrigation",
]
