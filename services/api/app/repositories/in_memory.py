"""In-memory dictionary-backed repository implementations for Phase 0 and fallback testing."""

from dataclasses import dataclass
from datetime import date
from typing import Any
import uuid

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
    ) -> None:
        self._chunks.append(
            _StoredChunk(doc_id=doc_id, title=title, reviewed_on=reviewed_on, chunk_text=chunk_text, embedding=embedding)
        )

    async def commit(self) -> None:
        pass  # nothing to flush — writes are already visible

    async def similarity_search(self, query_embedding: list[float], top_k: int) -> list[RetrievedChunk]:
        scored = [
            RetrievedChunk(
                doc_id=c.doc_id,
                title=c.title,
                reviewed_on=c.reviewed_on,
                chunk_text=c.chunk_text,
                score=cosine_similarity(query_embedding, c.embedding),
            )
            for c in self._chunks
        ]
        scored.sort(key=lambda c: c.score, reverse=True)
        return scored[:top_k]
