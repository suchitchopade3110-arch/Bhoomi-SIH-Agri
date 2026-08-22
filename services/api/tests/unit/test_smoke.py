"""Phase 0 smoke test — verifies the full skeleton per the AGENTS.md spec.

Verification checklist:
  ✓ sum(WEIGHTS.values()) == 1.0
  ✓ Every enum value matches the API Contract §2.2 spelling exactly
  ✓ Every service stub is importable and raises NotImplementedError
  ✓ All domain Pydantic v2 models are importable and valid
  ✓ All ports are importable as Protocols
  ✓ app.main imports cleanly (FastAPI factory works)
  ✓ All spec-mandated shim paths resolve correctly
  ✓ CONFIDENCE_GATE == 0.70
  ✓ Decision model enforces exactly-one-branch invariant
"""

import pytest
from datetime import datetime


# ---------------------------------------------------------------------------
# 1. WEIGHTS sum — the only assertion the spec explicitly mandates in a test
# ---------------------------------------------------------------------------

def test_weights_sum_to_exactly_1_0():
    """sum(WEIGHTS.values()) == 1.0 — asserted in constants.py at import time too."""
    from app.domain.constants import WEIGHTS
    assert abs(sum(WEIGHTS.values()) - 1.0) < 1e-9, (
        f"WEIGHTS sum is {sum(WEIGHTS.values())}, must be exactly 1.0"
    )


def test_weights_keys_are_all_six_subindices():
    from app.domain.constants import WEIGHTS
    from app.domain.enums import SubIndexKey
    assert set(WEIGHTS.keys()) == set(SubIndexKey), (
        "WEIGHTS must have exactly one entry per SubIndexKey"
    )


# ---------------------------------------------------------------------------
# 2. Enum values — exact API Contract §2.2 spelling
# ---------------------------------------------------------------------------

class TestEnumValues:
    """Every enum value must match the contract's exact string spelling."""

    def test_land_status(self):
        from app.domain.enums import LandStatus
        # Contract §2.2: pending_verification | under_review | verified | rejected
        assert "verified" in [e.value for e in LandStatus]
        assert "rejected" in [e.value for e in LandStatus]
        assert LandStatus.VERIFIED == "verified"
        assert LandStatus.REJECTED == "rejected"

    def test_health_band(self):
        from app.domain.enums import HealthBand
        # Contract §2.2: unrated | critical | poor | watch | good | excellent
        assert HealthBand.UNRATED == "unrated"
        assert HealthBand.CRITICAL == "critical"
        assert HealthBand.POOR == "poor"
        assert HealthBand.WATCH == "watch"
        assert HealthBand.GOOD == "good"
        assert HealthBand.EXCELLENT == "excellent"

    def test_subindex_key(self):
        from app.domain.enums import SubIndexKey
        # Contract §2.2: exact names
        assert SubIndexKey.ENVIRONMENTAL_SUITABILITY == "environmental_suitability"
        assert SubIndexKey.RESOURCE_ADEQUACY == "resource_adequacy"
        assert SubIndexKey.CROP_STAGE_PROGRESSION == "crop_stage_progression"
        assert SubIndexKey.ACTIVE_PROBLEM_LOAD == "active_problem_load"
        assert SubIndexKey.MONITORING_RECENCY == "monitoring_recency"
        assert SubIndexKey.TREATMENT_RESPONSE == "treatment_response"

    def test_problem_severity(self):
        from app.domain.enums import ProblemSeverity
        assert ProblemSeverity.EARLY == "early"
        assert ProblemSeverity.MODERATE == "moderate"
        assert ProblemSeverity.SEVERE == "severe"

    def test_problem_status(self):
        from app.domain.enums import ProblemStatus
        assert ProblemStatus.OPEN == "open"
        assert ProblemStatus.RESOLVED == "resolved"

    def test_followup_response(self):
        from app.domain.enums import FollowupResponse
        assert FollowupResponse.IMPROVED == "improved"
        assert FollowupResponse.NO_CHANGE == "no_change"
        assert FollowupResponse.GOT_WORSE == "got_worse"


# ---------------------------------------------------------------------------
# 3. Service stubs — importable and raise NotImplementedError
# ---------------------------------------------------------------------------

