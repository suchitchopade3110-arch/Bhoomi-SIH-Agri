"""Static interim guidance cards for crop stress containment (PRD §5.8, Phase 4).

Authored containment cards keyed by crop and problem label/type.
Provides immediate, actionable containment advice while awaiting expert review or diagnosis confirmation.
"""

from typing import Any
from pydantic import BaseModel, Field
from app.domain.gate.constants import SUPPORTED_LABELS


class GuidanceCard(BaseModel):
    """Interim containment guidance card for a specific crop and problem."""

    crop: str = Field(..., description="Target crop variety or category")
    problem_type: str = Field(default="general", description="Category: disease | pest | general")
    problem_label: str | None = Field(default=None, description="Standard problem identifier if specific")
    title: str = Field(..., description="Card headline")
    containment_advice: str = Field(..., description="Primary interim containment instruction")
    what_to_avoid: str = Field(..., description="Actions that could exacerbate the condition")
    immediate_actions: list[str] = Field(default_factory=list, description="Immediate 1-2 day field steps")
    expert_trigger: str = Field(..., description="When to request immediate agronomist escalation")

    model_config = {"frozen": True}


# Authored interim guidance entries for diseases
_DISEASE_GUIDANCE: dict[str, dict[str, Any]] = {
    "bacterial_leaf_blight": {
        "title": "Bacterial Leaf Blight (BLB) Containment",
        "containment_advice": "Drain standing water immediately and reduce nitrogen application until fresh tillers show no lesions.",
        "what_to_avoid": "Do not apply excess urea/nitrogen fertilizer. Do not irrigate from infected fields to healthy plots.",
        "immediate_actions": [
            "Drain excess water from field for 3-4 days.",
            "Avoid top-dressing nitrogenous fertilizers during active lesion expansion.",
            "Spray Copper Hydroxide (2.0 g/L) or Copper Oxychloride (2.5 g/L) at early symptom onset.",
        ],
        "expert_trigger": "If water-soaked lesions spread across more than 25% of canopy within 48 hours.",
    },
    "blast": {
        "title": "Rice Blast (Pyricularia oryzae) Interim Protocol",
        "containment_advice": "Maintain continuous shallow standing water (2-3 cm) to buffer microclimate; withhold nitrogen top-dressing.",
        "what_to_avoid": "Do not let the field dry out during blast flare-ups. Avoid dense planting canopy.",
        "immediate_actions": [
            "Apply Tricyclazole 75% WP @ 0.6 g/L or Isoprothiolane 40% EC @ 1.5 ml/L.",
            "Suspend urea application until new leaf emergence is lesion-free.",
            "Scout nursery and border rows early morning for spindle-shaped lesions.",
        ],
        "expert_trigger": "If neck blast lesions appear at panicle emergence or collar rot exceeds 10%.",
    },
    "brown_spot": {
        "title": "Brown Spot (Bipolaris oryzae) Management",
        "containment_advice": "Check soil nutrient balance; brown spot often signals potassium or silicon deficiency in light soils.",
        "what_to_avoid": "Do not water-stress the crop during tillering and flowering stages.",
        "immediate_actions": [
            "Apply muriate of potash (MOP) as recommended for balanced nutrition.",
            "Spray Mancozeb 75% WP @ 2.0 g/L or Propiconazole 25% EC @ 1.0 ml/L if lesions coalesce.",
            "Ensure field is not allowed to develop deep cracking drought stress.",
        ],
        "expert_trigger": "If oval spots with yellow haloes cover more than a third of flag leaves.",
    },
    "sheath_blight": {
        "title": "Sheath Blight (Rhizoctonia solani) Containment",
        "containment_advice": "Reduce field canopy density and avoid stagnant water to lower microclimatic humidity below 85%.",
        "what_to_avoid": "Do not apply nitrogen in excess. Do not retain deep stagnant water.",
        "immediate_actions": [
            "Drain field to lower relative humidity in the lower canopy.",
            "Apply Hexaconazole 5% SC @ 2.0 ml/L or Validamycin 3% L @ 2.5 ml/L targeted at the base.",
            "Remove weed hosts from field bunds.",
        ],
        "expert_trigger": "If snake-skin lesions reach the top leaf sheath or flag leaf collar.",
    },
    "early_blight": {
        "title": "Early Blight (Alternaria solani) Interim Protocol",
        "containment_advice": "Remove lower infected foliage and avoid overhead wetting of crop leaves.",
        "what_to_avoid": "Avoid overhead sprinkler irrigation that keeps leaves wet overnight.",
        "immediate_actions": [
            "Prune infected bottom leaves and dispose away from the field.",
            "Spray Chlorothalonil 75% WP @ 2.0 g/L or Mancozeb @ 2.5 g/L.",
            "Apply mulch to prevent soil-splashing onto lower leaves.",
        ],
        "expert_trigger": "If concentric ring lesions appear on stems or spread upwards past mid-canopy.",
    },
    "late_blight": {
        "title": "Late Blight (Phytophthora infestans) Emergency Containment",
        "containment_advice": "Immediate protective fungicide application required; destroy severely infected plant clusters.",
        "what_to_avoid": "Do not delay spraying in cool, foggy or humid weather. Do not compost infected debris.",
        "immediate_actions": [
            "Apply Metalaxyl + Mancozeb @ 2.5 g/L immediately upon detection.",
            "Ensure complete coverage of both upper and lower leaf surfaces.",
            "Cease overhead irrigation completely.",
        ],
        "expert_trigger": "If water-soaked dark lesions with white mold margins expand rapidly in cool humid weather.",
    },
    "leaf_curl_virus": {
        "title": "Leaf Curl Virus Vector Management",
        "containment_advice": "Viral disease cannot be cured chemically; manage whitefly vectors and rogue out severely stunted plants.",
        "what_to_avoid": "Do not apply excessive insecticides that kill natural predators of whiteflies.",
        "immediate_actions": [
            "Install yellow sticky traps (15-20 traps/acre) at canopy height.",
            "Spray Neem oil 1500 ppm @ 3 ml/L or Diafenthiuron 50% WP @ 1.2 g/L for vector suppression.",
            "Uproot and bury early-infected stunted plants.",
        ],
        "expert_trigger": "If vector population exceeds 5 whiteflies per leaf across the plot.",
    },
    "powdery_mildew": {
        "title": "Powdery Mildew Containment Card",
        "containment_advice": "Improve air circulation and apply wettable sulfur or systemic fungicides at first sign of white powder.",
        "what_to_avoid": "Avoid excessive shade and crowded planting.",
        "immediate_actions": [
            "Spray Wettable Sulfur 80% WP @ 2.5 g/L or Dinocap @ 1.0 ml/L in the early morning.",
            "Prune dense overlapping branches to improve sunlight penetration.",
        ],
        "expert_trigger": "If white powdery patches cover more than 30% of foliage.",
    },
}

