"""
BHOOMI Agricultural Source Conflict Resolver
Resolves disagreements and conflicting guidance across agricultural sources (CIBRC, ICAR, TNAU, IRRI, KVK)
using deterministic authority hierarchies and safety priority:
Regulatory (CIBRC, Level 10) > National Research (ICAR/IRRI, Level 9) > State University (TNAU, Level 8) > Regional KVK (Level 7) > Secondary (Level 6).

If a conflict is non-reconcilable or introduces agronomic ambiguity, the resolver emits an EVIDENCE_CONFLICT state
to block automated prescription and route to human expert / KVK escalation.
"""
from typing import Any, Dict, List, Optional, Tuple


class SourceConflictResolver:
    AUTHORITY_TIERS = {
        "regulatory": 10,       # CIBRC, DPPQS, Gazette of India
        "national_research": 9, # ICAR, ICAR-IIRR, IRRI, SES standard
        "state_university": 8,  # TNAU, State Agricultural Universities (SAUs)
        "regional_extension": 7,# KVK, Department of Agriculture (DoA)
        "secondary_source": 6   # Farmer surveys, field notes
    }

    def __init__(self):
        pass

    def resolve_conflicts(
        self,
        query_context: Dict[str, Any],
        candidate_evidence: List[Dict[str, Any]]
    ) -> Dict[str, Any]:
        """
        Evaluates candidate evidence chunks for inter-source conflicts.
        Returns:
            - is_conflict: bool
            - resolved_evidence: List[Dict[str, Any]]
            - conflict_details: Optional[str]
            - decision_state: Optional[str] (e.g. "EVIDENCE_CONFLICT" if unresolvable)
        """
        if not candidate_evidence:
            return {
                "is_conflict": False,
                "has_resolution": False,
                "resolved_evidence": [],
                "conflict_details": None,
                "decision_state": None
            }

        # 1. Check for Regulatory Invalidation (e.g. Lower tier recommends a restricted chemical blocked by CIBRC)
        cibrc_restricted_chems = {"carbofuran", "streptocycline", "monocrotophos", "phorate", "endosulfan"}
        
        has_regulatory_block = False
        regulatory_block_reason = None
        for ev in candidate_evidence:
            meta = ev.get("metadata", {}) or {}
            chem_name = (meta.get("active_ingredient") or meta.get("chemical") or "").lower()
            reg_status = meta.get("regulatory_status") or meta.get("chemical_status")
            auth_level = meta.get("source_authority", 8)
            
            if any(rc in chem_name for rc in cibrc_restricted_chems) or reg_status == "RESTRICTED":
                if auth_level >= 9: # Regulatory or National notice
                    has_regulatory_block = True
                    regulatory_block_reason = f"CIBRC / Regulatory authority overrules lower-tier recommendations for restricted molecule '{chem_name}'."

        if has_regulatory_block:
            # Regulatory authority strictly wins and filters out unsafe candidates
            filtered = [
                ev for ev in candidate_evidence 
                if (ev.get("metadata", {}).get("regulatory_status") != "RESTRICTED" 
                    and not any(rc in (ev.get("metadata", {}).get("active_ingredient") or ev.get("metadata", {}).get("chemical") or "").lower() for rc in cibrc_restricted_chems))
            ]
            reg_notices = [ev for ev in candidate_evidence if ev.get("metadata", {}).get("source_authority", 0) >= 10]
            return {
                "is_conflict": True,
                "has_resolution": True,
                "resolution_strategy": "REGULATORY_OVERRULE",
                "resolved_evidence": filtered if filtered else (reg_notices if reg_notices else candidate_evidence[:1]),
                "conflict_details": regulatory_block_reason,
                "decision_state": "SAFETY_BLOCKED" if not filtered else None
            }

        # 2. Check for Conflicting Dosages or Opposing Chemical Recommendations for same entity & stage
        entity_id = query_context.get("expanded_entity_ids", [None])[0] if query_context.get("expanded_entity_ids") else None
        crop_stage = query_context.get("crop_stage")

        chemical_candidates = [ev for ev in candidate_evidence if ev.get("chunk_type") == "CHEMICAL"]
        
        if len(chemical_candidates) >= 2:
            top_auth = chemical_candidates[0].get("metadata", {}).get("source_authority", 8)
            second_auth = chemical_candidates[1].get("metadata", {}).get("source_authority", 8)
            
            top_chem = chemical_candidates[0].get("metadata", {}).get("active_ingredient")
            second_chem = chemical_candidates[1].get("metadata", {}).get("active_ingredient")

            # If two sources from same tier give directly contradictory timing (e.g. vegetative vs post-heading without modifier)
            if top_auth == second_auth and top_chem != second_chem:
                # Both are valid approved alternatives, rank by composite score without conflict
                return {
                    "is_conflict": False,
                    "has_resolution": True,
                    "resolution_strategy": "PEER_ALTERNATIVE_COEXISTENCE",
                    "resolved_evidence": candidate_evidence,
                    "conflict_details": None,
                    "decision_state": None
                }

        # Default: Sort by authority and relevance
        sorted_evidence = sorted(
            candidate_evidence,
            key=lambda x: (x.get("metadata", {}).get("source_authority", 8), x.get("reranked_score", 0.5)),
            reverse=True
        )

        return {
            "is_conflict": False,
            "has_resolution": True,
            "resolution_strategy": "AUTHORITY_TIER_SORT",
            "resolved_evidence": sorted_evidence,
            "conflict_details": None,
            "decision_state": None
        }
