"""Unit tests for simplified Farm onboarding model and schema (SIH26131)."""

import uuid
import pytest
from pydantic import ValidationError

from app.models.farm import Farm
from app.schemas.farm import FarmCreateRequest, FarmResponse
from app.services.farm_service import FarmService, _to_farm_response
from app.repositories.in_memory import InMemoryFarmRepository


def test_farm_create_request_fields():
    """FarmCreateRequest requires exactly: farmer_id, crop, growth_stage, region."""
    farmer_id = str(uuid.uuid4())
    req = FarmCreateRequest(
        farmer_id=farmer_id,
        crop="samba_paddy",
        growth_stage="vegetative",
        region="Cauvery Delta",
    )
    assert req.farmer_id == farmer_id
    assert req.crop == "samba_paddy"
    assert req.growth_stage == "vegetative"
    assert req.region == "Cauvery Delta"

    # Missing required field raises ValidationError
    with pytest.raises(ValidationError):
        FarmCreateRequest(farmer_id=farmer_id, crop="samba_paddy")


def test_farm_orm_model_nullable_columns_and_region():
    """Verify Farm ORM table definition has region and nullable profile columns."""
    table = Farm.__table__
    cols = {c.name: c for c in table.columns}

    assert "region" in cols
    assert cols["region"].nullable is True

    # 7 columns made nullable for simplified onboarding
    nullable_cols = [
        "farm_name",
        "village",
        "taluk",
        "district",
        "latitude",
        "longitude",
        "total_area_acres",
    ]
    for col_name in nullable_cols:
        assert col_name in cols, f"Missing {col_name} in Farm columns"
        assert cols[col_name].nullable is True, f"{col_name} should be nullable"

    # primary_crop remains NOT NULL
    assert cols["primary_crop"].nullable is False


@pytest.mark.asyncio
async def test_farm_service_create_farm():
    """FarmService creates a Farm row from 4-field FarmCreateRequest."""
    repo = InMemoryFarmRepository()
    service = FarmService(repo)

    farmer_id = str(uuid.uuid4())
    req = FarmCreateRequest(
        farmer_id=farmer_id,
        crop="cotton",
        growth_stage="flowering",
        region="Erode",
    )
    res = await service.create_farm(req)

    assert isinstance(res, FarmResponse)
    assert res.farmer_id == farmer_id
    assert res.primary_crop == "cotton"
    assert res.growth_stage == "flowering"
    assert res.region == "Erode"
    assert res.farm_name is None
    assert res.village is None
    assert res.latitude is None
    assert res.longitude is None
    assert res.total_area_acres is None


def test_to_farm_response_handles_null_columns():
    """_to_farm_response gracefully serializes rows with null legacy fields."""
    row = {
        "id": "farm_123",
        "farmer_id": "farmer_456",
        "primary_crop": "samba_paddy",
        "growth_stage": "vegetative",
        "region": "Thanjavur",
        "farm_name": None,
        "village": None,
        "taluk": None,
        "district": None,
        "latitude": None,
        "longitude": None,
        "total_area_acres": None,
        "survey_number": None,
        "soil_type": None,
        "irrigation_source": None,
        "land_status": "unverified",
        "created_at": None,
    }
    res = _to_farm_response(row)
    assert res.id == "farm_123"
    assert res.primary_crop == "samba_paddy"
    assert res.region == "Thanjavur"
    assert res.latitude is None
