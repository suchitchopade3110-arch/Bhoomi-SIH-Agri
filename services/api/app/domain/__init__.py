"""Domain logic modules for Bhoomi."""

from app.domain.escalation import build_case_summary, promote_severity, should_auto_escalate
from app.domain.fao56 import calculate_fao56_irrigation
from app.domain.gate import decide as decide_gate
from app.domain.health import compute_health
from app.domain.rag import build_grounding_prompt, chunk_text, parse_advisory_output

__all__ = [
    "compute_health",
    "decide_gate",
    "parse_advisory_output",
    "build_grounding_prompt",
    "chunk_text",
    "build_case_summary",
    "promote_severity",
    "should_auto_escalate",
    "calculate_fao56_irrigation",
]
