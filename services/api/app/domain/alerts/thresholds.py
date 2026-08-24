"""Static pathogen risk threshold table (spec §3.4) — in-memory stub seeded
with ICAR PoP values for the one pathogen backed by ingested corpus content
(``rice_bacterial_leaf_blight.md``, doc_id ``rice_bacterial_leaf_blight``).

Every other entry is an illustrative placeholder using the same shape, not
sourced from a package-of-practices document — flagged individually below.
Replace wholesale once Tharun's full pathogen risk threshold matrix lands;
nothing outside this module needs to change (``evaluate_alert`` only
consumes ``PathogenRiskThreshold`` values, never this table directly).
"""

from app.domain.alerts.models import PathogenRiskThreshold

_SAMBA_PADDY_SUSCEPTIBLE_STAGES = ("vegetative", "tillering", "panicle_initiation", "flowering")

PATHOGEN_RISK_THRESHOLDS: dict[str, PathogenRiskThreshold] = {
    # ICAR PoP-sourced (rice_bacterial_leaf_blight.md, spec §2.1 example).
    "bacterial_leaf_blight": PathogenRiskThreshold(
        pathogen_id="bacterial_leaf_blight",
        pathogen_name="Bacterial Leaf Blight",
        target_crop="samba_paddy",
        susceptible_stages=_SAMBA_PADDY_SUSCEPTIBLE_STAGES,
        temp_min_c=25.0,
        temp_max_c=32.0,
        humidity_min_pct=80.0,
        sustained_hours=48,
        cluster_radius_km=10.0,
        cluster_count_threshold=3,
        preventative_action="Apply prophylactic Pseudomonas fluorescens; avoid field movement while wet.",
    ),
    # Illustrative placeholders pending Tharun's matrix — same shape, not
    # ICAR-sourced band values.
    "leaf_curl_virus": PathogenRiskThreshold(
        pathogen_id="leaf_curl_virus",
        pathogen_name="Leaf Curl Virus",
        target_crop="samba_paddy",
        susceptible_stages=_SAMBA_PADDY_SUSCEPTIBLE_STAGES,
        temp_min_c=28.0,
        temp_max_c=38.0,
        humidity_min_pct=60.0,
        sustained_hours=48,
        cluster_radius_km=10.0,
        cluster_count_threshold=3,
        preventative_action="Control whitefly vector population; rogue out visibly infected plants promptly.",
    ),
    "powdery_mildew": PathogenRiskThreshold(
        pathogen_id="powdery_mildew",
        pathogen_name="Powdery Mildew",
        target_crop="samba_paddy",
        susceptible_stages=_SAMBA_PADDY_SUSCEPTIBLE_STAGES,
        temp_min_c=20.0,
        temp_max_c=28.0,
        humidity_min_pct=70.0,
        sustained_hours=48,
        cluster_radius_km=10.0,
        cluster_count_threshold=3,
        preventative_action="Improve field air circulation; apply sulfur-based fungicide preventatively.",
    ),
}


def get_threshold(pathogen_id: str) -> PathogenRiskThreshold | None:
    return PATHOGEN_RISK_THRESHOLDS.get(pathogen_id)
