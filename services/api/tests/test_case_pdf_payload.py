"""Tests for Case PDF / Share-sheet Backend Payload (Phase 4 Objective 2).

Verifies:
  1. CasePDFPayload is a strict presentation superset of the Phase 3 CaseSummaryBundle.
  2. Every bundle key (crop, region, growth_stage, problem_history, images, treatments_tried,
     followup_trend, current_advisory) is intact inside the payload's bundle.
  3. No fabricated fields or resurrected land/soil fields (area_acres_verified, soil_type, polygon)
     exist in the payload.
  4. End-to-end payload construction from AgronomistService.
"""

from datetime import datetime
import pytest
from app.core.enums import CaseStatus, ProblemSeverity
from app.domain.escalation import compile_case_summary_bundle, build_case_summary
from app.repositories.in_memory import (
    InMemoryCaseRepository,
    InMemoryFarmRepository,
    InMemoryHealthRepository,
)
from app.schemas.case import CaseSummaryBundle
from app.schemas.case_pdf import CasePDFPayload
from app.services.agronomist_service import AgronomistService
from app.services.escalation.pdf_payload import build_case_pdf_payload
from app.services.health_service import HealthService
from app.adapters.stubs import StubWeatherAdapter


class _FakeProblemWriter:
    async def resolve_problem(self, problem_id: str):
        pass


FARM_ID = "farm_pdf_001"
CASE_ID = "case_pdf_999"


def test_case_pdf_payload_is_strict_superset_of_bundle():
    """CasePDFPayload must contain all 8 bundle keys inside .bundle and 0 land/soil keys."""
    bundle_keys = set(CaseSummaryBundle.model_fields.keys())
    expected_bundle_keys = {
        "crop",
        "region",
        "growth_stage",
        "problem_history",
        "images",
        "treatments_tried",
        "followup_trend",
        "current_advisory",
    }
    assert bundle_keys == expected_bundle_keys

    pdf_fields = set(CasePDFPayload.model_fields.keys())
    assert "bundle" in pdf_fields

    # Drift guard: No resurrected land/soil or geometry fields
    forbidden_keys = {
        "area_acres_verified",
        "soil_type",
        "total_area_acres",
        "boundary_geojson",
        "polygon",
        "Polygon",
        "cadastral_survey_number",
    }
    assert not (pdf_fields & forbidden_keys), f"Forbidden fields in PDF payload: {pdf_fields & forbidden_keys}"
    assert not (bundle_keys & forbidden_keys), f"Forbidden fields in bundle: {bundle_keys & forbidden_keys}"


def test_build_case_pdf_payload_direct():
    """build_case_pdf_payload builds clean structured payload from CaseSummary."""
    bundle = compile_case_summary_bundle(
        crop="samba_paddy",
        region="Madurai, Tamil Nadu",
        growth_stage="Tillering",
        problem_history=[{"problem": "Bacterial Leaf Blight", "severity": "moderate"}],
        images=["asset_img_01.jpg"],
        treatments_tried=["Copper Hydroxide spray"],
        followup_trend="got_worse",
        current_advisory="Drain field water and suspend nitrogen top-dressing.",
    )

    case_summary = build_case_summary(
        case_id=CASE_ID,
        farm_info={
            "id": FARM_ID,
            "farmer_name": "Kavitha",
            "village": "Alanganallur",
            "district": "Madurai",
            "primary_crop": "samba_paddy",
        },
        recent_events=[],
        current_health_score=68.0,
        problem_details={"severity": ProblemSeverity.MODERATE, "label": "bacterial_leaf_blight"},
        assigned_officer_or_kvk="TNAU KVK Madurai",
        status=CaseStatus.ESCALATED,
    )
    # Attach compiled bundle
    case_summary.bundle = bundle

    payload = build_case_pdf_payload(
        case_summary=case_summary,
        assigned_kvk="TNAU KVK Madurai",
        share_url=f"/cases/{CASE_ID}/share",
    )

    assert isinstance(payload, CasePDFPayload)
    assert payload.case_id == CASE_ID
    assert payload.farm_id == FARM_ID
    assert payload.farmer_name == "Kavitha"
    assert payload.village == "Alanganallur"
    assert payload.district == "Madurai"
    assert payload.assigned_kvk == "TNAU KVK Madurai"
    assert payload.severity == "moderate"
    assert payload.status == "escalated"
    assert payload.bundle.crop == "samba_paddy"
    assert payload.bundle.region == "Madurai, Tamil Nadu"
    assert payload.bundle.followup_trend == "got_worse"
    assert "Samba Paddy" in payload.summary_headline or "Rice" in payload.summary_headline


class _DummyHealthService:
    async def get_latest(self, farm_id: str):
        class _Snap:
            score = 68.0
        return _Snap()


@pytest.mark.asyncio
async def test_get_case_pdf_payload_from_agronomist_service():
    """AgronomistService.get_case_pdf_payload returns complete typed CasePDFPayload."""
    case_repo = InMemoryCaseRepository()
    farm_repo = InMemoryFarmRepository()
    health_service = _DummyHealthService()
    problem_repo = _FakeProblemWriter()

    service = AgronomistService(
        case_repo=case_repo,
        farm_repo=farm_repo,
        health_service=health_service,
        problem_writer=problem_repo,
    )

    # Seed farm and case
    await farm_repo.save({
        "id": FARM_ID,
        "farm_name": "Muthu Farm",
        "primary_crop": "samba_paddy",
        "village": "Samayanallur",
        "district": "Madurai",
        "growth_stage": "Flowering",
    })

    await case_repo.save({
        "id": CASE_ID,
        "farm_id": FARM_ID,
        "severity": ProblemSeverity.SEVERE.value,
        "status": CaseStatus.ESCALATED.value,
        "assigned_to": "TNAU KVK Madurai",
        "reason": "Brown planthopper resurgence past threshold",
    })

    pdf_payload = await service.get_case_pdf_payload(CASE_ID)

    assert isinstance(pdf_payload, CasePDFPayload)
    assert pdf_payload.case_id == CASE_ID
    assert pdf_payload.farm_id == FARM_ID
    assert pdf_payload.farmer_name == "Muthu Farm"
    assert pdf_payload.village == "Samayanallur"
    assert pdf_payload.district == "Madurai"
    assert pdf_payload.severity == "severe"
    assert pdf_payload.status == "escalated"
    assert pdf_payload.bundle.crop in ("samba_paddy", "Rice")
    assert pdf_payload.generated_at is not None
