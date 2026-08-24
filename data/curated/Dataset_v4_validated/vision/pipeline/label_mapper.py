"""
Canonical Label Mapping Engine for BHOOMI Vision Pipeline
Maps external dataset labels to 16 canonical BHOOMI classes:
PEST_001..008, DISEASE_001..008
Assigns deterministic confidence: EXACT, HIGH, REVIEW_REQUIRED, REJECTED
"""
import re
from typing import Optional, Tuple

CANONICAL_ENTITIES = {
    "PEST_001": {"name": "Stem Borer", "scientific": "Scirpophaga incertulas", "type": "pest"},
    "PEST_002": {"name": "Brown Planthopper", "scientific": "Nilaparvata lugens", "type": "pest"},
    "PEST_003": {"name": "Leaf Folder", "scientific": "Cnaphalocrocis medinalis", "type": "pest"},
    "PEST_004": {"name": "Green Leafhopper", "scientific": "Nephotettix virescens", "type": "pest"},
    "PEST_005": {"name": "Gall Midge", "scientific": "Orseolia oryzae", "type": "pest"},
    "PEST_006": {"name": "Thrips", "scientific": "Stenchaetothrips biformis", "type": "pest"},
    "PEST_007": {"name": "Whorl Maggot", "scientific": "Hydrellia philippina", "type": "pest"},
    "PEST_008": {"name": "Earhead Bug", "scientific": "Leptocorisa acuta", "type": "pest"},
    "DISEASE_001": {"name": "Bacterial Leaf Blight", "scientific": "Xanthomonas oryzae pv. oryzae", "type": "disease"},
    "DISEASE_002": {"name": "Bacterial Leaf Streak", "scientific": "Xanthomonas oryzae pv. oryzicola", "type": "disease"},
    "DISEASE_003": {"name": "Rice Blast", "scientific": "Magnaporthe oryzae", "type": "disease"},
    "DISEASE_004": {"name": "Brown Spot", "scientific": "Bipolaris oryzae", "type": "disease"},
    "DISEASE_005": {"name": "False Smut", "scientific": "Ustilaginoidea virens", "type": "disease"},
    "DISEASE_006": {"name": "Sheath Blight", "scientific": "Rhizoctonia solani", "type": "disease"},
    "DISEASE_007": {"name": "Sheath Rot", "scientific": "Sarocladium oryzae", "type": "disease"},
    "DISEASE_008": {"name": "Tungro Virus", "scientific": "Rice tungro bacilliform virus", "type": "disease"}
}

# Rule-based taxonomy patterns
LABEL_RULES = [
    # Diseases
    (r"\b(bacterial[_\s-]*leaf[_\s-]*blight|blb|bacterial[_\s-]*blight)\b", "DISEASE_001", "EXACT", "Exact clinical match to Bacterial Leaf Blight"),
    (r"\b(bacterial[_\s-]*leaf[_\s-]*streak|bls)\b", "DISEASE_002", "EXACT", "Exact clinical match to Bacterial Leaf Streak"),
    (r"\b(rice[_\s-]*blast|leaf[_\s-]*blast|neck[_\s-]*blast|blast)\b", "DISEASE_003", "EXACT", "Exact pathology match to Rice Blast"),
    (r"\b(brown[_\s-]*spot|helminthosporium)\b", "DISEASE_004", "EXACT", "Exact pathology match to Brown Spot"),
    (r"\b(false[_\s-]*smut|green[_\s-]*smut|leaf[_\s-]*smut)\b", "DISEASE_005", "HIGH", "Pathology match to False/Leaf Smut"),
    (r"\b(sheath[_\s-]*blight)\b", "DISEASE_006", "EXACT", "Exact clinical match to Sheath Blight"),
    (r"\b(sheath[_\s-]*rot)\b", "DISEASE_007", "EXACT", "Exact clinical match to Sheath Rot"),
    (r"\b(tungro|rice[_\s-]*tungro|tungro[_\s-]*virus)\b", "DISEASE_008", "EXACT", "Exact virology match to Rice Tungro Virus"),

    # Pests
    (r"\b(stem[_\s-]*borer|yellow[_\s-]*stem[_\s-]*borer|dead[_\s-]*heart|white[_\s-]*ear)\b", "PEST_001", "EXACT", "Exact entomology/symptom match to Stem Borer"),
    (r"\b(brown[_\s-]*planthopper|bph|hopper[_\s-]*burn)\b", "PEST_002", "EXACT", "Exact entomology/damage match to Brown Planthopper"),
    (r"\b(leaf[_\s-]*folder|leaffolder|folded[_\s-]*leaf)\b", "PEST_003", "EXACT", "Exact entomology match to Rice Leaf Folder"),
    (r"\b(green[_\s-]*leafhopper|glh)\b", "PEST_004", "EXACT", "Exact entomology match to Green Leafhopper"),
    (r"\b(gall[_\s-]*midge|silver[_\s-]*shoot|onion[_\s-]*leaf)\b", "PEST_005", "EXACT", "Exact entomology/gall match to Gall Midge"),
    (r"\b(thrips|rice[_\s-]*thrips)\b", "PEST_006", "EXACT", "Exact entomology match to Rice Thrips"),
    (r"\b(whorl[_\s-]*maggot)\b", "PEST_007", "EXACT", "Exact entomology match to Whorl Maggot"),
    (r"\b(earhead[_\s-]*bug|ear[_\s-]*head[_\s-]*bug|gundhi[_\s-]*bug|rice[_\s-]*bug)\b", "PEST_008", "EXACT", "Exact entomology match to Earhead Bug")
]

# Non-target / Out of Domain patterns
REJECTED_PATTERNS = [
    r"\b(apple|tomato|potato|corn|grape|pepper|peach|cherry|strawberry|soybean|squash|citrus|orange)\b",
    r"\b(healthy|normal|background|weed|unidentified)\b"
]


def map_source_label(source_label: str) -> Tuple[Optional[str], Optional[str], str, str]:
    """
    Maps an arbitrary raw source label string to a canonical BHOOMI entity.
    Returns: (canonical_id, canonical_name, mapping_confidence, mapping_basis)
    """
    norm = re.sub(r"[_\-\.]+", " ", source_label.lower()).strip()

    # Check explicit out of domain / non-target
    for pat in REJECTED_PATTERNS:
        if re.search(pat, norm):
            return None, None, "REJECTED", f"Out of domain or non-target category matched: '{source_label}'"

    # Match canonical rules
    for pat, cid, conf, basis in LABEL_RULES:
        if re.search(pat, norm):
            cname = CANONICAL_ENTITIES[cid]["name"]
            return cid, cname, conf, basis

    return None, None, "REVIEW_REQUIRED", f"Ambiguous or unrecognized label string: '{source_label}'"
