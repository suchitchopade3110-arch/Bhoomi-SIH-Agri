"""Treatment Efficacy Tracking domain package (SPEC-EFFICACY-001, Phase 4).

Only the pure scoring engine is built this phase — see
``app/domain/efficacy/score.py``'s module docstring for why the schema,
service, and route are deliberately not (they need cross-owner
coordination this phase file itself says not to do solo).
"""

from app.domain.efficacy.models import EfficacyResult, TreatmentApplicationSnapshot, normalize_treatment_key
from app.domain.efficacy.score import compute_efficacy

__all__ = [
    "compute_efficacy",
    "EfficacyResult",
    "TreatmentApplicationSnapshot",
    "normalize_treatment_key",
]
