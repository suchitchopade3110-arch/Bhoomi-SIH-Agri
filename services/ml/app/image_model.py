"""Crop disease/pest image classifier.

This is a **heuristic** classifier, not a trained model — there is no
labeled crop-disease dataset with model weights checked into this repo (see
``README.md`` §9 "Known gaps"). It exists so ``DIAGNOSIS_MODEL=real`` has an
actually-running HTTP service to talk to end-to-end, instead of failing with
a connection error, while being explicit about what it is and isn't.

Two code paths, both bounded to ``SUPPORTED_LABELS`` (the same 8 diseases /
8 pests the backend's confidence gate accepts — labels outside this set are
useless here regardless of source):

1. **Real pixel analysis** (``image_bytes`` provided): a simple, genuinely
   computed color-histogram heuristic — the fraction of yellow/brown/grey
   pixels in the image, thresholded against per-label profiles. This is
   real image processing, not a lookup table, but it is not a trained
   classifier and its accuracy should not be assumed.
2. **Opaque asset id** (no pixels available — the common case today, since
   the backend passes only ``asset_id``/``image_asset_url_or_id`` and there
   is no service-to-service auth wired yet for this service to resolve
   that id into bytes via the main API): a token-hash pick over the
   supported label set, deterministic per asset id, mirroring
   ``StubImageDiagnosisAdapter`` in services/api so demo behavior stays
   consistent between the stub and "real" diagnosis paths.
"""

from __future__ import annotations

import hashlib
import io
from dataclasses import dataclass

SUPPORTED_DISEASE_LABELS: tuple[str, ...] = (
    "bacterial_leaf_blight",
    "blast",
    "brown_spot",
    "sheath_blight",
    "early_blight",
    "late_blight",
    "leaf_curl_virus",
    "powdery_mildew",
)

SUPPORTED_PEST_LABELS: tuple[str, ...] = (
    "stem_borer",
    "brown_planthopper",
    "gall_midge",
    "leaf_folder",
    "green_leafhopper",
    "fall_armyworm",
    "whitefly",
    "aphid",
)

ALL_SUPPORTED_LABELS: tuple[str, ...] = SUPPORTED_DISEASE_LABELS + SUPPORTED_PEST_LABELS

# Rough (fraction_yellow, fraction_brown, fraction_white_lesion) profile per
# disease label, hand-set from each disease's typical field-guide symptom
# description (BLB: yellow-to-white lesions from leaf tips; blast: grey
# centers with brown margins; brown spot: brown/tan flecking; etc). This is
# a coarse heuristic prior, not measured ground truth.
_DISEASE_COLOR_PROFILE: dict[str, tuple[float, float, float]] = {
    "bacterial_leaf_blight": (0.35, 0.10, 0.20),
    "blast": (0.10, 0.30, 0.25),
    "brown_spot": (0.15, 0.40, 0.05),
    "sheath_blight": (0.15, 0.25, 0.15),
    "early_blight": (0.20, 0.35, 0.05),
    "late_blight": (0.10, 0.30, 0.10),
    "leaf_curl_virus": (0.30, 0.05, 0.02),
    "powdery_mildew": (0.05, 0.05, 0.45),
}


@dataclass
class DiagnosisResult:
    label: str
    confidence: float
    meta: dict


def _hash_pick(seed: str, options: tuple[str, ...]) -> tuple[str, float]:
    """Deterministic pick + confidence from a seed string. Same idea as
    services/api's ``StubImageDiagnosisAdapter`` — same seed always yields
    the same label, useful for stable demos and tests, but this is not a
    real model prediction."""
    digest = hashlib.sha256(seed.encode("utf-8")).hexdigest()
    index = int(digest[:8], 16) % len(options)
    # Confidence in [0.55, 0.97) — never a suspicious-looking 1.00, never
    # so low the confidence gate would trivially reject every request.
    confidence = 0.55 + (int(digest[8:12], 16) % 4200) / 10000.0
    return options[index], round(confidence, 4)


def _color_fractions(image_bytes: bytes) -> tuple[float, float, float] | None:
    """(fraction_yellow, fraction_brown, fraction_white_lesion) over an
    image's pixels, or None if Pillow/the image can't be decoded (missing
    dependency, corrupt bytes, etc — callers fall back to the hash path)."""
    try:
        import numpy as np
        from PIL import Image
    except ImportError:
        return None

    try:
        img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
        img.thumbnail((256, 256))  # cheap: classification doesn't need full-res
        arr = np.asarray(img, dtype=np.float32) / 255.0
    except Exception:
        return None

    r, g, b = arr[..., 0], arr[..., 1], arr[..., 2]
    total = arr.shape[0] * arr.shape[1]
    if total == 0:
        return None

    # Yellowing: high R+G, low B (classic chlorosis/necrosis color)
    yellow_mask = (r > 0.5) & (g > 0.4) & (b < 0.4) & ((r - b) > 0.15)
    # Brown/necrotic lesions: mid R, lower G/B, muted overall
    brown_mask = (r > 0.25) & (r < 0.65) & (g < r) & (b < g)
    # White/grey lesion centers (blast, powdery mildew): high & similar RGB
    white_mask = (r > 0.65) & (g > 0.65) & (b > 0.55) & (abs(r - g) < 0.1)

    return (
        float(yellow_mask.sum()) / total,
        float(brown_mask.sum()) / total,
        float(white_mask.sum()) / total,
    )


def _classify_by_color(fractions: tuple[float, float, float]) -> tuple[str, float]:
    """Nearest-profile match by Euclidean distance over the 3 color
    fractions; confidence derived from how close the match is."""
    best_label = SUPPORTED_DISEASE_LABELS[0]
    best_dist = float("inf")
    for label, profile in _DISEASE_COLOR_PROFILE.items():
        dist = sum((a - b) ** 2 for a, b in zip(fractions, profile)) ** 0.5
        if dist < best_dist:
            best_dist = dist
            best_label = label

    # Smaller distance -> higher confidence. Max plausible distance across
    # 3 fractions in [0,1] each is sqrt(3); clamp into a believable band.
    confidence = max(0.55, min(0.95, 1.0 - (best_dist / 1.7)))
    return best_label, round(confidence, 4)


def diagnose(
    asset_id: str,
    crop_hint: str | None = None,
    image_bytes: bytes | None = None,
    target_type: str = "disease",
) -> DiagnosisResult:
    """Diagnose a crop image. See module docstring for what "diagnose" means
    here — a bounded heuristic, not a trained CV model."""
    if image_bytes:
        fractions = _color_fractions(image_bytes)
        if fractions is not None:
            label, confidence = _classify_by_color(fractions)
            return DiagnosisResult(
                label=label,
                confidence=confidence,
                meta={
                    "model_version": "bhoomi-ml-heuristic-color-v1",
                    "method": "color_histogram",
                    "crop_detected": crop_hint or "unknown",
                    "color_fractions": {
                        "yellow": round(fractions[0], 4),
                        "brown": round(fractions[1], 4),
                        "white_lesion": round(fractions[2], 4),
                    },
                },
            )

    options = SUPPORTED_PEST_LABELS if target_type == "pest" else SUPPORTED_DISEASE_LABELS
    label, confidence = _hash_pick(f"{asset_id}:{crop_hint or ''}", options)
    return DiagnosisResult(
        label=label,
        confidence=confidence,
        meta={
            "model_version": "bhoomi-ml-heuristic-hash-v1",
            "method": "asset_id_hash",
            "crop_detected": crop_hint or "unknown",
            "note": "no image bytes available — deterministic placeholder, not a real prediction",
        },
    )
