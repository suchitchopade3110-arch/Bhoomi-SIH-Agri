"""Pure domain logic for government scheme staleness (checklist §10.4).

``SchemeResponse.last_verified`` (contract §2.14) exists, but until this
module nothing derived a live ``expiring``/``expired`` signal from it — the
seed data (``scripts/seed.py``) just hardcodes a ``status`` value per row
that happens to agree with its ``last_verified`` age on day one, and would
silently go stale forever after that (a scheme verified 200 days ago would
still read ``active`` if nobody remembered to flip the column by hand).

This computes the farmer-facing staleness status from ``last_verified``
every time a scheme is read, so it can never drift from the date it's
supposedly derived from. No I/O, no Settings dependency — same inputs,
same output, always.
"""

from datetime import date

from app.core.enums import SchemeStatus

# Named thresholds (not invented at the call site) — a scheme whose
# eligibility rules haven't been re-checked in this long is flagged so the
# farmer/officer knows to treat it with more caution, without the backend
# fabricating a claim that it's still fully current.
SCHEME_EXPIRING_AFTER_DAYS: int = 90
SCHEME_EXPIRED_AFTER_DAYS: int = 180

# Lifecycle statuses reflecting a farmer's own application progress —
# staleness recompute never overrides these; a farmer's "applied" scheme
# doesn't revert to "expired" just because the source rules aged.
_APPLICATION_LIFECYCLE_STATUSES = frozenset(
    {SchemeStatus.UPCOMING, SchemeStatus.APPLIED, SchemeStatus.APPROVED, SchemeStatus.REJECTED}
)


def compute_scheme_status(last_verified: date, stored_status: SchemeStatus, *, as_of: date | None = None) -> SchemeStatus:
    """The staleness-aware status to actually show for a scheme.

    ``stored_status`` is honored as-is for application-lifecycle states
    (upcoming/applied/approved/rejected) — those describe a farmer's own
    progress, not the source data's freshness. For active/expiring/expired,
    the status is always recomputed from ``last_verified`` against
    ``as_of`` (defaults to today), so a scheme can't stay "active" in the
    response just because a DB column was never updated.
    """
    if stored_status in _APPLICATION_LIFECYCLE_STATUSES:
        return stored_status

    today = as_of or date.today()
    days_since_verified = (today - last_verified).days
    if days_since_verified >= SCHEME_EXPIRED_AFTER_DAYS:
        return SchemeStatus.EXPIRED
    if days_since_verified >= SCHEME_EXPIRING_AFTER_DAYS:
        return SchemeStatus.EXPIRING
    return SchemeStatus.ACTIVE
