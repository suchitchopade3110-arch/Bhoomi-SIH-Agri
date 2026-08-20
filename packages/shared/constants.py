"""Constants and thresholds for Bhoomi system."""

# Confidence gate threshold below which model escalates to human expert
CONFIDENCE_GATE_THRESHOLD: float = 0.70

# RAG cosine similarity relevance cutoff (TODO-tune: calibrate on gold-standard Q&A dataset)
RAG_RELEVANCE_THRESHOLD: float = 0.35

# Health score model version
DEFAULT_WEIGHTS_VERSION: str = "v1.0.0"

# Six Sub-Index default weights (must sum to 1.0)
SUBINDEX_WEIGHTS: dict[str, float] = {
    "soil_water": 0.20,
    "crop_vigor": 0.20,
    "weather_risk": 0.15,
    "pest_disease": 0.20,
    "nutrient_balance": 0.15,
    "intervention_history": 0.10,
}

# Health score bands definition [min_score, max_score]
HEALTH_BAND_THRESHOLDS: dict[str, tuple[float, float]] = {
    "optimal": (80.0, 100.0),
    "good": (65.0, 79.99),
    "moderate": (50.0, 64.99),
    "at_risk": (35.0, 49.99),
    "critical": (0.0, 34.99),
}