# Authored interim guidance entries for insect pests
_PEST_GUIDANCE: dict[str, dict[str, Any]] = {
    "stem_borer": {
        "title": "Yellow Stem Borer (Scirpophaga incertulas) Containment",
        "containment_advice": "Set up pheromone traps to monitor adult moth activity; destroy egg masses during early tillering.",
        "what_to_avoid": "Avoid broad-spectrum chemical sprays that kill egg parasitoids (Trichogramma).",
        "immediate_actions": [
            "Install pheromone traps @ 5 per acre.",
            "Release Trichogramma japonicum @ 1,00,000 parasitoids/ha if available.",
            "Apply Chlorantraniliprole 0.4% G @ 10 kg/ha or Cartap Hydrochloride 4% G if dead-hearts exceed 5%.",
        ],
        "expert_trigger": "If dead-heart symptoms exceed 10% in vegetative stage or white-ears appear at panicle emergence.",
    },
    "brown_planthopper": {
        "title": "Brown Planthopper (BPH / Nilaparvata lugens) Protocol",
        "containment_advice": "Drain water completely to break pest lifecycle; create alleyways (30 cm every 2 meters) for sunlight.",
        "what_to_avoid": "Never use synthetic pyrethroids which cause intense BPH resurgence.",
        "immediate_actions": [
            "Drain standing water for 3-4 days (alternate wetting and drying).",
            "Spray Pymetrozine 50% WG @ 0.6 g/L or Triflumezopyrim 10% SC @ 0.5 ml/L directed at stem base.",
            "Avoid excessive nitrogen fertilizers.",
        ],
        "expert_trigger": "If hopper count exceeds 15-20 insects per hill or hopper-burn circles begin forming.",
    },
    "gall_midge": {
        "title": "Rice Gall Midge (Orseolia oryzae) Containment",
        "containment_advice": "Conserve predatory spiders and platygasterid parasitoids; avoid staggered planting in the locality.",
        "what_to_avoid": "Do not apply high nitrogen doses in endemic gall midge pockets.",
        "immediate_actions": [
            "Apply Chlorpyriphos 20% EC @ 2.5 ml/L or Fipronil 0.3% G @ 20 kg/ha at early silver-shoot stage.",
            "Maintain moderate water levels in field.",
        ],
        "expert_trigger": "If silver shoots (onion leaf galls) exceed 5% of tillers during vegetative growth.",
    },
    "leaf_folder": {
        "title": "Rice Leaf Folder (Cnaphalocrocis medinalis) Management",
        "containment_advice": "Pass an open rope or thorny brush across the crop canopy early morning to dislodge caterpillars.",
        "what_to_avoid": "Avoid close spacing and excessive nitrogenous fertilization.",
        "immediate_actions": [
            "Spray Flubendiamide 39.35% SC @ 0.2 ml/L or Chlorantraniliprole 18.5% SC @ 0.3 ml/L.",
            "Use light traps to monitor and trap adult moths.",
        ],
        "expert_trigger": "If folded longitudinal leaf damage exceeds 10% at maximum tillering or 5% at boot stage.",
    },
    "green_leafhopper": {
        "title": "Green Leafhopper (GLH / Nephotettix virescens) Vector Control",
        "containment_advice": "Monitor GLH populations to prevent transmission of Rice Tungro Virus.",
        "what_to_avoid": "Do not leave diseased volunteer rice plants on bunds.",
        "immediate_actions": [
            "Set up light traps during night hours.",
            "Spray Thiamethoxam 25% WG @ 0.3 g/L or Imidacloprid 17.8% SL @ 0.25 ml/L.",
        ],
        "expert_trigger": "If population exceeds 5-10 hoppers per hill during early vegetative stage.",
    },
    "fall_armyworm": {
        "title": "Fall Armyworm (Spodoptera frugiperda) Emergency Protocol",
        "containment_advice": "Scout whorl leaves for pinhole feeding and moist frass; apply targeted bio-rationals early.",
        "what_to_avoid": "Avoid broadcast spraying over canopy without targeting the central whorl.",
        "immediate_actions": [
            "Apply sand mixed with lime (9:1) or dry soil directly into central plant whorls.",
            "Spray Bacillus thuringiensis (Bt) @ 2.0 g/L or Spinetoram 11.7% SC @ 0.5 ml/L into the whorls.",
            "Install pheromone traps @ 4 per acre.",
        ],
        "expert_trigger": "If whorl infestation exceeds 10% in young crop (<30 days after emergence).",
    },
    "whitefly": {
        "title": "Whitefly (Bemisia tabaci) Integrated Management",
        "containment_advice": "Install mass yellow sticky traps and spray systemic or insect growth regulators early.",
        "what_to_avoid": "Avoid repeated sprays of single-chemistry insecticides causing resistance.",
        "immediate_actions": [
            "Place yellow sticky sheets (20-25/acre) at top canopy level.",
            "Spray Pyriproxyfen 10% EC @ 1.5 ml/L or Spiromesifen 22.9% SC @ 1.0 ml/L.",
            "Maintain weed-free field borders.",
        ],
        "expert_trigger": "If whitefly nymphs and adults cluster thickly under foliage causing sooty mold.",
    },
    "aphid": {
        "title": "Aphid (Aphis spp.) Containment Protocol",
        "containment_advice": "Conserve ladybird beetles and syrphid fly predators; spray neem or soap solutions for spot outbreaks.",
        "what_to_avoid": "Avoid water-stress which makes sap-feeding aphids more damaging.",
        "immediate_actions": [
            "Spray 1% horticultural soap or Neem Seed Kernel Extract (NSKE) 5%.",
            "Apply Acetamiprid 20% SP @ 0.2 g/L or Dimethoate 30% EC @ 1.7 ml/L for severe colonies.",
        ],
        "expert_trigger": "If colonies cause severe leaf curling and honey-dew accumulation across >20% plants.",
    },
}

