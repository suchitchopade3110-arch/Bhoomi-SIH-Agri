"""
Detailed inspection script for 28 rank != 1 cases
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


def inspect():
    engine = BhoomiRagEngine("v4.2.0-validated")
    golden_file = PROJECT_ROOT / "rag" / "evaluation" / "RAG_GOLDEN_SET.jsonl"
    with open(golden_file, "r", encoding="utf-8") as f:
        cases = [json.loads(line) for line in f if line.strip()]

    for idx, c in enumerate(cases, start=1):
        q = c["query"]
        exp_ent_id = normalize_id(c.get("expected_entity_id"))
        exp_doc_id = normalize_id(c.get("expected_doc_id"))
        exp_ev_id = normalize_id(c.get("expected_evidence_id"))
        exp_dec = c.get("expected_decision")

        if exp_dec in ["ASK_CLARIFYING_QUESTION", "SAFETY_INTERVENTION_WARNING", "REJECT_CROP_MISMATCH", "SAFETY_REJECTION_MRL_HAZARD", "ESCALATE_TO_KVK_OFFICER"]:
            continue

        res = engine.process_query(q)
        ev_list = [normalize_id(ev) for ev in res.get("evidence_ids", [])]

        rank = 0
        for r_i, ev in enumerate(ev_list, start=1):
            if (exp_ev_id and (exp_ev_id in ev or ev in exp_ev_id)) or \
               (exp_doc_id and (exp_doc_id in ev or ev in exp_doc_id)) or \
               (exp_ent_id and (exp_ent_id in ev or ev in exp_ent_id)):
                rank = r_i
                break

        if rank != 1:
            print(f"Case {idx:02d} ({c.get('test_id')}): Rank {rank}")
            print(f"  Query: {q}")
            print(f"  Expected: ev={exp_ev_id}, doc={exp_doc_id}, ent={exp_ent_id}")
            print(f"  Got: {ev_list}")


if __name__ == "__main__":
    inspect()
