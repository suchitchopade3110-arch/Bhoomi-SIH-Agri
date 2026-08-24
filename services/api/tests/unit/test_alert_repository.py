"""Phase 3: InMemoryAlertRepository — cluster query, cooldown, supersede,
dismiss, and the farm+broadcast resolve query (spec §3.3, §4.2, §5.2).
"""

from datetime import datetime, timedelta

import pytest

from app.repositories.in_memory import InMemoryAlertRepository

ERODE = (11.3410, 77.7172)
NEARBY = (11.35, 77.72)  # a few km from Erode
FAR_AWAY = (28.6139, 77.2090)  # Delhi — nowhere near Erode

NOW = datetime(2026, 8, 24, 6, 0, 0)


@pytest.mark.asyncio
async def test_cluster_summary_excludes_target_farm():
    repo = InMemoryAlertRepository()
    repo.seed_nearby_case(
        farm_id="f_target", latitude=ERODE[0], longitude=ERODE[1],
        label="bacterial_leaf_blight", severity="moderate", created_at=NOW,
    )
    summary = await repo.get_nearby_cluster_summary(*ERODE, target_farm_id="f_target", radius_km=10, window_days=7)
    assert summary == []


@pytest.mark.asyncio
async def test_cluster_summary_excludes_out_of_radius_and_stale_cases():
    repo = InMemoryAlertRepository()
    repo.seed_nearby_case(
        farm_id="f_far", latitude=FAR_AWAY[0], longitude=FAR_AWAY[1],
        label="bacterial_leaf_blight", severity="moderate", created_at=NOW,
    )
    repo.seed_nearby_case(
        farm_id="f_stale", latitude=NEARBY[0], longitude=NEARBY[1],
        label="bacterial_leaf_blight", severity="moderate", created_at=NOW - timedelta(days=30),
    )
    summary = await repo.get_nearby_cluster_summary(*ERODE, target_farm_id="f_target", radius_km=10, window_days=7)
    assert summary == []


@pytest.mark.asyncio
async def test_cluster_summary_groups_by_label_and_severity():
    repo = InMemoryAlertRepository()
    for i in range(3):
        repo.seed_nearby_case(
            farm_id=f"f_{i}", latitude=NEARBY[0], longitude=NEARBY[1],
            label="bacterial_leaf_blight", severity="moderate", created_at=NOW,
        )
    repo.seed_nearby_case(
        farm_id="f_other", latitude=NEARBY[0], longitude=NEARBY[1],
        label="powdery_mildew", severity="early", created_at=NOW,
    )

    summary = await repo.get_nearby_cluster_summary(*ERODE, target_farm_id="f_target", radius_km=10, window_days=7)
    blb = next(c for c in summary if c.label == "bacterial_leaf_blight")
    assert blb.case_count == 3
    assert len(summary) == 2


@pytest.mark.asyncio
async def test_active_cooldown_suppresses_duplicate_at_same_key():
    repo = InMemoryAlertRepository()
    await repo.save(
        {
            "id": "alt_1", "farm_id": "f_1", "district": "Erode", "pathogen_name": "BLB",
            "target_crop": "samba_paddy", "target": "per_farm", "severity": "warning",
            "trigger_reason": "x", "preventative_action": "y", "spoken_summary": "z",
            "delivery_channels": ["push"], "cooldown_key": "f_1:bacterial_leaf_blight:warning",
            "created_at": NOW, "expires_at": NOW + timedelta(hours=48),
        }
    )
    existing = await repo.get_active_cooldown("f_1:bacterial_leaf_blight:warning", as_of=NOW)
    assert existing is not None
    assert existing["id"] == "alt_1"


@pytest.mark.asyncio
async def test_active_cooldown_ignores_expired_alerts():
    repo = InMemoryAlertRepository()
    await repo.save(
        {
            "id": "alt_1", "farm_id": "f_1", "district": "Erode", "pathogen_name": "BLB",
            "target_crop": "samba_paddy", "target": "per_farm", "severity": "warning",
            "trigger_reason": "x", "preventative_action": "y", "spoken_summary": "z",
            "delivery_channels": ["push"], "cooldown_key": "f_1:bacterial_leaf_blight:warning",
            "created_at": NOW - timedelta(hours=50), "expires_at": NOW - timedelta(hours=2),
        }
    )
    existing = await repo.get_active_cooldown("f_1:bacterial_leaf_blight:warning", as_of=NOW)
    assert existing is None