# Crop-level fallback guidance entries
_CROP_DEFAULT_GUIDANCE: dict[str, dict[str, Any]] = {
    "rice": {
        "title": "Rice General Crop Health Protocol",
        "containment_advice": "Maintain 2-3 cm standing water; inspect tillers for water-soaked spots, blast lesions, or stem borer dead-hearts.",
        "what_to_avoid": "Do not apply excess nitrogen or allow prolonged unmonitored stagnation.",
        "immediate_actions": [
            "Scout field twice weekly along a 'W' path.",
            "Maintain balanced NPK with adequate potash.",
            "Keep field bunds clean of alternate host weeds.",
        ],
        "expert_trigger": "If yellowing, spotting, or wilting exceeds 10% of field area.",
    },
    "cotton": {
        "title": "Cotton Integrated Crop Care",
        "containment_advice": "Inspect lower leaf surfaces for sucking pests (aphids, whiteflies, thrips); monitor squares for bollworm entry holes.",
        "what_to_avoid": "Avoid excessive early-stage irrigation causing luxuriant vegetative growth.",
        "immediate_actions": [
            "Install yellow and blue sticky traps across the plot.",
            "Apply recommended sucking pest management if ETL is reached.",
        ],
        "expert_trigger": "If square drop or leaf curling exceeds 15%.",
    },
    "maize": {
        "title": "Maize Crop Health & Whorl Care",
        "containment_advice": "Examine central whorls for fall armyworm feeding and leaf blights.",
        "what_to_avoid": "Do not leave crop moisture-stressed during tasseling and silking.",
        "immediate_actions": [
            "Inspect central whorls for frass and pinholes.",
            "Ensure proper drainage during heavy rain events.",
        ],
        "expert_trigger": "If whorl damage or stem lodging exceeds 10%.",
    },
    "tomato": {
        "title": "Tomato Foliar Health & Vector Protocol",
        "containment_advice": "Stake plants to prevent ground contact; monitor for leaf curl and early/late blight symptoms.",
        "what_to_avoid": "Avoid overhead watering; avoid handling wet foliage.",
        "immediate_actions": [
            "Remove diseased lower leaves.",
            "Install sticky traps for whitefly control.",
        ],
        "expert_trigger": "If sudden leaf blighting or virus stunting spreads.",
    },
    "potato": {
        "title": "Potato Tuber & Foliage Protection",
        "containment_advice": "Keep ridges properly earthed up; apply preventive fungicides if late blight weather develops.",
        "what_to_avoid": "Do not expose tubers to sunlight; do not irrigate in late evening.",
        "immediate_actions": [
            "Ensure complete earthing up around root zones.",
            "Scout for water-soaked dark leaf margins.",
        ],
        "expert_trigger": "If rapid foliar blighting appears during cool foggy spells.",
    },
    "groundnut": {
        "title": "Groundnut Foliar Disease Protocol",
        "containment_advice": "Monitor for tikka leaf spot and collar rot; ensure gypsum application at pegging.",
        "what_to_avoid": "Avoid moisture stress during peg formation and pod development.",
        "immediate_actions": [
            "Spray Mancozeb 75% WP @ 2 g/L at early tikka spotting.",
            "Maintain loose, well-drained topsoil.",
        ],
        "expert_trigger": "If defoliation from tikka spots exceeds 20%.",
    },
    "sugarcane": {
        "title": "Sugarcane Cane & Foliage Management",
        "containment_advice": "Scout for shoot borer dead-hearts and red rot symptoms in early tillering.",
        "what_to_avoid": "Avoid waterlogging in early cane formation.",
        "immediate_actions": [
            "Trash mulching to conserve moisture and suppress early borer.",
            "Provide earthing up at 90-120 days.",
        ],
        "expert_trigger": "If central spindle wilts with red discoloration inside cane.",
    },
    "chilli": {
        "title": "Chilli Sucking Pest & Anthracnose Care",
        "containment_advice": "Monitor for thrips, mites, and fruit rot (anthracnose); apply protective sprays.",
        "what_to_avoid": "Avoid overhead sprinkler irrigation during flowering.",
        "immediate_actions": [
            "Install blue sticky traps for thrips monitoring.",
            "Spray Copper Oxychloride 50 WP @ 2.5 g/L if fruit rot appears.",
        ],
        "expert_trigger": "If upward/downward leaf curling or circular fruit lesions exceed 10%.",
    },
    "wheat": {
        "title": "Wheat Rust & Foliar Management",
        "containment_advice": "Scout for yellow/brown rust pustules during cool reproductive stages.",
        "what_to_avoid": "Avoid excessive late-season irrigation causing lodging.",
        "immediate_actions": [
            "Apply Propiconazole 25% EC @ 1 ml/L at first appearance of rust pustules.",
            "Ensure critical irrigation at CRI and flowering stages.",
        ],
        "expert_trigger": "If yellow stripe rust stripes appear on upper leaves.",
    },
}

