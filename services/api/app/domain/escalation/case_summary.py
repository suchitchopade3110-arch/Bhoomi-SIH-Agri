"""The pre-analyzed bundle an agronomist opens (PRD §5.11, contract §2.13).

``compile_case_summary`` is pure assembly + validation: every piece
(farm/land/soil, problem, timeline slice, images, treatments, follow-up
trend, current health) is fetched by the caller
(``services/escalation/case_summary.py``) from the relevant repository
first; this function only shapes and validates the result so a case
summary can never be missing a required field.
"""

from dataclasses import dataclass, field


@dataclass(frozen=True)
class FarmRef:
    id: str
    crop: str
    area_acres_verified: float | None
    soil_type: str | None


@dataclass(frozen=True)
class ProblemRef:
    id: str
    label: str
    severity: str


@dataclass(frozen=True)
class TimelineEntry:
    at: str
    event: str
    detail: str


@dataclass(frozen=True)
class ImageRef:
    asset_id: str
    url: str


@dataclass(frozen=True)
class HealthRef:
    score: int | None
    band: str


@dataclass(frozen=True)
class CaseSummaryData:
    """Mirrors contract §2.13's ``GET /cases/{id}`` shape exactly."""

    case_id: str
    farm: FarmRef
    problem: ProblemRef | None
    current_health: HealthRef
    timeline: list[TimelineEntry] = field(default_factory=list)
    images: list[ImageRef] = field(default_factory=list)
    treatments_tried: list[str] = field(default_factory=list)
    followup_trend: str | None = None
    status: str = "open"


def compile_case_summary(
    case_id: str,
    farm: FarmRef,
    problem: ProblemRef | None,
    timeline: list[TimelineEntry],
    images: list[ImageRef],
    treatments_tried: list[str],
    followup_trend: str | None,
    current_health: HealthRef,
    status: str,
) -> CaseSummaryData:
    """Assemble and validate the CaseSummary. Never returns a summary
    missing ``case_id``, ``farm``, or ``current_health`` — those are the
    fields an agronomist cannot review a case without.

    Args:
        case_id: UUID string of the case.
        farm: Farm/land/soil reference (contract §2.13 ``farm``).
        problem: The confirmed problem, or ``None`` for a case opened
            before any problem was confirmed (e.g. a below-gate diagnosis).
        timeline: Chronological slice of events leading to escalation.
        images: Linked photo assets.
        treatments_tried: Treatments attempted so far.
        followup_trend: The latest follow-up response, or ``None``.
        current_health: The farm's current health score + band.
        status: Case lifecycle status (``open`` | ``assigned`` | ``resolved``).

    Returns:
        A populated ``CaseSummaryData``.
    """
    if not case_id:
        raise ValueError("case_id is required to compile a CaseSummary")
    if farm is None:
        raise ValueError("farm is required to compile a CaseSummary")
    if current_health is None:
        raise ValueError("current_health is required to compile a CaseSummary")

    return CaseSummaryData(
        case_id=case_id,
        farm=farm,
        problem=problem,
        timeline=list(timeline),
        images=list(images),
        treatments_tried=list(treatments_tried),
        followup_trend=followup_trend,
        current_health=current_health,
        status=status,
    )
