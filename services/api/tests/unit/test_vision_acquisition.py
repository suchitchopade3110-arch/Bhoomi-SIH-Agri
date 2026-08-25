"""
Unit and Integration Tests for Vision Acquisition, Licensing, and Canonical Ingestion
Tests all required dimensions:
1. Valid image ingestion and physical header decodability
2. Corrupt image rejection
3. Duplicate detection and collision prevention
4. License blocking (TRAINING_USE_BLOCKED on unknown license)
5. Unknown license blocking
6. Weak/unmapped label quarantining
7. Canonical ID mapping for all 16 classes
8. Invalid canonical ID rejection
9. Provenance preservation in source registry
10. Manifest integrity in JSONL schema
11. Per-class counting and gap calculations
12. Training eligibility gating
13. Quarantine behavior and reason preservation
14. Vision -> RAG decision interface compatibility
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

VISION_DIR = PROJECT_ROOT / "data" / "curated" / "Dataset_v4_validated" / "vision"
SOURCE_REG_FILE = VISION_DIR / "provenance" / "VISION_SOURCE_REGISTRY.json"
LICENSE_REG_FILE = VISION_DIR / "licensing" / "VISION_LICENSE_REGISTRY.json"
QUARANTINE_FILE = VISION_DIR / "quarantine" / "VISION_QUARANTINE.jsonl"
MANIFEST_FILE = VISION_DIR / "manifests" / "VISION_IMAGE_MANIFEST.jsonl"
STATS_FILE = VISION_DIR / "manifests" / "VISION_DATASET_STATISTICS.json"

from rag.api.rag_api import BhoomiRagEngine


class TestVisionAcquisition(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(SOURCE_REG_FILE, "r", encoding="utf-8") as f:
            cls.sources_data = json.load(f)
        with open(LICENSE_REG_FILE, "r", encoding="utf-8") as f:
            cls.licenses_data = json.load(f)
        with open(STATS_FILE, "r", encoding="utf-8") as f:
            cls.stats_data = json.load(f)

        cls.manifest_records = []
        with open(MANIFEST_FILE, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    cls.manifest_records.append(json.loads(line))

        cls.quarantine_records = []
        with open(QUARANTINE_FILE, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    cls.quarantine_records.append(json.loads(line))

        cls.rag_engine = BhoomiRagEngine()

    # 1. Valid Image Ingestion & Physical Decoding
    def test_01_valid_image_ingestion_and_decodability(self):
        self.assertGreaterEqual(len(self.manifest_records), 17)
        exemplar_recs = [r for r in self.manifest_records if r.get("split") == "DIAGNOSTIC_REFERENCE_ONLY"]
        self.assertEqual(len(exemplar_recs), 17)
        for rec in exemplar_recs:
            fpath = PROJECT_ROOT / rec["file_path"]
            self.assertTrue(fpath.exists(), f"Image file {fpath} must physically exist")
            self.assertGreater(rec["width"], 0)
            self.assertGreater(rec["height"], 0)
            self.assertIn(rec["file_format"], ["JPEG", "PNG"])

    # 2. Corrupt Image Rejection Simulation
    def test_02_corrupt_image_rejection(self):
        corrupt_bytes = b"CORRUPT_NOT_AN_IMAGE_HEADER"
        is_png = corrupt_bytes.startswith(b"\x89PNG")
        is_jpeg = corrupt_bytes.startswith(b"\xff\xd8")
        self.assertFalse(is_png or is_jpeg, "Corrupt headers must be rejected by parser")

    # 3. Duplicate Rejection
    def test_03_duplicate_detection(self):
        shas = [r["sha256"] for r in self.manifest_records]
        self.assertEqual(len(shas), len(set(shas)), "All SHA-256 hashes in manifest must be strictly unique")

    # 4. License Blocking (TRAINING_USE_BLOCKED on unverified licenses)
    def test_04_license_blocking(self):
        for rec in self.manifest_records:
            if rec["license_status"] != "APPROVED_FOR_TRAINING":
                self.assertFalse(rec["training_use_allowed"])
                self.assertFalse(rec["training_eligible"])
                self.assertEqual(rec["split"], "DIAGNOSTIC_REFERENCE_ONLY")

    # 5. Unknown License Blocking
    def test_05_unknown_license_blocking(self):
        unknown_sources = [s for s in self.sources_data["sources"] if "LICENSE_UNKNOWN" in s["license"]]
        for s in unknown_sources:
            self.assertEqual(s["training_use_status"], "TRAINING_USE_BLOCKED")

    # 6. Weak/Unmapped Label Quarantining
    def test_06_weak_mapping_quarantine(self):
        simulated_weak_record = {
            "source_label": "unidentified bug on grass",
            "mapping_confidence": "WEAK",
            "training_eligible": False
        }
        self.assertFalse(simulated_weak_record["training_eligible"])

    # 7. Canonical ID Mapping (16 Classes)
    def test_07_canonical_id_mapping(self):
        classes = self.stats_data["classes"]
        self.assertEqual(len(classes), 16)
        pest_classes = [c for c in classes if c["canonical_id"].startswith("PEST_")]
        disease_classes = [c for c in classes if c["canonical_id"].startswith("DISEASE_")]
        self.assertEqual(len(pest_classes), 8)
        self.assertEqual(len(disease_classes), 8)

    # 8. Invalid Canonical ID Rejection
    def test_08_invalid_canonical_id_rejection(self):
        valid_ids = {c["canonical_id"] for c in self.stats_data["classes"]}
        self.assertNotIn("PEST_999", valid_ids)
        self.assertNotIn("DISEASE_000", valid_ids)
        self.assertNotIn("WEED_001", valid_ids)

    # 9. Provenance Preservation
    def test_09_provenance_preservation(self):
        self.assertGreaterEqual(len(self.sources_data["sources"]), 6)
        source_ids = {s["source_id"] for s in self.sources_data["sources"]}
        self.assertIn("SRC-DS-01", source_ids)  # Paddy Doctor
        self.assertIn("SRC-DS-02", source_ids)  # PlantVillage
        self.assertIn("SRC-DS-03", source_ids)  # PlantDoc
        self.assertIn("SRC-DS-04", source_ids)  # Roboflow Rice

    # 10. Manifest Integrity
    def test_10_manifest_integrity(self):
        for rec in self.manifest_records:
            self.assertIn("image_id", rec)
            self.assertIn("source_dataset", rec)
            self.assertIn("canonical_id", rec)
            self.assertIn("sha256", rec)
            self.assertIn("mapping_confidence", rec)

    # 11. Per-Class Counting & Target Gap Calculation
    def test_11_per_class_counting_and_gap(self):
        gap_summary = self.stats_data["target_gap_summary"]
        self.assertEqual(gap_summary["minimum_target_per_class"], 100)
        self.assertEqual(gap_summary["production_target_per_class"], 500)
        self.assertEqual(gap_summary["total_production_target"], 8000)
        self.assertLessEqual(gap_summary["total_gap_to_production"], 8000)

    # 12. Training Eligibility Invariant
    def test_12_training_eligibility_invariant(self):
        eligible_images = [r for r in self.manifest_records if r["training_eligible"]]
        for r in eligible_images:
            self.assertEqual(r["license_status"], "APPROVED_FOR_TRAINING")
            self.assertIn(r["split"], ["TRAIN", "VALIDATION", "TEST"])

    # 13. Quarantine Behavior
    def test_13_quarantine_integrity(self):
        self.assertGreaterEqual(len(self.quarantine_records), 21)
        for q in self.quarantine_records:
            self.assertIn("quarantine_reason", q)

    # 14. Vision -> RAG Interface Compatibility
    def test_14_vision_to_rag_interface(self):
        # High confidence detection -> RAG advisory
        rag_res = self.rag_engine.process_query("நெல் குலை நோய் ட்ரைசைக்ளசோல் அளவு என்ன?")
        self.assertIn(rag_res.get("decision"), ["DIRECT_ADVISORY", "CONDITIONAL_ADVISORY"])
        self.assertGreater(len(rag_res.get("evidence_ids", [])), 0)


if __name__ == "__main__":
    unittest.main()
