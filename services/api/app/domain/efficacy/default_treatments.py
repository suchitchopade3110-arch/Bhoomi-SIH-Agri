"""Bounded label -> default first-line treatment mapping (SPEC-EFFICACY-001 §3.1).

The spec requires ``treatment_name`` to come from a controlled vocabulary
("validated against canonical active ingredients in the ICAR Package of
Practices catalog"), not free text parsed out of a generated advisory. This
table *is* that catalog, for exactly the diseases the ingested corpus
(``services/api/corpus/``) actually documents a first-line treatment for —
each entry is the first recommended treatment line in that disease's
corpus doc. Diseases without a corpus doc already escalate at the gate
before diagnosis composes an advisory, so they never reach the caller of
this lookup — this table is deliberately not padded out with placeholders
for labels ``SUPPORTED_LABELS`` accepts but the corpus doesn't back yet.
"""

from app.domain.efficacy.models import normalize_treatment_key

# label -> (treatment_name, treatment_category), sourced from each label's
# corpus doc's first recommended chemical control line.
_DEFAULT_TREATMENT_BY_LABEL: dict[str, tuple[str, str]] = {
    "bacterial_leaf_blight": ("Copper Hydroxide 77% WP", "chemical"),
    "blast": ("Tricyclazole 75% WP", "chemical"),
    "brown_spot": ("Mancozeb 75% WP", "chemical"),
}


def get_default_treatment(label: str) -> tuple[str, str] | None:
    """``(normalized_treatment_name, treatment_category)`` for a diagnosed
    label, or ``None`` when the corpus has no first-line treatment recorded
    for it yet — callers must skip opening a TreatmentApplication in that
    case rather than guessing."""
    entry = _DEFAULT_TREATMENT_BY_LABEL.get(label)
    if entry is None:
        return None
    raw_name, category = entry
    return normalize_treatment_key(raw_name), category
