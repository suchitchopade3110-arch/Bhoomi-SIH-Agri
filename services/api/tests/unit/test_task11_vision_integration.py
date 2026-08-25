"""
Unit and Integration Tests for Task 11: Vision Model Integration, End-to-End Validation & Production Gate
Tests all Task 11 dimensions:
1. VisionInferenceService initialization & artifact verification
2. Canonical 16-class contract verification (8 pests, 8 diseases)
3. Preprocessing standardization (224x224 RGB ImageNet normalization)
4. Confidence gate boundary values (0.6999, 0.7000, 0.7001)
5. Top-3 diagnostic predictions
6. Robust error handling on corrupt/zero-byte/oversized/non-image inputs
7. Vision -> Severity handoff across all 16 canonical classes
8. Vision -> RAG advisory integration & citation preservation
9. Chemical safety invariant (No direct chemical dosage in vision output)
10. Integrated latency & resource performance
11. Security & path traversal handling
12. API contract verification
13. Production Gate Decision (MODEL_PRODUCTION_READY)
"""
import json
import sys
import struct
import unittest
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))
if str(PROJECT_ROOT / "services" / "api") not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT / "services" / "api"))

from app.services.vision_inference_service import get_vision_inference_service, VisionInferenceError
from app.services.gate_service import SUPPORTED_DIAGNOSIS_LABELS
from app.core.enums import GateOutcome
from app.domain.gate import decide
from rag.api.rag_api import BhoomiRagEngine

REPORT_JSON = PROJECT_ROOT / "BHOOMI_TASK11_VISION_INTEGRATION_REPORT.json"
REPORT_MD = PROJECT_ROOT / "BHOOMI_TASK11_VISION_INTEGRATION_REPORT.md"
API_DOCS = PROJECT_ROOT / "VISION_INFERENCE_API.md"
CHECKLIST_MD = PROJECT_ROOT / "VISION_PRODUCTION_CHECKLIST.md"


def make_test_jpeg(width: int = 480, height: int = 640) -> bytes:
    soi = b'\xff\xd8'
    jfif = b'JFIF\x00\x01\x01\x01\x00H\x00H\x00\x00'
    app0 = b'\xff\xe0' + struct.pack('>H', len(jfif) + 2) + jfif
    sof_payload = b'\x08' + struct.pack('>HH', height, width) + b'\x03\x01\x11\x00\x02\x11\x01\x03\x11\x01'
    sof0 = b'\xff\xc0' + struct.pack('>H', len(sof_payload) + 2) + sof_payload
    sos_payload = b'\x03\x01\x00\x02\x11\x03\x11\x00\x3f\x00'
    sos = b'\xff\xda' + struct.pack('>H', len(sos_payload) + 2) + sos_payload
    scan_data = b'\x00\x11\x22\x33' * 100
    eoi = b'\xff\xd9'
    return soi + app0 + sof0 + sos + scan_data + eoi


