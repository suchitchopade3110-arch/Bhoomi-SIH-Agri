"""PROBLEM_STATEMENT feature gating: the flag-off contract.

``PROBLEM_STATEMENT`` (app/core/config.py) selects which feature set this
deployment serves. Under ``sih26131`` the surveillance features — early
warning alerts and treatment efficacy — are live. Under any other value they
are not part of the contract, and this module defines the single, stable
answer callers get instead.

Design rules, from docs/specs/problem_statement_flag_off_contract.md:

- **Never an empty 200.** ``{"active_alerts": []}`` is indistinguishable from
  "this farm currently has no alerts", so a client would render a healthy
  empty state for a feature that does not exist here.
- **Never a 500.** Nothing failed. The deployment is configured for a
  different problem statement, which is a normal, expected state.
- **Never a bare 404.** ``/farms/{id}/alerts`` returning ``NOT_FOUND`` cannot
  be told apart from "that farm id does not exist".
- **Always ``501 FEATURE_NOT_AVAILABLE``**, in the standard Bhoomi error
  envelope, carrying which feature, which endpoint, the active problem
  statement, and the one that would enable it.
"""

from typing import Final

from app.core.config import PROBLEM_STATEMENT_DEFAULT, Settings, get_settings
from app.core.errors import FeatureNotAvailableError

# The problem statement the SIH26131-only features require. Named rather than
# inlined so the router gate, the stub responses, and the tests all agree.
SIH26131: Final[str] = PROBLEM_STATEMENT_DEFAULT

# Stable ``details.feature`` identifiers. Clients may branch on these; they
# are part of the published contract and must not be renamed silently.
FEATURE_ALERTS: Final[str] = "early_warning_alerts"
FEATURE_TREATMENT_EFFICACY: Final[str] = "treatment_efficacy"


def is_sih26131(settings: Settings | None = None) -> bool:
    """True when the SIH26131 feature set (alerts, treatment efficacy) is on.

    Reads the always-defined ``PROBLEM_STATEMENT`` field — no ``getattr``
    fallback, no ``os.environ`` lookup, so this cannot silently evaluate
    against an undefined flag.
    """
    return (settings or get_settings()).PROBLEM_STATEMENT == SIH26131


def feature_not_available(feature: str, endpoint: str) -> FeatureNotAvailableError:
    """Build the documented flag-off error for one SIH26131-only endpoint."""
    active = get_settings().PROBLEM_STATEMENT
    return FeatureNotAvailableError(
        message=(
            f"'{feature}' is not available under PROBLEM_STATEMENT={active}. "
            f"It is part of the {SIH26131} feature set; set PROBLEM_STATEMENT={SIH26131} "
            "to enable it."
        ),
        details={
            "feature": feature,
            "endpoint": endpoint,
            "active_problem_statement": active,
            "required_problem_statement": SIH26131,
        },
    )


def raise_feature_not_available(feature: str, endpoint: str) -> None:
    """Raise the documented flag-off error. Never returns."""
    raise feature_not_available(feature, endpoint)
