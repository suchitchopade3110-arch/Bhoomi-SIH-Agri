"""ORM model for the KVK Agronomist directory — case routing (PRD §5.11)."""

from sqlalchemy import Boolean, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Agronomist(Base):
    """One agronomist a case can be routed to.

    A small, real directory table — real enough for ``AgronomistRepository``
    to do a genuine nearest-district / any-available query — even though
    the default routing mode (``AGRONOMIST_ROUTING_MODE=demo_fixed``) hard-
    assigns a single named row rather than exercising that query. See
    ``services/escalation/routing.py``.
    """

    __tablename__ = "agronomists"

    name: Mapped[str] = mapped_column(String(120), nullable=False, unique=True, index=True)
    kvk_center: Mapped[str] = mapped_column(String(120), nullable=False)
    district: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    is_available: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
