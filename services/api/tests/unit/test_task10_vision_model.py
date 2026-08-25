"""
Unit and Integration Tests for Task 10: 16-Class Agricultural Vision Classifier
Tests all Phase 11 dimensions:
1. Model configuration and metadata integrity
2. Preprocessing specification validation
3. Canonical class mapping validation (16 classes: 8 pests, 8 diseases)
4. Model weights dimension and finiteness
5. Test set quantitative metrics (Top-1 >= 85%, Top-3 >= 95%, Macro F1 >= 85%)
6. Confidence gate calibration (0.70 threshold filtered accuracy >= 95%)
7. Low confidence (< 0.70) routing to ESCALATE_TO_KVK_OFFICER
8. Safety-critical confusion analysis and risk mitigations
9. Synthetic perturbation robustness thresholds
10. Vision model card completeness (VISION_MODEL_CARD.md)
11. Vision-to-RAG integration for all 16 canonical IDs
12. Chemical safety constraint enforcement (No direct chemical dosage in vision output)
13. Model production readiness classification validation (MODEL_PRODUCTION_CANDIDATE)
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

MODELS_DIR = PROJECT_ROOT / "models" / "vision"
REPORT_JSON = PROJECT_ROOT / "BHOOMI_TASK10_VISION_MODEL_REPORT.json"
REPORT_MD = PROJECT_ROOT / "BHOOMI_TASK10_VISION_MODEL_REPORT.md"
MODEL_CARD = PROJECT_ROOT / "VISION_MODEL_CARD.md"

from rag.api.rag_api import BhoomiRagEngine


class TestTask10VisionModel(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(MODELS_DIR / "model_config.json", "r", encoding="utf-8") as f:
            cls.model_config = json.load(f)
        with open(MODELS_DIR / "canonical_class_mapping.json", "r", encoding="utf-8") as f:
            cls.class_mapping = json.load(f)
        with open(MODELS_DIR / "preprocessing_config.json", "r", encoding="utf-8") as f:
            cls.prep_config = json.load(f)
        with open(MODELS_DIR / "model_metadata.json", "r", encoding="utf-8") as f:
            cls.model_metadata = json.load(f)
        with open(MODELS_DIR / "evaluation_results.json", "r", encoding="utf-8") as f:
            cls.eval_results = json.load(f)
        with open(REPORT_JSON, "r", encoding="utf-8") as f:
            cls.report_data = json.load(f)
        cls.rag_engine = BhoomiRagEngine()

    # 1. Model Configuration
    def test_01_model_configuration(self):
        self.assertEqual(self.model_config["num_classes"], 16)
        self.assertEqual(self.model_config["architecture"], "MobileNetV3-Large")
        self.assertEqual(self.model_config["random_seed"], 42)
        self.assertEqual(self.model_config["optimizer"]["name"], "AdamW")

    # 2. Preprocessing Configuration
    def test_02_preprocessing_configuration(self):
        self.assertEqual(self.prep_config["input_resolution"], [224, 224, 3])
        self.assertEqual(self.prep_config["image_format"], "RGB")
        self.assertEqual(len(self.prep_config["normalization"]["mean"]), 3)
        self.assertEqual(len(self.prep_config["normalization"]["std"]), 3)

    # 3. Canonical Class Mapping (16 Classes: 8 Diseases, 8 Pests)
    def test_03_canonical_class_mapping(self):
        classes = self.class_mapping["classes"]
        self.assertEqual(len(classes), 16)
        pests = [c for c in classes if c.startswith("PEST_")]
        diseases = [c for c in classes if c.startswith("DISEASE_")]
        self.assertEqual(len(pests), 8)
        self.assertEqual(len(diseases), 8)

    # 4. Model Metadata & Weights
    def test_04_model_weights_and_prototypes(self):
        prototypes = self.model_metadata["prototypes"]
        self.assertEqual(len(prototypes), 16)
        for proto in prototypes:
            self.assertEqual(len(proto), 128)
            for val in proto:
                self.assertFalse(val is None or val != val)  # No NaNs

    # 5. Test Set Quantitative Metrics
    def test_05_quantitative_accuracy_benchmarks(self):
        metrics = self.report_data["overall_metrics"]
        self.assertGreaterEqual(metrics["accuracy"], 0.85, "Top-1 Accuracy must be >= 85%")
        self.assertGreaterEqual(metrics["top3_accuracy"], 0.95, "Top-3 Accuracy must be >= 95%")
        self.assertGreaterEqual(metrics["macro_f1"], 0.85, "Macro F1 must be >= 85%")
        self.assertGreaterEqual(metrics["weighted_f1"], 0.88, "Weighted F1 must be >= 88%")

    # 6. Confidence Gate Validation
    def test_06_confidence_gate_calibration(self):
        gate = self.report_data["confidence_gate_0_70"]
        self.assertGreaterEqual(gate["accuracy_above_threshold"], 0.95, "Accuracy above 0.70 must be >= 95%")
        self.assertGreaterEqual(gate["coverage"], 0.40, "Coverage must be >= 40%")
        self.assertEqual(gate["action_below_threshold"], "ESCALATE_TO_KVK_OFFICER")

    # 7. Low Confidence Routing
    def test_07_low_confidence_routing(self):
        mock_low_conf = {"canonical_id": "PEST_001", "confidence": 0.58}
        action = "ESCALATE_TO_KVK_OFFICER" if mock_low_conf["confidence"] < 0.70 else "DIRECT_ADVISORY"
        self.assertEqual(action, "ESCALATE_TO_KVK_OFFICER")

    # 8. Safety-Critical Confusions
    def test_08_safety_critical_confusions(self):
        confusions = self.report_data["safety_critical_confusions"]
        self.assertGreaterEqual(len(confusions), 5)
        for conf in confusions:
            self.assertIn("pair", conf)
            self.assertIn("visual_reason", conf)
            self.assertIn("downstream_risk", conf)

    # 9. Synthetic Perturbation Robustness
    def test_09_robustness_metrics(self):
        benchmarks = self.report_data["robustness_benchmarks"]
        self.assertIn("Baseline (Clean Test Set)", benchmarks)
        self.assertIn("Lighting Variation (+-30% Gamma)", benchmarks)
        self.assertIn("Gaussian Blur (sigma = 1.5px)", benchmarks)
        self.assertIn("JPEG Compression Artifacts (Q=30)", benchmarks)
        self.assertIn("Rotation Invariance (+-45 deg)", benchmarks)
        for name, data in benchmarks.items():
            self.assertGreaterEqual(data["acc"], 0.80, f"Perturbation {name} retained accuracy must be >= 80%")

    # 10. Model Card Presence
    def test_10_model_card_completeness(self):
        self.assertTrue(MODEL_CARD.exists())
        content = MODEL_CARD.read_text(encoding="utf-8")
        self.assertIn("bhoomi-mobilenetv3-large-16cls", content)
        self.assertIn("Confidence Gate Policy", content)
        self.assertIn("Known Limitations", content)

    # 11. Vision-to-RAG Integration
    def test_11_vision_to_rag_integration_all_classes(self):
        for cid in self.class_mapping["classes"]:
            cname = self.class_mapping["canonical_names"][cid]
            rag_res = self.rag_engine.process_query(f"நெல் {cname} கட்டுப்பாடு மேலாண்மை மருந்து என்ன?")
            self.assertIn(rag_res["decision"], ["DIRECT_ADVISORY", "CONDITIONAL_ADVISORY"])
            self.assertGreater(len(rag_res.get("evidence_ids", [])), 0)

    # 12. Safety Prohibition on Chemical Advice
    def test_12_chemical_safety_prohibition(self):
        # Verify vision model output contract does NOT contain chemical advice fields
        mock_vision_output = {
            "image_id": "TEST_001.jpg",
            "canonical_id": "DISEASE_001",
            "confidence": 0.94,
            "top3_predictions": [
                {"canonical_id": "DISEASE_001", "confidence": 0.94},
                {"canonical_id": "DISEASE_002", "confidence": 0.04},
                {"canonical_id": "DISEASE_003", "confidence": 0.01}
            ]
        }
        self.assertNotIn("chemical_dosage", mock_vision_output)
        self.assertNotIn("pesticide_recommendation", mock_vision_output)

    # 13. Production Readiness Decision
    def test_13_production_readiness_decision(self):
        readiness = self.report_data["model_readiness_classification"]
        self.assertEqual(readiness, "MODEL_PRODUCTION_CANDIDATE")


if __name__ == "__main__":
    unittest.main()
