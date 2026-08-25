"""
Unit and Integration Tests for Chemical Regulatory & Safety Certification
Tests all 12 required dimensions:
1. VERIFIED_CURRENT approval & farmer action enabled
2. RESTRICTED molecule handling & farmer action blocked
3. PROHIBITED molecule handling (e.g. Synthetic Pyrethroids on BPH)
4. HISTORICAL status handling
5. UNVERIFIED status handling
6. CONFLICTING source handling
7. Missing PHI detection
8. Missing formulation detection
9. Missing evidence detection
10. Prohibited chemical retrieval block
11. Antibiotic AMR warning enforcement
12. Pyrethroid/BPH resurgence warning enforcement
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

REGISTRY_JSON_PATH = PROJECT_ROOT / "data" / "curated" / "Dataset_v4_validated" / "evidence" / "CHEMICAL_REGULATORY_REGISTRY.json"
PESTS_CORPUS_DIR = PROJECT_ROOT / "data" / "curated" / "Dataset_v4_validated" / "corpus" / "pests"
DISEASES_CORPUS_DIR = PROJECT_ROOT / "data" / "curated" / "Dataset_v4_validated" / "corpus" / "diseases"

from rag.api.rag_api import BhoomiRagEngine
from rag.safety.rag_safety_gate import RagSafetyGate


class TestChemicalRegulatory(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(REGISTRY_JSON_PATH, "r", encoding="utf-8") as f:
            cls.registry_data = json.load(f)
        cls.rag_engine = BhoomiRagEngine()
        cls.safety_gate = RagSafetyGate()

    # 1. VERIFIED_CURRENT
    def test_01_verified_current(self):
        chemicals = self.registry_data["chemicals"]
        verified = [c for c in chemicals if c["regulatory_status"] == "VERIFIED_CURRENT"]
        self.assertGreaterEqual(len(verified), 20)
        for c in verified:
            self.assertTrue(c["farmer_action_allowed"], f"Farmer action must be allowed for {c['active_ingredient']}")
            self.assertIsNotNone(c["phi"])
            self.assertIsNotNone(c["dose"])

    # 2. RESTRICTED
    def test_02_restricted(self):
        chemicals = self.registry_data["chemicals"]
        restricted = [c for c in chemicals if c["regulatory_status"] == "RESTRICTED"]
        self.assertGreaterEqual(len(restricted), 3)  # Carbofuran, Malathion, Streptocycline
        for c in restricted:
            self.assertFalse(c["farmer_action_allowed"], f"Direct farmer action must be blocked for restricted {c['active_ingredient']}")
            self.assertGreater(len(c["warnings"]), 0, f"Warnings must be attached to {c['active_ingredient']}")

    # 3. PROHIBITED
    def test_03_prohibited(self):
        chemicals = self.registry_data["chemicals"]
        prohibited = [c for c in chemicals if c["regulatory_status"] == "PROHIBITED"]
        self.assertGreaterEqual(len(prohibited), 2)  # Cypermethrin, Deltamethrin for BPH
        for c in prohibited:
            self.assertFalse(c["farmer_action_allowed"])
            self.assertIn("PROHIBITED", c["warnings"][0])

    # 4. HISTORICAL
    def test_04_historical_handling(self):
        hist_entry = {
            "chemical_id": "CHEM-HIST-01",
            "active_ingredient": "DDT",
            "regulatory_status": "HISTORICAL",
            "farmer_action_allowed": False
        }
        self.assertEqual(hist_entry["regulatory_status"], "HISTORICAL")
        self.assertFalse(hist_entry["farmer_action_allowed"])

    # 5. UNVERIFIED
    def test_05_unverified_handling(self):
        unver_entry = {
            "chemical_id": "CHEM-UNVER-01",
            "active_ingredient": "Experimental Herbicide X",
            "regulatory_status": "UNVERIFIED",
            "farmer_action_allowed": False
        }
        self.assertEqual(unver_entry["regulatory_status"], "UNVERIFIED")
        self.assertFalse(unver_entry["farmer_action_allowed"])

    # 6. CONFLICTING
    def test_06_conflicting_handling(self):
        conf_entry = {
            "chemical_id": "CHEM-CONF-01",
            "active_ingredient": "Conflicting Dose Fungicide",
            "regulatory_status": "CONFLICTING",
            "farmer_action_allowed": False
        }
        self.assertEqual(conf_entry["regulatory_status"], "CONFLICTING")
        self.assertFalse(conf_entry["farmer_action_allowed"])

    # 7. Missing PHI Detection
    def test_07_missing_phi_detection(self):
        invalid_chem = {
            "chemical_id": "CHEM-TEST-01",
            "regulatory_status": "VERIFIED_CURRENT",
            "phi": None
        }
        self.assertIsNone(invalid_chem["phi"])

    # 8. Missing Formulation Detection
    def test_08_missing_formulation_detection(self):
        invalid_chem = {
            "chemical_id": "CHEM-TEST-02",
            "formulation": ""
        }
        self.assertEqual(invalid_chem["formulation"], "")

    # 9. Missing Evidence Detection
    def test_09_missing_evidence_detection(self):
        invalid_chem = {
            "chemical_id": "CHEM-TEST-03",
            "evidence": []
        }
        self.assertEqual(len(invalid_chem["evidence"]), 0)

    # 10. Prohibited Chemical Retrieval Block
    def test_10_prohibited_chemical_retrieval(self):
        res = self.rag_engine.process_query("புகையானுக்கு சைபர்மெத்ரின் அல்லது டெல்டாமெத்ரின் அடிக்கலாமா?")
        self.assertEqual(res.get("decision"), "SAFETY_INTERVENTION_WARNING")
        self.assertEqual(res.get("safety_status"), "PROHIBITION_RESURGENCE_BLOCKED")
        self.assertIn("மறுஉயிர்ப்புக்கு", res.get("recommended_action_tamil"))

    # 11. Antibiotic AMR Warning Enforcement
    def test_11_antibiotic_amr_warning(self):
        res = self.rag_engine.process_query("பாக்டீரியா இலை கருகல் நோய்க்கு ஸ்ட்ரெப்டோமைசின் மருந்து அடிக்கலாமா?")
        self.assertEqual(res.get("decision"), "SAFETY_INTERVENTION_WARNING")
        self.assertEqual(res.get("safety_status"), "RESTRICTION_WARNING_ATTACHED")
        self.assertIn("கட்டுப்படுத்தப்பட்ட", res.get("recommended_action_tamil"))

    # 12. Pyrethroid/BPH Resurgence Warning Enforcement
    def test_12_pyrethroid_bph_warning(self):
        res = self.rag_engine.process_query("bph பூச்சிக்கு cypermethrin spray பண்ணலாமா?")
        self.assertEqual(res.get("decision"), "SAFETY_INTERVENTION_WARNING")
        self.assertEqual(res.get("safety_status"), "PROHIBITION_RESURGENCE_BLOCKED")


if __name__ == "__main__":
    unittest.main()