# Universal fallback card for any unrecognized crop
_UNIVERSAL_FALLBACK: dict[str, Any] = {
    "title": "Crop Stress Interim Containment Protocol",
    "containment_advice": "Inspect affected crop area, withhold non-essential chemical inputs, and consult local extension officer.",
    "what_to_avoid": "Do not apply heavy doses of unverified chemicals without expert confirmation.",
    "immediate_actions": [
        "Take clear, close-up photos of symptoms in natural morning light.",
        "Isolate heavily diseased plant debris away from drainage channels.",
        "Record recent fertilizer and weather events for extension review.",
    ],
    "expert_trigger": "If crop stress symptoms expand across more than 15% of plot area within 3 days.",
}


def get_guidance_card(
    crop: str,
    problem_label: str | None = None,
    problem_type: str | None = None,
) -> GuidanceCard:
    """Look up an interim containment guidance card for crop and problem.

    Lookup resolution:
      1. Specific (problem_label) entry in disease or pest dictionary
      2. Crop-specific default guidance card
      3. Universal agricultural containment fallback card
    Guarantees no crop or label ever falls through without guidance.
    """
    clean_crop = crop.strip().lower() if crop else "crop"
    if clean_crop in ("paddy", "samba_paddy", "kuruvai_paddy", "thaladi_paddy"):
        clean_crop = "rice"

    clean_label = problem_label.strip().lower() if problem_label else None
    ptype = problem_type.strip().lower() if problem_type else "general"

    # 1. Match specific problem label
    if clean_label:
        if clean_label in _DISEASE_GUIDANCE:
            raw = _DISEASE_GUIDANCE[clean_label]
            return GuidanceCard(
                crop=clean_crop,
                problem_type="disease",
                problem_label=clean_label,
                title=raw["title"],
                containment_advice=raw["containment_advice"],
                what_to_avoid=raw["what_to_avoid"],
                immediate_actions=raw["immediate_actions"],
                expert_trigger=raw["expert_trigger"],
            )
        if clean_label in _PEST_GUIDANCE:
            raw = _PEST_GUIDANCE[clean_label]
            return GuidanceCard(
                crop=clean_crop,
                problem_type="pest",
                problem_label=clean_label,
                title=raw["title"],
                containment_advice=raw["containment_advice"],
                what_to_avoid=raw["what_to_avoid"],
                immediate_actions=raw["immediate_actions"],
                expert_trigger=raw["expert_trigger"],
            )

    # 2. Match crop-level default
    if clean_crop in _CROP_DEFAULT_GUIDANCE:
        raw = _CROP_DEFAULT_GUIDANCE[clean_crop]
        return GuidanceCard(
            crop=clean_crop,
            problem_type=ptype,
            problem_label=clean_label,
            title=raw["title"],
            containment_advice=raw["containment_advice"],
            what_to_avoid=raw["what_to_avoid"],
            immediate_actions=raw["immediate_actions"],
            expert_trigger=raw["expert_trigger"],
        )

    # 3. Universal agricultural fallback
    return GuidanceCard(
        crop=clean_crop,
        problem_type=ptype,
        problem_label=clean_label,
        title=_UNIVERSAL_FALLBACK["title"],
        containment_advice=_UNIVERSAL_FALLBACK["containment_advice"],
        what_to_avoid=_UNIVERSAL_FALLBACK["what_to_avoid"],
        immediate_actions=_UNIVERSAL_FALLBACK["immediate_actions"],
        expert_trigger=_UNIVERSAL_FALLBACK["expert_trigger"],
    )


