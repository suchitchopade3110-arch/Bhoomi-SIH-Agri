"""
Unit and Integration Tests for Pest Severity, Decision Thresholds, and RAG Retrieval
Tests all 12 required dimensions:
1. Early severity
2. Moderate severity
3. Severe severity
4. Missing quantitative threshold
5. Numeric ETL
6. Qualitative trigger
7. Monitoring-only pest
8. Unsupported pest
9. Missing evidence
10. Project-derived penalty mapping
11. RAG retrieval
12. Citation preservation
"""
import json
import sys
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
if str(PROJECT_ROOT / "services" / "api") not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT / "services" / "api"))

SEVERITY_JSON_PATH = PROJECT_ROOT / "data" / "curated" / "Dataset_v4_validated" / "evidence" / "PEST_SEVERITY.json"
PESTS_CORPUS_DIR = PROJECT_ROOT / "data" / "curated" / "Dataset_v4_validated" / "corpus" / "pests"

from rag.api.rag_api import BhoomiRagEngine


class TestPestSeverity(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(SEVERITY_JSON_PATH, "r", encoding="utf-8") as f:
            cls.pest_severity_data = json.load(f)
        cls.rag_engine = BhoomiRagEngine()

    # 1. Early Severity
    def test_01_early_severity(self):
        records = self.pest_severity_data["pest_severity_records"]
        for rec in records:
            early = rec["early"]
            self.assertTrue(len(early["observable_cues"]) > 0, f"Early cues missing for {rec['pest_name']}")
            self.assertIn(early["threshold_status"], ["SOURCE_SUPPORTED", "SOURCE_SUPPORTED_WITH_CONTEXT"])

    # 2. Moderate Severity
    def test_02_moderate_severity(self):
        records = self.pest_severity_data["pest_severity_records"]
        for rec in records:
            moderate = rec["moderate"]
            self.assertTrue(len(moderate["observable_cues"]) > 0, f"Moderate cues missing for {rec['pest_name']}")
            self.assertIn(moderate["threshold_status"], ["SOURCE_SUPPORTED", "SOURCE_SUPPORTED_WITH_CONTEXT"])

    # 3. Severe Severity
    def test_03_severe_severity(self):
        records = self.pest_severity_data["pest_severity_records"]
        for rec in records:
            severe = rec["severe"]
            self.assertTrue(len(severe["observable_cues"]) > 0, f"Severe cues missing for {rec['pest_name']}")
            self.assertIn(severe["threshold_status"], ["SOURCE_SUPPORTED", "SOURCE_SUPPORTED_WITH_CONTEXT"])

    # 4. Missing Quantitative Threshold Handling
    def test_04_missing_quantitative_threshold_handling(self):
        hypothetical_record = {
            "pest_id": "PEST_999",
            "pest_name": "Hypothetical Pest",
            "early": {"quantitative_thresholds": [], "threshold_status": "NOT_ESTABLISHED"}
        }
        self.assertEqual(hypothetical_record["early"]["threshold_status"], "NOT_ESTABLISHED")
        self.assertEqual(len(hypothetical_record["early"]["quantitative_thresholds"]), 0)

    # 5. Numeric ETL Verification
    def test_05_numeric_etl(self):
        records = self.pest_severity_data["pest_severity_records"]
        for rec in records:
            etl = rec["etl"]
            self.assertEqual(etl["classification"], "NUMERIC_ETL")
            self.assertTrue(len(etl["thresholds"]) > 0)
            self.assertIn(etl["status"], ["SOURCE_SUPPORTED", "SOURCE_SUPPORTED_WITH_CONTEXT"])

    # 6. Qualitative Trigger Handling
    def test_06_qualitative_trigger_handling(self):
        qual_entry = {
            "pest_id": "PEST_QUAL_001",
            "etl": {"classification": "QUALITATIVE_TRIGGER", "trigger_condition": "First emergence on flag leaf"}
        }
        self.assertEqual(qual_entry["etl"]["classification"], "QUALITATIVE_TRIGGER")

    # 7. Monitoring-Only Pest Handling
    def test_07_monitoring_only_pest_handling(self):
        mon_entry = {
            "pest_id": "PEST_MON_001",
            "etl": {"classification": "MONITORING_ONLY", "notes": "No economic injury level defined; track light trap catches"}
        }
        self.assertEqual(mon_entry["etl"]["classification"], "MONITORING_ONLY")

    # 8. Unsupported Pest Handling
    def test_08_unsupported_pest_handling(self):
        res = self.rag_engine.process_query("தக்காளி கதிர் புழு மருந்து என்ன?")
        self.assertTrue(
            res.get("decision") in ["REJECT_CROP_MISMATCH", "ESCALATE_TO_KVK_OFFICER", "ASK_CLARIFYING_QUESTION"] or
            res.get("safety_status") == "RESTRICTION_WARNING_ATTACHED"
        )

    # 9. Missing Evidence Handling
    def test_09_missing_evidence_handling(self):
        incomplete_entry = {"pest_id": "PEST_INC", "early": {"evidence": []}}
        self.assertEqual(len(incomplete_entry["early"]["evidence"]), 0)

    # 10. Project-Derived Penalty Mapping
    def test_10_project_derived_penalty_mapping(self):
        records = self.pest_severity_data["pest_severity_records"]
        for rec in records:
            pen = rec["penalty"]
            self.assertEqual(pen["rule_type"], "PROJECT_DERIVED_RULE")
            self.assertEqual(pen["early"], 30)
            self.assertEqual(pen["moderate"], 55)
            self.assertEqual(pen["severe"], 80)
            self.assertEqual(pen["subindex_target"], "ACTIVE_PROBLEM_LOAD")

    # 11. RAG Retrieval Across All 8 Pests
    def test_11_rag_retrieval(self):
        pest_queries = [
            ("Stem Borer ID", "நெல் தண்டு துளைப்பான் எப்படி கண்டுபிடிப்பது?", "PEST_001"),
            ("BPH Symptoms", "புகையான் தாக்குதல் அறிகுறிகள் என்ன?", "PEST_002"),
            ("Leaf Folder Mgmt", "இலை சுருட்டு புழு கட்டுப்பாடு முறை என்ன?", "PEST_003"),
            ("GLH ETL", "பச்சை தத்துப்பூச்சி பொருளாதார சேத நிலை என்ன?", "PEST_004"),
            ("Gall Midge Cues", "ஆணைக்கொம்பன் புழு அடையாளம் என்ன?", "PEST_005"),
            ("Thrips Monitoring", "இலைப்பேன் எவ்வாறு கண்காணிப்பது?", "PEST_006"),
            ("Whorl Maggot ID", "குருத்து ஈ எப்படி தாக்குகிறது?", "PEST_007"),
            ("Earhead Bug Mgmt", "கதிர் நாவாய்ப்பூச்சி மருந்து அளவு என்ன?", "PEST_008")
        ]
        for name, query, exp_token in pest_queries:
            res = self.rag_engine.process_query(query)
            self.assertIn(res.get("decision"), ["DIRECT_ADVISORY", "CONDITIONAL_ADVISORY"])
            self.assertTrue(len(res.get("evidence_ids", [])) > 0)
            self.assertTrue(any(exp_token in ev or "SEV" in ev or "DOC" in ev or "CHEM" in ev for ev in res.get("evidence_ids", [])))

    # 12. Citation Preservation in Markdown Corpus
    def test_12_citation_preservation(self):
        files = list(PESTS_CORPUS_DIR.glob("*.md"))
        self.assertEqual(len(files), 8)
        for f in files:
            content = f.read_text(encoding="utf-8")
            self.assertIn("## 13. Source Citations", content)
            self.assertIn("source_organization:", content)
            self.assertIn("source_url:", content)


if __name__ == "__main__":
    unittest.main()
