"""Real ``AlertRepository`` backed by the ``alerts`` table (SPEC-ALERT-001,
Phase 3, build order Step 2).

Spatial filtering: a cheap bounding-box SQL pre-filter, then the exact
radius cut via ``domain.geo.haversine_distance_km`` in Python — Phase 1's
geo-approach decision (no PostGIS extension in the actual DB image; see
``docs/specs/early_warning_alert_spec.md`` §3.3). All SQL for this
aggregate lives only in this file — ``services/alerts/alert_service.py``
never sees a query.
"""

from datetime import datetime, timedelta
from typing import Any

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.errors import NotFoundError
from app.domain.alerts.models import ClusterCase
from app.domain.geo import bounding_box, haversine_distance_km
from app.models.alert import Alert
from app.models.farm import Farm
from app.models.problem import Problem


def _row_to_dict(row: Any) -> dict[str, Any]:
    return {c.name: getattr(row, c.name) for c in row.__table__.columns}


class PostgresAlertRepository:
    def __init__(self, session: AsyncSession) -> None:
        self._session = session

    async def get_nearby_cluster_summary(
        self, target_farm_id: str, radius_meters: float, window_days: int
    ) -> list[ClusterCase]:
        target_farm = await self._session.get(Farm, target_farm_id)
        if target_farm is None:
            raise NotFoundError("Farm not found.", details={"farm_id": target_farm_id})

        radius_km = radius_meters / 1000.0
        min_lat, max_lat, min_lon, max_lon = bounding_box(target_farm.latitude, target_farm.longitude, radius_km)
        cutoff = datetime.utcnow() - timedelta(days=window_days)

        stmt = (
            select(Problem.label, Problem.severity, Farm.id, Farm.latitude, Farm.longitude)
            .join(Farm, Problem.farm_id == Farm.id)
            .where(
                Problem.created_at >= cutoff,
                Farm.latitude.between(min_lat, max_lat),
                Farm.longitude.between(min_lon, max_lon),
                Farm.id != target_farm_id,
            )
        )
        result = await self._session.execute(stmt)

        grouped: dict[tuple[str, str], list[float]] = {}
        for label, severity, _farm_id, latitude, longitude in result.all():
            distance = haversine_distance_km(target_farm.latitude, target_farm.longitude, latitude, longitude)
            if distance > radius_km:
                continue
            grouped.setdefault((label, severity), []).append(distance)

        return [
            ClusterCase(label=label, severity=severity, case_count=len(distances), min_distance_km=min(distances))
            for (label, severity), distances in grouped.items()
        ]

    async def get_active_cooldown(self, cooldown_key: str, as_of: datetime) -> dict[str, Any] | None:
        stmt = select(Alert).where(
            Alert.cooldown_key == cooldown_key, Alert.status == "active", Alert.expires_at > as_of
        )
        result = await self._session.execute(stmt)
        row = result.scalars().first()
        return _row_to_dict(row) if row else None

    async def supersede_active_alerts(self, subject: str, pathogen_id: str, as_of: datetime) -> None:
        prefix = f"{subject}:{pathogen_id}:"
        stmt = select(Alert).where(
            Alert.cooldown_key.like(f"{prefix}%"), Alert.status == "active", Alert.expires_at > as_of
        )
        result = await self._session.execute(stmt)
        for row in result.scalars().all():
            row.status = "superseded"
        await self._session.commit()

    async def save(self, alert_data: dict[str, Any]) -> dict[str, Any]:
        alert_id = alert_data["id"]
        existing = await self._session.get(Alert, alert_id)
        if existing is not None:
            # Re-evaluating identical inputs on the same day (same deterministic
            # alert_id) is idempotent — update in place, not a duplicate row.
            for key, value in alert_data.items():
                if hasattr(Alert, key):
                    setattr(existing, key, value)
            await self._session.commit()
            await self._session.refresh(existing)
            return _row_to_dict(existing)

        alert_data.setdefault("status", "active")
        row = Alert(**{k: v for k, v in alert_data.items() if hasattr(Alert, k)})
        self._session.add(row)
        await self._session.commit()
        await self._session.refresh(row)
        return _row_to_dict(row)

    async def get_farm_alerts(self, farm_id: str, district: str, crop: str | None, as_of: datetime) -> list[dict[str, Any]]:
        per_farm = Alert.farm_id == farm_id
        broadcast = (Alert.farm_id.is_(None)) & (Alert.district == district)
        if crop is not None:
            broadcast = broadcast & ((Alert.target_crop.is_(None)) | (Alert.target_crop == crop))

        stmt = (
            select(Alert)
            .where(Alert.status == "active", Alert.expires_at > as_of, per_farm | broadcast)
            .order_by(Alert.created_at.desc())
        )
        result = await self._session.execute(stmt)
        return [_row_to_dict(r) for r in result.scalars().all()]

    async def dismiss(self, alert_id: str, farm_id: str, reason: str, as_of: datetime) -> dict[str, Any] | None:
        row = await self._session.get(Alert, alert_id)
        if row is None:
            return None
        row.status = "dismissed"
        row.dismissed_at = as_of
        row.dismiss_reason = reason
        await self._session.commit()
        await self._session.refresh(row)
        return _row_to_dict(row)
