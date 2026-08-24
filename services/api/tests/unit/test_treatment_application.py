"""Unit tests for TreatmentApplication model and FollowUp attribution field."""

from datetime import date
import uuid

from app.models.followup import FollowUp
from app.models.treatment_application import TreatmentApplication


def test_treatment_application_instantiation():
    """Verify TreatmentApplication can be instantiated with valid data."""
    app_id = str(uuid.uuid4())
    problem_id = str(uuid.uuid4())
    farm_id = str(uuid.uuid4())
    today = date(2026, 8, 24)

    app = TreatmentApplication(
        id=app_id,
        problem_id=problem_id,
        farm_id=farm_id,
        pathogen_type="bacterial_leaf_blight",
        treatment_name="copper_hydroxide_77_wp",
        treatment_category="chemical",
        applied_on=today,
        crop="samba_paddy",
        district="Erode",
        failed_on_got_worse=False,
        escalated_for_expert=False,
    )

    assert app.id == app_id
    assert app.problem_id == problem_id
    assert app.farm_id == farm_id
    assert app.pathogen_type == "bacterial_leaf_blight"
    assert app.treatment_name == "copper_hydroxide_77_wp"
    assert app.treatment_category == "chemical"
    assert app.applied_on == today
    assert app.crop == "samba_paddy"
    assert app.district == "Erode"
    assert app.final_outcome is None
    assert app.followups_to_resolution is None
    assert app.days_to_resolution is None
    assert app.failed_on_got_worse is False
    assert app.escalated_for_expert is False


def test_treatment_application_with_outcome():
    """Verify TreatmentApplication with resolved outcome fields."""
    app = TreatmentApplication(
        problem_id=str(uuid.uuid4()),
        farm_id=str(uuid.uuid4()),
        pathogen_type="bacterial_leaf_blight",
        treatment_name="pseudomonas_fluorescens_spray",
        treatment_category="biological",
        applied_on=date(2026, 8, 1),
        crop="samba_paddy",
        district="Thanjavur",
        final_outcome="improved",
        followups_to_resolution=2,
        days_to_resolution=14,
        failed_on_got_worse=False,
        escalated_for_expert=False,
    )

    assert app.final_outcome == "improved"
    assert app.followups_to_resolution == 2
    assert app.days_to_resolution == 14


def test_treatment_application_table_columns_and_foreign_keys():
    """Verify SQLAlchemy table schema, columns, defaults, and FK constraints."""
    table = TreatmentApplication.__table__
    assert table.name == "treatment_applications"

    cols = {c.name: c for c in table.columns}
    assert "id" in cols
    assert "created_at" in cols
    assert "updated_at" in cols
    assert "problem_id" in cols
    assert "farm_id" in cols
    assert "pathogen_type" in cols
    assert "treatment_name" in cols
    assert "treatment_category" in cols
    assert "applied_on" in cols
    assert "crop" in cols
    assert "district" in cols
    assert "final_outcome" in cols
    assert "followups_to_resolution" in cols
    assert "days_to_resolution" in cols
    assert "failed_on_got_worse" in cols
    assert "escalated_for_expert" in cols

    # Default checks
    assert cols["failed_on_got_worse"].default.arg is False
    assert cols["escalated_for_expert"].default.arg is False

    # FK checks on problem_id and farm_id
    problem_fks = list(cols["problem_id"].foreign_keys)
    assert len(problem_fks) == 1
    assert problem_fks[0].target_fullname == "problems.id"
    assert problem_fks[0].ondelete == "RESTRICT"

    farm_fks = list(cols["farm_id"].foreign_keys)
    assert len(farm_fks) == 1
    assert farm_fks[0].target_fullname == "farms.id"
    assert farm_fks[0].ondelete == "RESTRICT"


def test_followup_treatment_application_fk():
    """Verify FollowUp has the treatment_application_id column with SET NULL ondelete."""
    table = FollowUp.__table__
    cols = {c.name: c for c in table.columns}

    assert "treatment_application_id" in cols
    col = cols["treatment_application_id"]
    assert col.nullable is True

    fks = list(col.foreign_keys)
    assert len(fks) == 1
    assert fks[0].target_fullname == "treatment_applications.id"
    assert fks[0].ondelete == "SET NULL"

    # Instantiation check
    fu = FollowUp(
        problem_id=str(uuid.uuid4()),
        farm_id=str(uuid.uuid4()),
        response="improved",
        treatment_application_id="app_123",
    )
    assert fu.treatment_application_id == "app_123"
