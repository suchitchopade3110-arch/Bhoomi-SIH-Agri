"""ORM model for the User aggregate (farmer / officer / agronomist)."""

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class User(Base):
    """A farmer, officer, or agronomist account (contract §2.3, PRD §3).

    Farmer accounts key on ``phone_number``; officer/agronomist accounts key
    on ``email``. Both columns are nullable + independently unique so either
    identifier can be absent depending on role — simpler than two subtype
    tables for a hackathon-scale user base.
    """

    __tablename__ = "users"

    phone_number: Mapped[str | None] = mapped_column(String(20), unique=True, nullable=True, index=True)
    email: Mapped[str | None] = mapped_column(String(255), unique=True, nullable=True, index=True)
    full_name: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    preferred_language: Mapped[str] = mapped_column(String(10), nullable=False, default="ta")
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    # Officer/agronomist jurisdiction, e.g. "taluk_erode" / "kvk_erode" — used
    # for HITL queue routing (contract §2.7, §2.13). Unused for farmers.
    jurisdiction: Mapped[str | None] = mapped_column(String(100), nullable=True)
