"""In-memory dictionary-backed repository implementations for Phase 0 and fallback testing."""

from dataclasses import dataclass
from datetime import date, datetime, timedelta
from typing import Any
import uuid

from app.core.errors import NotFoundError
from app.domain.alerts.models import ClusterCase
from app.domain.geo import haversine_distance_km
from app.domain.rag.similarity import cosine_similarity
from app.repositories.interfaces import RetrievedChunk


class InMemoryUserRepository:
    def __init__(self) -> None:
        self._users: dict[str, dict[str, Any]] = {}

    async def get_by_id(self, user_id: str) -> dict[str, Any] | None:
        return self._users.get(user_id)

    async def get_by_phone(self, phone: str) -> dict[str, Any] | None:
        for u in self._users.values():
            if u.get("phone_number") == phone:
                return u
        return None

    async def save(self, user_data: dict[str, Any]) -> dict[str, Any]:
        user_id = user_data.get("id") or str(uuid.uuid4())
        user_data["id"] = user_id
        self._users[user_id] = user_data
        return user_data


class InMemoryFarmRepository:
    def __init__(self) -> None:
        self._farms: dict[str, dict[str, Any]] = {}

    async def get_by_id(self, farm_id: str) -> dict[str, Any] | None:
        return self._farms.get(farm_id)

    async def get_by_farmer_id(self, farmer_id: str) -> list[dict[str, Any]]:
        return [f for f in self._farms.values() if f.get("farmer_id") == farmer_id]

    async def save(self, farm_data: dict[str, Any]) -> dict[str, Any]:
        farm_id = farm_data.get("id") or str(uuid.uuid4())
        farm_data["id"] = farm_id
        self._farms[farm_id] = farm_data
        return farm_data

    async def update(self, farm_id: str, updates: dict[str, Any]) -> dict[str, Any] | None:
        if farm_id in self._farms:
            self._farms[farm_id].update(updates)
            return self._farms[farm_id]
        return None


class InMemoryLandParcelRepository:
    def __init__(self) -> None:
        self._parcels: dict[str, dict[str, Any]] = {}

    async def get_by_id(self, parcel_id: str) -> dict[str, Any] | None:
        return self._parcels.get(parcel_id)

    async def get_by_farm_id(self, farm_id: str) -> dict[str, Any] | None:
        for p in self._parcels.values():
            if p.get("farm_id") == farm_id:
                return p
        return None

    async def get_pending_queue(self, district: str | None = None) -> list[dict[str, Any]]:
        results = [p for p in self._parcels.values() if p.get("status") == "pending_review"]
        if district:
            results = [p for p in results if p.get("district") == district]
        return results

    async def save(self, parcel_data: dict[str, Any]) -> dict[str, Any]:
        parcel_id = parcel_data.get("id") or str(uuid.uuid4())
        parcel_data["id"] = parcel_id
        self._parcels[parcel_id] = parcel_data
        return parcel_data

    async def update_status(self, parcel_id: str, status: str, boundary: dict[str, Any] | None = None) -> dict[str, Any] | None:
        if parcel_id in self._parcels:
            self._parcels[parcel_id]["status"] = status
            if boundary:
                self._parcels[parcel_id]["confirmed_boundary"] = boundary
            return self._parcels[parcel_id]
        return None


