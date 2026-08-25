"""Orchestration for the confidence gate: runs the image model,
then hands its confidence — plus scope and retrieval-relevance signals — to
the pure ``domain.gate.decide``. No decision logic lives here, only wiring.
"""

from typing import Annotated

from fastapi import Depends

from app.adapters.dependencies import get_image_diagnosis_adapter
from app.ports.image_diagnosis import ImageDiagnosisPort
from app.core.config import Settings, get_settings
from app.domain.gate import GateDecision, SUPPORTED_LABELS, check_gate, decide

# Bounded crop/disease set this version supports (PRD §5.6: "3-5 well-
# supported crops/diseases with a confidence gate"). A label outside this
# set is out-of-scope and always escalates, regardless of confidence.
SUPPORTED_DIAGNOSIS_LABELS: frozenset[str] = frozenset(
    {
        # Canonical 16 BHOOMI Classes (IDs)
        "PEST_001", "PEST_002", "PEST_003", "PEST_004",
        "PEST_005", "PEST_006", "PEST_007", "PEST_008",
        "DISEASE_001", "DISEASE_002", "DISEASE_003", "DISEASE_004",
        "DISEASE_005", "DISEASE_006", "DISEASE_007", "DISEASE_008",
        # Canonical 16 BHOOMI Classes (Label Names)
        "stem_borer", "brown_planthopper", "leaf_folder", "green_leafhopper",
        "gall_midge", "thrips", "whorl_maggot", "earhead_bug",
        "bacterial_leaf_blight", "bacterial_leaf_streak", "rice_blast", "brown_spot",
        "false_smut", "sheath_blight", "sheath_rot", "tungro",
        # Legacy/prototype strings
        "early_blight", "late_blight", "leaf_curl_virus", "powdery_mildew", "blast",
    }
)


class GateService:
    """Runs the image model, then the confidence gate, for one diagnosis attempt."""

    def __init__(self, image_port: ImageDiagnosisPort, settings: Settings) -> None:
        self._image_port = image_port
        self._settings = settings

    async def evaluate_image_diagnosis(
        self,
        image_asset_url_or_id: str,
        crop_hint: str | None = None,
        retrieval_relevance: float | None = None,
        target_type: str = "disease",
    ) -> tuple[GateDecision, str, float]:
        """Run ``ImageDiagnosisPort`` then the gate.

        Args:
            image_asset_url_or_id: The uploaded image's asset reference.
            crop_hint: Optional farmer-stated crop to constrain the model.
            retrieval_relevance: Optional cosine-similarity score from RAG retrieval.
            target_type: "disease" or "pest".

        Returns:
            ``(decision, label, confidence)`` — the label/confidence are
            surfaced alongside the decision so a caller can still show what
            the model guessed even when the gate escalates.
        """
        label, confidence, _meta = await self._image_port.diagnose_crop_image(
            image_asset_url_or_id, crop_hint=crop_hint
        )
        norm_target_type = "pest" if target_type == "pest" else "disease"
        decision = check_gate(
            target_type=norm_target_type,
            label=label,
            confidence=confidence,
            retrieval_relevance=retrieval_relevance,
            confidence_gate=self._settings.CONFIDENCE_GATE,
            relevance_threshold=self._settings.RAG_RELEVANCE_THRESHOLD,
        )
        return decision, label, confidence


def get_gate_service(
    image_port: Annotated[ImageDiagnosisPort, Depends(get_image_diagnosis_adapter)],
    settings: Annotated[Settings, Depends(get_settings)],
) -> GateService:
    """FastAPI dependency provider assembling ``GateService`` from its port + config."""
    return GateService(image_port, settings)
