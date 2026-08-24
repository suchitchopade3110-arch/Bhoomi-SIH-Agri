"""Static pathogen risk threshold table (spec §3.4) — in-memory stub seeded
with ICAR PoP values for the one pathogen backed by ingested corpus content:
``services/api/corpus/rice_blb.md`` (doc_id ``rice_blb`` — the spec's
original ``rice_bacterial_leaf_blight.md`` reference is a Phase 3 build-order
correction; that filename doesn't exist in the corpus).

Note on the temp/duration band: the corpus prose itself only states "high
humidity (above 70%)" — it doesn't give an exact temperature range or a
sustained-hours figure. ``RH >= 80%, 25-32C, sustained >=48h`` are the
Phase-3-directed values (tighter than the corpus's bare "above 70%"), kept
as specified pending Tharun's full pathogen risk matrix — this table
remains an explicitly flagged stub, not a literal transcription of the
corpus prose.

Every other entry is an illustrative placeholder using the same shape, not
sourced from any corpus document — flagged individually below. Replace
wholesale once Tharun's full pathogen risk threshold matrix lands; nothing
outside this module needs to change (``evaluate_alert`` only consumes
``PathogenRiskThreshold`` values, never this table directly).
"""

from app.domain.alerts.models import PathogenRiskThreshold

_SAMBA_PADDY_SUSCEPTIBLE_STAGES = ("vegetative", "tillering", "panicle_initiation", "flowering")

PATHOGEN_RISK_THRESHOLDS: dict[str, PathogenRiskThreshold] = {
    # ICAR PoP-sourced: services/api/corpus/rice_blb.md (doc_id "rice_blb").
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
        # Sourced from rice_blb.md's "Key diagnostic indicators" and
        # "Severity Staging" sections — real inspection checklist items,
        # not fabricated.
        inspection_tasks=(
            "Check leaf margins and tips for water-soaked, translucent streaks along the veins",
            "Look for yellow to straw-coloured leaf tips, drying in a 'V' pattern from the tip downward",
            "Cut a fresh lesion in early morning and check for milky/yellowish bacterial ooze",
            "Estimate the % of leaves/canopy showing lesions to gauge severity (early <20%, moderate 20-50%, severe >50%)",
        ),
    ),
    # Illustrative placeholders pending Tharun's matrix — same shape, not
    # sourced from any corpus document. inspection_tasks here are generic
    # placeholders, flagged the same way.
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
        inspection_tasks=(
            "Check young leaves for upward curling and puckering",
            "Look for whitefly presence on the underside of leaves",
        ),
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
        inspection_tasks=(
            "Check upper leaf surfaces for white, powdery fungal patches",
            "Check for stunted or distorted new growth",
        ),
    ),
}


def get_threshold(pathogen_id: str) -> PathogenRiskThreshold | None:
    return PATHOGEN_RISK_THRESHOLDS.get(pathogen_id)