def list_all_guidance_cards() -> list[GuidanceCard]:
    """List all available static guidance cards."""
    cards: list[GuidanceCard] = []
    for label, raw in _DISEASE_GUIDANCE.items():
        cards.append(
            GuidanceCard(
                crop="rice",
                problem_type="disease",
                problem_label=label,
                title=raw["title"],
                containment_advice=raw["containment_advice"],
                what_to_avoid=raw["what_to_avoid"],
                immediate_actions=raw["immediate_actions"],
                expert_trigger=raw["expert_trigger"],
            )
        )
    for label, raw in _PEST_GUIDANCE.items():
        cards.append(
            GuidanceCard(
                crop="rice",
                problem_type="pest",
                problem_label=label,
                title=raw["title"],
                containment_advice=raw["containment_advice"],
                what_to_avoid=raw["what_to_avoid"],
                immediate_actions=raw["immediate_actions"],
                expert_trigger=raw["expert_trigger"],
            )
        )
    for crop_name, raw in _CROP_DEFAULT_GUIDANCE.items():
        cards.append(
            GuidanceCard(
                crop=crop_name,
                problem_type="general",
                problem_label=None,
                title=raw["title"],
                containment_advice=raw["containment_advice"],
                what_to_avoid=raw["what_to_avoid"],
                immediate_actions=raw["immediate_actions"],
                expert_trigger=raw["expert_trigger"],
            )
        )
    return cards
