"""Gathers the data a CaseSummary needs from repositories, then hands it to
the pure ``domain.escalation.compile_case_summary`` (execution plan item 2).
"""

from typing import Annotated

from fastapi import Depends

from app.adapters.dependencies import get_storage_adapter
from app.adapters.ports import StoragePort
from app.domain.escalation import (
    CaseSummaryData,
    FarmRef,
    HealthRef,
    ImageRef,
    ProblemRef,
    TimelineEntry,
    compile_case_summary,
)
from app.repositories.dependencies import (
    get_farm_repository,
    get_problem_registry,
    get_treatment_trend_reader,
)
from app.repositories.health_context import TreatmentTrendReader
from app.repositories.interfaces import FarmRepository
from app.repositories.problem_registry import ProblemRegistry
from app.services.health_service import HealthService, get_health_service

# Fallbacks for farm fields when the Farm aggregate (no phase yet — Phase-0
# in-memory placeholder) has no profile on record for this farm_id.
UNKNOWN_CROP = "unspecified"
UNKNOWN_SOIL_TYPE = None


class CaseSummaryService:
    def __init__(
        self,
        farm_repo: FarmRepository,
        problem_registry: ProblemRegistry,
        health_service: HealthService,
        storage_port: StoragePort,
        treatment_trend_reader: TreatmentTrendReader,
    ) -> None:
        self._farms = farm_repo
        self._problems = problem_registry
        self._health = health_service
        self._storage = storage_port
        self._treatment_trend = treatment_trend_reader

    async def build(self, case_id: str, farm_id: str, problem_id: str | None, status: str) -> CaseSummaryData:
        """Assemble a full CaseSummaryData for ``farm_id`` / ``problem_id``.

        Every piece is fetched independently so a farm or problem missing
        one piece of data (e.g. no farm profile yet) degrades to an honest
        placeholder rather than failing the whole compilation — an
        agronomist should still get whatever context IS available.
        """
        farm_data = await self._farms.get_by_id(farm_id) or {}
        farm_ref = FarmRef(
            id=farm_id,
            crop=farm_data.get("primary_crop", UNKNOWN_CROP),
            area_acres_verified=farm_data.get("total_area_acres"),
            soil_type=farm_data.get("soil_type", UNKNOWN_SOIL_TYPE),
        )

        problem_ref: ProblemRef | None = None
        timeline: list[TimelineEntry] = []
        images: list[ImageRef] = []
        treatments_tried: list[str] = []
        followup_trend: str | None = None

        if problem_id:
            problem = await self._problems.get_problem(problem_id)
            if problem is not None:
                problem_ref = ProblemRef(id=problem.problem_id, label=problem.label, severity=problem.severity.value)
                timeline = [TimelineEntry(**e) for e in problem.timeline]
                treatments_tried = list(problem.treatments_tried)
                images = [
                    ImageRef(asset_id=asset_id, url=await self._storage.generate_presigned_download_url(asset_id))
                    for asset_id in problem.image_asset_ids
                ]

        trend = await self._treatment_trend.get_treatment_trend(farm_id)
        followup_trend = trend.latest_followup_response.value if trend.latest_followup_response else None

        snapshot = await self._health.get_latest(farm_id)
        current_health = HealthRef(score=snapshot.score, band=snapshot.band)

        return compile_case_summary(
            case_id=case_id,
            farm=farm_ref,
            problem=problem_ref,
            timeline=timeline,
            images=images,
            treatments_tried=treatments_tried,
            followup_trend=followup_trend,
            current_health=current_health,
            status=status,
        )


def get_case_summary_service(
    farm_repo: Annotated[FarmRepository, Depends(get_farm_repository)],
    problem_registry: Annotated[ProblemRegistry, Depends(get_problem_registry)],
    health_service: Annotated[HealthService, Depends(get_health_service)],
    storage_port: Annotated[StoragePort, Depends(get_storage_adapter)],
    treatment_trend_reader: Annotated[TreatmentTrendReader, Depends(get_treatment_trend_reader)],
) -> CaseSummaryService:
    return CaseSummaryService(farm_repo, problem_registry, health_service, storage_port, treatment_trend_reader)
