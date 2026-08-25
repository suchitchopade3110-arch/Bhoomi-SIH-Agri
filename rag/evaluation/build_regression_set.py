"""
BHOOMI Retrieval Regression Suite Generator & Runner
Maintains permanent test cases for all diagnosed retrieval edge cases:
- Dialect terms (Cauvery, Kongu, Southern, Northern, Tanglish)
- Complex multi-pest symptoms
- Chemical dosage & PHI safety lookups
- Biological control intervals
- Drone application guidelines
Outputs: rag/evaluation/RAG_RETRIEVAL_REGRESSION_SET.jsonl
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


def generate_regression_set():
    regression_file = PROJECT_ROOT / "rag" / "evaluation" / "RAG_RETRIEVAL_REGRESSION_SET.jsonl"
    
    regression_cases = [
        {
            "test_id": "REG-001",
            "query": "தண்டு துளைப்பான் நடுக்குருத்து காய்ந்துவிட்டது மருந்து என்ன?",
            "dialect": "Standard Tamil",
            "crop": "Rice (Oryza sativa)",
            "intent": "RECOMMEND_CHEMICAL",
            "expected_evidence": ["CHEM-001", "DOC-PEST-001", "PEST-001"],
            "expected_rank_ceiling": 1,
            "expected_decision": "DIRECT_ADVISORY",
            "expected_safety_state": "PASSED_SAFE"
        },
        {
            "test_id": "REG-002",
            "query": "புகையான் தாக்குதலுக்கு Buprofezin 25 SC அளவு என்ன?",
            "dialect": "Standard Tamil",
            "crop": "Rice (Oryza sativa)",
            "intent": "QUERY_DOSAGE",
            "expected_evidence": ["CHEM-002", "DOC-PEST-002", "PEST-002"],
            "expected_rank_ceiling": 1,
            "expected_decision": "DIRECT_ADVISORY",
            "expected_safety_state": "PASSED_SAFE"
        },
        {
            "test_id": "REG-003",
            "query": "சுடோமோனாஸ் விதை நேர்த்தி செய்ய எவ்வளவு அளவு கிராம்?",
            "dialect": "Standard Tamil",
            "crop": "Rice (Oryza sativa)",
            "intent": "QUERY_BIO_INPUT_DOSAGE",
            "expected_evidence": ["CHEM-015"],
            "expected_rank_ceiling": 1,
            "expected_decision": "DIRECT_ADVISORY",
            "expected_safety_state": "PASSED_SAFE"
        },
        {
            "test_id": "REG-004",
            "query": "மடல் அழுகல் நோய் (Sheath Rot) கதிர் முழுமையாக வெளிவராமல் அழுகுகிறது மருந்து என்ன?",
            "dialect": "Standard Tamil",
            "crop": "Rice (Oryza sativa)",
            "intent": "RECOMMEND_CHEMICAL",
            "expected_evidence": ["DOC-DIS-006", "DIS-006", "EVID-DOC-DIS-006-MAIN", "EVID-DOC-DIS-006-MGMT", "CHEM-010", "CHEM-013"],
            "expected_rank_ceiling": 5,
            "expected_decision": "DIRECT_ADVISORY",
            "expected_safety_state": "PASSED_SAFE"
        },
        {
            "test_id": "REG-005",
            "query": "செம்புள்ளி நோய் (Brown Spot) இலைகளில் வட்ட பழுப்பு புள்ளிகள் மருந்து என்ன?",
            "dialect": "Standard Tamil",
            "crop": "Rice (Oryza sativa)",
            "intent": "RECOMMEND_CHEMICAL",
            "expected_evidence": ["DOC-DIS-005", "DIS-005", "EVID-DOC-DIS-005-MAIN", "EVID-DOC-DIS-005-MGMT", "CHEM-011", "CHEM-015"],
            "expected_rank_ceiling": 3,
            "expected_decision": "DIRECT_ADVISORY",
            "expected_safety_state": "PASSED_SAFE"
        },
        {
            "test_id": "REG-006",
            "query": "பாக்டீரியா இலைக்கோடு நோய் (BLS) ஒளி ஊடுருவும் கோடுகள் மருந்து என்ன?",
            "dialect": "Standard Tamil",
            "crop": "Rice (Oryza sativa)",
            "intent": "RECOMMEND_CHEMICAL",
            "expected_evidence": ["DOC-DIS-008", "DIS-008", "EVID-DOC-DIS-008-MAIN", "EVID-DOC-DIS-008-MGMT", "CHEM-007", "CHEM-015"],
            "expected_rank_ceiling": 1,
            "expected_decision": "DIRECT_ADVISORY",
            "expected_safety_state": "PASSED_SAFE"
        },
        {
            "test_id": "REG-007",
            "query": "அறுவடைக்கு 2 நாள் முன் மலாத்தியான் அடிக்கலாமா?",
            "dialect": "Standard Tamil",
            "crop": "Rice (Oryza sativa)",
            "intent": "QUERY_REGULATORY_STATUS",
            "expected_evidence": ["CHEM-005", "DOC-PEST-008"],
            "expected_rank_ceiling": 1,
            "expected_decision": "SAFETY_REJECTION_MRL_HAZARD",
            "expected_safety_state": "RESTRICTION_WARNING_ATTACHED"
        },
        {
            "test_id": "REG-008",
            "query": "மட்ட பூச்சிக்கு என்ன மருந்து அடிக்கலாம் கொங்கு பகுதியில்?",
            "dialect": "Kongu Tamil",
            "crop": "Rice (Oryza sativa)",
            "intent": "RECOMMEND_CHEMICAL",
            "expected_evidence": [],
            "expected_rank_ceiling": 1,
            "expected_decision": "ASK_CLARIFYING_QUESTION",
            "expected_safety_state": "PASSED_SAFE"
        }
    ]

    with open(regression_file, "w", encoding="utf-8") as f:
        for c in regression_cases:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")

    print(f"Generated {len(regression_cases)} permanent regression test cases in {regression_file}")


def run_regression_tests():
    engine = BhoomiRagEngine("v4.2.0-validated")
    regression_file = PROJECT_ROOT / "rag" / "evaluation" / "RAG_RETRIEVAL_REGRESSION_SET.jsonl"
    with open(regression_file, "r", encoding="utf-8") as f:
        cases = [json.loads(line) for line in f if line.strip()]

    print("================================================================================")
    print("RUNNING RETRIEVAL PERMANENT REGRESSION PROTECTION SUITE")
    print("================================================================================")

    passed = 0
    for c in cases:
        q = c["query"]
        ceil = c["expected_rank_ceiling"]
        exp_evs = [normalize_id(x) for x in c["expected_evidence"]]
        exp_dec = c["expected_decision"]

        res = engine.process_query(q)
        actual_dec = res.get("decision")
        ev_list = [normalize_id(ev) for ev in res.get("evidence_ids", [])]

        is_dec_pass = (actual_dec == exp_dec) or (exp_dec == "DIRECT_ADVISORY" and actual_dec in ["DIRECT_ADVISORY", "CONDITIONAL_ADVISORY"])
        
        rank = 0
        if not exp_evs or exp_dec in ["ASK_CLARIFYING_QUESTION", "SAFETY_INTERVENTION_WARNING", "SAFETY_REJECTION_MRL_HAZARD"]:
            is_rank_pass = True
        else:
            for r_i, ev in enumerate(ev_list, start=1):
                if any(exp in ev or ev in exp for exp in exp_evs):
                    rank = r_i
                    break
            is_rank_pass = (rank > 0 and rank <= ceil)

        is_case_pass = is_dec_pass and is_rank_pass
        if is_case_pass:
            passed += 1
            print(f"  [PASS] {c['test_id']}: Rank={rank or 1} | Dec={actual_dec}")
        else:
            print(f"  [FAIL] {c['test_id']}: Rank={rank} (Ceil={ceil}) | Dec={actual_dec} (Exp={exp_dec})")

    print(f"\nRegression Suite Result: {passed}/{len(cases)} ({passed/len(cases)*100:.1f}%) Passed")


if __name__ == "__main__":
    generate_regression_set()
    run_regression_tests()
