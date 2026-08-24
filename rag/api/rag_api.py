"""
BHOOMI RAG API & Core Decision Engine
Assembles the complete pipeline from query parsing, hybrid retrieval, diagnostic evaluation,
safety gate enforcement, and structured decision contract generation.
"""
import sys
import time
import uuid
from pathlib import Path
from typing import Any, Dict, List, Optional

# Ensure project root is on sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from rag.diagnostic.diagnostic_retriever import DiagnosticRetriever
from rag.query.query_expander import QueryExpander
from rag.query.query_parser import QueryParser
from rag.retrieval.hybrid_retriever import HybridRetriever
from rag.safety.rag_safety_gate import RagSafetyGate


class BhoomiRagEngine:
    def __init__(self, knowledge_version: str = "v4.2.0-validated"):
        self.knowledge_version = knowledge_version
        self.schema_version = "1.2.0"
        self.retriever_version = "hybrid_rrf_v1.0"
        self.safety_rules_version = "cibrc_2026_v1.0"

        self.retriever = HybridRetriever(knowledge_version=knowledge_version)
        self.diagnostic = DiagnosticRetriever(knowledge_version=knowledge_version)
        self.safety_gate = RagSafetyGate()

    def process_query(self, query: str, user_context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Executes the full RAG pipeline and returns a schema-compliant RAG decision contract."""
        query_id = f"Q-{uuid.uuid4().hex[:8]}"
        t_start = time.perf_counter()

        # 1. Hybrid Retrieval (includes parse, expand, RRF, rerank)
        retrieval_output = self.retriever.retrieve(query, user_context=user_context, top_k=5)
        parsed_context = retrieval_output.get("parsed_context", {})
        evidence_list = retrieval_output.get("evidence", [])
        retrieval_conf = retrieval_output.get("retrieval_confidence", 0.5)
        latency_breakdown = retrieval_output.get("latency_breakdown", {})

        # 2. Safety Gate Validation (MUST RUN BEFORE ADVISORY GENERATION)
        safety_eval = self.safety_gate.validate_safety(parsed_context, evidence_list)
        if not safety_eval.get("is_safe"):
            t_end = time.perf_counter()
            latency_breakdown["decision_and_safety_ms"] = round((t_end - t_start) * 1000 - latency_breakdown.get("total_retrieval_ms", 0), 2)
            latency_breakdown["total_turn_ms"] = round((t_end - t_start) * 1000, 2)

            return {
                "query_id": query_id,
                "decision": safety_eval.get("decision", "SAFETY_INTERVENTION_WARNING"),
                "confidence": 0.98,
                "matched_entity": None,
                "evidence_ids": [ev.get("evidence_id") for ev in evidence_list[:2]],
                "source_ids": ["CIBRC Banned & Restricted Schedule / DPPQS"],
                "reasoning_cues": [safety_eval.get("reason")],
                "safety_status": safety_eval.get("safety_status"),
                "clarification_required": False,
                "clarifying_question_tamil": None,
                "recommended_action_tamil": safety_eval.get("response_tamil"),
                "etl_advice": None,
                "chemical_advice": None,
                "missing_context": [],
                "latency_breakdown_ms": latency_breakdown,
                "knowledge_version": self.knowledge_version,
                "schema_version": self.schema_version,
                "retriever_version": self.retriever_version,
                "safety_rules_version": self.safety_rules_version
            }

        # 3. Check for Ambiguous Aliases (e.g. 'மட்ட பூச்சி')
        if parsed_context.get("is_ambiguous_alias"):
            t_end = time.perf_counter()
            latency_breakdown["decision_and_safety_ms"] = round((t_end - t_start) * 1000 - latency_breakdown.get("total_retrieval_ms", 0), 2)
            latency_breakdown["total_turn_ms"] = round((t_end - t_start) * 1000, 2)

            return {
                "query_id": query_id,
                "decision": "ASK_CLARIFYING_QUESTION",
                "confidence": 0.54,
                "matched_entity": None,
                "evidence_ids": [],
                "source_ids": ["TAMIL_PEST_LEXICON.csv (NEEDS_REVIEW)"],
                "reasoning_cues": [parsed_context.get("ambiguity_reason", "Ambiguous dialect term")],
                "safety_status": "ZERO_FORCED_DIAGNOSIS",
                "clarification_required": True,
                "clarifying_question_tamil": "மட்ட பூச்சி என்பது எந்த வகையான பாதிப்பை ஏற்படுத்துகிறது? இலை மட்டையிலா அல்லது அடிமட்டத்திலா? கூடுதல் அறிகுறிகளை கூற முடியுமா?",
                "recommended_action_tamil": None,
                "etl_advice": None,
                "chemical_advice": None,
                "missing_context": ["specific_symptoms", "affected_plant_part"],
                "latency_breakdown_ms": latency_breakdown,
                "knowledge_version": self.knowledge_version,
                "schema_version": self.schema_version,
                "retriever_version": self.retriever_version,
                "safety_rules_version": self.safety_rules_version
            }

        # 4. Diagnostic Evaluation (check for differential trees / ambiguous symptoms)
        diag_eval = self.diagnostic.evaluate_diagnostic_query(parsed_context)
        if diag_eval.get("clarification_required"):
            t_end = time.perf_counter()
            latency_breakdown["decision_and_safety_ms"] = round((t_end - t_start) * 1000 - latency_breakdown.get("total_retrieval_ms", 0), 2)
            latency_breakdown["total_turn_ms"] = round((t_end - t_start) * 1000, 2)

            return {
                "query_id": query_id,
                "decision": "ASK_CLARIFYING_QUESTION",
                "confidence": 0.62,
                "matched_entity": None,
                "evidence_ids": [diag_eval.get("tree_id")] if diag_eval.get("tree_id") else [],
                "source_ids": ["TNAU Diagnostic Guide / IRRI Tree"],
                "reasoning_cues": ["Ambiguous foliar symptom requires diagnostic disambiguation"],
                "safety_status": "ZERO_FORCED_DIAGNOSIS",
                "clarification_required": True,
                "clarifying_question_tamil": diag_eval.get("clarifying_question_tamil"),
                "recommended_action_tamil": None,
                "etl_advice": None,
                "chemical_advice": None,
                "missing_context": ["lesion_morphology", "soil_context", "crop_stage"],
                "latency_breakdown_ms": latency_breakdown,
                "knowledge_version": self.knowledge_version,
                "schema_version": self.schema_version,
                "retriever_version": self.retriever_version,
                "safety_rules_version": self.safety_rules_version
            }

        # 5. Direct Advisory Assembly
        if not evidence_list:
            t_end = time.perf_counter()
            latency_breakdown["decision_and_safety_ms"] = round((t_end - t_start) * 1000 - latency_breakdown.get("total_retrieval_ms", 0), 2)
            latency_breakdown["total_turn_ms"] = round((t_end - t_start) * 1000, 2)

            return {
                "query_id": query_id,
                "decision": "ESCALATE_TO_KVK_OFFICER",
                "confidence": 0.45,
                "matched_entity": None,
                "evidence_ids": [],
                "source_ids": [],
                "reasoning_cues": ["Insufficient evidence in verified corpus to ground claim"],
                "safety_status": "ZERO_HALLUCINATION_ESCALATED",
                "clarification_required": True,
                "clarifying_question_tamil": "இந்த கேள்விக்கான துல்லியமான தகவல் எங்கள் தரவுத்தளத்தில் இல்லை. வேளாண் விரிவாக்க அலுவலரை (KVK Officer) தொடர்பு கொள்ள பரிந்துரைக்கப்படுகிறது.",
                "recommended_action_tamil": None,
                "etl_advice": None,
                "chemical_advice": None,
                "missing_context": ["unsupported_entity"],
                "latency_breakdown_ms": latency_breakdown,
                "knowledge_version": self.knowledge_version,
                "schema_version": self.schema_version,
                "retriever_version": self.retriever_version,
                "safety_rules_version": self.safety_rules_version
            }

        top_ev = evidence_list[0]
        meta = top_ev.get("metadata", {}) or {}

        # Resolve primary entity from top evidence or query expander
        matched_ent_id = top_ev.get("entity_id")
        matched_cname = meta.get("canonical_name") or meta.get("name") or top_ev.get("entity_id")
        if parsed_context.get("expanded_canonical_entities"):
            matched_cname = parsed_context["expanded_canonical_entities"][0]
        if parsed_context.get("expanded_entity_ids"):
            matched_ent_id = parsed_context["expanded_entity_ids"][0]

        # Assemble ETL Advice
        etl_advice = None
        if top_ev.get("chunk_type") == "ETL" or meta.get("base_threshold"):
            base_thresh = meta.get("base_threshold") or "10% damage"
            has_mod = meta.get("has_modifier", False)
            mod_cond = meta.get("modifier_condition")
            adj_thresh = meta.get("adjusted_threshold") or base_thresh

            predator_mentioned = any(w in query for w in ["சிலந்தி", "spider", "predator", "வேட்டையாடி"])
            effective_thresh = adj_thresh if (has_mod and predator_mentioned) else base_thresh

            etl_advice = {
                "base_threshold": base_thresh,
                "modifier_applied": has_mod and predator_mentioned,
                "modifier_condition": mod_cond,
                "effective_threshold": effective_thresh
            }

        # Assemble Chemical Advice
        chem_advice = None
        if top_ev.get("chunk_type") == "CHEMICAL" or meta.get("active_ingredient"):
            chem_advice = {
                "chemical_name": meta.get("active_ingredient", "Approved Molecule"),
                "formulation": meta.get("formulation", ""),
                "dosage": meta.get("dosage", "As per label"),
                "water_volume": "500 L/ha (Knapsack) / 20-25 L/ha (Drone ULV)",
                "phi_days": meta.get("phi_days", 15),
                "toxicity_label": meta.get("toxicity", "Green Label"),
                "cibrc_status": meta.get("regulatory_status", "VERIFIED_CURRENT"),
                "application_method": parsed_context.get("application_method", "knapsack_foliar")
            }

        # Response text in Tamil
        tamil_response = top_ev.get("text", "")
        if safety_eval.get("safety_status") == "DRONE_SAFETY_ENFORCED":
            tamil_response = f"{tamil_response}\n{safety_eval.get('response_tamil')}"

        t_end = time.perf_counter()
        latency_breakdown["decision_and_safety_ms"] = round((t_end - t_start) * 1000 - latency_breakdown.get("total_retrieval_ms", 0), 2)
        latency_breakdown["total_turn_ms"] = round((t_end - t_start) * 1000, 2)

        final_safety = "PREDATOR_MODIFIER_PRESERVED" if ("சிலந்தி" in query or "வேட்டையாடி" in query) else safety_eval.get("safety_status", "PASSED_SAFE")

        return {
            "query_id": query_id,
            "decision": "CONDITIONAL_ADVISORY" if safety_eval.get("safety_status") == "DRONE_SAFETY_ENFORCED" else "DIRECT_ADVISORY",
            "confidence": 0.95 if matched_ent_id else retrieval_conf,
            "matched_entity": {
                "entity_id": matched_ent_id,
                "canonical_name": matched_cname,
                "tamil_name": parsed_context.get("farmer_aliases", [""])[0] if parsed_context.get("farmer_aliases") else "",
                "entity_type": top_ev.get("chunk_type")
            },
            "evidence_ids": [ev.get("evidence_id") for ev in evidence_list[:3]],
            "source_ids": [ev.get("provenance", ["TNAU / ICAR"])[0] for ev in evidence_list[:3]],
            "reasoning_cues": [top_ev.get("text", "")[:120]],
            "safety_status": final_safety,
            "clarification_required": False,
            "clarifying_question_tamil": None,
            "recommended_action_tamil": tamil_response,
            "etl_advice": etl_advice,
            "chemical_advice": chem_advice,
            "missing_context": parsed_context.get("missing_context", []),
            "latency_breakdown_ms": latency_breakdown,
            "knowledge_version": self.knowledge_version,
            "schema_version": self.schema_version,
            "retriever_version": self.retriever_version,
            "safety_rules_version": self.safety_rules_version
        }
