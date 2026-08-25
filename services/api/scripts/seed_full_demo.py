"""Staged Demo Fixture Generator (Phase 3 & 4).

Generates the complete Ramesh demo lifecycle at each exact state with deterministic health scores:
  - baseline:  Score 82 (band: good) — Onboarded farm + clean baseline
  - diagnosed: Score 68 (band: watch) — BLB disease diagnosed (moderate)
  - escalated: Score 59 (band: poor) — Followup got_worse + Case escalated to Dr. Lakshmi
  - resolved:  Score 86 (band: good) — Case resolved with prescription + problem resolved
  - full:      Full history tracking the complete 82 -> 68 -> 59 -> 86 walkthrough

Usage:
    python -m scripts.seed_full_demo --stage [baseline|diagnosed|escalated|resolved|full]
"""

from __future__ import annotations

import argparse
import asyncio
from datetime import date, datetime, timedelta
import uuid

from sqlalchemy import delete, select

from app.core.db import AsyncSessionLocal
from app.core.enums import (
    CaseStatus,
    FollowupResponse,
    HealthBand,
    LandStatus,
    ProblemSeverity,
    ProblemStatus,
    SchemeStatus,
    SubIndexKey,
    UserRole,
)
from app.core.security import get_password_hash
from app.domain.farm_reference_data import get_expected_stage_day
from app.domain.health.constants import WEIGHTS_V2_SIH26131, WEIGHTS_VERSION
from app.models.advisory import Advisory
from app.models.case import Case
from app.models.farm import Farm
from app.models.followup import FollowUp
from app.models.health_snapshot import HealthSnapshot
from app.models.land_parcel import LandParcel
from app.models.problem import Problem
from app.models.scheme import Scheme
from app.models.user import User

FARMER_PHONE = "+919944400001"
OFFICER_PHONE = "+919944400002"
AGRONOMIST_PHONE = "+919944400003"
DEMO_PASSWORD = "bhoomi123"

SAMPLE_BOUNDARY_GEOJSON = {
    "type": "Polygon",
    "coordinates": [[
        [77.7085, 11.3395],
        [77.7115, 11.3395],
        [77.7115, 11.3415],
        [77.7085, 11.3415],
        [77.7085, 11.3395],
    ]],
}


def _make_snapshot(farm_id: str, score: int, band: HealthBand, subindices: dict[str, float], dt: datetime) -> HealthSnapshot:
    # Matches app/models/health_snapshot.py's actual columns (``band``,
    # ``weights_version``) and the ``{"key", "value", "weight",
    # "contribution"}`` subindex shape the API contract returns — this
    # script previously used ``health_band``/``rubric_version``, which
    # don't exist on the model, and a bare ``{"key", "value"}`` shape.
    weight = WEIGHTS_V2_SIH26131
    subindices_list = [
        {
            "key": k,
            "value": v,
            "weight": weight[SubIndexKey(k)],
            "contribution": round(v * weight[SubIndexKey(k)], 2),
        }
        for k, v in subindices.items()
    ]
    snapshot = HealthSnapshot(
        id=str(uuid.uuid4()),
        farm_id=farm_id,
        score=score,
        band=band.value,
        subindices=subindices_list,
        weights_version=WEIGHTS_VERSION,
        computed_at=dt,
        missing_fields=[],
    )
    snapshot.created_at = dt
    snapshot.updated_at = dt
    return snapshot