class InMemoryCaseRepository:
    def __init__(self) -> None:
        self._cases: dict[str, dict[str, Any]] = {}

    async def get_by_id(self, case_id: str) -> dict[str, Any] | None:
        return self._cases.get(case_id)

    async def get_by_farm_id(self, farm_id: str) -> list[dict[str, Any]]:
        return [c for c in self._cases.values() if c.get("farm_id") == farm_id]

    async def get_agronomist_queue(self, status: str | None = None) -> list[dict[str, Any]]:
        if status:
            return [c for c in self._cases.values() if c.get("status") == status]
        return list(self._cases.values())

    async def get_open_case_counts(self) -> dict[str, int]:
        counts: dict[str, int] = {}
        for case in self._cases.values():
            if case.get("status") in ("resolved", "closed"):
                continue
            assigned_to = case.get("assigned_to")
            if assigned_to:
                counts[assigned_to] = counts.get(assigned_to, 0) + 1
        return counts

    async def save(self, case_data: dict[str, Any]) -> dict[str, Any]:
        case_id = case_data.get("id") or str(uuid.uuid4())
        case_data["id"] = case_id
        self._cases[case_id] = case_data
        return case_data

    async def update_status(self, case_id: str, status: str, resolution: dict[str, Any] | None = None) -> dict[str, Any] | None:
        if case_id in self._cases:
            self._cases[case_id]["status"] = status
            if resolution:
                self._cases[case_id]["resolution"] = resolution
            return self._cases[case_id]
        return None


class InMemoryAdvisoryRepository:
    def __init__(self) -> None:
        self._advisories: dict[str, dict[str, Any]] = {}

    async def get_by_id(self, advisory_id: str) -> dict[str, Any] | None:
        return self._advisories.get(advisory_id)

    async def get_by_farm_id(self, farm_id: str) -> list[dict[str, Any]]:
        return [a for a in self._advisories.values() if a.get("farm_id") == farm_id]

    async def save(self, advisory_data: dict[str, Any]) -> dict[str, Any]:
        advisory_id = advisory_data.get("id") or str(uuid.uuid4())
        advisory_data["id"] = advisory_id
        self._advisories[advisory_id] = advisory_data
        return advisory_data


class InMemoryHealthRepository:
    def __init__(self) -> None:
        self._snapshots: list[dict[str, Any]] = []

    async def get_latest_by_farm_id(self, farm_id: str) -> dict[str, Any] | None:
        farm_snapshots = [s for s in self._snapshots if s.get("farm_id") == farm_id]
        return farm_snapshots[-1] if farm_snapshots else None

    async def get_history_by_farm_id(self, farm_id: str) -> list[dict[str, Any]]:
        return [s for s in self._snapshots if s.get("farm_id") == farm_id]

    async def save_snapshot(self, snapshot_data: dict[str, Any]) -> dict[str, Any]:
        self._snapshots.append(snapshot_data)
        return snapshot_data


class InMemorySchemeRepository:
    def __init__(self) -> None:
        self._schemes: dict[str, dict[str, Any]] = {}

    async def get_by_id(self, scheme_id: str) -> dict[str, Any] | None:
        return self._schemes.get(scheme_id)

    async def list_active_schemes(self) -> list[dict[str, Any]]:
        return list(self._schemes.values())

    async def match_schemes(self, crop: str, category: str, acres: float) -> list[dict[str, Any]]:
        return list(self._schemes.values())


class InMemoryAssetRepository:
    def __init__(self) -> None:
        self._assets: dict[str, dict[str, Any]] = {}

    async def get_by_id(self, asset_id: str) -> dict[str, Any] | None:
        return self._assets.get(asset_id)

    async def save(self, asset_data: dict[str, Any]) -> dict[str, Any]:
        asset_id = asset_data.get("id") or str(uuid.uuid4())
        asset_data["id"] = asset_id
        self._assets[asset_id] = asset_data
        return asset_data


@dataclass(frozen=True)
class _StoredChunk:
    doc_id: str
    title: str
    reviewed_on: date
    chunk_text: str
    embedding: list[float]
    content_type: str | None = None
    crop: str | None = None


