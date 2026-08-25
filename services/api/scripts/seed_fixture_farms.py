"""Seed additional fixture farms covering non-Ramesh states and pest lifecycles.

Fixtures seeded:
  1. unrated:       Fresh onboarded farm, no monitoring data, no diagnosis
  2. healthy:       Resource plan run, good health score, no open problem
  3. pest_open:     target_type="pest", stem_borer label, above PEST_CONFIDENCE_GATE,
                    open Problem row with target_type="pest"
  4. pest_no_corpus: target_type="pest", whitefly label (in-scope, zero corpus content),
                    demonstrates escalate path for pest
  5. pest_escalate: got_worse followup on a pest Problem, Case row created,
                    routed to Dr. Lakshmi (+919944400003)
  6. pest_resolved: Case resolved, Problem cleared, target_type retained on closed record

Usage:
    python -m scripts.seed_fixture_farms --stage [unrated|healthy|pest_open|pest_no_corpus|pest_escalate|pest_resolved|full]
"""

from __future__ import annotations

import argparse
import asyncio
from datetime import datetime, timedelta
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
from app.models.problem import Problem
from app.models.user import User

DEMO_PASSWORD = "bhoomi123"
AGRONOMIST_PHONE = "+919944400003"

FIXTURE_STAGES = {
    "unrated": "+919944400011",
    "healthy": "+919944400012",
    "pest_open": "+919944400013",
    "pest_no_corpus": "+919944400014",
    "pest_escalate": "+919944400015",
    "pest_resolved": "+919944400016",
}


def _make_snapshot(farm_id: str, score: int, band: HealthBand, subindices: dict[str, float], dt: datetime) -> HealthSnapshot:
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


async def _delete_existing_phones(session, phones: list[str]) -> None:
    users = (await session.execute(select(User).where(User.phone_number.in_(phones)))).scalars().all()
    for u in users:
        farms = (await session.execute(select(Farm).where(Farm.farmer_id == u.id))).scalars().all()
        for f in farms:
            await session.execute(delete(HealthSnapshot).where(HealthSnapshot.farm_id == f.id))
            await session.execute(delete(Advisory).where(Advisory.farm_id == f.id))
            await session.execute(delete(Case).where(Case.farm_id == f.id))
            await session.execute(delete(FollowUp).where(FollowUp.farm_id == f.id))
            await session.execute(delete(Problem).where(Problem.farm_id == f.id))
            await session.delete(f)
        await session.delete(u)
    await session.commit()


async def _get_or_create_agronomist(session) -> User:
    stmt = select(User).where(User.phone_number == AGRONOMIST_PHONE)
    agron = (await session.execute(stmt)).scalars().first()
    if agron is None:
        pw = get_password_hash(DEMO_PASSWORD)
        agron = User(
            id=str(uuid.uuid4()),
            phone_number=AGRONOMIST_PHONE,
            email="lakshmi@bhoomi.demo",
            full_name="Dr. Lakshmi",
            role=UserRole.AGRONOMIST.value,
            preferred_language="ta",
            password_hash=pw,
            jurisdiction="kvk_erode",
        )
        session.add(agron)
        await session.flush()
    return agron