async def seed_stage(stage: str = "full") -> dict:
    async with AsyncSessionLocal() as session:
        # Cleanup
        users = (await session.execute(select(User).where(User.phone_number.in_([FARMER_PHONE, OFFICER_PHONE, AGRONOMIST_PHONE])))).scalars().all()
        for u in users:
            farms = (await session.execute(select(Farm).where(Farm.farmer_id == u.id))).scalars().all()
            for f in farms:
                await session.execute(delete(HealthSnapshot).where(HealthSnapshot.farm_id == f.id))
                await session.execute(delete(Advisory).where(Advisory.farm_id == f.id))
                await session.execute(delete(Case).where(Case.farm_id == f.id))
                await session.execute(delete(FollowUp).where(FollowUp.farm_id == f.id))
                await session.execute(delete(Problem).where(Problem.farm_id == f.id))
                await session.execute(delete(LandParcel).where(LandParcel.farm_id == f.id))
                await session.delete(f)
            await session.delete(u)
        await session.execute(delete(Scheme).where(Scheme.name.in_(["TN Crop Protection Subsidy", "PM-KISAN Samman Nidhi"])))
        await session.commit()

        # Seed Users
        pw = get_password_hash(DEMO_PASSWORD)
        farmer = User(id=str(uuid.uuid4()), phone_number=FARMER_PHONE, email="ramesh@bhoomi.demo", full_name="Ramesh", role=UserRole.FARMER.value, preferred_language="ta", password_hash=pw)
        officer = User(id=str(uuid.uuid4()), phone_number=OFFICER_PHONE, email="kumar@bhoomi.demo", full_name="Officer Kumar", role=UserRole.OFFICER.value, preferred_language="ta", password_hash=pw, jurisdiction="taluk_erode")
        agronomist = User(id=str(uuid.uuid4()), phone_number=AGRONOMIST_PHONE, email="lakshmi@bhoomi.demo", full_name="Dr. Lakshmi", role=UserRole.AGRONOMIST.value, preferred_language="ta", password_hash=pw, jurisdiction="kvk_erode")
        session.add_all([farmer, officer, agronomist])
        await session.flush()

        # Seed Farm
        farm_id = str(uuid.uuid4())
        farm = Farm(
            id=farm_id,
            farmer_id=farmer.id,
            farm_name="Ramesh's Paddy Farm",
            village="Chithode",
            taluk="Erode",
            district="Erode",
            state="Tamil Nadu",
            latitude=11.3400,
            longitude=77.7100,
            total_area_acres=2.0,
            survey_number="142/3B",
            land_status=LandStatus.VERIFIED.value,
            primary_crop="samba_paddy",
            growth_stage="vegetative",
            soil_type="clay_loam",
            irrigation_source="canal",
            soil_moisture_pct=45.0,
            days_since_planting=20,
            expected_stage_day=get_expected_stage_day("vegetative"),
            days_since_last_scan=2,
            irrigation_delivered_mm=25.0,
            irrigation_required_mm=25.0,
        )
        session.add(farm)

        # Land parcel
        parcel = LandParcel(
            id=str(uuid.uuid4()),
            farm_id=farm_id,
            survey_number="142/3B",
            district="Erode",
            status=LandStatus.VERIFIED.value,
            auto_lookup_outcome="matched",
            suggested_boundary=SAMPLE_BOUNDARY_GEOJSON,
            confirmed_boundary=SAMPLE_BOUNDARY_GEOJSON,
            verified_by=officer.id,
            verified_at=datetime.utcnow() - timedelta(days=28),
        )
        session.add(parcel)

        now = datetime.utcnow()

        # Baseline snapshot (Score 82)
        # Keyed to the live 4 sub-index SIH26131 risk model (SubIndexKey,
        # app/domain/health/constants.py) — this script previously wrote
        # the retired 6-key v1 names (ENVIRONMENTAL_SUITABILITY,
        # RESOURCE_ADEQUACY, CROP_STAGE_PROGRESSION, ACTIVE_PROBLEM_LOAD),
        # which no longer exist on SubIndexKey and made `make seed` crash
        # with AttributeError before a single row was written.
        base_subindices = {
            SubIndexKey.ACTIVE_PROBLEM_SEVERITY.value: 90.0,
            SubIndexKey.ENVIRONMENTAL_RISK.value: 85.0,
            SubIndexKey.MONITORING_RECENCY.value: 78.0,
            SubIndexKey.TREATMENT_RESPONSE.value: 75.0,
        }
        s1 = _make_snapshot(farm_id, 82, HealthBand.GOOD, base_subindices, now - timedelta(days=7))
        session.add(s1)

        # Stage 2: Diagnosed (Score 68)
        problem_id = str(uuid.uuid4())
        if stage in ["diagnosed", "escalated", "resolved", "full"]:
            prob = Problem(
                id=problem_id,
                farm_id=farm_id,
                label="Bacterial Leaf Blight (BLB)",
                severity=ProblemSeverity.MODERATE.value,
                status=ProblemStatus.OPEN.value if stage in ["diagnosed", "escalated"] else ProblemStatus.RESOLVED.value,
                resolved_at=now - timedelta(hours=2) if stage in ["resolved", "full"] else None,
            )
            prob.created_at = now - timedelta(days=4)
            session.add(prob)

            # Advisory
            adv = Advisory(
                id=str(uuid.uuid4()),
                farm_id=farm_id,
                problem_id=problem_id,
                possible_issue="Bacterial Leaf Blight (BLB) — Xanthomonas oryzae",
                what_to_check="Yellow translucent lesions along leaf margins spreading from tips.",
                what_to_do_next="Apply Copper Hydroxide 77% WP at 2.5 g/L. Drain excess standing water.",
                what_to_avoid="Do not apply nitrogen top-dressing during active infection.",
                expert_triggers="If lesions spread to >30% canopy within 7 days, escalate to KVK.",
                citations=[{"doc_id": "rice_blb", "title": "ICAR PoP: Rice — Bacterial Leaf Blight", "reviewed_on": "2025-11-02"}],
                confidence=0.88,
                model_version="bhoomi-rag-v1",
                lang="ta-IN",
            )
            session.add(adv)

            diag_subindices = {
                **base_subindices,
                SubIndexKey.ACTIVE_PROBLEM_SEVERITY.value: 55.0,
                SubIndexKey.TREATMENT_RESPONSE.value: 60.0,
            }
            s2 = _make_snapshot(farm_id, 68, HealthBand.WATCH, diag_subindices, now - timedelta(days=4))
            session.add(s2)

        # Stage 3: Escalated (Score 59)
        case_id = str(uuid.uuid4())
        if stage in ["escalated", "resolved", "full"]:
            fu = FollowUp(
                id=str(uuid.uuid4()),
                problem_id=problem_id,
                farm_id=farm_id,
                response=FollowupResponse.GOT_WORSE.value,
                farmer_notes="இலைகளில் மஞ்சள் நிறம் வேகமாகப் பரவுகிறது",
            )
            fu.created_at = now - timedelta(days=2)
            session.add(fu)

            c = Case(
                id=case_id,
                farm_id=farm_id,
                problem_id=problem_id,
                reason="BLB symptoms expanded rapidly after rain; follow-up worsened.",
                severity=ProblemSeverity.SEVERE.value,
                status=CaseStatus.ASSIGNED.value if stage == "escalated" else CaseStatus.RESOLVED.value,
                assigned_to=agronomist.id,
                case_summary={
                    "farmer_name": "Ramesh",
                    "crop": "Samba Paddy",
                    "disease": "Bacterial Leaf Blight",
                    "initial_severity": "moderate",
                    "followup": "got_worse",
                },
                resolution={
                    "prescribed_treatment": "Copper Hydroxide 77% WP @ 2.5g/L + field drainage for 48h",
                    "notes": "Verified BLB spread. Advised immediate drainage and strict nitrogen pause.",
                } if stage in ["resolved", "full"] else None,
                resolved_at=now - timedelta(hours=2) if stage in ["resolved", "full"] else None,
            )
            c.created_at = now - timedelta(days=2)
            session.add(c)

            esc_subindices = {
                **base_subindices,
                SubIndexKey.ACTIVE_PROBLEM_SEVERITY.value: 35.0,
                SubIndexKey.TREATMENT_RESPONSE.value: 40.0,
            }
            s3 = _make_snapshot(farm_id, 59, HealthBand.POOR, esc_subindices, now - timedelta(days=2))
            session.add(s3)

        # Stage 4: Resolved (Score 86)
        if stage in ["resolved", "full"]:
            fu_resolved = FollowUp(
                id=str(uuid.uuid4()),
                problem_id=problem_id,
                farm_id=farm_id,
                response=FollowupResponse.IMPROVED.value,
                farmer_notes="தண்ணீர் வடித்த பிறகு இலைகள் நலம் பெறுகின்றன",
            )
            fu_resolved.created_at = now - timedelta(hours=2)
            session.add(fu_resolved)

            res_subindices = {
                **base_subindices,
                SubIndexKey.ACTIVE_PROBLEM_SEVERITY.value: 95.0,
                SubIndexKey.TREATMENT_RESPONSE.value: 92.0,
                SubIndexKey.MONITORING_RECENCY.value: 90.0,
            }
            s4 = _make_snapshot(farm_id, 86, HealthBand.GOOD, res_subindices, now)
            session.add(s4)

        # Commit everything
        await session.commit()

        print(f"[OK] Seeded stage: [{stage.upper()}]")
        print(f"  Farmer ID:     {farmer.id}")
        print(f"  Farm ID:       {farm_id}")
        if stage == "baseline":
            print("  Score Track:   82 (good)")
        elif stage == "diagnosed":
            print("  Score Track:   82 -> 68 (watch)")
        elif stage == "escalated":
            print("  Score Track:   82 -> 68 -> 59 (poor)")
        elif stage in ["resolved", "full"]:
            print("  Score Track:   82 -> 68 -> 59 -> 86 (good) [resolved]")

        return {"farm_id": farm_id, "farmer_id": farmer.id, "stage": stage}


async def main() -> None:
    parser = argparse.ArgumentParser(description="Seed staged demo fixtures")
    parser.add_argument(
        "--stage",
        choices=["baseline", "diagnosed", "escalated", "resolved", "full"],
        default="full",
        help="Demo progression stage to seed",
    )
    args = parser.parse_args()
    await seed_stage(args.stage)


if __name__ == "__main__":
    asyncio.run(main())
