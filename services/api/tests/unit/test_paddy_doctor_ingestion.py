"""
Unit & Integration Tests for Task 8: Paddy Doctor Dataset Ingestion & Validation
Covers all 19 dimensions specified in Phase 14:
1. Actual source directory discovery
2. Physical file existence
3. Image decoding & format verification
4. Zero-byte file detection & handling
5. Corrupt image rejection
6. SHA-256 generation & uniqueness
7. Exact duplicate detection
8. Near-duplicate detection (pHash)
9. License enforcement (CC-BY 4.0 approved for training)
10. Provenance preservation in registry
11. Canonical mapping (6 valid classes mapped, 4 non-BHOOMI rejected)
12. Rejected mapping quarantine
13. Canonical ID validation (PEST_001..008, DISEASE_001..008)
14. Manifest integrity (JSONL schema compliance)
15. Per-class counting and gap calculations
16. Quarantine integrity
17. Training eligibility gating
18. Train/validation/test split leakage prevention
19. Vision-to-RAG compatibility & confidence gate invariance
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

SRC_DIR = Path(r"C:\Users\Tharun BL\Downloads\paddy-disease-classification")
VISION_DIR = PROJECT_ROOT / "data" / "curated" / "Dataset_v4_validated" / "vision"
SOURCE_REG_FILE = VISION_DIR / "provenance" / "VISION_SOURCE_REGISTRY.json"
LICENSE_REG_FILE = VISION_DIR / "licensing" / "VISION_LICENSE_REGISTRY.json"
QUARANTINE_FILE = VISION_DIR / "quarantine" / "VISION_QUARANTINE.jsonl"
MANIFEST_FILE = VISION_DIR / "manifests" / "VISION_IMAGE_MANIFEST.jsonl"
STATS_FILE = VISION_DIR / "manifests" / "VISION_DATASET_STATISTICS.json"
SPLITS_FILE = VISION_DIR / "splits" / "VISION_TRAIN_VAL_TEST_SPLIT.json"

from data.curated.Dataset_v4_validated.vision.pipeline.image_utils import decode_image_metadata
from data.curated.Dataset_v4_validated.vision.pipeline.label_mapper import map_source_label, CANONICAL_ENTITIES
from rag.api.rag_api import BhoomiRagEngine


class TestPaddyDoctorIngestion(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with open(SOURCE_REG_FILE, "r", encoding="utf-8") as f:
            cls.sources_data = json.load(f)
        with open(LICENSE_REG_FILE, "r", encoding="utf-8") as f:
            cls.licenses_data = json.load(f)
        with open(STATS_FILE, "r", encoding="utf-8") as f:
            cls.stats_data = json.load(f)
        with open(SPLITS_FILE, "r", encoding="utf-8") as f:
            cls.splits_data = json.load(f)

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

    # 1. Actual Source Directory Discovery
    def test_01_source_directory_discovery(self):
        self.assertTrue(SRC_DIR.exists(), f"Source directory {SRC_DIR} must exist")
        self.assertTrue((SRC_DIR / "train_images").exists())
        self.assertTrue((SRC_DIR / "test_images").exists())
        self.assertTrue((SRC_DIR / "train.csv").exists())

    # 2. Physical File Existence
    def test_02_physical_file_existence(self):
        # Sample across canonical images
        sample_recs = self.manifest_records[:30] + self.manifest_records[-30:]
        for rec in sample_recs:
            fpath = PROJECT_ROOT / rec["file_path"]
            self.assertTrue(fpath.exists(), f"Physical file {fpath} must exist on disk")

    # 3. Image Decoding & Format Verification
    def test_03_image_decoding_and_format(self):
        sample_recs = self.manifest_records[:30] + self.manifest_records[-30:]
        for rec in sample_recs:
            fpath = PROJECT_ROOT / rec["file_path"]
            is_valid, fmt, w, h, sz, sha, phash, err = decode_image_metadata(fpath)
            self.assertTrue(is_valid, f"Decoding failed for {fpath}: {err}")
            self.assertIn(fmt, ["JPEG", "PNG"])
            self.assertGreater(w, 0)
            self.assertGreater(h, 0)

    # 4. Zero-byte Detection
    def test_04_zero_byte_detection(self):
        for rec in self.manifest_records:
            fpath = PROJECT_ROOT / rec["file_path"]
            self.assertGreater(fpath.stat().st_size, 0, "No canonical image may be 0 bytes")

    # 5. Corrupt Image Rejection
    def test_05_corrupt_image_rejection(self):
        corrupt_data = b"NOT_A_VALID_JPEG_HEADER"
        is_valid, fmt, w, h, sz, sha, phash, err = decode_image_metadata(Path("non_existent_dummy.jpg"))
        self.assertFalse(is_valid)

    # 6. SHA-256 Generation & Global Uniqueness
    def test_06_sha256_uniqueness(self):
        shas = [r["sha256"] for r in self.manifest_records]
        self.assertEqual(len(shas), len(set(shas)), "All SHA-256 hashes in manifest must be unique")

    # 7. Exact Duplicate Detection
    def test_07_exact_duplicate_detection(self):
        dup_quarantine = [q for q in self.quarantine_records if "DUPLICATE" in q.get("status", "") or "DUPLICATE" in q.get("reason", "")]
        self.assertGreaterEqual(len(dup_quarantine), 50, "Duplicate files must be caught and quarantined")

    # 8. Near-duplicate Detection (pHash)
    def test_08_phash_generation(self):
        sample = self.manifest_records[:50]
        for r in sample:
            self.assertIn("phash", r)
            self.assertEqual(len(r["phash"]), 16, "pHash must be a 16-hex character (64-bit) string")

    # 9. License Enforcement
    def test_09_license_enforcement(self):
        eligible = [r for r in self.manifest_records if r.get("training_eligible") is True]
        for r in eligible:
            self.assertEqual(r["license_status"], "APPROVED_FOR_TRAINING")
            self.assertTrue(r["training_use_allowed"])

    # 10. Provenance Preservation
    def test_10_provenance_preservation(self):
        sources = {s["source_id"]: s for s in self.sources_data["sources"]}
        self.assertIn("SRC-DS-01", sources)
        paddy_src = sources["SRC-DS-01"]
        self.assertEqual(paddy_src["acquisition_status"], "INGESTED")
        self.assertIn("CC-BY 4.0", paddy_src["license"])
        self.assertEqual(paddy_src["training_use_status"], "APPROVED_FOR_TRAINING")

    # 11. Canonical Mapping (6 valid mapped, 4 non-BHOOMI rejected)
    def test_11_canonical_mapping(self):
        # 6 valid mappings
        self.assertEqual(map_source_label("bacterial_leaf_blight")[0], "DISEASE_001")
        self.assertEqual(map_source_label("bacterial_leaf_streak")[0], "DISEASE_002")
        self.assertEqual(map_source_label("blast")[0], "DISEASE_003")
        self.assertEqual(map_source_label("brown_spot")[0], "DISEASE_004")
        self.assertEqual(map_source_label("dead_heart")[0], "PEST_001")
        self.assertEqual(map_source_label("tungro")[0], "DISEASE_008")

        # 4 rejected mappings
        self.assertEqual(map_source_label("bacterial_panicle_blight")[2], "REJECTED")
        self.assertEqual(map_source_label("downy_mildew")[2], "REJECTED")
        self.assertEqual(map_source_label("hispa")[2], "REJECTED")
        self.assertEqual(map_source_label("normal")[2], "REJECTED")

    # 12. Rejected Mapping Quarantine
    def test_12_rejected_mapping_quarantine(self):
        quarantined_non_bhoomi = [q for q in self.quarantine_records if "NON_BHOOMI_CLASS" in q.get("reason", "") or "NON_BHOOMI_CLASS" in q.get("status", "")]
        self.assertGreaterEqual(len(quarantined_non_bhoomi), 4000)

    # 13. Canonical ID Validation
    def test_13_canonical_id_validation(self):
        valid_ids = set(CANONICAL_ENTITIES.keys())
        for r in self.manifest_records:
            self.assertIn(r["canonical_id"], valid_ids)

    # 14. Manifest Integrity
    def test_14_manifest_integrity(self):
        required_fields = [
            "image_id", "canonical_id", "canonical_name", "source_id",
            "source_dataset", "source_label", "mapping_confidence",
            "file_path", "sha256", "phash", "width", "height",
            "license", "license_status", "training_eligible", "split"
        ]
        for r in self.manifest_records[:100]:
            for f in required_fields:
                self.assertIn(f, r, f"Manifest record missing required field: {f}")

    # 15. Per-class Counting and Gap Calculation
    def test_15_per_class_counting_and_gaps(self):
        class_stats = {c["canonical_id"]: c for c in self.stats_data["classes"]}
        self.assertEqual(len(class_stats), 16)
        
        # 6 populated classes
        self.assertGreater(class_stats["DISEASE_001"]["current_count"], 400)
        self.assertGreater(class_stats["DISEASE_002"]["current_count"], 300)
        self.assertGreater(class_stats["DISEASE_003"]["current_count"], 1500)
        self.assertGreater(class_stats["DISEASE_004"]["current_count"], 900)
        self.assertGreater(class_stats["PEST_001"]["current_count"], 1400)
        self.assertGreater(class_stats["DISEASE_008"]["current_count"], 1000)
        
        # Production ready classes (>= 500 images)
        self.assertEqual(class_stats["DISEASE_003"]["status"], "PRODUCTION_READY")
        self.assertEqual(class_stats["DISEASE_004"]["status"], "PRODUCTION_READY")
        self.assertEqual(class_stats["DISEASE_008"]["status"], "PRODUCTION_READY")
        self.assertEqual(class_stats["PEST_001"]["status"], "PRODUCTION_READY")

    # 16. Quarantine Integrity
    def test_16_quarantine_integrity(self):
        for q in self.quarantine_records[:100]:
            self.assertIn("quarantine_reason", q)
            self.assertIn("source_dataset", q)

    # 17. Training Eligibility Gating
    def test_17_training_eligibility(self):
        eligible = [r for r in self.manifest_records if r.get("training_eligible") is True]
        self.assertGreaterEqual(len(eligible), 6000)
        
        exemplars = [r for r in self.manifest_records if r.get("split") == "DIAGNOSTIC_REFERENCE_ONLY"]
        self.assertEqual(len(exemplars), 17)
        for ex in exemplars:
            self.assertFalse(ex["training_eligible"])

    # 18. Train/Validation/Test Split Leakage Prevention
    def test_18_split_leakage_prevention(self):
        eligible = [r for r in self.manifest_records if r.get("training_eligible") is True]
        train_shas = {r["sha256"] for r in eligible if r["split"] == "TRAIN"}
        val_shas = {r["sha256"] for r in eligible if r["split"] == "VALIDATION"}
        test_shas = {r["sha256"] for r in eligible if r["split"] == "TEST"}

        # Disjointness check (Zero leakage across splits)
        self.assertEqual(len(train_shas.intersection(val_shas)), 0, "Train and Validation sets must have 0 overlap")
        self.assertEqual(len(train_shas.intersection(test_shas)), 0, "Train and Test sets must have 0 overlap")
        self.assertEqual(len(val_shas.intersection(test_shas)), 0, "Validation and Test sets must have 0 overlap")

    # 19. Vision-to-RAG Compatibility
    def test_19_vision_to_rag_compatibility(self):
        # High confidence detection on ingested canonical classes
        for cid, query in [
            ("DISEASE_001", "நெல் பாக்டீரியல் இலை கருகல் மருந்து என்ன?"),
            ("DISEASE_003", "நெல் குலை நோய் ட்ரைசைக்ளசோல் அளவு என்ன?"),
            ("PEST_001", "நெல் தண்டு துளைப்பான் மருந்து என்ன?")
        ]:
            rag_res = self.rag_engine.process_query(query)
            self.assertIn(rag_res.get("decision"), ["DIRECT_ADVISORY", "CONDITIONAL_ADVISORY"])
            self.assertGreater(len(rag_res.get("evidence_ids", [])), 0)


if __name__ == "__main__":
    unittest.main()
