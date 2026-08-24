"""Phase 3: AlertService wiring — evaluate_and_list end to end through
in-memory repositories (no DB), cooldown/supersede at the full-pipeline
level, the inspection_tasks "never cut" enforcement, and acknowledge.
"""

from datetime import datetime, timedelta

import pytest

from app.repositories.in_memory import InMemoryAlertRepository, InMemoryFarmRepository
from app.services.alerts.alert_service import AlertService

ERODE = (11.3410, 77.7172)
NEARBY = (11.35, 77.72)


class _FavorableWeather:
    """RH 84%, 28C — squarely inside BLB's 25-32C / RH>=80% band."""

    async def get_current_weather(self, latitude, longitude):
        return {"temperature_c": 28.0, "relative_humidity_pct": 84.0}

    async def get_daily_et0(self, latitude, longitude, target_date):
        return 4.8

    async def get_forecast(self, latitude, longitude, days=7):
        return []


class _UnfavorableWeather:
    async def get_current_weather(self, latitude, longitude):
        return {"temperature_c": 15.0, "relative_humidity_pct": 30.0}

    async def get_daily_et0(self, latitude, longitude, target_date):
        return 4.8

    async def get_forecast(self, latitude, longitude, days=7):
        return []


async def _make_farm(
    farm_repo: InMemoryFarmRepository, alert_repo: InMemoryAlertRepository, farm_id: str, **overrides
) -> dict:
    data = {
        "id": farm_id,
        "farmer_id": "u_1",
        "district": "Erode",
        "primary_crop": "samba_paddy",
        "growth_stage": "vegetative",
        "latitude": ERODE[0],
        "longitude": ERODE[1],
        **overrides,
    }
    saved = await farm_repo.save(data)
    # The Postgres alert repo looks up a farm's coordinates via a join;
    # the in-memory double needs the same info registered explicitly.
    alert_repo.register_farm(farm_id, saved["latitude"], saved["longitude"])
    return saved


def _blb_alert(alerts: list[dict]) -> dict:
    return next(a for a in alerts if a["pathogen_name"] == "Bacterial Leaf Blight")


@pytest.mark.asyncio
async def test_no_trigger_returns_empty_list():
    farm_repo = InMemoryFarmRepository()
    alert_repo = InMemoryAlertRepository()
    await _make_farm(farm_repo, alert_repo, "f_1")

    service = AlertService(alert_repo, farm_repo, _UnfavorableWeather())
    alerts = await service.evaluate_and_list("f_1")
    assert alerts == []


@pytest.mark.asyncio
async def test_favorable_weather_alone_creates_advisory_alert():
    # Note: this weather reading (28C/84% RH) also happens to satisfy the
    # two illustrative placeholder thresholds' bands, so all three pathogens
    # alert — a real consequence of the stub table's overlapping bands, not
    # a defect. This test only asserts on the ICAR-sourced BLB threshold.
    farm_repo = InMemoryFarmRepository()
    alert_repo = InMemoryAlertRepository()
    await _make_farm(farm_repo, alert_repo, "f_1")

    service = AlertService(alert_repo, farm_repo, _FavorableWeather())
    alerts = await service.evaluate_and_list("f_1")
    blb = _blb_alert(alerts)
    assert blb["severity"] == "advisory"
    assert blb["farm_id"] == "f_1"


@pytest.mark.asyncio
async def test_issued_alert_always_has_at_least_one_inspection_task():
    """Verification gate: inspection_tasks[] is never empty on an issued alert."""
    farm_repo = InMemoryFarmRepository()
    alert_repo = InMemoryAlertRepository()
    await _make_farm(farm_repo, alert_repo, "f_1")

    service = AlertService(alert_repo, farm_repo, _FavorableWeather())
    alerts = await service.evaluate_and_list("f_1")
    assert len(alerts) > 0
    for alert in alerts:
        assert len(alert["inspection_tasks"]) >= 1


@pytest.mark.asyncio
async def test_cluster_plus_weather_creates_emergency_alert():
    farm_repo = InMemoryFarmRepository()
    alert_repo = InMemoryAlertRepository()
    await _make_farm(farm_repo, alert_repo, "f_1")
    for i in range(3):
        alert_repo.seed_nearby_case(
            farm_id=f"f_nearby_{i}", latitude=NEARBY[0], longitude=NEARBY[1],
            label="bacterial_leaf_blight", severity="moderate", created_at=datetime.utcnow(),
        )

    service = AlertService(alert_repo, farm_repo, _FavorableWeather())
    alerts = await service.evaluate_and_list("f_1")
    assert _blb_alert(alerts)["severity"] == "emergency"


