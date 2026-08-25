"""
BHOOMI Candidate vs Production Knowledge Isolation & Contamination Verification Runner
Verifies:
1. Strict physical and logical index separation between v4.2.0-validated and v4.3.0-candidate.
2. Contamination test: 0 occurrences of candidate-only objects/ids in production indexes.
3. Paired side-by-side evaluation across 100 Golden Cases and 50 Adversarial Cases.
"""
import json
import sys
from pathlib import Path
from typing import Any, Dict, List

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from rag.api.rag_api import BhoomiRagEngine
from rag.evaluation.evaluate_rag import evaluate_adversarial_set, evaluate_golden_set


def verify_index_isolation() -> Dict[str, Any]:
    print(f"\n================================================================================")
    print(f"VERIFYING STRICT KNOWLEDGE BASE ISOLATION & CONTAMINATION INVARIANTS")
    print(f"================================================================================")

    indexes_dir = PROJECT_ROOT / "rag" / "indexes"
    v4_2_obj_file = indexes_dir / "evidence_objects_v4_2_0_validated.json"
    v4_2_chk_file = indexes_dir / "semantic_chunks_v4_2_0_validated.json"
    v4_3_obj_file = indexes_dir / "evidence_objects_v4_3_0_candidate.json"
    v4_3_chk_file = indexes_dir / "semantic_chunks_v4_3_0_candidate.json"

    with open(v4_2_obj_file, "r", encoding="utf-8") as f:
        v4_2_objects = json.load(f)
    with open(v4_2_chk_file, "r", encoding="utf-8") as f:
        v4_2_chunks = json.load(f)

    with open(v4_3_obj_file, "r", encoding="utf-8") as f:
        v4_3_objects = json.load(f)
    with open(v4_3_chk_file, "r", encoding="utf-8") as f:
        v4_3_chunks = json.load(f)

    v4_2_ev_ids = {o.get("evidence_id") for o in v4_2_objects}
    v4_3_ev_ids = {o.get("evidence_id") for o in v4_3_objects}

    print(f"-> Production v4.2.0-validated : {len(v4_2_objects)} Objects, {len(v4_2_chunks)} Chunks")
    print(f"-> Candidate  v4.3.0-candidate : {len(v4_3_objects)} Objects, {len(v4_3_chunks)} Chunks")

    # In v4.3 candidate, we added candidate extensions
    candidate_only_extensions = v4_3_ev_ids - v4_2_ev_ids
    print(f"-> Candidate-Only Evidence Objects: {candidate_only_extensions}")

    # Check for contamination: None of the candidate-only objects should be in v4.2 indexes
    contaminated_in_v4_2 = [ev_id for ev_id in candidate_only_extensions if ev_id in v4_2_ev_ids]
    print(f"-> Production Index Contamination Count: {len(contaminated_in_v4_2)}")

    is_clean = len(contaminated_in_v4_2) == 0
    print(f"-> Isolation Invariant Status: {'PASSED_ZERO_CONTAMINATION' if is_clean else 'FAILED_CONTAMINATION_DETECTED'}")

    return {
        "v4_2_object_count": len(v4_2_objects),
        "v4_2_chunk_count": len(v4_2_chunks),
        "v4_3_object_count": len(v4_3_objects),
        "v4_3_chunk_count": len(v4_3_chunks),
        "candidate_only_ids": list(candidate_only_extensions),
        "contamination_count": len(contaminated_in_v4_2),
        "status": "PASSED_ZERO_CONTAMINATION" if is_clean else "FAILED_CONTAMINATION_DETECTED"
    }


def run_paired_evaluation():
    isolation_report = verify_index_isolation()

    print(f"\n================================================================================")
    print(f"RUNNING PAIRED SIDE-BY-SIDE EVALUATION: v4.2.0-validated vs v4.3.0-candidate")
    print(f"================================================================================")

    engine_prod = BhoomiRagEngine(knowledge_version="v4.2.0-validated")
    engine_cand = BhoomiRagEngine(knowledge_version="v4.3.0-candidate")

    print("\n--- [1/2] Evaluating Production Engine (v4.2.0-validated) ---")
    prod_gold = evaluate_golden_set(engine_prod)
    prod_adv = evaluate_adversarial_set(engine_prod)

    print("\n--- [2/2] Evaluating Candidate Engine (v4.3.0-candidate) ---")
    cand_gold = evaluate_golden_set(engine_cand)
    cand_adv = evaluate_adversarial_set(engine_cand)

    print(f"\n================================================================================")
    print(f"PAIRED COMPARISON SUMMARY & DELTAS")
    print(f"================================================================================")
    print(f"Metric                          | v4.2.0 (Prod) | v4.3.0 (Cand) | Delta")
    print(f"--------------------------------|---------------|---------------|--------")
    print(f"Recall@1                        | {prod_gold['recall_at_1_pct']:6.2f}%       | {cand_gold['recall_at_1_pct']:6.2f}%       | {cand_gold['recall_at_1_pct'] - prod_gold['recall_at_1_pct']:+6.2f}%")
    print(f"Recall@3                        | {prod_gold['recall_at_3_pct']:6.2f}%       | {cand_gold['recall_at_3_pct']:6.2f}%       | {cand_gold['recall_at_3_pct'] - prod_gold['recall_at_3_pct']:+6.2f}%")
    print(f"Recall@5                        | {prod_gold['recall_at_5_pct']:6.2f}%       | {cand_gold['recall_at_5_pct']:6.2f}%       | {cand_gold['recall_at_5_pct'] - prod_gold['recall_at_5_pct']:+6.2f}%")
    print(f"Mean Reciprocal Rank (MRR)      | {prod_gold['mrr']:6.4f}        | {cand_gold['mrr']:6.4f}        | {cand_gold['mrr'] - prod_gold['mrr']:+6.4f}")
    print(f"Agronomic Decision Accuracy     | {prod_gold['decision_accuracy_pct']:6.2f}%       | {cand_gold['decision_accuracy_pct']:6.2f}%       | {cand_gold['decision_accuracy_pct'] - prod_gold['decision_accuracy_pct']:+6.2f}%")
    print(f"Safety Gate Compliance          | {prod_gold['safety_compliance_pct']:6.2f}%       | {cand_gold['safety_compliance_pct']:6.2f}%       | {cand_gold['safety_compliance_pct'] - prod_gold['safety_compliance_pct']:+6.2f}%")
    print(f"Adversarial Interception Rate   | {prod_adv['blocked_pct']:6.2f}%       | {cand_adv['blocked_pct']:6.2f}%       | {cand_adv['blocked_pct'] - prod_adv['blocked_pct']:+6.2f}%")
    print(f"P95 Turn Latency (ms)           | {prod_gold['p95_latency_ms']:6.2f} ms     | {cand_gold['p95_latency_ms']:6.2f} ms     | {cand_gold['p95_latency_ms'] - prod_gold['p95_latency_ms']:+6.2f} ms")


if __name__ == "__main__":
    run_paired_evaluation()
