"""Assembles the Living Case Summary (contract §2.13's ``GET /cases/{id}``
shape, exactly) from repositories — farm + soil, the problem, the current
health snapshot, and the follow-up trend — then hands the plain,
already-fetched values to the pure ``domain.escalation.build_case_summary``.
All I/O for the compiler lives here; the domain function does no fetching
of its own.
"""

from datetime import datetime, timezone

from app.adapters.ports import StoragePort
from app.core.enums import HealthBand, ProblemSeverity
from app.domain.escalation import build_case_summary
from app.repositories.health_context import OpenProblemRecord, ProblemLoadReader, TreatmentTrendReader
from app.repositories.interfaces import FarmRepository
from app.schemas.case import CaseImage, CaseSummary, TimelineEvent
from app.services.health_service import HealthService

UNKNOWN_CROP = "Unknown crop"
UNKNOWN_SOIL_TYPE = "Unknown"
UNKNOWN_PROBLEM_LABEL = "Under investigation — not yet diagnosed"


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


class CaseSummaryCompiler:
    """Compiles one ``CaseSummary`` per escalation (contract §2.13)."""

    def __init__(
        self,
        farm_repo: FarmRepository,
        health_service: HealthService,
        problem_reader: ProblemLoadReader,
        treatment_reader: TreatmentTrendReader,
        storage_port: StoragePort | None = None,
    ) -> None:
        self._farm_repo = farm_repo
        self._health = health_service
        self._problem_reader = problem_reader
        self._treatment_reader = treatment_reader
        self._storage = storage_port

    async def compile(
        self,
        case_id: str,
        farm_id: str,
        severity: ProblemSeverity,
        status,
        problem_id: str | None = None,
        problem_summary: str | None = None,
        latest_image_asset_ids: list[str] | None = None,
    ) -> CaseSummary:
        """Gather every field contract §2.13's ``GET /cases/{id}`` requires
        and build the CaseSummary.

        Args:
            case_id: The new case's UUID string, assigned by the caller.
            farm_id: UUID string of the escalated farm.
            severity: Assessed problem severity.
            status: Case lifecycle status at the moment of compilation.
            problem_id: The open problem this case is about, if any — a
                below-gate/out-of-scope diagnosis escalation has none yet.
            problem_summary: Fallback problem label when there is no
                registered problem to look up (e.g. "confidence too low to
                diagnose").
            latest_image_asset_ids: Asset IDs of relevant photos.

        Returns:
            A complete ``CaseSummary`` matching contract §2.13 exactly.
        """
        farm = await self._farm_repo.get_by_id(farm_id) or {}
        snapshot = await self._health.get_latest(farm_id)
        open_problems = await self._problem_reader.get_open_problems(farm_id)
        trend = await self._treatment_reader.get_treatment_trend(farm_id)

        problem_record = self._resolve_problem(open_problems, problem_id)
        resolved_problem_id = problem_record.problem_id if problem_record else (problem_id or "unassigned")
        problem_label = (
            problem_record.label if problem_record and problem_record.label else (problem_summary or UNKNOWN_PROBLEM_LABEL)
        )

        timeline = await self._build_timeline(open_problems, trend, snapshot)
        images = await self._build_images(latest_image_asset_ids or [])

        return build_case_summary(
            case_id=case_id,
            farm_id=farm_id,
            crop=farm.get("primary_crop") or UNKNOWN_CROP,
            # Land verification (PRD §5.3) isn't this phase's aggregate — the
            # verified area is only known once that HITL flow lands; falls
            # back to the self-reported area until then (flagged assumption).
            area_acres_verified=farm.get("area_acres_verified") or farm.get("total_area_acres"),
            soil_type=farm.get("soil_type") or UNKNOWN_SOIL_TYPE,
            problem_id=resolved_problem_id,
            problem_label=problem_label,
            severity=severity,
            timeline=timeline,
            images=images,
            # No dedicated Treatment aggregate has its own phase yet — see
            # the class docstring's cross-reference. Empty rather than
            # fabricated.
            treatments_tried=[],
            followup_trend=trend.latest_followup_response,
            health_score=snapshot.score,
            health_band=HealthBand(snapshot.band),
            status=status,
        )

    @staticmethod
    def _resolve_problem(open_problems: list[OpenProblemRecord], problem_id: str | None) -> OpenProblemRecord | None:
        if problem_id is not None:
            match = next((p for p in open_problems if p.problem_id == problem_id), None)
            if match is not None:
                return match
        # A below-gate/out-of-scope escalation has no registered problem yet
        # — fall back to the farm's sole open problem, if it has exactly one.
        return open_problems[0] if len(open_problems) == 1 else None

    async def _build_images(self, asset_ids: list[str]) -> list[CaseImage]:
        images: list[CaseImage] = []
        for asset_id in asset_ids:
            url = f"/api/v1/assets/{asset_id}"
            if self._storage is not None:
                try:
                    url = await self._storage.generate_presigned_download_url(asset_id)
                except Exception:  # pragma: no cover — storage unavailable, fall back to the asset path
                    pass
            images.append(CaseImage(asset_id=asset_id, url=url))
        return images

    @staticmethod
    async def _build_timeline(open_problems, trend, snapshot) -> list[TimelineEvent]:
        """Key milestones leading to this escalation, assembled from the
        health engine's own read models.

        Flagged assumption: no dedicated Timeline aggregate/repository has
        its own phase yet, so this reads from the same problem/treatment/
        health-snapshot sources the score itself uses rather than a fuller
        event log — swap in a real ``TimelineRepository`` here once that
        phase lands; nothing else in the escalation subsystem would change.
        """
        timeline: list[TimelineEvent] = [
            TimelineEvent(at=_now_iso(), event="diagnosis", detail=f"{p.label or p.problem_id} ({p.severity.value})")
            for p in open_problems
        ]
        if trend.latest_followup_response is not None:
            timeline.append(
                TimelineEvent(
                    at=_now_iso(),
                    event="followup",
                    detail=f"{trend.latest_followup_response.value} (x{trend.consecutive_got_worse_count} worse in a row)",
                )
            )
        if snapshot is not None and snapshot.triggering_input:
            timeline.append(
                TimelineEvent(
                    at=snapshot.computed_at.isoformat() if snapshot.computed_at else _now_iso(),
                    event="health_recompute",
                    detail=str(snapshot.triggering_input),
                )
            )
        return timeline
