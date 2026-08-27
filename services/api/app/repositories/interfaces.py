"""Repository interface protocols for all database aggregates."""

from dataclasses import dataclass
from datetime import date, datetime
from typing import Any, Protocol

from app.domain.alerts.models import ClusterCase


class UserRepository(Protocol):
    async def get_by_id(self, user_id: str) -> dict[str, Any] | None: ...
    async def get_by_phone(self, phone: str) -> dict[str, Any] | None: ...
    async def save(self, user_data: dict[str, Any]) -> dict[str, Any]: ...


class FarmRepository(Protocol):
    async def get_by_id(self, farm_id: str) -> dict[str, Any] | None: ...
    async def get_by_farmer_id(self, farmer_id: str) -> list[dict[str, Any]]: ...
    async def save(self, farm_data: dict[str, Any]) -> dict[str, Any]: ...
    async def update(self, farm_id: str, updates: dict[str, Any]) -> dict[str, Any] | None: ...


class CaseRepository(Protocol):
    async def get_by_id(self, case_id: str) -> dict[str, Any] | None: ...
    async def get_by_farm_id(self, farm_id: str) -> list[dict[str, Any]]: ...
    async def get_agronomist_queue(self, status: str | None = None) -> list[dict[str, Any]]: ...
    async def get_open_case_counts(self) -> dict[str, int]:
        """Count of open/assigned/escalated/investigating cases per
        ``assigned_to`` agronomist id (Phase 2, PRD §5.11) — backs
        next-available routing. Resolved/closed cases don't count."""
        ...
    async def save(self, case_data: dict[str, Any]) -> dict[str, Any]: ...
    async def update_status(self, case_id: str, status: str, resolution: dict[str, Any] | None = None) -> dict[str, Any] | None: ...


class AdvisoryRepository(Protocol):
    async def get_by_id(self, advisory_id: str) -> dict[str, Any] | None: ...
    async def get_by_farm_id(self, farm_id: str) -> list[dict[str, Any]]: ...
    async def save(self, advisory_data: dict[str, Any]) -> dict[str, Any]: ...


class HealthRepository(Protocol):
    async def get_latest_by_farm_id(self, farm_id: str) -> dict[str, Any] | None: ...
    async def get_history_by_farm_id(self, farm_id: str) -> list[dict[str, Any]]: ...
    async def save_snapshot(self, snapshot_data: dict[str, Any]) -> dict[str, Any]: ...


class SchemeRepository(Protocol):
    async def get_by_id(self, scheme_id: str) -> dict[str, Any] | None: ...
    async def list_active_schemes(self) -> list[dict[str, Any]]: ...
    async def match_schemes(self, crop: str, category: str, acres: float) -> list[dict[str, Any]]: ...


class AssetRepository(Protocol):
    async def get_by_id(self, asset_id: str) -> dict[str, Any] | None: ...
    async def save(self, asset_data: dict[str, Any]) -> dict[str, Any]: ...


class AlertRepository(Protocol):
    """Backs the Early-Warning Alert System (SPEC-ALERT-001, Phase 3).

    All spatial filtering happens here — bounding box in SQL, exact radius
    cut via ``app.domain.geo.haversine_distance_km`` in Python (Phase 1's
    geo-approach decision: no PostGIS extension in the actual DB image).
    Callers in ``services/`` never see SQL or raw ``problems``/``farms`` rows.
    """

    async def get_nearby_cluster_summary(
        self, target_farm_id: str, radius_meters: float, window_days: int
    ) -> list[ClusterCase]:
        """Confirmed-diagnosis clusters near ``target_farm_id`` — the
        repository looks up that farm's own coordinates internally (a
        caller never passes lat/lon)."""
        ...

    async def get_active_cooldown(self, cooldown_key: str, as_of: datetime) -> dict[str, Any] | None: ...

    async def supersede_active_alerts(self, subject: str, pathogen_id: str, as_of: datetime) -> None:
        """Mark active alerts for ``(subject, pathogen_id)`` (any severity)
        superseded — subject is ``farm_id`` or ``district`` matching
        ``AlertDraft.cooldown_key``'s first segment (spec §4.2's upgrade
        exception: a farmer never sees two contradictory concurrent alerts
        for the same pathogen)."""
        ...

    async def save(self, alert_data: dict[str, Any]) -> dict[str, Any]: ...

    async def get_farm_alerts(self, farm_id: str, district: str, crop: str | None, as_of: datetime) -> list[dict[str, Any]]: ...

    async def dismiss(self, alert_id: str, farm_id: str, reason: str, as_of: datetime) -> dict[str, Any] | None: ...


class TreatmentApplicationRepository(Protocol):
    """Backs Treatment Efficacy Tracking (SPEC-EFFICACY-001).

    Writers open one application per (problem, treatment) and close it as
    the followup lifecycle resolves it (spec §3.3); the aggregation reader
    lists every application matching one (pathogen, treatment, crop,
    district) combination for ``domain.efficacy.score.compute_efficacy`` to
    reduce over — filtering by window is the pure function's job, not the
    repository's, so the same rows always produce the same result
    regardless of which window a caller asks for.
    """

    async def open_application(self, application: dict[str, Any]) -> dict[str, Any]: ...

    async def get_latest_open_for_problem(self, problem_id: str) -> dict[str, Any] | None: ...

    async def close_application(self, application_id: str, updates: dict[str, Any]) -> dict[str, Any] | None: ...

    async def increment_followups(self, application_id: str) -> dict[str, Any] | None: ...

    async def list_for_aggregation(
        self, pathogen_type: str, treatment_name: str, crop: str, district: str
    ) -> list[dict[str, Any]]: ...


@dataclass(frozen=True)
class RetrievedChunk:
    """One corpus chunk returned by similarity search, with its score.

    Decoupled from the ``KnowledgeChunk`` ORM model so callers (and tests)
    never need a live Postgres/pgvector connection to work with retrieval
    results.
    """

    doc_id: str
    title: str
    reviewed_on: date
    chunk_text: str
    score: float  # cosine similarity in [0.0, 1.0]; 1.0 = identical


class KnowledgeChunkReader(Protocol):
    """Read-only similarity search over the curated RAG corpus (PRD §5.7)."""

    async def similarity_search(
        self, query_embedding: list[float], top_k: int, content_type: str | None = None
    ) -> list[RetrievedChunk]: ...
