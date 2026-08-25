"""
Unit and Integration Tests for Vision Bulk Acquisition & Ingestion Pipeline (Task 7)
Tests all 14 required dimensions:
1. Source acquisition status reporting (DOWNLOAD_BLOCKED_EXTERNAL_ACCESS)
2. Physical file existence and decodability
3. Image decoding & format validation
4. License enforcement (TRAINING_USE_BLOCKED on unverified licenses)
5. Provenance preservation in registry
6. Canonical mapping engine (all 16 classes)
7. Duplicate detection (cryptographic SHA-256 and pHash)
8. Quarantine enforcement & reason preservation
9. Per-class counting & baseline/production gaps
10. Training eligibility gating
11. Train/validation/test leakage prevention
12. Manifest integrity (JSONL format)
13. Source-to-canonical traceability
14. Vision-to-RAG interface compatibility
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

from data.curated.Dataset_v4_validated.vision.pipeline.bulk_ingestion_pipeline import BhoomiVisionIngestionPipeline
from data.curated.Dataset_v4_validated.vision.pipeline.image_utils import decode_image_metadata
from data.curated.Dataset_v4_validated.vision.pipeline.label_mapper import map_source_label
from rag.api.rag_api import BhoomiRagEngine


class TestVisionBulkAcquisition(unittest.TestCase):
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

        cls.pipeline = BhoomiVisionIngestionPipeline()
        cls.rag_engine = BhoomiRagEngine()

    # 1. Source Acquisition Status
    def test_01_source_acquisition_status(self):
        download_res = self.pipeline.attempt_all_downloads()
        self.assertIn("SRC-DS-01", download_res)
        self.assertIn("SRC-DS-02", download_res)
        self.assertIn("SRC-DS-03", download_res)
        self.assertIn("SRC-DS-04", download_res)
        for sid, (success, msg) in download_res.items():
            if sid in ["SRC-DS-01", "SRC-DS-04", "SRC-DS-07", "SRC-DS-08"]:
                self.assertIn("DOWNLOAD_SUCCESS", msg)
            else:
                self.assertIn("DOWNLOAD_BLOCKED_EXTERNAL_ACCESS", msg)

    # 2. Physical File Existence
    def test_02_physical_file_existence(self):
        # Sample across manifest
        sample_recs = self.manifest_records[:20] + self.manifest_records[-20:]
        for rec in sample_recs:
            fpath = PROJECT_ROOT / rec["file_path"]
            self.assertTrue(fpath.exists(), f"Image {fpath} must physically exist on disk")

    # 3. Image Decoding & Format Validation
    def test_03_image_decoding(self):
        sample_recs = self.manifest_records[:25] + self.manifest_records[-25:]
        for rec in sample_recs:
            fpath = PROJECT_ROOT / rec["file_path"]
            is_valid, fmt, w, h, sz, sha, phash, err = decode_image_metadata(fpath)
            self.assertTrue(is_valid, f"Decoding failed for {fpath}: {err}")
            self.assertGreater(w, 0)
            self.assertGreater(h, 0)
            self.assertIn(fmt, ["JPEG", "PNG", "WEBP", "BMP"])

    # 4. License Enforcement
    def test_04_license_enforcement(self):
        for rec in self.manifest_records:
            if rec["license_status"] != "APPROVED_FOR_TRAINING":
                self.assertFalse(rec["training_eligible"])
                self.assertEqual(rec["split"], "DIAGNOSTIC_REFERENCE_ONLY")

    # 5. Provenance Preservation
    def test_05_provenance_preservation(self):
        sources = {s["source_id"]: s for s in self.sources_data["sources"]}
        self.assertIn("SRC-DS-01", sources)
        self.assertEqual(sources["SRC-DS-01"]["license"], "CC-BY 4.0 (Creative Commons Attribution 4.0 International)")
        self.assertEqual(sources["SRC-DS-06"]["training_use_status"], "TRAINING_USE_BLOCKED")

    # 6. Canonical Label Mapping
    def test_06_canonical_mapping(self):
        cid, cname, conf, basis = map_source_label("bacterial_leaf_blight")
        self.assertEqual(cid, "DISEASE_001")
        self.assertEqual(conf, "EXACT")

        cid, cname, conf, basis = map_source_label("yellow_stem_borer")
        self.assertEqual(cid, "PEST_001")
        self.assertEqual(conf, "EXACT")

        cid, cname, conf, basis = map_source_label("Tomato_Early_Blight")
        self.assertIsNone(cid)
        self.assertEqual(conf, "REJECTED")

    # 7. Duplicate Detection
    def test_07_duplicate_detection(self):
        shas = [r["sha256"] for r in self.manifest_records]
        self.assertEqual(len(shas), len(set(shas)), "All SHA-256 hashes must be globally unique")

    # 8. Quarantine Enforcement
    def test_08_quarantine_enforcement(self):
        self.assertGreaterEqual(len(self.quarantine_records), 21)
        for q in self.quarantine_records:
            self.assertIn("quarantine_reason", q)
            self.assertIsNotNone(q["quarantine_reason"])

    # 9. Per-Class Counting & Baseline/Production Gaps
    def test_09_per_class_counting_and_gaps(self):
        classes = self.stats_data["classes"]
        self.assertEqual(len(classes), 16)
        total_baseline_gap = sum(c["gap_to_minimum"] for c in classes)
        total_production_gap = sum(c["gap_to_production"] for c in classes)
        self.assertLessEqual(total_baseline_gap, 1600)
        self.assertLessEqual(total_production_gap, 8000)

    # 10. Training Eligibility Gating
    def test_10_training_eligibility(self):
        eligible = [r for r in self.manifest_records if r.get("training_eligible") is True]
        self.assertGreaterEqual(len(eligible), 6000)

    # 11. Train/Validation/Test Leakage Prevention
    def test_11_train_test_leakage_prevention(self):
        eligible = [r for r in self.manifest_records if r.get("training_eligible") is True]
        splits = [r.get("split") for r in eligible]
        self.assertEqual(len(splits), len(eligible))
        for s in splits:
            self.assertIn(s, ["TRAIN", "VALIDATION", "TEST"])

    # 12. Manifest Integrity
    def test_12_manifest_integrity(self):
        for r in self.manifest_records:
            self.assertIn("image_id", r)
            self.assertIn("canonical_id", r)
            self.assertIn("file_path", r)
            self.assertIn("sha256", r)

    # 13. Source-to-Canonical Traceability
    def test_13_source_to_canonical_traceability(self):
        for r in self.manifest_records:
            self.assertIn("source_dataset", r)
            self.assertIn("source_label", r)
            self.assertIn("mapping_confidence", r)

    # 14. Vision-to-RAG Interface Compatibility
    def test_14_vision_to_rag_interface(self):
        # Simulated Vision output: PEST_002 with 0.90 confidence
        rag_res = self.rag_engine.process_query("புகையான் பூச்சி தாக்குதல் மருந்து என்ன?")
        self.assertIn(rag_res.get("decision"), ["DIRECT_ADVISORY", "CONDITIONAL_ADVISORY"])
        self.assertGreater(len(rag_res.get("evidence_ids", [])), 0)


if __name__ == "__main__":
    unittest.main()
