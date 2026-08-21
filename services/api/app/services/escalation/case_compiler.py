"""Assembles the Living Case Summary (contract §2.13) from repositories —
farm + land/soil, the current health snapshot, open-problem timeline, and
follow-up trend — then hands the plain, already-fetched values to the pure
``domain.escalation.build_case_summary``. All I/O for the compiler lives
here; the domain function does no fetching of its own.
"""

from app.core.enums import CaseStatus, LandStatus, ProblemSeverity
from app.domain.escalation import build_case_summary
from app.repositories.health_context import ProblemLoadReader, TreatmentTrendReader
from app.repositories.interfaces import FarmRepository, UserRepository
from app.schemas.case import CaseSummary
from app.services.health_service import HealthService

UNKNOWN_FARMER_NAME = "Unknown Farmer"
UNKNOWN_VILLAGE = "Unknown village"
UNKNOWN_DISTRICT = "Unknown district"
UNKNOWN_CROP = "Unknown crop"
DEFAULT_GROWTH_STAGE = "unspecified"


def _spoken_summary_for(farmer_name: str, crop: str, severity: ProblemSeverity, status: CaseStatus) -> str:
    """Short PRD §1.4 spoken summary for the case handoff."""
    if status == CaseStatus.RESOLVED:
        return f"{farmer_name}'s {crop} case has been resolved by an expert."
    return f"{farmer_name}'s {crop} case ({severity.value} severity) has been sent to an expert."


class CaseSummaryCompiler:
    """Compiles one ``CaseSummary`` per escalation (Phase 4 item 2)."""

    def __init__(
        self,
        farm_repo: FarmRepository,
        user_repo: UserRepository,
        health_service: HealthService,
        problem_reader: ProblemLoadReader,
        treatment_reader: TreatmentTrendReader,
    ) -> None:
        self._farm_repo = farm_repo
        self._user_repo = user_repo
        self._health = health_service
        self._problem_reader = problem_reader
        self._treatment_reader = treatment_reader

    async def compile(
        self,
        case_id: str,
        farm_id: str,
        problem_summary: str,
        severity: ProblemSeverity,
        status: CaseStatus,
        latest_images: list[str],
        escalated_to: str | None,
    ) -> CaseSummary:
        """Gather every field contract §2.13 requires and build the CaseSummary.

        Args:
            case_id: The new case's UUID string, assigned by the caller.
            farm_id: UUID string of the escalated farm.
            problem_summary: A concise description of the problem/trigger.
            severity: Assessed problem severity.
            status: Case lifecycle status at the moment of compilation.
            latest_images: Presigned URLs / asset IDs of relevant photos.
            escalated_to: Display name of the assigned agronomist, if routed.

        Returns:
            A complete, non-empty ``CaseSummary``.
        """
        farm = await self._farm_repo.get_by_id(farm_id) or {}
        farmer_name = UNKNOWN_FARMER_NAME
        farmer_id = farm.get("farmer_id")
        if farmer_id:
            user = await self._user_repo.get_by_id(farmer_id)
            if user:
                farmer_name = user.get("full_name") or UNKNOWN_FARMER_NAME

        snapshot = await self._health.get_latest(farm_id)
        open_problems = await self._problem_reader.get_open_problems(farm_id)
        trend = await self._treatment_reader.get_treatment_trend(farm_id)
        timeline_summary = self._build_timeline(open_problems, trend, snapshot)

        crop = farm.get("primary_crop") or UNKNOWN_CROP
        land_verified = str(farm.get("land_status", "")) == LandStatus.VERIFIED.value

        return build_case_summary(
            case_id=case_id,
            farm_id=farm_id,
            farmer_name=farmer_name,
            village=farm.get("village") or UNKNOWN_VILLAGE,
            district=farm.get("district") or UNKNOWN_DISTRICT,
            crop=crop,
            growth_stage=farm.get("growth_stage") or DEFAULT_GROWTH_STAGE,
            health_score=float(snapshot.score) if snapshot.score is not None else 0.0,
            land_verified=land_verified,
            problem_summary=problem_summary,
            severity=severity,
            status=status,
            timeline_summary=timeline_summary,
            latest_images=latest_images,
            escalated_to=escalated_to,
            spoken_summary=_spoken_summary_for(farmer_name, crop, severity, status),
        )

    @staticmethod
    def _build_timeline(open_problems, trend, snapshot) -> list[dict]:
        """Key milestones leading to this escalation, assembled from the
        health engine's own read models.

        Flagged assumption: no dedicated Timeline aggregate/repository has
        its own phase yet, so this reads from the same problem/treatment/
        health-snapshot sources the score itself uses rather than a fuller
        event log — swap in a real ``TimelineRepository`` here once that
        phase lands; nothing else in the escalation subsystem would change.
        """
        timeline: list[dict] = [
            {"type": "open_problem", "problem_id": p.problem_id, "severity": p.severity.value}
            for p in open_problems
        ]
        if trend.latest_followup_response is not None:
            timeline.append(
                {
                    "type": "followup",
                    "response": trend.latest_followup_response.value,
                    "consecutive_got_worse_count": trend.consecutive_got_worse_count,
                }
            )
        if snapshot is not None and snapshot.triggering_input:
            timeline.append({"type": "health_snapshot", **snapshot.triggering_input})
        return timeline
