"""OTP delivery port — typed Protocol for sending a one-time passcode to a phone."""

from typing import Protocol


class OtpDeliveryPort(Protocol):
    """Port for delivering a one-time passcode over SMS (PRD §2.3 farmer login)."""

    async def send_otp(self, phone_number: str, otp: str) -> None:
        """Deliver ``otp`` to ``phone_number``. Never raises for a
        deliverable-but-unconfirmed send — SMS delivery is fire-and-forget
        by nature; the farmer proves receipt by typing the code back."""
        ...


__all__ = ["OtpDeliveryPort"]