async def seed_fixture_stage(stage: str = "full") -> dict:
    stages_to_seed = list(FIXTURE_STAGES.keys()) if stage == "full" else [stage]
    phones_to_clean = [FIXTURE_STAGES[s] for s in stages_to_seed]

    async with AsyncSessionLocal() as session:
        await _delete_existing_phones(session, phones_to_clean)
        pw = get_password_hash(DEMO_PASSWORD)
        now = datetime.utcnow()
        results = {}

        agron = await _get_or_create_agronomist(session)

        if "unrated" in stages_to_seed:
            farmer = User(
                id=str(uuid.uuid4()),
                phone_number=FIXTURE_STAGES["unrated"],
                email="karthik@bhoomi.demo",
                full_name="Karthik",
                role=UserRole.FARMER.value,
                preferred_language="ta",
                password_hash=pw,
            )
            session.add(farmer)
            await session.flush()

            farm = Farm(
                id=str(uuid.uuid4()),
                farmer_id=farmer.id,
                farm_name="Karthik's Paddy Field",
                village="Tiruchengodu",
                taluk="Tiruchengodu",
                district="Namakkal",
                region="Namakkal",
                state="Tamil Nadu",
                primary_crop="samba_paddy",
                growth_stage="seedling",
                expected_stage_day=get_expected_stage_day("seedling"),
                land_status=LandStatus.UNVERIFIED.value,
            )
            session.add(farm)
            results["unrated"] = {"farmer_id": farmer.id, "farm_id": farm.id}

        if "healthy" in stages_to_seed:
            farmer = User(
                id=str(uuid.uuid4()),
                phone_number=FIXTURE_STAGES["healthy"],
                email="priya@bhoomi.demo",
                full_name="Priya",
                role=UserRole.FARMER.value,
                preferred_language="ta",
                password_hash=pw,
            )
            session.add(farmer)
            await session.flush()

            farm_id = str(uuid.uuid4())
            farm = Farm(
                id=farm_id,
                farmer_id=farmer.id,
                farm_name="Priya's Green Farm",
                village="Veerapandi",
                taluk="Salem",
                district="Salem",
                region="Salem",
                state="Tamil Nadu",
                latitude=11.66,
                longitude=78.14,
                total_area_acres=3.0,
                land_status=LandStatus.VERIFIED.value,
                primary_crop="samba_paddy",
                growth_stage="vegetative",
                soil_type="clay_loam",
                irrigation_source="canal",
                soil_moisture_pct=48.0,
                days_since_planting=25,
                expected_stage_day=get_expected_stage_day("vegetative"),
                days_since_last_scan=1,
                irrigation_delivered_mm=30.0,
                irrigation_required_mm=30.0,
            )
            session.add(farm)

            subindices = {
                SubIndexKey.ACTIVE_PROBLEM_SEVERITY.value: 100.0,
                SubIndexKey.ENVIRONMENTAL_RISK.value: 88.0,
                SubIndexKey.MONITORING_RECENCY.value: 90.0,
                SubIndexKey.TREATMENT_RESPONSE.value: 75.0,
            }
            snap = _make_snapshot(farm_id, 85, HealthBand.GOOD, subindices, now)
            session.add(snap)
            results["healthy"] = {"farmer_id": farmer.id, "farm_id": farm_id}

        if "pest_open" in stages_to_seed:
            farmer = User(
                id=str(uuid.uuid4()),
                phone_number=FIXTURE_STAGES["pest_open"],
                email="murugan@bhoomi.demo",
                full_name="Murugan",
                role=UserRole.FARMER.value,
                preferred_language="ta",
                password_hash=pw,
            )
            session.add(farmer)
            await session.flush()

            farm_id = str(uuid.uuid4())
            farm = Farm(
                id=farm_id,
                farmer_id=farmer.id,
                farm_name="Murugan's Paddy Field",
                village="Melur",
                taluk="Madurai",
                district="Madurai",
                region="Madurai",
                state="Tamil Nadu",
                latitude=9.92,
                longitude=78.11,
                total_area_acres=2.5,
                land_status=LandStatus.VERIFIED.value,
                primary_crop="samba_paddy",
                growth_stage="vegetative",
                soil_type="clay_loam",
                irrigation_source="canal",
                soil_moisture_pct=42.0,
                days_since_planting=20,
                expected_stage_day=get_expected_stage_day("vegetative"),
                days_since_last_scan=2,
            )
            session.add(farm)

            prob_id = str(uuid.uuid4())
            prob = Problem(
                id=prob_id,
                farm_id=farm_id,
                label="stem_borer",
                severity=ProblemSeverity.EARLY.value,
                status=ProblemStatus.OPEN.value,
                target_type="pest",
                image_asset_id="pest-photo-stem-borer",
            )
            prob.created_at = now - timedelta(days=2)
            session.add(prob)

            adv = Advisory(
                id=str(uuid.uuid4()),
                farm_id=farm_id,
                problem_id=prob_id,
                possible_issue="Rice Yellow Stem Borer (Scirpophaga incertulas)",
                what_to_check="Check for deadhearts in vegetative stage and whiteheads in reproductive stage.",
                what_to_do_next="Install light traps at 1 per acre and release Trichogramma japonicum egg parasitoids at 100,000/ha.",
                what_to_avoid="Avoid excessive nitrogen application which attracts ovipositing moths.",
                expert_triggers="If deadheart damage exceeds 10%, consult KVK agronomist.",
                citations=[{"doc_id": "kb_p301", "title": "ICAR PoP: Rice Stem Borer Management", "reviewed_on": "2025-11-01"}],
                confidence=0.88,
                model_version="bhoomi-rag-v1",
                lang="ta-IN",
            )
            session.add(adv)

            subindices = {
                SubIndexKey.ACTIVE_PROBLEM_SEVERITY.value: 65.0,
                SubIndexKey.ENVIRONMENTAL_RISK.value: 80.0,
                SubIndexKey.MONITORING_RECENCY.value: 75.0,
                SubIndexKey.TREATMENT_RESPONSE.value: 70.0,
            }
            snap = _make_snapshot(farm_id, 68, HealthBand.WATCH, subindices, now)
            session.add(snap)
            results["pest_open"] = {"farmer_id": farmer.id, "farm_id": farm_id, "problem_id": prob_id}

        if "pest_no_corpus" in stages_to_seed:
            farmer = User(
                id=str(uuid.uuid4()),
                phone_number=FIXTURE_STAGES["pest_no_corpus"],
                email="anbu@bhoomi.demo",
                full_name="Anbu",
                role=UserRole.FARMER.value,
                preferred_language="ta",
                password_hash=pw,
            )
            session.add(farmer)
            await session.flush()

            farm_id = str(uuid.uuid4())
            farm = Farm(
                id=farm_id,
                farmer_id=farmer.id,
                farm_name="Anbu's Paddy Farm",
                village="Lalgudi",
                taluk="Trichy",
                district="Trichy",
                region="Trichy",
                state="Tamil Nadu",
                total_area_acres=1.5,
                land_status=LandStatus.VERIFIED.value,
                primary_crop="samba_paddy",
                growth_stage="vegetative",
                days_since_planting=22,
                expected_stage_day=get_expected_stage_day("vegetative"),
                days_since_last_scan=2,
            )
            session.add(farm)

            prob_id = str(uuid.uuid4())
            prob = Problem(
                id=prob_id,
                farm_id=farm_id,
                label="whitefly",
                severity=ProblemSeverity.EARLY.value,
                status=ProblemStatus.OPEN.value,
                target_type="pest",
                image_asset_id="pest-photo-whitefly",
            )
            prob.created_at = now - timedelta(days=1)
            session.add(prob)

            case_id = str(uuid.uuid4())
            case = Case(
                id=case_id,
                farm_id=farm_id,
                problem_id=prob_id,
                reason="NO_RELEVANT_SOURCE: No relevant source document available for whitefly",
                severity=ProblemSeverity.EARLY.value,
                status=CaseStatus.ASSIGNED.value,
                assigned_to=agron.id,
                case_summary={
                    "farmer_name": "Anbu",
                    "crop": "Samba Paddy",
                    "pest": "whitefly",
                    "reason": "NO_RELEVANT_SOURCE",
                },
            )
            case.created_at = now - timedelta(days=1)
            session.add(case)

            subindices = {
                SubIndexKey.ACTIVE_PROBLEM_SEVERITY.value: 60.0,
                SubIndexKey.ENVIRONMENTAL_RISK.value: 75.0,
                SubIndexKey.MONITORING_RECENCY.value: 70.0,
                SubIndexKey.TREATMENT_RESPONSE.value: 65.0,
            }
            snap = _make_snapshot(farm_id, 62, HealthBand.WATCH, subindices, now)
            session.add(snap)
            results["pest_no_corpus"] = {"farmer_id": farmer.id, "farm_id": farm_id, "problem_id": prob_id, "case_id": case_id}

        if "pest_escalate" in stages_to_seed:
            farmer = User(
                id=str(uuid.uuid4()),
                phone_number=FIXTURE_STAGES["pest_escalate"],
                email="senthil@bhoomi.demo",
                full_name="Senthil",
                role=UserRole.FARMER.value,
                preferred_language="ta",
                password_hash=pw,
            )
            session.add(farmer)
            await session.flush()

            farm_id = str(uuid.uuid4())
            farm = Farm(
                id=farm_id,
                farmer_id=farmer.id,
                farm_name="Senthil's Paddy Farm",
                village="Perundurai",
                taluk="Erode",
                district="Erode",
                region="Erode",
                state="Tamil Nadu",
                total_area_acres=2.0,
                land_status=LandStatus.VERIFIED.value,
                primary_crop="samba_paddy",
                growth_stage="vegetative",
                days_since_planting=30,
                expected_stage_day=get_expected_stage_day("vegetative"),
                days_since_last_scan=1,
            )
            session.add(farm)

            prob_id = str(uuid.uuid4())
            prob = Problem(
                id=prob_id,
                farm_id=farm_id,
                label="stem_borer",
                severity=ProblemSeverity.SEVERE.value,
                status=ProblemStatus.OPEN.value,
                target_type="pest",
                image_asset_id="pest-photo-stem-borer-severe",
            )
            prob.created_at = now - timedelta(days=3)
            session.add(prob)

            fu = FollowUp(
                id=str(uuid.uuid4()),
                problem_id=prob_id,
                farm_id=farm_id,
                response=FollowupResponse.GOT_WORSE.value,
                farmer_notes="குருத்து அழுகல் அதிகமாயுள்ளது, கட்டுப்படவிலை",
            )
            fu.created_at = now - timedelta(days=1)
            session.add(fu)

            case_id = str(uuid.uuid4())
            case = Case(
                id=case_id,
                farm_id=farm_id,
                problem_id=prob_id,
                reason="Stem borer deadhearts expanded rapidly after release; follow-up worsened.",
                severity=ProblemSeverity.SEVERE.value,
                status=CaseStatus.ASSIGNED.value,
                assigned_to=agron.id,
                case_summary={
                    "farmer_name": "Senthil",
                    "crop": "Samba Paddy",
                    "pest": "stem_borer",
                    "initial_severity": "early",
                    "followup": "got_worse",
                },
            )
            case.created_at = now - timedelta(days=1)
            session.add(case)

            subindices = {
                SubIndexKey.ACTIVE_PROBLEM_SEVERITY.value: 30.0,
                SubIndexKey.ENVIRONMENTAL_RISK.value: 70.0,
                SubIndexKey.MONITORING_RECENCY.value: 80.0,
                SubIndexKey.TREATMENT_RESPONSE.value: 40.0,
            }
            snap = _make_snapshot(farm_id, 55, HealthBand.POOR, subindices, now)
            session.add(snap)
            results["pest_escalate"] = {"farmer_id": farmer.id, "farm_id": farm_id, "problem_id": prob_id, "case_id": case_id}

        if "pest_resolved" in stages_to_seed:
            farmer = User(
                id=str(uuid.uuid4()),
                phone_number=FIXTURE_STAGES["pest_resolved"],
                email="venkatesh@bhoomi.demo",
                full_name="Venkatesh",
                role=UserRole.FARMER.value,
                preferred_language="ta",
                password_hash=pw,
            )
            session.add(farmer)
            await session.flush()

            farm_id = str(uuid.uuid4())
            farm = Farm(
                id=farm_id,
                farmer_id=farmer.id,
                farm_name="Venkatesh's Paddy Farm",
                village="Mannargudi",
                taluk="Mannargudi",
                district="Thiruvarur",
                region="Thiruvarur",
                state="Tamil Nadu",
                total_area_acres=3.5,
                land_status=LandStatus.VERIFIED.value,
                primary_crop="samba_paddy",
                growth_stage="vegetative",
                days_since_planting=35,
                expected_stage_day=get_expected_stage_day("vegetative"),
                days_since_last_scan=1,
            )
            session.add(farm)

            prob_id = str(uuid.uuid4())
            prob = Problem(
                id=prob_id,
                farm_id=farm_id,
                label="stem_borer",
                severity=ProblemSeverity.SEVERE.value,
                status=ProblemStatus.RESOLVED.value,
                target_type="pest",
                image_asset_id="pest-photo-stem-borer-resolved",
                resolved_at=now - timedelta(hours=2),
            )
            prob.created_at = now - timedelta(days=5)
            session.add(prob)

            fu = FollowUp(
                id=str(uuid.uuid4()),
                problem_id=prob_id,
                farm_id=farm_id,
                response=FollowupResponse.IMPROVED.value,
                farmer_notes="தண்டுத் துளைப்பான் கட்டுக்குள் வந்துவிட்டது",
            )
            fu.created_at = now - timedelta(hours=2)
            session.add(fu)

            case_id = str(uuid.uuid4())
            case = Case(
                id=case_id,
                farm_id=farm_id,
                problem_id=prob_id,
                reason="Stem borer infestation resolved following biocontrol Parasitoid release and neem oil spray.",
                severity=ProblemSeverity.SEVERE.value,
                status=CaseStatus.RESOLVED.value,
                assigned_to=agron.id,
                case_summary={
                    "farmer_name": "Venkatesh",
                    "crop": "Samba Paddy",
                    "pest": "stem_borer",
                },
                resolution={
                    "prescribed_treatment": "Trichogramma release + 3% Neem oil spray",
                    "notes": "Infestation controlled, crop recovering.",
                },
                resolved_at=now - timedelta(hours=2),
            )
            case.created_at = now - timedelta(days=3)
            session.add(case)

            subindices = {
                SubIndexKey.ACTIVE_PROBLEM_SEVERITY.value: 95.0,
                SubIndexKey.ENVIRONMENTAL_RISK.value: 85.0,
                SubIndexKey.MONITORING_RECENCY.value: 90.0,
                SubIndexKey.TREATMENT_RESPONSE.value: 92.0,
            }
            snap = _make_snapshot(farm_id, 86, HealthBand.GOOD, subindices, now)
            session.add(snap)
            results["pest_resolved"] = {"farmer_id": farmer.id, "farm_id": farm_id, "problem_id": prob_id, "case_id": case_id}

        await session.commit()
        return results


async def main() -> None:
    parser = argparse.ArgumentParser(description="Seed additional fixture farms covering non-Ramesh states")
    parser.add_argument(
        "--stage",
        choices=["unrated", "healthy", "pest_open", "pest_no_corpus", "pest_escalate", "pest_resolved", "full"],
        default="full",
        help="Fixture stage to seed",
    )
    args = parser.parse_args()
    results = await seed_fixture_stage(args.stage)
    print(f"[OK] Seeded fixture farms stage: [{args.stage.upper()}]")
    for key, val in results.items():
        print(f"  [{key}] farmer_id={val['farmer_id']} farm_id={val['farm_id']}")


if __name__ == "__main__":
    asyncio.run(main())
