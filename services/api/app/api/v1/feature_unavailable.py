"""Flag-off stubs for the SIH26131-only routers (alerts, treatment efficacy).

Mounted by ``app/api/v1/__init__.py`` **only** when
``PROBLEM_STATEMENT != "sih26131"``, in place of the real ``alerts`` and
``efficacy`` routers. Every path the live routers publish is declared here so
that a client built against the SIH26131 contract gets one stable, documented
answer (``501 FEATURE_NOT_AVAILABLE``) instead of the framework's bare
``404 Not Found`` for an unmounted route — which is indistinguishable from
"that farm id does not exist".

Two deliberate choices:

- ``include_in_schema=False``. The OpenAPI document stays an honest
  description of what this deployment actually serves: under ``sih25076``
  these features are not in the contract, so they are not in the schema. The
  runtime answer is still explicit. ``tests/unit/test_problem_statement_gating.py``
  asserts this absence.
- **No auth dependency.** The flag-off answer does not depend on who is
  asking, so it is returned before authentication rather than hiding behind a
  ``401``. A client with an expired token still learns the real reason the
  call will never work here.

See docs/specs/problem_statement_flag_off_contract.md.
"""

from fastapi import APIRouter

from app.core.feature_flags import (
    FEATURE_ALERTS,
    FEATURE_TREATMENT_EFFICACY,
    raise_feature_not_available,
)

router = APIRouter(include_in_schema=False)


@router.get("/farms/{farm_id}/alerts")
async def alerts_unavailable(farm_id: str) -> None:
    raise_feature_not_available(FEATURE_ALERTS, "GET /api/v1/farms/{farm_id}/alerts")


@router.post("/alerts/{alert_id}/acknowledge")
async def alert_acknowledge_unavailable(alert_id: str) -> None:
    raise_feature_not_available(FEATURE_ALERTS, "POST /api/v1/alerts/{alert_id}/acknowledge")


@router.get("/treatments/{treatment_id}/efficacy")
async def treatment_efficacy_unavailable(treatment_id: str) -> None:
    raise_feature_not_available(
        FEATURE_TREATMENT_EFFICACY, "GET /api/v1/treatments/{treatment_id}/efficacy"
    )