@pytest.mark.asyncio
async def test_repeated_identical_evaluation_is_suppressed_by_cooldown():
    """Verification gate: a second identical evaluation within the window
    is suppressed — same alert, not a duplicate, not a re-trigger."""
    farm_repo = InMemoryFarmRepository()
    alert_repo = InMemoryAlertRepository()
    await _make_farm(farm_repo, alert_repo, "f_1")
    service = AlertService(alert_repo, farm_repo, _FavorableWeather())

    first = await service.evaluate_and_list("f_1")
    second = await service.evaluate_and_list("f_1")
    third = await service.evaluate_and_list("f_1")

    assert len(first) == len(second) == len(third)
    first_ids = sorted(a["id"] for a in first)
    second_ids = sorted(a["id"] for a in second)
    third_ids = sorted(a["id"] for a in third)
    assert first_ids == second_ids == third_ids


@pytest.mark.asyncio
async def test_severity_upgrade_bypasses_cooldown_and_supersedes_prior_alert():
    """Verification gate: a severity upgrade bypasses cooldown and
    supersedes the prior lower-severity alert — advisory (weather only)
    upgrades to emergency (weather + cluster) once a cluster forms, and the
    farmer never sees both concurrently."""
    farm_repo = InMemoryFarmRepository()
    alert_repo = InMemoryAlertRepository()
    await _make_farm(farm_repo, alert_repo, "f_1")
    service = AlertService(alert_repo, farm_repo, _FavorableWeather())

    before = await service.evaluate_and_list("f_1")
    advisory_id = _blb_alert(before)["id"]
    assert _blb_alert(before)["severity"] == "advisory"

    # A cluster forms nearby -> BLB should now hit emergency.
    for i in range(3):
        alert_repo.seed_nearby_case(
            farm_id=f"f_nearby_{i}", latitude=NEARBY[0], longitude=NEARBY[1],
            label="bacterial_leaf_blight", severity="moderate", created_at=datetime.utcnow(),
        )

    after = await service.evaluate_and_list("f_1")
    blb_after = _blb_alert(after)
    assert blb_after["severity"] == "emergency"
    assert blb_after["id"] != advisory_id

    # The old advisory alert is superseded, not still active alongside it.
    blb_alerts = [a for a in after if a["pathogen_name"] == "Bacterial Leaf Blight"]
    assert len(blb_alerts) == 1
    assert all(a["id"] != advisory_id for a in blb_alerts)


@pytest.mark.asyncio
async def test_unknown_farm_raises_not_found():
    from app.core.errors import NotFoundError

    farm_repo = InMemoryFarmRepository()
    alert_repo = InMemoryAlertRepository()
    service = AlertService(alert_repo, farm_repo, _FavorableWeather())

    with pytest.raises(NotFoundError):
        await service.evaluate_and_list("nonexistent")


@pytest.mark.asyncio
async def test_acknowledge_removes_alert_from_subsequent_list():
    farm_repo = InMemoryFarmRepository()
    alert_repo = InMemoryAlertRepository()
    await _make_farm(farm_repo, alert_repo, "f_1")
    service = AlertService(alert_repo, farm_repo, _FavorableWeather())

    alerts = await service.evaluate_and_list("f_1")
    alert_id = alerts[0]["id"]

    await service.acknowledge(alert_id, "f_1", "action_taken")

    remaining = await alert_repo.get_farm_alerts(
        farm_id="f_1", district="Erode", crop="samba_paddy", as_of=datetime.utcnow()
    )
    assert all(a["id"] != alert_id for a in remaining)


@pytest.mark.asyncio
async def test_emergency_alert_does_not_touch_farm_or_health_state():
    """Verification gate: emergency does not create an open Problem row and
    does not drop the health score until a diagnosis confirms. AlertService
    has no ProblemWriter/HealthService dependency at all — structurally
    guaranteed — this test additionally checks the farm row itself (the
    thing a health-affecting write would touch) is unchanged."""
    farm_repo = InMemoryFarmRepository()
    alert_repo = InMemoryAlertRepository()
    farm_before = await _make_farm(farm_repo, alert_repo, "f_1")
    for i in range(3):
        alert_repo.seed_nearby_case(
            farm_id=f"f_nearby_{i}", latitude=NEARBY[0], longitude=NEARBY[1],
            label="bacterial_leaf_blight", severity="moderate", created_at=datetime.utcnow(),
        )

    service = AlertService(alert_repo, farm_repo, _FavorableWeather())
    alerts = await service.evaluate_and_list("f_1")
    assert _blb_alert(alerts)["severity"] == "emergency"

    farm_after = await farm_repo.get_by_id("f_1")
    assert farm_after == farm_before
