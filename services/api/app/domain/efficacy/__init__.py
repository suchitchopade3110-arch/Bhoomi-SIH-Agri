"""Treatment Efficacy Tracking domain package (SPEC-EFFICACY-001).

The pure scoring engine (``score.py``), the write-side lifecycle
(``services/efficacy/tracking_service.py``, hooked into diagnosis /
follow-up / agronomist-resolve), the read-side aggregator
(``services/efficacy/aggregator_service.py``), and the route
(``GET /api/v1/treatments/{treatment_id}/efficacy``, ``sih26131``-only) are
all built. ``default_treatments.py`` is the controlled vocabulary spec §3.1
asks for, scoped to the 3 diseases the ingested corpus actually documents a
first-line treatment for (see that module's docstring).
"""

from app.domain.efficacy.default_treatments import get_default_treatment
from app.domain.efficacy.models import EfficacyResult, TreatmentApplicationSnapshot, normalize_treatment_key
from app.domain.efficacy.score import compute_efficacy

__all__ = [
    "compute_efficacy",
    "get_default_treatment",
    "EfficacyResult",
    "TreatmentApplicationSnapshot",
    "normalize_treatment_key",
]
