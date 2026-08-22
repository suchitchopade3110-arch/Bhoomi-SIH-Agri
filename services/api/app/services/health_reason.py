"""Health score change reason mapper — explains sub-index deltas in Tamil.

Compares current vs previous HealthSnapshot to identify which sub-index
changed the most and returns a one-sentence Tamil explanation.
"""

from __future__ import annotations

from typing import Any, Optional


# Sub-index key → Tamil reason for drop / rise
_REASONS_DROP: dict[str, str] = {
    "active_problem_load": "ஒரு செயலில் உள்ள நோய்",
    "resource_adequacy": "நீர் பற்றாக்குறை",
    "treatment_response": "சிகிச்சை பலனளிக்கவில்லை",
    "environmental_suitability": "சுற்றுச்சூழல் சாதகமாக இல்லை",
    "crop_stage_progression": "பயிர் வளர்ச்சி பின்தங்கியுள்ளது",
    "monitoring_recency": "சமீபத்திய தரவு இல்லை",
}

_REASONS_RISE: dict[str, str] = {
    "active_problem_load": "நோய் தீர்க்கப்பட்டது",
    "resource_adequacy": "நீர் வழங்கல் மேம்பட்டது",
    "treatment_response": "சிகிச்சை பலனளித்தது",
    "environmental_suitability": "சுற்றுச்சூழல் மேம்பட்டது",
    "crop_stage_progression": "பயிர் வளர்ச்சி இயல்பாக உள்ளது",
    "monitoring_recency": "சமீபத்தில் கண்காணிக்கப்பட்டது",
}


def _extract_subindex_map(snapshot: dict[str, Any]) -> dict[str, float]:
    """Extract a {key: value} map from a snapshot's subindices.

    Supports both formats:
    - JSONB list: [{"key": "...", "value": N}, ...]
    - Flat dict: {"environmental_suitability": N, ...}
    """
    subindices = snapshot.get("subindices", [])

    if isinstance(subindices, list):
        return {
            item.get("key", ""): float(item.get("value", 0) or 0)
            for item in subindices
            if isinstance(item, dict)
        }
    elif isinstance(subindices, dict):
        return {k: float(v or 0) for k, v in subindices.items()}

    return {}


def explain_health_change(
    current: dict[str, Any],
    previous: Optional[dict[str, Any]] = None,
) -> str:
    """Return a one-sentence Tamil explanation of why the score changed.

    Args:
        current: Current HealthSnapshot as dict (with 'subindices').
        previous: Previous HealthSnapshot as dict, or None if first assessment.

    Returns:
        Tamil reason string.
    """
    if previous is None:
        return "முதல் மதிப்பீடு"  # "First assessment"

    curr_map = _extract_subindex_map(current)
    prev_map = _extract_subindex_map(previous)

    if not curr_map or not prev_map:
        return "மதிப்பெண் மாற்றம்"  # "Score changed"

    # Find the sub-index with the largest absolute change
    max_key = ""
    max_delta = 0.0

    for key in curr_map:
        if key in prev_map:
            delta = curr_map[key] - prev_map[key]
            if abs(delta) > abs(max_delta):
                max_delta = delta
                max_key = key

    if not max_key:
        return "மதிப்பெண் மாற்றம்"

    if max_delta < 0:
        return _REASONS_DROP.get(max_key, "மதிப்பெண் குறைந்தது")
    else:
        return _REASONS_RISE.get(max_key, "மதிப்பெண் உயர்ந்தது")