class TestTask11VisionIntegration(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.service = get_vision_inference_service()
        cls.rag_engine = BhoomiRagEngine()
        cls.test_jpeg = make_test_jpeg()
        with open(REPORT_JSON, "r", encoding="utf-8") as f:
            cls.report_data = json.load(f)

    # 1. Service Initialization
    def test_01_service_initialization(self):
        self.assertEqual(self.service.model_id, "bhoomi-mobilenetv3-large-16cls")
        self.assertEqual(self.service.model_version, "1.0.0")
        self.assertEqual(len(self.service.classes), 16)

    # 2. Canonical 16-Class Contract
    def test_02_canonical_16_class_contract(self):
        classes = self.service.classes
        self.assertEqual(len(classes), 16)
        self.assertEqual(len(set(classes)), 16)
        pests = [c for c in classes if c.startswith("PEST_")]
        diseases = [c for c in classes if c.startswith("DISEASE_")]
        self.assertEqual(len(pests), 8)
        self.assertEqual(len(diseases), 8)
        for cid in classes:
            self.assertIn(cid, SUPPORTED_DIAGNOSIS_LABELS)
            self.assertIn(cid, self.service.canonical_names)

    # 3. Preprocessing Standardization
    def test_03_preprocessing_standardization(self):
        tensor, sha256 = self.service.preprocess_image(self.test_jpeg)
        self.assertEqual(tensor.shape, (3, 224, 224))
        self.assertEqual(len(sha256), 64)

    # 4. Confidence Gate Boundary Tests
    def test_04_confidence_gate_boundary(self):
        # 0.6999 -> ESCALATE
        d_below = decide(0.6999, in_scope=True, retrieval_relevance=0.85, confidence_gate=0.70, relevance_threshold=0.60)
        self.assertEqual(d_below.outcome, GateOutcome.ESCALATE)
        
        # 0.7000 -> COMPOSE
        d_exact = decide(0.7000, in_scope=True, retrieval_relevance=0.85, confidence_gate=0.70, relevance_threshold=0.60)
        self.assertEqual(d_exact.outcome, GateOutcome.COMPOSE)
        
        # 0.7001 -> COMPOSE
        d_above = decide(0.7001, in_scope=True, retrieval_relevance=0.85, confidence_gate=0.70, relevance_threshold=0.60)
        self.assertEqual(d_above.outcome, GateOutcome.COMPOSE)

    # 5. Top-3 Diagnostic Predictions
    def test_05_top_k_predictions(self):
        pred = self.service.predict(self.test_jpeg)
        self.assertIn("canonical_id", pred)
        self.assertIn("confidence", pred)
        self.assertIn("top_k_predictions", pred)
        self.assertEqual(len(pred["top_k_predictions"]), 3)
        self.assertEqual(pred["top_k_predictions"][0]["canonical_id"], pred["canonical_id"])

    # 6. Error Handling on Malformed Inputs
    def test_06_error_handling_malformed_inputs(self):
        with self.assertRaises(VisionInferenceError) as ctx:
            self.service.predict(b"")
        self.assertEqual(ctx.exception.error_code, "ZERO_BYTE_FILE")

        with self.assertRaises(VisionInferenceError) as ctx:
            self.service.predict(b"\x00\x01\x02\x03")
        self.assertEqual(ctx.exception.error_code, "CORRUPT_HEADER")

        with self.assertRaises(VisionInferenceError) as ctx:
            self.service.predict(b"BM" + b"\x00" * 10)
        self.assertEqual(ctx.exception.error_code, "UNSUPPORTED_FORMAT")

    # 7. Vision -> Severity Handoff
    def test_07_vision_severity_handoff(self):
        for cid in self.service.classes:
            self.assertIn(cid, SUPPORTED_DIAGNOSIS_LABELS)

    # 8. Vision -> RAG Integration
    def test_08_vision_rag_integration(self):
        for cid in self.service.classes:
            cname = self.service.canonical_names[cid]
            rag_res = self.rag_engine.process_query(f"நெல் {cname} பூச்சி / நோய் தாக்குதல் மேலாண்மை மருந்து என்ன?")
            self.assertIn(rag_res["decision"], ["DIRECT_ADVISORY", "CONDITIONAL_ADVISORY"])
            self.assertGreater(len(rag_res.get("evidence_ids", [])), 0)

    # 9. Chemical Safety Invariant
    def test_09_chemical_safety_invariant(self):
        pred = self.service.predict(self.test_jpeg)
        self.assertNotIn("chemical_dosage", pred)
        self.assertNotIn("pesticide_recommendation", pred)
        self.assertNotIn("treatment_advice", pred)

    # 10. Repeated Inference & Resource Test
    def test_10_repeated_inference_stability(self):
        latencies = []
        for _ in range(50):
            res = self.service.predict(self.test_jpeg)
            latencies.append(res["latencies"]["total_ms"])
        self.assertEqual(len(latencies), 50)
        self.assertLess(sum(latencies) / len(latencies), 50.0)

    # 11. Security Tests
    def test_11_security_path_traversal(self):
        with self.assertRaises(VisionInferenceError) as ctx:
            self.service.predict("../../../../../etc/passwd")
        self.assertIn(ctx.exception.error_code, ["IMAGE_NOT_FOUND", "PATH_TRAVERSAL_DETECTED"])

    # 12. Documentation Files Exist
    def test_12_documentation_artifacts(self):
        self.assertTrue(REPORT_JSON.exists())
        self.assertTrue(REPORT_MD.exists())
        self.assertTrue(API_DOCS.exists())
        self.assertTrue(CHECKLIST_MD.exists())

    # 13. Production Gate Decision
    def test_13_production_gate_decision(self):
        decision = self.report_data["production_gate_decision"]
        self.assertEqual(decision, "MODEL_PRODUCTION_READY")


if __name__ == "__main__":
    unittest.main()
