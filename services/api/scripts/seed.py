"""Demo seed script (Phase 5) — replays from a clean DB in seconds.

Creates:
  * Farmer "Ramesh" — 2-acre samba paddy, Tamil, Erode taluk
    (PRD §6's own scenario), with the exact monitoring baseline that makes
    ``GET /farms/{id}/health`` compute to score 82 / band "good" once the
    resource plan is run (see ``app/services/*_service.py`` module
    docstrings for why these specific numbers).
  * Officer "Officer Kumar" (jurisdiction: taluk_erode) to work the land
    HITL queue.
  * Agronomist "Dr. Lakshmi" (jurisdiction: kvk_erode) to resolve escalated
    cases.
  * Two dated schemes matching samba paddy / Small-Marginal farmers
    (PRD §5.12) — one active, one expiring, so scheme discovery has
    something real to show.

Idempotent: re-running against the same DB deletes and recreates every row
this script owns (matched by phone number / scheme name), so it can be
replayed repeatedly without manual cleanup.

Run as:  python -m scripts.seed
"""

import asyncio
from datetime import date, timedelta

from sqlalchemy import delete, select

from app.core.db import AsyncSessionLocal
from app.core.enums import LandStatus, SchemeStatus, UserRole
from app.core.security import get_password_hash
from app.domain.farm_reference_data import get_expected_stage_day
from app.models.farm import Farm
from app.models.scheme import Scheme
from app.models.user import User

FARMER_PHONE = "+919944400001"
OFFICER_PHONE = "+919944400002"
AGRONOMIST_PHONE = "+919944400003"
DEMO_PASSWORD = "bhoomi123"

# The exact baseline that, once the FAO-56 resource plan fills in the
# remaining irrigation inputs, computes to score 82 / band "good" — see
# app/services/farm_service.py and app/services/resource_plan_service.py.
BASELINE_SOIL_MOISTURE_PCT = 45.0
BASELINE_DAYS_SINCE_PLANTING = 20
BASELINE_DAYS_SINCE_LAST_SCAN = 2


async def _delete_existing(session, phones: list[str], scheme_names: list[str]) -> None:
    existing_users = (await session.execute(select(User).where(User.phone_number.in_(phones)))).scalars().all()
    for user in existing_users:
        farms = (await session.execute(select(Farm).where(Farm.farmer_id == user.id))).scalars().all()
        for farm in farms:
            await session.delete(farm)
        await session.delete(user)
    await session.execute(delete(Scheme).where(Scheme.name.in_(scheme_names)))
    await session.commit()


async def seed() -> dict[str, str]:
    """Insert the demo dataset and return the created ids, keyed by role."""
    async with AsyncSessionLocal() as session:
        await _delete_existing(
            session,
            phones=[FARMER_PHONE, OFFICER_PHONE, AGRONOMIST_PHONE],
            scheme_names=["TN Crop Protection Subsidy", "PM-KISAN Samman Nidhi"],
        )

        password_hash = get_password_hash(DEMO_PASSWORD)

        farmer = User(
            phone_number=FARMER_PHONE,
            full_name="Ramesh",
            role=UserRole.FARMER.value,
            preferred_language="ta",
            password_hash=password_hash,
        )
        officer = User(
            phone_number=OFFICER_PHONE,
            full_name="Officer Kumar",
            role=UserRole.OFFICER.value,
            preferred_language="ta",
            password_hash=password_hash,
            jurisdiction="taluk_erode",
        )
        agronomist = User(
            phone_number=AGRONOMIST_PHONE,
            full_name="Dr. Lakshmi",
            role=UserRole.AGRONOMIST.value,
            preferred_language="ta",
            password_hash=password_hash,
            jurisdiction="kvk_erode",
        )
        session.add_all([farmer, officer, agronomist])
        await session.flush()

        farm = Farm(
            farmer_id=farmer.id,
            farm_name="Ramesh's Paddy Farm",
            village="Chithode",
            taluk="Erode",
            district="Erode",
            state="Tamil Nadu",
            latitude=11.34,
            longitude=77.71,
            total_area_acres=2.0,
            survey_number="142/3B",
            land_status=LandStatus.UNVERIFIED.value,
            primary_crop="samba_paddy",
            growth_stage="vegetative",
            soil_type="clay_loam",
            irrigation_source="canal",
            soil_moisture_pct=BASELINE_SOIL_MOISTURE_PCT,
            days_since_planting=BASELINE_DAYS_SINCE_PLANTING,
            expected_stage_day=get_expected_stage_day("vegetative"),
            days_since_last_scan=BASELINE_DAYS_SINCE_LAST_SCAN,
            # irrigation_delivered/required_mm intentionally left NULL — the
            # runbook's resource-plan step fills these in (contract §2.8).
        )
        session.add(farm)

        today = date.today()
        session.add_all(
            [
                Scheme(
                    name="TN Crop Protection Subsidy",
                    ministry="Tamil Nadu Department of Agriculture",
                    jurisdiction="TN",
                    description="Subsidy toward approved crop-protection inputs for paddy smallholders.",
                    benefits="Up to 50% subsidy on approved bactericide/fungicide purchases, capped per acre.",
                    eligibility_criteria={"crop": "samba_paddy", "category": "Small/Marginal", "land_status": "verified"},
                    subsidy_percentage=50.0,
                    max_amount_inr=5000.0,
                    portal_url="https://www.tnagrisnet.tn.gov.in",
                    status=SchemeStatus.ACTIVE.value,
                    last_verified=today - timedelta(days=23),
                    crop_filter="samba_paddy",
                    category_filter="Small/Marginal",
                ),
                Scheme(
                    name="PM-KISAN Samman Nidhi",
                    ministry="Ministry of Agriculture & Farmers Welfare, GoI",
                    jurisdiction="National",
                    description="Direct income support for eligible smallholder farmer families.",
                    benefits="₹6,000/year in three equal installments, direct to bank account.",
                    eligibility_criteria={"category": "Small/Marginal", "land_status": "verified"},
                    subsidy_percentage=None,
                    max_amount_inr=6000.0,
                    portal_url="https://pmkisan.gov.in",
                    status=SchemeStatus.EXPIRING.value,
                    last_verified=today - timedelta(days=170),
                    crop_filter=None,
                    category_filter="Small/Marginal",
                ),
            ]
        )

        await session.commit()

        return {
            "farmer_id": farmer.id,
            "officer_id": officer.id,
            "agronomist_id": agronomist.id,
            "farm_id": farm.id,
        }


async def main() -> None:
    ids = await seed()
    print("Seeded demo data:")
    for key, value in ids.items():
        print(f"  {key}: {value}")
    print(f"\nLogin any account with password: {DEMO_PASSWORD}")
    print(f"  farmer:     {FARMER_PHONE}")
    print(f"  officer:    {OFFICER_PHONE}")
    print(f"  agronomist: {AGRONOMIST_PHONE}")


if __name__ == "__main__":
    asyncio.run(main())
