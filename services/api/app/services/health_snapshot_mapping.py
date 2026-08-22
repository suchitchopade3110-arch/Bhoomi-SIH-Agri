"""Shared ORM-row -> API-schema mapping for ``HealthSnapshot`` (contract §2.9).

Factored out of ``api/v1/health.py`` so any other service that needs to hand
a farmer a fresh snapshot (follow-up check-in, case resolution) uses the
exact same mapping instead of re-deriving it.
"""

from app.core.enums import HealthBand
from app.models.health_snapshot import HealthSnapshot as HealthSnapshotRow
from app.schemas.health import HealthSnapshot as HealthSnapshotSchema
from app.schemas.health import SubIndexBreakdown


def spoken_summary_for(row: HealthSnapshotRow) -> str:
    """Short, voice-first summary for local TTS (PRD §5.1, contract §1.4)."""
    if row.band == HealthBand.UNRATED.value:
        return "Your farm health score is not yet available. A few more details are needed."
    summary = f"Your farm health score is {row.score}, which is {row.band}."
    trigger_type = (row.triggering_input or {}).get("type")
    if trigger_type == "diagnosis":
        summary += " This reflects an active problem on your farm."
    elif trigger_type == "followup":
        summary += " This reflects your latest follow-up report."
    elif trigger_type == "case_resolution":
        summary += " Your problem has been resolved."
    return summary


def snapshot_row_to_schema(row: HealthSnapshotRow) -> HealthSnapshotSchema:
    """Map a persisted ``HealthSnapshot`` row onto the contract §2.9 response shape."""
    return HealthSnapshotSchema(
        score=row.score,
        band=HealthBand(row.band),
        computed_at=row.computed_at,
        weights_version=row.weights_version,
        subindices=[SubIndexBreakdown(**s) for s in row.subindices],
        triggering_input=row.triggering_input,
        missing_fields=row.missing_fields,
        spoken_summary=spoken_summary_for(row),
    )
