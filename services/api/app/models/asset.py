"""ORM model for the Asset aggregate — presigned-upload media (contract §2.4, PRD §1.4)."""

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Asset(Base):
    """Metadata for one client-uploaded blob (photo/audio), referenced by
    ``asset_id`` everywhere else — the bytes themselves never touch the API
    (contract §2.4)."""

    __tablename__ = "assets"

    asset_kind: Mapped[str] = mapped_column(String(30), nullable=False)
    file_name: Mapped[str] = mapped_column(String(500), nullable=False)
    content_type: Mapped[str] = mapped_column(String(100), nullable=False)
    farm_id: Mapped[str | None] = mapped_column(String(36), nullable=True, index=True)
    storage_key: Mapped[str] = mapped_column(String(500), nullable=False)
