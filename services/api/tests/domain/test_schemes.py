"""Scheme staleness (checklist §10.4): ``expiring``/``expired`` must be a
live signal derived from ``last_verified``, not a static seed-data column
that can silently drift forever once nobody remembers to update it.
"""

from datetime import date, timedelta

from app.core.enums import SchemeStatus
from app.domain.schemes import (
    SCHEME_EXPIRED_AFTER_DAYS,
    SCHEME_EXPIRING_AFTER_DAYS,
    compute_scheme_status,
)

TODAY = date(2026, 8, 26)


def test_recently_verified_scheme_is_active():
    last_verified = TODAY - timedelta(days=SCHEME_EXPIRING_AFTER_DAYS - 1)
    assert compute_scheme_status(last_verified, SchemeStatus.ACTIVE, as_of=TODAY) == SchemeStatus.ACTIVE


def test_scheme_past_expiring_threshold_is_flagged_expiring():
    last_verified = TODAY - timedelta(days=SCHEME_EXPIRING_AFTER_DAYS)
    assert compute_scheme_status(last_verified, SchemeStatus.ACTIVE, as_of=TODAY) == SchemeStatus.EXPIRING


def test_scheme_past_expired_threshold_is_flagged_expired():
    last_verified = TODAY - timedelta(days=SCHEME_EXPIRED_AFTER_DAYS)
    assert compute_scheme_status(last_verified, SchemeStatus.ACTIVE, as_of=TODAY) == SchemeStatus.EXPIRED


def test_stale_seed_row_never_stuck_reading_active():
    # This is the exact bug the checklist flagged: a row whose stored
    # `status` column was hand-set to ACTIVE on day one and never touched
    # again must NOT keep reporting active once last_verified is old.
    ancient = TODAY - timedelta(days=SCHEME_EXPIRED_AFTER_DAYS + 100)
    assert compute_scheme_status(ancient, SchemeStatus.ACTIVE, as_of=TODAY) == SchemeStatus.EXPIRED


def test_application_lifecycle_status_is_never_overridden_by_staleness():
    ancient = TODAY - timedelta(days=SCHEME_EXPIRED_AFTER_DAYS + 100)
    for lifecycle_status in (
        SchemeStatus.UPCOMING,
        SchemeStatus.APPLIED,
        SchemeStatus.APPROVED,
        SchemeStatus.REJECTED,
    ):
        assert compute_scheme_status(ancient, lifecycle_status, as_of=TODAY) == lifecycle_status


def test_defaults_to_todays_date_when_as_of_omitted():
    # No as_of passed — must use the real current date, not silently no-op.
    assert compute_scheme_status(date.today(), SchemeStatus.ACTIVE) == SchemeStatus.ACTIVE
    long_ago = date.today() - timedelta(days=SCHEME_EXPIRED_AFTER_DAYS + 1)
    assert compute_scheme_status(long_ago, SchemeStatus.ACTIVE) == SchemeStatus.EXPIRED
