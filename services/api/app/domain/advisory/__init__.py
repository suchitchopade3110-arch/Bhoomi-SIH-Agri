"""Advisory domain module."""

from app.domain.advisory.derive import (
    AdvisoryTrend,
    QualitativeAdvisoryResult,
    derive_qualitative_advisory,
)

__all__ = [
    "AdvisoryTrend",
    "QualitativeAdvisoryResult",
    "derive_qualitative_advisory",
]
