"""Treatment application lifecycle (SPEC-EFFICACY-001 §3.3): opens one
``TreatmentApplication`` per diagnosed problem the corpus has a first-line
treatment for, then keeps it up to date as follow-up check-ins and
agronomist resolutions come in — synchronously, inside the same call, per
the spec's own rationale ("guarantee immediate consistency for KVK
analytics dashboards, eliminate background job lag").

Every method is best-effort and silent on "nothing to do" (no default
treatment for this label, no open application for this problem) — treatment
tracking is a secondary analytics concern layered on top of the diagnosis/
follow-up/resolution flows, never a reason those flows should fail.
"""

from datetime import date
from typing import Annotated
from uuid import uuid4

from fastapi import Depends

from app.core.enums import FollowupResponse
from app.domain.efficacy.default_treatments import get_default_treatment
from app.repositories.dependencies import get_treatment_application_repository
from app.repositories.interfaces import TreatmentApplicationRepository

# Spec §3.3: more than this many consecutive no_change check-ins without
# improvement closes the application as failed.
MAX_NO_CHANGE_BEFORE_FAILED = 2


class EfficacyTrackingService:
    """Writes to ``treatment_applications`` from the diagnose / follow-up /
    agronomist-resolve flows. Read-side aggregation lives in
    ``EfficacyAggregatorService`` — this service only ever mutates rows for
    one problem at a time, never scans across farms."""

    def __init__(self, repo: TreatmentApplicationRepository) -> None:
        self._repo = repo

    async def open_for_diagnosis(
        self,
        *,
        problem_id: str,
        farm_id: str,
        label: str,
        crop: str,
        district: str,
        applied_on: date | None = None,
    ) -> None:
        """Spec §3.4 Day-0: a fresh above-gate diagnosis is the moment the
        corpus's first-line treatment was recommended. Silently does
        nothing for labels the corpus has no first-line treatment for
        (``get_default_treatment`` returns ``None``) — never guesses one."""
        default = get_default_treatment(label)
        if default is None:
            return
        treatment_name, treatment_category = default
        await self._repo.open_application(
            {
                "id": str(uuid4()),
                "problem_id": problem_id,
                "farm_id": farm_id,
                "pathogen_type": label,
                "treatment_name": treatment_name,
                "treatment_category": treatment_category,
                "applied_on": applied_on or date.today(),
                "crop": crop,
                "district": district,
            }
        )

    async def attribute_followup(
        self,
        *,
        problem_id: str,
        response: FollowupResponse,
        as_of: date | None = None,
    ) -> None:
        """Spec §3.3's default attribution rule: every check-in attributes
        to the most recent still-open application for this problem. No-op
        if none is open (e.g. this problem's label had no default
        treatment, or every application on it is already closed)."""
        application = await self._repo.get_latest_open_for_problem(problem_id)
        if application is None:
            return

        if response == FollowupResponse.GOT_WORSE:
            await self._repo.close_application(
                application["id"],
                {"final_outcome": "failed", "failed_on_got_worse": True},
            )
            return

        if response == FollowupResponse.IMPROVED:
            followups = (application.get("followups_to_resolution") or 0) + 1
            today = as_of or date.today()
            days = (today - application["applied_on"]).days
            await self._repo.close_application(
                application["id"],
                {
                    "final_outcome": "improved",
                    "followups_to_resolution": followups,
                    "days_to_resolution": days,
                },
            )
            return

        # NO_CHANGE: bump the counter; close as failed once it stalls past
        # the spec's threshold rather than leave it open indefinitely.
        updated = await self._repo.increment_followups(application["id"])
        followups = (updated or {}).get("followups_to_resolution") or 0
        if followups > MAX_NO_CHANGE_BEFORE_FAILED:
            await self._repo.close_application(application["id"], {"final_outcome": "failed"})

    async def close_for_expert_resolution(self, *, problem_id: str, as_of: date | None = None) -> None:
        """Spec §3.3: a confirmed agronomist resolution closes whatever
        application is still open on this problem as ``resolved`` (distinct
        from a farmer's own ``improved`` self-report) and flags it as an
        expert-escalated case for the precautionary-vs-failure distinction
        in scoring (spec §4.1)."""
        application = await self._repo.get_latest_open_for_problem(problem_id)
        if application is None:
            return
        today = as_of or date.today()
        await self._repo.close_application(
            application["id"],
            {
                "final_outcome": "resolved",
                "days_to_resolution": (today - application["applied_on"]).days,
                "escalated_for_expert": True,
            },
        )


def get_efficacy_tracking_service(
    repo: Annotated[TreatmentApplicationRepository, Depends(get_treatment_application_repository)],
) -> EfficacyTrackingService:
    return EfficacyTrackingService(repo)