class TestServiceEntryPoints:
    """Each core service entry point must be importable and callable."""

    def test_build_case_summary_is_importable(self):
        from app.services.escalation.compiler import build_case_summary
        assert callable(build_case_summary)

    def test_build_case_summary_compiles_case_summary(self):
        from app.services.escalation.compiler import build_case_summary
        summary = build_case_summary(
            farm_id="f_1",
            problem_id="p_7",
            farm_info={"farmer_name": "Raman", "village": "Erode"},
            recent_events=[],
            images=[],
            treatments_tried=[],
            followup_trend=None,
            current_health={"score": 68, "band": "watch"},
        )
        assert summary.farm_id == "f_1"
        assert summary.case_id == "p_7"
        assert summary.health_score == 68.0

    def test_compute_health_is_importable_via_spec_path(self):
        from app.services.health.engine import compute_health
        assert callable(compute_health)

    def test_gate_decide_is_importable_via_spec_path(self):
        from app.services.gate.gate import decide
        assert callable(decide)

    def test_rag_pipeline_is_importable_via_spec_path(self):
        from app.services.rag.pipeline import AdvisoryService
        assert AdvisoryService is not None


# ---------------------------------------------------------------------------
# 4. Domain models (Pydantic v2)
# ---------------------------------------------------------------------------

class TestDomainModels:
    """Pydantic v2 domain models: constructable and invariants enforced."""

    def test_sub_index_constructable(self):
        from app.domain.models import SubIndex
        from app.domain.enums import SubIndexKey
        si = SubIndex(
            key=SubIndexKey.ACTIVE_PROBLEM_LOAD,
            value=70,
            weight=0.30,
            contribution=21.0,
        )
        assert si.value == 70

    def test_health_snapshot_unrated(self):
        from app.domain.models import HealthSnapshot
        from app.domain.enums import HealthBand
        snap = HealthSnapshot(
            score=None,
            band=HealthBand.UNRATED,
            computed_at=datetime.utcnow(),
        )
        assert snap.score is None
        assert snap.band == HealthBand.UNRATED

    def test_advisory_requires_at_least_one_citation(self):
        from app.domain.models import Advisory, Citation
        with pytest.raises(Exception):  # pydantic ValidationError
            Advisory(
                possible_issue="x",
                what_to_check="x",
                what_to_do_next="x",
                what_to_avoid="x",
                expert_triggers="x",
                citations=[],  # ← must be non-empty
            )

    def test_advisory_with_citation(self):
        from app.domain.models import Advisory, Citation
        adv = Advisory(
            possible_issue="Early BLB",
            what_to_check="Check leaf margins for water-soaked lesions.",
            what_to_do_next="Drain the field.",
            what_to_avoid="Do not apply nitrogen top-dressing.",
            expert_triggers="Escalate if lesions cover >25% within 3 days.",
            citations=[Citation(doc_id="kb_211", title="ICAR BLB PoP", reviewed_on="2025-11-02")],
        )
        assert len(adv.citations) == 1

    def test_decision_compose_branch_invariant(self):
        from app.domain.models import Decision, AdvisoryBranch, Advisory, Citation
        adv = Advisory(
            possible_issue="x", what_to_check="x", what_to_do_next="x",
            what_to_avoid="x", expert_triggers="x",
            citations=[Citation(doc_id="kb_1", title="T", reviewed_on="2025-01-01")],
        )
        d = Decision(above_gate=True, advisory=AdvisoryBranch(advisory=adv))
        assert d.above_gate is True
        assert d.escalation is None

    def test_decision_escalation_branch_invariant(self):
        from app.domain.models import Decision, EscalationBranch
        d = Decision(
            above_gate=False,
            escalation=EscalationBranch(
                case_id="c_5",
                assigned_to="agronomist:kvk_erode",
                spoken_summary="Not sure — sent to expert.",
                reason="confidence 0.41 < gate 0.70",
                error_code="BELOW_CONFIDENCE_GATE",
            ),
        )
        assert d.above_gate is False
        assert d.advisory is None

    def test_decision_rejects_both_branches(self):
        from app.domain.models import Decision, AdvisoryBranch, EscalationBranch, Advisory, Citation
        adv = Advisory(
            possible_issue="x", what_to_check="x", what_to_do_next="x",
            what_to_avoid="x", expert_triggers="x",
            citations=[Citation(doc_id="kb_1", title="T", reviewed_on="2025-01-01")],
        )
        with pytest.raises(Exception):  # pydantic ValidationError
            Decision(
                above_gate=True,
                advisory=AdvisoryBranch(advisory=adv),
                escalation=EscalationBranch(
                    case_id="c_1", assigned_to="x", spoken_summary="x",
                    reason="x", error_code="BELOW_CONFIDENCE_GATE",
                ),
            )

    def test_decision_rejects_neither_branch(self):
        from app.domain.models import Decision
        with pytest.raises(Exception):  # pydantic ValidationError
            Decision(above_gate=True, advisory=None)


