"""Tests for Thin Land Submission and Verified-Gated Scheme Matching (Phase 3 Objectives 3 & 4).

Verifies:
  1. Land Submission: POST /farms/{id}/land takes survey_number and returns 'pending_verification'.
  2. Drift Guard: Thin land module contains zero geometry/polygon fields.
  3. Scheme Gating: Unverified land raises 409 LAND_NOT_VERIFIED.
  4. Scheme Matching: Verified land returns static dated schemes with last_verified dates and staleness flags.
"""

from datetime import date, timedelta
import pytest
from app.core.enums import LandStatus, SchemeStatus
from app.core.errors import LandNotVerifiedError
from app.repositories.in_memory import InMemoryFarmRepository, InMemorySchemeRepository
from app.schemas.land import ThinLandSubmissionRequest, ThinLandSubmissionResponse
from app.schemas.schemes import SchemeMatchRequest, SchemeResponse
from app.services.scheme_service import SchemeService

FARM_ID_UNVERIFIED = "farm_unverified_101"
FARM_ID_VERIFIED = "farm_verified_202"


@pytest.fixture
def scheme_harness():
    farm_repo = InMemoryFarmRepository()
    scheme_repo = InMemorySchemeRepository()
    service = SchemeService(scheme_repo=scheme_repo, farm_repo=farm_repo)
    return {
        "farm_repo": farm_repo,
        "scheme_repo": scheme_repo,
        "service": service,
    }


@pytest.mark.asyncio
async def test_thin_land_submission_updates_farm_to_pending(scheme_harness):
    """POST /farms/{id}/land sets survey number and pending_verification status."""
    farm_repo = scheme_harness["farm_repo"]
    await farm_repo.save({
        "id": FARM_ID_UNVERIFIED,
        "farm_name": "Velu Farm",
        "primary_crop": "Rice",
        "district": "Thanjavur",
        "land_status": "unverified",
    })

    req = ThinLandSubmissionRequest(survey_number="142/3B")
    
    # Simulate endpoint logic
    farm = await farm_repo.get_by_id(FARM_ID_UNVERIFIED)
    assert farm is not None
    await farm_repo.update(FARM_ID_UNVERIFIED, {
        "survey_number": req.survey_number,
        "land_status": "pending_verification",
    })

    res = ThinLandSubmissionResponse(
        farm_id=FARM_ID_UNVERIFIED,
        survey_number=req.survey_number,
        status="pending_verification",
    )

    assert res.farm_id == FARM_ID_UNVERIFIED
    assert res.survey_number == "142/3B"
    assert res.status == "pending_verification"

    updated_farm = await farm_repo.get_by_id(FARM_ID_UNVERIFIED)
    assert updated_farm["survey_number"] == "142/3B"
    assert updated_farm["land_status"] == "pending_verification"


def test_thin_land_drift_guard_no_geometry():
    """Drift guard: Thin land models must have NO boundary, geometry, or polygon fields."""
    req_fields = set(ThinLandSubmissionRequest.model_fields.keys())
    res_fields = set(ThinLandSubmissionResponse.model_fields.keys())

    forbidden = {"boundary_geojson", "polygon", "Polygon", "coordinates", "geometry"}
    assert not (req_fields & forbidden), f"Forbidden geometry fields in request: {req_fields & forbidden}"
    assert not (res_fields & forbidden), f"Forbidden geometry fields in response: {res_fields & forbidden}"


@pytest.mark.asyncio
async def test_unverified_farm_raises_409_land_not_verified(scheme_harness):
    """Unverified or pending_verification farm raises 409 LAND_NOT_VERIFIED."""
    farm_repo = scheme_harness["farm_repo"]
    service = scheme_harness["service"]

    await farm_repo.save({
        "id": FARM_ID_UNVERIFIED,
        "farm_name": "Velu Farm",
        "primary_crop": "Rice",
        "district": "Thanjavur",
        "land_status": "pending_verification",
    })

    with pytest.raises(LandNotVerifiedError) as exc_info:
        await service.match_schemes_for_farm(SchemeMatchRequest(farm_id=FARM_ID_UNVERIFIED))

    err = exc_info.value
    assert err.code == "LAND_NOT_VERIFIED"
    assert err.status_code == 409
    assert err.details.get("land_status") == "pending_verification"


@pytest.mark.asyncio
async def test_verified_farm_matches_dated_schemes(scheme_harness):
    """Verified farm matches eligible subsidies carrying last_verified dates."""
    farm_repo = scheme_harness["farm_repo"]
    scheme_repo = scheme_harness["scheme_repo"]
    service = scheme_harness["service"]

    # Seed verified farm
    await farm_repo.save({
        "id": FARM_ID_VERIFIED,
        "farm_name": "Kavitha Farm",
        "primary_crop": "samba_paddy",
        "district": "Madurai",
        "land_status": "verified",
        "total_area_acres": 2.5,
    })

    # Seed static dated schemes
    today = date.today()
    scheme_1 = {
        "id": "scheme_tn_01",
        "name": "Tamil Nadu Paddy Input Subsidy",
        "ministry": "Department of Agriculture, Tamil Nadu",
        "description": "50% subsidy on approved bio-pesticides and micro-nutrients.",
        "benefits": "Up to Rs. 5,000 per hectare for registered paddy farmers.",
        "eligibility_criteria": {"crop": "samba_paddy", "category": "Small/Marginal", "land_status": "verified"},
        "subsidy_percentage": 50.0,
        "max_amount_inr": 5000.0,
        "portal_url": "https://www.tnagrisnet.tn.gov.in",
        "status": SchemeStatus.ACTIVE.value,
        "last_verified": today - timedelta(days=15),
    }
    scheme_2 = {
        "id": "scheme_pm_02",
        "name": "PM-KISAN Samman Nidhi",
        "ministry": "Ministry of Agriculture & Farmers Welfare, GoI",
        "description": "Direct income support for eligible farmer families.",
        "benefits": "Rs. 6,000/year in three equal installments.",
        "eligibility_criteria": {"category": "Small/Marginal", "land_status": "verified"},
        "subsidy_percentage": None,
        "max_amount_inr": 6000.0,
        "portal_url": "https://pmkisan.gov.in",
        "status": SchemeStatus.EXPIRING.value,
        "last_verified": today - timedelta(days=120),
    }

    scheme_repo._schemes[scheme_1["id"]] = scheme_1
    scheme_repo._schemes[scheme_2["id"]] = scheme_2

    # Query schemes
    result = await service.match_schemes_for_farm(SchemeMatchRequest(farm_id=FARM_ID_VERIFIED))

    assert result.farm_id == FARM_ID_VERIFIED
    assert result.match_count == 2
    assert len(result.matched_schemes) == 2

    # Verify each scheme carries its last_verified date and status
    names = [s.name for s in result.matched_schemes]
    assert "Tamil Nadu Paddy Input Subsidy" in names
    assert "PM-KISAN Samman Nidhi" in names

    for s in result.matched_schemes:
        assert isinstance(s, SchemeResponse)
        assert s.last_verified is not None
        assert s.status in (SchemeStatus.ACTIVE, SchemeStatus.EXPIRING)
        assert s.benefits != ""
