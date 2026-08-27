"""Enhanced demo seed script (Phase 1).

Seeds the complete demo environment:
  - Farmer "Ramesh" (+919944400001, password: bhoomi123)
  - Officer "Officer Kumar" (+919944400002, jurisdiction: taluk_erode)
  - Agronomist "Dr. Lakshmi" (+919944400003, jurisdiction: kvk_erode)
  - Farm "Ramesh's Paddy Farm" (2 acres, Samba Paddy, Erode)
  - LandParcel (verified cadastral record with GeoJSON boundary)
  - 3 Government Schemes (TN Crop Protection, PM-KISAN, Micro Irrigation)

Usage:
    python -m scripts.seed_demo
"""

import asyncio
from datetime import date, datetime, timedelta
import uuid

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

# Baseline metrics producing health score 82 (band: good) after resource plan
BASELINE_SOIL_MOISTURE_PCT = 45.0
BASELINE_DAYS_SINCE_PLANTING = 20
BASELINE_DAYS_SINCE_LAST_SCAN = 2

# Demo polygon for Ramesh's 2-acre plot in Chithode, Erode
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


async def _cleanup_existing(session, phones: list[str], scheme_names: list[str]) -> None:
    """Clean up existing demo records for idempotency."""
    existing_users = (
        await session.execute(select(User).where(User.phone_number.in_(phones)))
    ).scalars().all()

    for user in existing_users:
        farms = (
            await session.execute(select(Farm).where(Farm.farmer_id == user.id))
        ).scalars().all()
        for farm in farms:
            # Delete associated land parcels
            parcels = (
                await session.execute(select(LandParcel).where(LandParcel.farm_id == farm.id))
            ).scalars().all()
            for parcel in parcels:
                await session.delete(parcel)
            await session.delete(farm)
        await session.delete(user)

    await session.execute(delete(Scheme).where(Scheme.name.in_(scheme_names)))
    await session.commit()


async def seed_demo() -> dict[str, str]:
    """Insert full demo seed data and return created IDs."""
    async with AsyncSessionLocal() as session:
        scheme_names = [
            "TN Crop Protection Subsidy",
            "PM-KISAN Samman Nidhi",
            "TN Micro Irrigation Subsidy Scheme",
        ]
        await _cleanup_existing(
            session,
            phones=[FARMER_PHONE, OFFICER_PHONE, AGRONOMIST_PHONE],
            scheme_names=scheme_names,
        )

        password_hash = get_password_hash(DEMO_PASSWORD)

        # 1. Users
        farmer = User(
            phone_number=FARMER_PHONE,
            email="ramesh.farmer@bhoomi.demo",
            full_name="Ramesh",
            role=UserRole.FARMER.value,
            preferred_language="ta",
            password_hash=password_hash,
        )
        officer = User(
            phone_number=OFFICER_PHONE,
            email="kumar.officer@bhoomi.demo",
            full_name="Officer Kumar",
            role=UserRole.OFFICER.value,
            preferred_language="ta",
            password_hash=password_hash,
            jurisdiction="taluk_erode",
        )
        agronomist = User(
            phone_number=AGRONOMIST_PHONE,
            email="lakshmi.agronomist@bhoomi.demo",
            full_name="Dr. Lakshmi",
            role=UserRole.AGRONOMIST.value,
            preferred_language="ta",
            password_hash=password_hash,
            jurisdiction="kvk_erode",
        )
        session.add_all([farmer, officer, agronomist])
        await session.flush()

        # 2. Farm
        farm = Farm(
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
            soil_moisture_pct=BASELINE_SOIL_MOISTURE_PCT,
            days_since_planting=BASELINE_DAYS_SINCE_PLANTING,
            expected_stage_day=get_expected_stage_day("vegetative"),
            days_since_last_scan=BASELINE_DAYS_SINCE_LAST_SCAN,
        )
        session.add(farm)
        await session.flush()

        # 3. Schemes (3 dated schemes)
        today = date.today()
        schemes = [
            Scheme(
                name="TN Crop Protection Subsidy",
                ministry="Tamil Nadu Department of Agriculture",
                jurisdiction="TN",
                description="Subsidy toward approved crop-protection inputs for paddy smallholders.",
                benefits="Up to 50% subsidy on approved bactericide/fungicide purchases, capped per acre.",
                eligibility_criteria={
                    "crop": "samba_paddy",
                    "category": "Small/Marginal",
                    "land_status": "verified",
                },
                subsidy_percentage=50.0,
                max_amount_inr=5000.0,
                portal_url="https://www.tnagrisnet.tn.gov.in",
                status=SchemeStatus.ACTIVE.value,
                last_verified=today - timedelta(days=15),
                crop_filter="samba_paddy",
                category_filter="Small/Marginal",
            ),
            Scheme(
                name="PM-KISAN Samman Nidhi",
                ministry="Ministry of Agriculture & Farmers Welfare, GoI",
                jurisdiction="National",
                description="Direct income support for eligible smallholder farmer families.",
                benefits="₹6,000/year in three equal installments, direct to bank account.",
                eligibility_criteria={
                    "category": "Small/Marginal",
                    "land_status": "verified",
                },
                subsidy_percentage=None,
                max_amount_inr=6000.0,
                portal_url="https://pmkisan.gov.in",
                status=SchemeStatus.EXPIRING.value,
                last_verified=today - timedelta(days=170),
                crop_filter=None,
                category_filter="Small/Marginal",
            ),
            Scheme(
                name="TN Micro Irrigation Subsidy Scheme",
                ministry="Tamil Nadu Horticulture & Plantation Crops Department",
                jurisdiction="TN",
                description="Promoting water use efficiency via drip and sprinkler systems.",
                benefits="100% subsidy for Small/Marginal farmers up to ₹25,000 per acre.",
                eligibility_criteria={
                    "category": "Small/Marginal",
                    "land_status": "verified",
                },
                subsidy_percentage=100.0,
                max_amount_inr=25000.0,
                portal_url="https://tnhorticulture.tn.gov.in",
                status=SchemeStatus.ACTIVE.value,
                last_verified=today - timedelta(days=10),
                crop_filter=None,
                category_filter="Small/Marginal",
            ),
        ]
        session.add_all(schemes)

        await session.commit()

        return {
            "farmer_id": farmer.id,
            "officer_id": officer.id,
            "agronomist_id": agronomist.id,
            "farm_id": farm.id,
        }


async def main() -> None:
    ids = await seed_demo()
    print("==================================================")
    print("  Bhoomi SIH25076 — Demo Environment Seeded")
    print("==================================================")
    for key, value in ids.items():
        print(f"  {key:15}: {value}")
    print("\nCredentials (password: bhoomi123 for all):")
    print(f"  Farmer:     {FARMER_PHONE} (Ramesh)")
    print(f"  Officer:    {OFFICER_PHONE} (Officer Kumar)")
    print(f"  Agronomist: {AGRONOMIST_PHONE} (Dr. Lakshmi)")
    print("==================================================")


if __name__ == "__main__":
    asyncio.run(main())
