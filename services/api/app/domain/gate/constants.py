"""Named constants for the confidence gate (PRD §5.6, §5.7, SIH26131 §2).

Thresholds themselves are named in ``app.domain.constants`` (``CONFIDENCE_GATE``,
``RAG_RELEVANCE_THRESHOLD_PRODUCTION``) and injected into ``decide()`` / ``check_gate()``.
This module defines the scope vocabularies (``SUPPORTED_LABELS``), escalation reason codes,
and their mapping onto the contract's machine error codes.
"""

SUPPORTED_LABELS: dict[str, frozenset[str]] = {
    "disease": frozenset(
        {
            "bacterial_leaf_blight",
            "blast",
            "brown_spot",
            "sheath_blight",
            "early_blight",
            "late_blight",
            "leaf_curl_virus",
            "powdery_mildew",
        }
    ),
    "pest": frozenset(
        {
            "stem_borer",
            "brown_planthopper",
            "gall_midge",
            "leaf_folder",
            "green_leafhopper",
            "fall_armyworm",
            "whitefly",
            "aphid",
        }
    ),
}

# Domain-level escalation reasons.
GATE_REASON_BELOW_IMAGE_CONFIDENCE = "below_image_confidence_gate"
GATE_REASON_OUT_OF_SCOPE = "OUT_OF_SCOPE_TARGET"
GATE_REASON_BELOW_RETRIEVAL_RELEVANCE = "no_relevant_source"

# Maps each domain reason onto the contract's machine error code
GATE_REASON_TO_ERROR_CODE: dict[str, str] = {
    GATE_REASON_BELOW_IMAGE_CONFIDENCE: "BELOW_CONFIDENCE_GATE",
    GATE_REASON_OUT_OF_SCOPE: "OUT_OF_SCOPE_TARGET",
    "out_of_scope": "OUT_OF_SCOPE_TARGET",
    GATE_REASON_BELOW_RETRIEVAL_RELEVANCE: "NO_RELEVANT_SOURCE",
}