class InMemoryKnowledgeChunkRepository:
    """Pure-Python stand-in for ``KnowledgeChunkRepository`` — no Postgres/
    pgvector required. Computes cosine similarity directly, so it agrees
    with the real repository's ranking for the same embeddings. Used in
    tests to keep the RAG pipeline deterministic and offline."""

    def __init__(self) -> None:
        self._chunks: list[_StoredChunk] = []

    # Same async method names/signatures as KnowledgeChunkRepository (minus
    # chunk_index, which this store doesn't need to keep) so
    # services.rag.ingest.ingest_corpus works unmodified against either.
    async def delete_all(self) -> None:
        self._chunks = []

    async def add_chunk(
        self,
        doc_id: str,
        title: str,
        reviewed_on: date,
        chunk_index: int,
        chunk_text: str,
        embedding: list[float],
        content_type: str | None = None,
        crop: str | None = None,
    ) -> None:
        self._chunks.append(
            _StoredChunk(
                doc_id=doc_id,
                title=title,
                reviewed_on=reviewed_on,
                chunk_text=chunk_text,
                embedding=embedding,
                content_type=content_type,
                crop=crop,
            )
        )

    async def commit(self) -> None:
        pass  # nothing to flush — writes are already visible

    async def similarity_search(
        self, query_embedding: list[float], top_k: int, content_type: str | None = None
    ) -> list[RetrievedChunk]:
        candidates = self._chunks
        if content_type is not None:
            candidates = [c for c in candidates if c.content_type == content_type]

        scored = [
            RetrievedChunk(
                doc_id=c.doc_id,
                title=c.title,
                reviewed_on=c.reviewed_on,
                chunk_text=c.chunk_text,
                score=cosine_similarity(query_embedding, c.embedding),
            )
            for c in candidates
        ]
        scored.sort(key=lambda c: c.score, reverse=True)
        return scored[:top_k]


class InMemoryAlertRepository:
    """In-memory ``AlertRepository`` (Phase 3) — tests seed nearby confirmed
    diagnoses directly via ``seed_nearby_case`` rather than joining live
    ``farms``/``problems`` state, keeping this repository double self
    contained and independent of other repositories' internal storage."""

    def __init__(self) -> None:
        self._alerts: dict[str, dict[str, Any]] = {}
        self._nearby_cases: list[dict[str, Any]] = []
        self._farm_locations: dict[str, tuple[float, float]] = {}

    def register_farm(self, farm_id: str, latitude: float, longitude: float) -> None:
        """Register a farm's own coordinates — needed so
        ``get_nearby_cluster_summary(target_farm_id, ...)`` can look up
        ``target_farm_id``'s location itself, matching the Postgres
        implementation's internal ``Farm`` lookup."""
        self._farm_locations[farm_id] = (latitude, longitude)

    def seed_nearby_case(
        self, *, farm_id: str, latitude: float, longitude: float, label: str, severity: str, created_at: datetime
    ) -> None:
        self._farm_locations[farm_id] = (latitude, longitude)
        self._nearby_cases.append(
            {
                "farm_id": farm_id,
                "latitude": latitude,
                "longitude": longitude,
                "label": label,
                "severity": severity,
                "created_at": created_at,
            }
        )

    async def get_nearby_cluster_summary(
        self, target_farm_id: str, radius_meters: float, window_days: int
    ) -> list[ClusterCase]:
        if target_farm_id not in self._farm_locations:
            raise NotFoundError("Farm not found.", details={"farm_id": target_farm_id})
        target_farm_lat, target_farm_lon = self._farm_locations[target_farm_id]
        radius_km = radius_meters / 1000.0

        cutoff = datetime.utcnow() - timedelta(days=window_days)
        grouped: dict[tuple[str, str], list[float]] = {}
        for case in self._nearby_cases:
            if case["farm_id"] == target_farm_id:
                continue
            if case["created_at"] < cutoff:
                continue
            distance = haversine_distance_km(target_farm_lat, target_farm_lon, case["latitude"], case["longitude"])
            if distance > radius_km:
                continue
            key = (case["label"], case["severity"])
            grouped.setdefault(key, []).append(distance)

        return [
            ClusterCase(label=label, severity=severity, case_count=len(distances), min_distance_km=min(distances))
            for (label, severity), distances in grouped.items()
        ]

    async def get_active_cooldown(self, cooldown_key: str, as_of: datetime) -> dict[str, Any] | None:
        for alert in self._alerts.values():
            if (
                alert["cooldown_key"] == cooldown_key
                and alert["status"] == "active"
                and alert["expires_at"] > as_of
            ):
                return alert
        return None

    async def supersede_active_alerts(self, subject: str, pathogen_id: str, as_of: datetime) -> None:
        for alert in self._alerts.values():
            if (
                alert["cooldown_key"].startswith(f"{subject}:{pathogen_id}:")
                and alert["status"] == "active"
                and alert["expires_at"] > as_of
            ):
                alert["status"] = "superseded"

    async def save(self, alert_data: dict[str, Any]) -> dict[str, Any]:
        alert_id = alert_data["id"]
        alert_data.setdefault("status", "active")
        self._alerts[alert_id] = alert_data
        return alert_data

    async def get_farm_alerts(self, farm_id: str, district: str, crop: str | None, as_of: datetime) -> list[dict[str, Any]]:
        results = []
        for alert in self._alerts.values():
            if alert["status"] != "active" or alert["expires_at"] <= as_of:
                continue
            per_farm_match = alert.get("farm_id") == farm_id
            broadcast_match = alert.get("farm_id") is None and alert["district"] == district and (
                alert.get("target_crop") is None or alert.get("target_crop") == crop
            )
            if per_farm_match or broadcast_match:
                results.append(alert)
        results.sort(key=lambda a: a["created_at"], reverse=True)
        return results

    async def dismiss(self, alert_id: str, farm_id: str, reason: str, as_of: datetime) -> dict[str, Any] | None:
        alert = self._alerts.get(alert_id)
        if alert is None:
            return None
        alert["status"] = "dismissed"
        alert["dismissed_at"] = as_of
        alert["dismiss_reason"] = reason
        return alert