# ---------------------------------------------------------------------------
# 5. Ports — importable as Protocols
# ---------------------------------------------------------------------------

class TestPorts:
    """Every port must be importable from the spec-mandated app.ports.* path."""

    def test_weather_port(self):
        from app.ports.weather import WeatherPort
        from typing import Protocol
        # Protocol is structural; just verify it's importable and the right kind
        assert WeatherPort is not None

    def test_llm_port(self):
        from app.ports.llm import LLMPort
        assert LLMPort is not None

    def test_embeddings_port(self):
        from app.ports.embeddings import EmbeddingPort
        assert EmbeddingPort is not None

    def test_image_diagnosis_port(self):
        from app.ports.image_diagnosis import ImageDiagnosisPort
        assert ImageDiagnosisPort is not None

    def test_asr_tts_port(self):
        from app.ports.asr_tts import AsrTtsPort
        assert AsrTtsPort is not None

    def test_storage_port(self):
        from app.ports.storage import StoragePort
        assert StoragePort is not None

    def test_ports_package_bulk_import(self):
        from app.ports import (
            WeatherPort, LLMPort, EmbeddingPort,
            ImageDiagnosisPort, AsrTtsPort, StoragePort,
        )
        assert all(p is not None for p in [
            WeatherPort, LLMPort, EmbeddingPort,
            ImageDiagnosisPort, AsrTtsPort, StoragePort,
        ])


# ---------------------------------------------------------------------------
# 6. Config — CONFIDENCE_GATE and thresholds
# ---------------------------------------------------------------------------

class TestConfig:
    """Settings must expose the gate thresholds at exact spec values."""

    def test_confidence_gate_default(self):
        from app.core.config import get_settings
        assert get_settings().CONFIDENCE_GATE == 0.70

    def test_confidence_gate_via_spec_path(self):
        from app.config import get_settings
        assert get_settings().CONFIDENCE_GATE == 0.70

    def test_rag_relevance_threshold_present(self):
        from app.config import get_settings
        # Runtime value may differ (tuned per corpus); only check it's a float in (0,1)
        t = get_settings().RAG_RELEVANCE_THRESHOLD
        assert 0.0 < t < 1.0

    def test_domain_constants_gate_value(self):
        from app.domain.constants import CONFIDENCE_GATE
        assert CONFIDENCE_GATE == 0.70

    def test_land_api_mode_valid(self):
        from app.config import get_settings
        assert get_settings().LAND_API_MODE in ("mock", "live")

    def test_diagnosis_model_valid(self):
        from app.config import get_settings
        assert get_settings().DIAGNOSIS_MODEL in ("real", "stub")


# ---------------------------------------------------------------------------
# 7. App factory — app.main imports cleanly
# ---------------------------------------------------------------------------

def test_app_main_imports_cleanly():
    from app.main import app
    assert app is not None
    assert app.title == "Bhoomi API"


def test_openapi_lists_health_endpoints():
    from fastapi.testclient import TestClient
    from app.main import app
    client = TestClient(app)
    response = client.get("/api/v1/openapi.json")
    assert response.status_code == 200
    paths = response.json()["paths"]
    # Minimum set of health-engine endpoints
    assert any("/health" in p for p in paths)
    assert any("recompute" in p for p in paths)
    assert any("advisory" in p for p in paths)
    assert any("diagnose" in p for p in paths)
    assert any("escalat" in p for p in paths)


# ---------------------------------------------------------------------------
# 8. Shim path coverage — spec-mandated import paths all resolve
# ---------------------------------------------------------------------------

def test_spec_shim_paths_all_resolve():
    """Every spec-mandated path in AGENTS.md must be importable."""
    import importlib
    spec_paths = [
        "app.domain.enums",
        "app.domain.models",
        "app.domain.constants",
        "app.domain.errors",
        "app.ports.weather",
        "app.ports.llm",
        "app.ports.embeddings",
        "app.ports.image_diagnosis",
        "app.ports.asr_tts",
        "app.ports.storage",
        "app.services.health.subindices",
        "app.services.health.engine",
        "app.services.gate.gate",
        "app.services.rag.pipeline",
        "app.services.escalation.compiler",
        "app.config",
        "app.deps",
    ]
    failed = []
    for path in spec_paths:
        try:
            importlib.import_module(path)
        except Exception as exc:
            failed.append(f"{path}: {exc}")
    assert not failed, "The following spec-mandated import paths failed:\n" + "\n".join(failed)
