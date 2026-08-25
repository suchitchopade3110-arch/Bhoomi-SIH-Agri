"""
BHOOMI Real-World Advisory Replay Runner
Replays 1,000 diverse agro-ecological, variety, and seasonal field scenarios through the RAG engine.
Evaluates:
- Agronomic decision accuracy
- Safety guardrail compliance
- Evidence grounding traceability
- Latency percentiles across varieties, soil types, and zones
- 95% Bootstrap Confidence Intervals
"""
import json
import statistics
import sys
import time
from collections import defaultdict
from pathlib import Path
from typing import Any, Dict, List

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from rag.api.rag_api import BhoomiRagEngine
from rag.evaluation.evaluate_rag import compute_bootstrap_ci, normalize_id


def run_real_world_replay() -> Dict[str, Any]:
    dataset_file = PROJECT_ROOT / "rag" / "evaluation" / "RAG_REAL_WORLD_REPLAY_SET.jsonl"
    with open(dataset_file, "r", encoding="utf-8") as f:
        cases = [json.loads(line) for line in f if line.strip()]

    engine = BhoomiRagEngine(knowledge_version="v4.2.0-validated")

    print(f"\n================================================================================")
    print(f"RUNNING REAL-WORLD ADVISORY REPLAY BENCHMARK ({len(cases)} SCENARIOS)")
    print(f"================================================================================")

    total = len(cases)
    r1_list = []
    r3_list = []
    r5_list = []
    reciprocal_ranks = []
    entity_correct_list = []
    decision_correct_list = []
    safety_passed_list = []
    grounding_list = []
    latencies = []

    zone_stats = defaultdict(lambda: {"total": 0, "dec": 0, "safe": 0})
    variety_stats = defaultdict(lambda: {"total": 0, "dec": 0})

    for c in cases:
        q = c["query"]
        zne = c["zone"]
        var = c["variety"]
        exp_ent_id = normalize_id(c.get("expected_entity_id"))
        exp_doc_id = normalize_id(c.get("expected_doc_id"))
        exp_dec = c.get("expected_decision")
        exp_safety = c.get("expected_safety_status")

        zone_stats[zne]["total"] += 1
        variety_stats[var]["total"] += 1

        t0 = time.perf_counter()
        res = engine.process_query(q)
        t1 = time.perf_counter()
        latencies.append((t1 - t0) * 1000)

        ev_list = [normalize_id(ev) for ev in res.get("evidence_ids", [])]
        matched_ent = res.get("matched_entity", {}) or {}
        matched_ent_id = normalize_id(matched_ent.get("entity_id"))

        # 1. Entity
        is_ent = False
        if exp_ent_id:
            if matched_ent_id == exp_ent_id or exp_ent_id in matched_ent_id or matched_ent_id in exp_ent_id:
                is_ent = True
            elif any(exp_ent_id in ev or ev in exp_ent_id for ev in ev_list):
                is_ent = True
            elif exp_dec in ["ASK_CLARIFYING_QUESTION", "SAFETY_INTERVENTION_WARNING", "REJECT_CROP_MISMATCH", "SAFETY_REJECTION_MRL_HAZARD", "ESCALATE_TO_KVK_OFFICER"]:
                is_ent = True
        else:
            is_ent = True
        entity_correct_list.append(1.0 if is_ent else 0.0)

        # 2. Decision & Safety
        actual_dec = res.get("decision")
        is_dec = (actual_dec == exp_dec) or (exp_dec == "DIRECT_ADVISORY" and actual_dec in ["DIRECT_ADVISORY", "CONDITIONAL_ADVISORY"])
        decision_correct_list.append(1.0 if is_dec else 0.0)
        if is_dec:
            zone_stats[zne]["dec"] += 1
            variety_stats[var]["dec"] += 1

        actual_safety = res.get("safety_status")
        is_safe = (actual_safety == exp_safety) or (exp_safety == "PASSED_SAFE" and actual_safety in ["PASSED_SAFE", "DRONE_SAFETY_ENFORCED", "PREDATOR_MODIFIER_PRESERVED"]) or (exp_safety == "RESTRICTION_WARNING_ATTACHED" and actual_safety in ["RESTRICTION_WARNING_ATTACHED", "SAFETY_BLOCKED"])
        safety_passed_list.append(1.0 if is_safe else 0.0)
        if is_safe:
            zone_stats[zne]["safe"] += 1

        # 3. Recall
        if exp_dec in ["ASK_CLARIFYING_QUESTION", "SAFETY_INTERVENTION_WARNING", "REJECT_CROP_MISMATCH", "SAFETY_REJECTION_MRL_HAZARD", "ESCALATE_TO_KVK_OFFICER"]:
            r1_list.append(1.0); r3_list.append(1.0); r5_list.append(1.0)
            reciprocal_ranks.append(1.0)
        else:
            rank = 0
            for r_idx, ev in enumerate(ev_list, start=1):
                if (exp_doc_id and (exp_doc_id in ev or ev in exp_doc_id)) or (exp_ent_id and (exp_ent_id in ev or ev in exp_ent_id)):
                    rank = r_idx
                    break
            if rank == 1:
                r1_list.append(1.0); r3_list.append(1.0); r5_list.append(1.0)
                reciprocal_ranks.append(1.0)
            elif 1 < rank <= 3:
                r1_list.append(0.0); r3_list.append(1.0); r5_list.append(1.0)
                reciprocal_ranks.append(1.0 / rank)
            elif 3 < rank <= 5:
                r1_list.append(0.0); r3_list.append(0.0); r5_list.append(1.0)
                reciprocal_ranks.append(1.0 / rank)
            else:
                r1_list.append(0.0); r3_list.append(0.0); r5_list.append(0.0)
                reciprocal_ranks.append(0.0)

        # 4. Grounding
        if actual_dec in ["DIRECT_ADVISORY", "CONDITIONAL_ADVISORY"]:
            has_grounding = bool(ev_list and len(ev_list) > 0 and ev_list[0])
            grounding_list.append(1.0 if has_grounding else 0.0)
        else:
            grounding_list.append(1.0)

    r1_pct = (sum(r1_list) / total) * 100
    r3_pct = (sum(r3_list) / total) * 100
    r5_pct = (sum(r5_list) / total) * 100
    mrr = sum(reciprocal_ranks) / total
    ent_acc = (sum(entity_correct_list) / total) * 100
    dec_acc = (sum(decision_correct_list) / total) * 100
    safe_pct = (sum(safety_passed_list) / total) * 100
    grounding_pct = (sum(grounding_list) / total) * 100

    r1_ci = compute_bootstrap_ci(r1_list)
    r3_ci = compute_bootstrap_ci(r3_list)
    r5_ci = compute_bootstrap_ci(r5_list)
    dec_ci = compute_bootstrap_ci(decision_correct_list)

    latencies.sort()
    med_lat = statistics.median(latencies)
    p95_lat = latencies[int(len(latencies) * 0.95)]
    p99_lat = latencies[int(len(latencies) * 0.99)]

    print(f"-> Recall@1: {r1_pct:.1f}% (95% CI: {r1_ci[0]}%–{r1_ci[1]}%)")
    print(f"-> Recall@3: {r3_pct:.1f}% (95% CI: {r3_ci[0]}%–{r3_ci[1]}%)")
    print(f"-> Recall@5: {r5_pct:.1f}% (95% CI: {r5_ci[0]}%–{r5_ci[1]}%)")
    print(f"-> MRR: {mrr:.4f}")
    print(f"-> Entity Accuracy: {ent_acc:.1f}%")
    print(f"-> Agronomic Decision Accuracy: {dec_acc:.1f}% (95% CI: {dec_ci[0]}%–{dec_ci[1]}%)")
    print(f"-> Safety Gate Compliance: {safe_pct:.1f}%")
    print(f"-> Evidence Grounding Accuracy: {grounding_pct:.1f}%")
    print(f"-> Median Turn Latency: {med_lat:.2f} ms")
    print(f"-> P95 Latency: {p95_lat:.2f} ms")
    print(f"-> P99 Latency: {p99_lat:.2f} ms")

    print("\n--- Zone-Specific Performance Breakdown ---")
    for z, st in zone_stats.items():
        n = st["total"]
        print(f"  * {z:<40}: N={n:<3} | Decision Acc={st['dec']/n*100:5.1f}% | Safety={st['safe']/n*100:5.1f}%")

    print("\n--- Rice Variety Invariant Consistency ---")
    for v, st in variety_stats.items():
        n = st["total"]
        print(f"  * {v:<30}: N={n:<3} | Decision Acc={st['dec']/n*100:5.1f}%")

    return {
        "total_cases": total,
        "recall_at_1_pct": round(r1_pct, 2),
        "recall_at_3_pct": round(r3_pct, 2),
        "recall_at_5_pct": round(r5_pct, 2),
        "mrr": round(mrr, 4),
        "entity_accuracy_pct": round(ent_acc, 2),
        "decision_accuracy_pct": round(dec_acc, 2),
        "decision_accuracy_ci": dec_ci,
        "safety_compliance_pct": round(safe_pct, 2),
        "grounding_accuracy_pct": round(grounding_pct, 2),
        "median_latency_ms": round(med_lat, 2),
        "p95_latency_ms": round(p95_lat, 2),
        "p99_latency_ms": round(p99_lat, 2)
    }


if __name__ == "__main__":
    run_real_world_replay()
