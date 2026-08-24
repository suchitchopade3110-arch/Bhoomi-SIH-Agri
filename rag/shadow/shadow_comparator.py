"""
BHOOMI Shadow Comparator
Performs granular record-by-record comparison of Production baseline outputs versus
Shadow RAG outputs and flags any semantic or safety discrepancies.
"""
from typing import Any, Dict, List, Tuple


class ShadowComparator:
    def __init__(self):
        pass

    def compare_turn(self, production_turn: Dict[str, Any], shadow_turn: Dict[str, Any]) -> Dict[str, Any]:
        """Compares a single interaction turn between Production and Shadow RAG."""
        prod_dec = production_turn.get("decision")
        shad_dec = shadow_turn.get("decision")

        prod_safety = production_turn.get("safety_status")
        shad_safety = shadow_turn.get("safety_status")

        is_decision_match = (prod_dec == shad_dec) or (prod_dec == "DIRECT_ADVISORY" and shad_dec in ["DIRECT_ADVISORY", "CONDITIONAL_ADVISORY"])
        is_safety_match = (prod_safety == shad_safety) or (prod_safety == "PASSED_SAFE" and shad_safety in ["PASSED_SAFE", "DRONE_SAFETY_ENFORCED"])

        discrepancies = []
        if not is_decision_match:
            discrepancies.append(f"Decision Mismatch: Prod={prod_dec} vs Shadow={shad_dec}")
        if not is_safety_match:
            discrepancies.append(f"Safety Mismatch: Prod={prod_safety} vs Shadow={shad_safety}")

        return {
            "query_id": shadow_turn.get("query_id"),
            "is_concordant": is_decision_match and is_safety_match,
            "discrepancies": discrepancies,
            "latency_delta_ms": shadow_turn.get("latency_breakdown_ms", {}).get("total_turn_ms", 0.0) - production_turn.get("latency_ms", 0.0)
        }
