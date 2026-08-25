"""Read-side aggregation for ``GET /treatments/{treatment_id}/efficacy``
(SPEC-EFFICACY-001 §5). Loads every application matching one (pathogen,
treatment, crop, district) combination and reduces them with the pure
``domain.efficacy.score.compute_efficacy`` — this service's only job is the
I/O + row-shape translation around that pure function; the scoring rules
themselves live there, not here.
"""

from datetime import date
from typing import Annotated

from fastapi import Depends

from app.domain.efficacy import EfficacyResult, TreatmentApplicationSnapshot, compute_efficacy
from app.repositories.dependencies import get_treatment_application_repository
from app.repositories.interfaces import TreatmentApplicationRepository

DEFAULT_WINDOW_MONTHS = 12
MIN_SAMPLE_THRESHOLD = 10
# Spec §2.2's default window is literally 365 days, not 12 * 30 = 360 —
# months->days only approximates that for a caller-supplied window_months.
_DAYS_PER_MONTH = 365 / 12


def _row_to_snapshot(row: dict) -> TreatmentApplicationSnapshot:
    return TreatmentApplicationSnapshot(
        id=row["id"],
        pathogen_type=row["pathogen_type"],
        treatment_name=row["treatment_name"],
        crop=row["crop"],
        district=row["district"],
        applied_on=row["applied_on"],
        final_outcome=row.get("final_outcome"),
        followups_to_resolution=row.get("followups_to_resolution"),
        days_to_resolution=row.get("days_to_resolution"),
        failed_on_got_worse=bool(row.get("failed_on_got_worse")),
        escalated_for_expert=bool(row.get("escalated_for_expert")),
    )


class EfficacyAggregatorService:
    def __init__(self, repo: TreatmentApplicationRepository) -> None:
        self._repo = repo

    async def get_efficacy(
        self,
        *,
        treatment_name: str,
        pathogen_type: str,
        crop: str,
        district: str,
        window_months: int = DEFAULT_WINDOW_MONTHS,
        as_of: date | None = None,
    ) -> EfficacyResult:
        rows = await self._repo.list_for_aggregation(pathogen_type, treatment_name, crop, district)
        applications = [_row_to_snapshot(r) for r in rows]
        return compute_efficacy(
            treatment_name=treatment_name,
            pathogen_type=pathogen_type,
            crop=crop,
            district=district,
            applications=applications,
            as_of=as_of or date.today(),
            window_days=round(window_months * _DAYS_PER_MONTH),
            min_sample_threshold=MIN_SAMPLE_THRESHOLD,
        )


def get_efficacy_aggregator_service(
    repo: Annotated[TreatmentApplicationRepository, Depends(get_treatment_application_repository)],
) -> EfficacyAggregatorService:
    return EfficacyAggregatorService(repo)
