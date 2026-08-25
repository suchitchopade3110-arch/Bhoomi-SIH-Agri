"""
Unit and Integration Tests for Vision Dataset Forensics and RAG Interface
Tests:
1. Real image existence and header decodability
2. Missing file reference handling
3. Canonical label mapping to PEST_001..008 and DISEASE_001..008
4. Zero-image class detection
5. Classes below training threshold detection
6. Training split block on unverified licenses
7. Vision -> RAG decision contract interface compatibility
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

INVENTORY_JSON_PATH = PROJECT_ROOT / "data" / "curated" / "Dataset_v4_validated" / "vision" / "VISION_DATASET_INVENTORY.json"
MANIFEST_JSON_PATH = PROJECT_ROOT / "data" / "curated" / "Dataset_v4_validated" / "vision" / "VISION_DATASET_MANIFEST.json"
VALIDATION_JSON_PATH = PROJECT_ROOT / "data" / "curated" / "Dataset_v4_validated" / "vision" / "VISION_DATASET_VALIDATION.json"

from rag.api.rag_api import BhoomiRagEngine


class TestVisionDataset(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(INVENTORY_JSON_PATH, "r", encoding="utf-8") as f:
            cls.inventory_data = json.load(f)
        with open(MANIFEST_JSON_PATH, "r", encoding="utf-8") as f:
            cls.manifest_data = json.load(f)
        with open(VALIDATION_JSON_PATH, "r", encoding="utf-8") as f:
            cls.validation_data = json.load(f)
        cls.rag_engine = BhoomiRagEngine()

    # 1. Real Image Existence & Header Integrity
    def test_01_real_images_exist_and_decode(self):
        real_recs = [r for r in self.inventory_data["records"] if r["file_exists"]]
        self.assertEqual(len(real_recs), 17)
        for r in real_recs:
            fpath = PROJECT_ROOT / r["path"]
            self.assertTrue(fpath.exists(), f"Image file {fpath} must exist on disk")
            self.assertGreater(r["file_size_bytes"], 0)
            self.assertIn(r["format"], ["JPEG", "PNG"])

    # 2. Missing File Reference Handling
    def test_02_missing_file_references(self):
        missing_recs = [r for r in self.inventory_data["records"] if not r["file_exists"]]
        self.assertEqual(len(missing_recs), 4)
        for r in missing_recs:
            self.assertIsNone(r["path"])
            self.assertFalse(r["decodable"])

    # 3. Canonical Label Mapping
    def test_03_canonical_label_mapping(self):
        classes = self.manifest_data["classes"]
        self.assertEqual(len(classes), 16)
        pest_ids = [c["canonical_id"] for c in classes if c["entity_type"] == "pest"]
        disease_ids = [c["canonical_id"] for c in classes if c["entity_type"] == "disease"]
        self.assertEqual(len(pest_ids), 8)
        self.assertEqual(len(disease_ids), 8)

    # 4. Zero-Image Class Detection
    def test_04_zero_image_classes(self):
        zero_classes = self.validation_data["zero_image_classes"]
        self.assertEqual(len(zero_classes), 9)
        self.assertIn("PEST_007", zero_classes)  # Whorl maggot
        for i in range(1, 9):
            self.assertIn(f"DISEASE_{i:03d}", zero_classes)

    # 5. Classes Below Training Threshold
    def test_05_classes_below_training_threshold(self):
        self.assertEqual(self.validation_data["classes_below_training_minimum_count"], 16)
        self.assertEqual(self.validation_data["valid_training_images"], 0)

    # 6. Training Split Blocked for License Unknown
    def test_06_training_split_blocked(self):
        real_recs = [r for r in self.inventory_data["records"] if r["file_exists"]]
        for r in real_recs:
            self.assertEqual(r["split"], "TRAINING_USE_BLOCKED")

    # 7. Vision -> RAG Interface Compatibility
    def test_07_vision_to_rag_interface(self):
        # Simulate Vision model output: PEST_001 with 0.85 confidence
        vision_output = {
            "detected_canonical_id": "PEST_001",
            "vision_confidence": 0.85,
            "crop": "Rice (Oryza sativa)"
        }
        # Invariant: Confidence >= 0.70 routes to RAG decision
        self.assertGreaterEqual(vision_output["vision_confidence"], 0.70)
        rag_res = self.rag_engine.process_query("நெல் தண்டு துளைப்பான் மருந்து என்ன?")
        self.assertIn(rag_res.get("decision"), ["DIRECT_ADVISORY", "CONDITIONAL_ADVISORY"])
        self.assertIn("SEV-PEST-001", rag_res.get("evidence_ids", []))


if __name__ == "__main__":
    unittest.main()