class InMemoryTreatmentApplicationRepository:
    """Settable in-memory ``TreatmentApplicationRepository`` (SPEC-EFFICACY-001)
    for demo/dev/tests — same dict-in/dict-out shape as
    ``PostgresTreatmentApplicationRepository``."""

    def __init__(self) -> None:
        self._applications: dict[str, dict[str, Any]] = {}

    async def open_application(self, application: dict[str, Any]) -> dict[str, Any]:
        application_id = application.get("id") or str(uuid.uuid4())
        application["id"] = application_id
        application.setdefault("final_outcome", None)
        application.setdefault("followups_to_resolution", None)
        application.setdefault("days_to_resolution", None)
        application.setdefault("failed_on_got_worse", False)
        application.setdefault("escalated_for_expert", False)
        self._applications[application_id] = application
        return application

    async def get_latest_open_for_problem(self, problem_id: str) -> dict[str, Any] | None:
        open_apps = [
            a for a in self._applications.values() if a["problem_id"] == problem_id and a.get("final_outcome") is None
        ]
        if not open_apps:
            return None
        return max(open_apps, key=lambda a: a["applied_on"])

    async def close_application(self, application_id: str, updates: dict[str, Any]) -> dict[str, Any] | None:
        application = self._applications.get(application_id)
        if application is None:
            return None
        application.update(updates)
        return application

    async def increment_followups(self, application_id: str) -> dict[str, Any] | None:
        application = self._applications.get(application_id)
        if application is None:
            return None
        application["followups_to_resolution"] = (application.get("followups_to_resolution") or 0) + 1
        return application

    async def list_for_aggregation(
        self, pathogen_type: str, treatment_name: str, crop: str, district: str
    ) -> list[dict[str, Any]]:
        return [
            a
            for a in self._applications.values()
            if a["pathogen_type"] == pathogen_type
            and a["treatment_name"] == treatment_name
            and a["crop"] == crop
            and a["district"] == district
        ]