@pytest.mark.asyncio
async def test_supersede_marks_prior_lower_severity_alert():
    repo = InMemoryAlertRepository()
    await repo.save(
        {
            "id": "alt_advisory", "farm_id": "f_1", "district": "Erode", "pathogen_name": "BLB",
            "target_crop": "samba_paddy", "target": "per_farm", "severity": "advisory",
            "trigger_reason": "x", "preventative_action": "y", "spoken_summary": "z",
            "delivery_channels": [], "cooldown_key": "f_1:bacterial_leaf_blight:advisory",
            "created_at": NOW, "expires_at": NOW + timedelta(hours=72),
        }
    )
    await repo.supersede_active_alerts("f_1", "bacterial_leaf_blight", as_of=NOW)
    superseded = await repo.get_active_cooldown("f_1:bacterial_leaf_blight:advisory", as_of=NOW)
    assert superseded is None  # no longer active


@pytest.mark.asyncio
async def test_get_farm_alerts_includes_per_farm_and_matching_broadcast():
    repo = InMemoryAlertRepository()
    await repo.save(
        {
            "id": "alt_farm", "farm_id": "f_1", "district": "Erode", "pathogen_name": "BLB",
            "target_crop": "samba_paddy", "target": "per_farm", "severity": "warning",
            "trigger_reason": "x", "preventative_action": "y", "spoken_summary": "z",
            "delivery_channels": [], "cooldown_key": "f_1:bacterial_leaf_blight:warning",
            "created_at": NOW, "expires_at": NOW + timedelta(hours=48),
        }
    )
    await repo.save(
        {
            "id": "alt_broadcast", "farm_id": None, "district": "Erode", "pathogen_name": "BLB",
            "target_crop": "samba_paddy", "target": "regional_broadcast", "severity": "advisory",
            "trigger_reason": "x", "preventative_action": "y", "spoken_summary": "z",
            "delivery_channels": [], "cooldown_key": "Erode:bacterial_leaf_blight:advisory",
            "created_at": NOW, "expires_at": NOW + timedelta(hours=72),
        }
    )
    await repo.save(
        {
            "id": "alt_other_district", "farm_id": None, "district": "Madurai", "pathogen_name": "BLB",
            "target_crop": "samba_paddy", "target": "regional_broadcast", "severity": "advisory",
            "trigger_reason": "x", "preventative_action": "y", "spoken_summary": "z",
            "delivery_channels": [], "cooldown_key": "Madurai:bacterial_leaf_blight:advisory",
            "created_at": NOW, "expires_at": NOW + timedelta(hours=72),
        }
    )

    results = await repo.get_farm_alerts(farm_id="f_1", district="Erode", crop="samba_paddy", as_of=NOW)
    ids = {r["id"] for r in results}
    assert ids == {"alt_farm", "alt_broadcast"}


@pytest.mark.asyncio
async def test_no_duplicate_rows_when_same_key_saved_twice():
    """Re-evaluating identical inputs (same deterministic alert_id) upserts,
    never duplicates — the phase-map gate: 'no dup rows'."""
    repo = InMemoryAlertRepository()
    row = {
        "id": "alt_1", "farm_id": "f_1", "district": "Erode", "pathogen_name": "BLB",
        "target_crop": "samba_paddy", "target": "per_farm", "severity": "warning",
        "trigger_reason": "x", "preventative_action": "y", "spoken_summary": "z",
        "delivery_channels": [], "cooldown_key": "f_1:bacterial_leaf_blight:warning",
        "created_at": NOW, "expires_at": NOW + timedelta(hours=48),
    }
    await repo.save(dict(row))
    await repo.save(dict(row))
    results = await repo.get_farm_alerts(farm_id="f_1", district="Erode", crop="samba_paddy", as_of=NOW)
    assert len(results) == 1


@pytest.mark.asyncio
async def test_dismiss_marks_dismissed_and_excludes_from_farm_alerts():
    repo = InMemoryAlertRepository()
    await repo.save(
        {
            "id": "alt_1", "farm_id": "f_1", "district": "Erode", "pathogen_name": "BLB",
            "target_crop": "samba_paddy", "target": "per_farm", "severity": "warning",
            "trigger_reason": "x", "preventative_action": "y", "spoken_summary": "z",
            "delivery_channels": [], "cooldown_key": "f_1:bacterial_leaf_blight:warning",
            "created_at": NOW, "expires_at": NOW + timedelta(hours=48),
        }
    )
    dismissed = await repo.dismiss("alt_1", "f_1", "action_taken", as_of=NOW)
    assert dismissed["status"] == "dismissed"

    results = await repo.get_farm_alerts(farm_id="f_1", district="Erode", crop="samba_paddy", as_of=NOW)
    assert results == []


@pytest.mark.asyncio
async def test_dismiss_unknown_alert_returns_none():
    repo = InMemoryAlertRepository()
    assert await repo.dismiss("nonexistent", "f_1", "action_taken", as_of=NOW) is None
