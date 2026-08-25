"""In-memory OTP code store with expiry, resend cooldown, and attempt
limiting (PRD §2.3 farmer phone-OTP login).

In-memory rather than DB-backed: an OTP is a short-lived (5 minute)
credential, never queried historically, and losing it on a process
restart just means the farmer requests a new one — a strictly weaker
consistency requirement than every other piece of state in this app,
which is why this is the one place an in-memory store is the right
choice rather than a stopgap (contrast ``repositories/in_memory.py``,
which exists only because the Postgres-backed counterpart isn't wired for
tests). The real caveat: this does not survive a multi-worker/multi-
process deployment (each worker has its own store) — fine for this
project's single-process demo deployment, a real constraint to flag if
this ever runs behind multiple uvicorn workers.
"""

from dataclasses import dataclass, field
from datetime import datetime, timedelta

OTP_LENGTH = 6
OTP_TTL = timedelta(minutes=5)
RESEND_COOLDOWN = timedelta(seconds=60)
MAX_VERIFY_ATTEMPTS = 5


@dataclass
class _OtpRecord:
    code: str
    expires_at: datetime
    requested_at: datetime
    attempts: int = 0


class OtpStore:
    """Keyed by phone number. One live code per phone at a time — a new
    request overwrites the old one (matches how every real OTP UX works:
    "resend" invalidates the previous code)."""

    def __init__(self) -> None:
        self._records: dict[str, _OtpRecord] = {}

    def can_request(self, phone_number: str, as_of: datetime) -> bool:
        """False if a code was requested for this phone within the last
        ``RESEND_COOLDOWN`` — prevents SMS-bombing a phone number."""
        record = self._records.get(phone_number)
        if record is None:
            return True
        return as_of - record.requested_at >= RESEND_COOLDOWN

    def issue(self, phone_number: str, code: str, as_of: datetime) -> None:
        self._records[phone_number] = _OtpRecord(code=code, expires_at=as_of + OTP_TTL, requested_at=as_of)

    def verify(self, phone_number: str, code: str, as_of: datetime) -> bool:
        """Consumes the attempt regardless of outcome (a wrong guess still
        counts toward ``MAX_VERIFY_ATTEMPTS``) and consumes the code itself
        on success (single-use) or once attempts are exhausted (forces a
        fresh ``/otp/request``)."""
        record = self._records.get(phone_number)
        if record is None:
            return False
        if as_of > record.expires_at:
            del self._records[phone_number]
            return False

        record.attempts += 1
        if record.attempts > MAX_VERIFY_ATTEMPTS:
            del self._records[phone_number]
            return False

        if record.code != code:
            return False

        del self._records[phone_number]
        return True


_default_store = OtpStore()


def get_otp_store() -> OtpStore:
    """Process-wide singleton — see module docstring for why in-memory is
    the right call here, and its one real caveat."""
    return _default_store
