"""
Inspection of the remaining 21 sub-optimal cases
"""
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

sys.stdout.reconfigure(encoding="utf-8")

from rag.api.rag_api import BhoomiRagEngine
from rag.evaluation.evaluate_rag import normalize_id


def inspect_remaining():
    engine = BhoomiRagEngine("v4.2.0-validated")
    golden_file = PROJECT_ROOT / "rag" / "evaluation" / "RAG_GOLDEN_SET_AUDIT.jsonl"
    with open(golden_file, "r", encoding="utf-8") as f:
        cases = [json.loads(line) for line in f if line.strip()]

    for idx, c in enumerate(cases, start=1):
        q = c["query_text"]
        exp_dec = c.get("expected_decision_state")
        acc_ids = [normalize_id(x) for x in c.get("acceptable_evidence_chunk_ids", [])]

        if not acc_ids or exp_dec in ["ASK_CLARIFYING_QUESTION", "SAFETY_INTERVENTION_WARNING", "REJECT_CROP_MISMATCH", "SAFETY_REJECTION_MRL_HAZARD", "ESCALATE_TO_KVK_OFFICER"]:
            continue

        res = engine.process_query(q)
        ev_list = [normalize_id(ev) for ev in res.get("evidence_ids", [])]

        rank = 0
        for r_i, ev in enumerate(ev_list, start=1):
            if any(acc in ev or ev in acc for acc in acc_ids):
                rank = r_i
                break

        if rank != 1:
            print(f"Case {idx:02d} ({c.get('query_id')}): Rank {rank}")
            print(f"  Query: {q}")
            print(f"  Acceptable: {acc_ids}")
            print(f"  Got: {ev_list}")


if __name__ == "__main__":
    inspect_remaining()
