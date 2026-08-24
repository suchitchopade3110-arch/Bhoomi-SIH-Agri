"""
BHOOMI Agronomic Evidence Reranker
Reranks hybrid retrieval candidate evidence chunks using source authority weighting,
crop growth stage alignment, symptom overlap, and regulatory constraints.
"""
from typing import Any, Dict, List, Optional


class AgronomicReranker:
    def __init__(self):
        # Base authority multipliers: Level 10 (CIBRC) = 1.0, Level 9 (ICAR) = 0.95, Level 8 (TNAU) = 0.90
        self.authority_weights = {
            10: 1.00,
            9: 0.95,
            8: 0.90,
            7: 0.85,
            6: 0.80,
            3: 0.30
        }

    def rerank(self, query_context: Dict[str, Any], candidates: List[Dict[str, Any]], top_k: int = 5) -> List[Dict[str, Any]]:
        """Reranks candidate evidence objects based on domain authority and contextual fit."""
        if not candidates:
            return []

        target_stage = query_context.get("crop_stage")
        target_intent = query_context.get("requested_action")
        target_symptoms = set(query_context.get("symptoms", []))
        target_chem = query_context.get("chemical")

        scored_candidates = []

        for cand in candidates:
            base_score = cand.get("rrf_score", 0.5)
            meta = cand.get("metadata", {}) or {}
            
            # 1. Authority Weight Multiplier
            auth_level = meta.get("source_authority", 8)
            auth_weight = self.authority_weights.get(auth_level, 0.85)

            # 2. Stage Alignment Bonus
            stage_bonus = 1.0
            cand_stage = meta.get("crop_stage")
            if target_stage and cand_stage:
                if cand_stage == target_stage or cand_stage == "all_stages":
                    stage_bonus = 1.15
                else:
                    stage_bonus = 0.85  # Mild penalty for mismatched stage

            # 3. Intent & Chunk Type Alignment
            intent_bonus = 1.0
            chunk_type = cand.get("chunk_type", "")
            if target_intent == "QUERY_ETL" and chunk_type == "ETL":
                intent_bonus = 1.25
            elif target_intent == "QUERY_DOSAGE" and chunk_type == "CHEMICAL":
                intent_bonus = 1.25
            elif target_intent == "QUERY_REGULATORY_STATUS" and chunk_type == "CHEMICAL":
                intent_bonus = 1.30
            elif target_intent == "DIAGNOSE_SYMPTOM" and chunk_type in ["DIAGNOSTIC", "SEVERITY", "ENTITY", "DECISION_TREE"]:
                intent_bonus = 1.20

            # 4. Chemical Mention Match
            chem_bonus = 1.0
            if target_chem:
                cand_text = cand.get("text", "").lower()
                if target_chem.lower() in cand_text:
                    chem_bonus = 1.30

            final_score = base_score * auth_weight * stage_bonus * intent_bonus * chem_bonus
            
            cand_copy = dict(cand)
            cand_copy["reranked_score"] = round(final_score, 4)
            cand_copy["authority_weight"] = auth_weight
            scored_candidates.append(cand_copy)

        # Sort descending by reranked score
        scored_candidates.sort(key=lambda x: x["reranked_score"], reverse=True)
        return scored_candidates[:top_k]
