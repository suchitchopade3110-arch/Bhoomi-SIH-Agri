"""The curated corpus (PRD §5.7): "named, dated, owned." This is the seed
slice for the demo — Samba paddy, centered on Bacterial Leaf Blight (BLB),
the disease in the PRD §6 walkthrough — plus enough adjacent and unrelated
paddy agronomy docs that relevance thresholding is meaningful (a BLB query
should score the BLB docs high and the unrelated ones low).

Each entry is one source document: a stable ``doc_id``, a ``title`` fit to
show a farmer or judge as a citation, a ``reviewed_on`` date (contract
§2.10/§2.11 citations), and the curated ``body`` text that gets chunked and
embedded by ``services/rag/ingest.py``.

In production these would be sourced from ICAR / state agricultural
university package-of-practices and KVK advisories, each with a named
curator and review date (PRD §5.7). This seed slice is written for the demo
corpus rather than reproduced from a specific external publication.
"""

from datetime import date
from typing import TypedDict


class CorpusDoc(TypedDict):
    doc_id: str
    title: str
    reviewed_on: date
    body: str


CORPUS_DOCS: list[CorpusDoc] = [
    {
        "doc_id": "kb_211",
        "title": "ICAR PoP: Rice — Bacterial Leaf Blight",
        "reviewed_on": date(2025, 11, 2),
        "body": (
            "Bacterial Leaf Blight (BLB) is one of the most destructive bacterial diseases of paddy "
            "(rice), caused by the bacterium Xanthomonas oryzae pv. oryzae. It is most damaging during "
            "the vegetative to reproductive growth stages, and can cause yield losses of 20-50% in "
            "susceptible varieties under favorable conditions.\n\n"
            "Early symptoms appear as small, water-soaked lesions near the leaf tip or margins. These "
            "lesions elongate along the veins, turning yellow and then grayish-white as they mature, "
            "with a characteristic wavy margin separating diseased from healthy tissue. In the early "
            "morning, a milky bacterial ooze may be visible on the lesion surface — this is diagnostic "
            "for BLB and distinguishes it from fungal leaf diseases.\n\n"
            "As the disease progresses, lesions coalesce and can cover the entire leaf blade, causing "
            "the leaf to dry out and wither. In severe infections, especially in young seedlings, the "
            "disease can cause a distinct wilting phase locally known as 'Kresek,' where entire seedlings "
            "collapse and die within days of transplanting."
        ),
    },
    {
        "doc_id": "kb_212",
        "title": "ICAR PoP: Rice — BLB Causal Agent and Disease Cycle",
        "reviewed_on": date(2025, 11, 2),
        "body": (
            "The causal organism, Xanthomonas oryzae pv. oryzae (Xoo), is a gram-negative, rod-shaped "
            "bacterium. It survives between cropping seasons in infected rice stubble, seeds, weed hosts "
            "growing near paddy fields, and irrigation water and canal systems.\n\n"
            "The pathogen enters the leaf primarily through hydathodes at the leaf tip and margins, and "
            "through wounds caused by wind damage, insect feeding, or field operations. Once inside, the "
            "bacteria multiply in the xylem vessels and spread systemically along the veins, which "
            "explains the characteristic vein-following lesion pattern.\n\n"
            "Secondary spread within a field happens rapidly via wind-driven rain, irrigation water "
            "movement between plots, and mechanical contact between plants during field operations. "
            "This is why BLB can appear to spread in a directional pattern following prevailing wind or "
            "water-flow direction across a field."
        ),
    },
    {
        "doc_id": "kb_213",
        "title": "ICAR PoP: Rice — BLB Favorable Environmental Conditions",
        "reviewed_on": date(2025, 10, 20),
        "body": (
            "Bacterial Leaf Blight thrives under warm, humid conditions. Disease development is most "
            "rapid at temperatures between 25-34°C combined with relative humidity above 70%. Extended "
            "periods of leaf wetness — from dew, drizzle, or standing water splashing onto leaves — "
            "strongly favor infection and secondary spread.\n\n"
            "Standing water in the field, especially deep flooding, increases BLB severity by keeping "
            "humidity high at canopy level and by facilitating bacterial movement through the water "
            "itself. Fields with poor drainage, or those flooded continuously through a heavy monsoon "
            "spell, consistently show higher BLB incidence than fields with intermittent, controlled "
            "irrigation.\n\n"
            "High nitrogen fertilization, particularly excess or late top-dressed urea, produces lush, "
            "succulent leaf tissue that is more susceptible to bacterial infection and supports faster "
            "lesion expansion once infection has occurred."
        ),
    },
    {
        "doc_id": "kb_214",
        "title": "ICAR PoP: Rice — BLB Cultural Control Measures",
        "reviewed_on": date(2025, 9, 15),
        "body": (
            "Cultural control is the first line of defense against BLB and should be combined with, not "
            "replaced by, chemical measures. Drain the field to remove standing water as soon as BLB "
            "symptoms are noticed — this reduces the humid microclimate the bacterium needs and slows "
            "secondary spread through water movement.\n\n"
            "Avoid excess nitrogen application, especially late top-dressing after symptoms appear — this "
            "accelerates disease spread by producing more susceptible new growth. Balance nitrogen with "
            "adequate potassium, which improves the plant's structural resistance to infection.\n\n"
            "Remove and destroy (burn or bury away from the field) severely infected plant debris after "
            "harvest, since infected stubble is a primary carryover source of the pathogen to the next "
            "season. Avoid working in wet fields when BLB is present, since field operations easily "
            "spread bacterial ooze between plants on tools, clothing, and hands."
        ),
    },
    {
        "doc_id": "kb_215",
        "title": "ICAR PoP: Rice — BLB Chemical Control",
        "reviewed_on": date(2025, 9, 15),
        "body": (
            "Where BLB is confirmed and spreading, copper-based bactericides are the standard chemical "
            "control: copper oxychloride 50% WP at 2.5 g/liter, or copper hydroxide formulations per "
            "label rate, applied as a foliar spray at first symptom appearance and repeated at 10-14 day "
            "intervals if conditions remain favorable for disease.\n\n"
            "Streptocycline (a streptomycin-based bactericide) at 100-200 ppm, tank-mixed with copper "
            "oxychloride, improves control in severe outbreaks — always follow the local label rate and "
            "pre-harvest interval restrictions.\n\n"
            "Chemical control works best as a preventive or early-curative measure combined with "
            "drainage and nitrogen management; it is far less effective once lesions have already "
            "covered a large portion of the leaf area. Spraying alone, without correcting field drainage "
            "and nitrogen excess, generally gives disappointing results."
        ),
    },
    {
        "doc_id": "kb_216",
        "title": "ICAR PoP: Rice — BLB-Resistant Varieties",
        "reviewed_on": date(2025, 8, 5),
        "body": (
            "Growing a BLB-resistant or tolerant variety is the most durable long-term control strategy. "
            "Varieties carrying resistance genes such as Xa4, xa5, Xa7, Xa13, and Xa21 (individually or "
            "pyramided) show substantially reduced lesion development compared to susceptible varieties "
            "under the same field conditions.\n\n"
            "In Tamil Nadu, several released Samba-season paddy varieties carry partial to strong BLB "
            "resistance; consult the current TNAU variety recommendation list for the district before "
            "sowing, since resistance can be race-specific and varies by region.\n\n"
            "Even a resistant variety should still be managed with balanced nitrogen and good drainage — "
            "resistance reduces severity but does not eliminate risk entirely, especially under sustained "
            "high-humidity conditions."
        ),
    },
    {
        "doc_id": "kb_217",
        "title": "ICAR PoP: Rice — Field Drainage and Water Management for Disease Control",
        "reviewed_on": date(2025, 7, 28),
        "body": (
            "Water management is a central lever for controlling several paddy diseases, BLB included. "
            "Alternate wetting and drying (AWD) — allowing the field to dry to a few centimeters below "
            "the soil surface between irrigations rather than maintaining continuous flooding — reduces "
            "humidity-favoring conditions for bacterial and fungal diseases while also cutting water use.\n\n"
            "During an active BLB outbreak, drain the field completely for several days if the growth "
            "stage allows it, then resume controlled irrigation rather than continuous flooding. Ensure "
            "field bunds are intact so drained water does not simply flow into a neighboring plot and "
            "spread the pathogen further.\n\n"
            "Good drainage design — a functioning outlet, properly graded field, and bunds maintained "
            "between plots — pays for itself across the season in reduced disease pressure, not only "
            "during an active outbreak."
        ),
    },
    {
        "doc_id": "kb_218",
        "title": "ICAR PoP: Rice — Nitrogen Management and Disease Susceptibility",
        "reviewed_on": date(2025, 7, 10),
        "body": (
            "Nitrogen is the single most influential nutrient on paddy disease susceptibility. Excess or "
            "poorly timed nitrogen, especially a large late top-dressing, produces soft, nitrogen-rich "
            "leaf tissue that both bacterial pathogens (like BLB) and fungal pathogens (like blast) "
            "exploit more readily.\n\n"
            "Split nitrogen application — basal plus staged top-dressings tied to growth stage rather "
            "than a single heavy dose — gives more even plant growth and lower disease pressure than the "
            "same total nitrogen applied all at once.\n\n"
            "If BLB symptoms are already present, withhold any planned nitrogen top-dressing until the "
            "outbreak is controlled; adding nitrogen mid-outbreak measurably accelerates lesion spread."
        ),
    },
    {
        "doc_id": "kb_219",
        "title": "ICAR PoP: Rice — BLB Field Scouting and Monitoring",
        "reviewed_on": date(2025, 6, 22),
        "body": (
            "Regular field scouting, at least weekly during the vegetative and reproductive stages, "
            "gives the earliest possible warning of a BLB outbreak. Walk the field in a zigzag pattern "
            "and examine the upper leaves of plants near field margins, drainage channels, and low spots "
            "first — these are the earliest and most severely affected locations.\n\n"
            "Look specifically for water-soaked lesions at the leaf tip or margin, the wavy yellow-to-"
            "grayish lesion boundary, and early-morning bacterial ooze on lesion surfaces. Photograph and "
            "record the date, location, and approximate percentage of affected leaf area for any "
            "suspected case, so severity trend can be tracked across follow-up visits.\n\n"
            "If more than 25% of leaf area on multiple plants shows active lesions, or if the wilting "
            "'Kresek' phase appears in young seedlings, escalate to a KVK agronomist for confirmation and "
            "a tailored treatment plan rather than continuing self-treatment alone."
        ),
    },
    {
        "doc_id": "kb_220",
        "title": "ICAR PoP: Rice — Seed Treatment and Nursery-Stage BLB Prevention",
        "reviewed_on": date(2025, 5, 30),
        "body": (
            "Since BLB can be seed-borne, treating seed before sowing meaningfully reduces the risk of "
            "introducing the pathogen into a new nursery. Soak seed in a solution of Streptocycline (100 "
            "ppm) combined with a recommended fungicide seed treatment for 8-12 hours before sowing, "
            "following the current package-of-practices rate.\n\n"
            "Raise nurseries away from previously BLB-affected fields and irrigation sources known to "
            "carry the pathogen. Avoid transplanting seedlings that already show tip lesions — this "
            "directly transfers an active infection into the new field.\n\n"
            "Maintain a clean water source for the nursery; avoid drawing irrigation water from a canal "
            "or drain that passes through or near an infected field."
        ),
    },
    {
        "doc_id": "kb_230",
        "title": "ICAR PoP: Rice — Blast Disease (Magnaporthe oryzae)",
        "reviewed_on": date(2025, 4, 18),
        "body": (
            "Rice blast, caused by the fungus Magnaporthe oryzae, produces distinct spindle-shaped "
            "lesions with a gray-white center and reddish-brown margin on leaves, unlike the water-soaked "
            "vein-following lesions of bacterial leaf blight. Blast can also attack the neck of the "
            "panicle, causing 'neck blast' which can result in complete grain loss on affected tillers.\n\n"
            "Blast is favored by high humidity, extended leaf wetness, and moderate temperatures (20-28°C) "
            "— cooler and more humid than the range that most favors BLB. Excess nitrogen similarly "
            "increases blast susceptibility.\n\n"
            "Management includes resistant varieties, balanced nitrogen, and tricyclazole-based fungicide "
            "sprays at the recommended rate when the disease is confirmed."
        ),
    },
    {
        "doc_id": "kb_231",
        "title": "ICAR PoP: Rice — Sheath Blight (Rhizoctonia solani)",
        "reviewed_on": date(2025, 4, 18),
        "body": (
            "Sheath blight, caused by the soil-borne fungus Rhizoctonia solani, produces irregular, "
            "greenish-gray lesions with a straw-colored center on the leaf sheath near the waterline, "
            "distinct from the leaf-blade lesions typical of both BLB and blast.\n\n"
            "Dense planting, heavy nitrogen use, and continuous flooding all favor sheath blight by "
            "keeping humidity high within the canopy and encouraging the fungus to climb from the water "
            "surface up the plant. Wider spacing and alternate wetting and drying reduce incidence.\n\n"
            "Validamycin or hexaconazole-based fungicides, applied at early sheath symptom onset, are the "
            "standard chemical control."
        ),
    },
    {
        "doc_id": "kb_232",
        "title": "ICAR PoP: Rice — Brown Spot Disease",
        "reviewed_on": date(2025, 3, 5),
        "body": (
            "Brown spot, caused by the fungus Bipolaris oryzae, produces small, oval, brown lesions "
            "scattered across the leaf blade, often associated with nutrient-deficient soils — "
            "particularly potassium deficiency — rather than the nitrogen-excess conditions that favor "
            "BLB and blast.\n\n"
            "Correcting soil fertility, particularly potassium and zinc status, is often more effective "
            "long-term control than repeated fungicide spraying. Seed treatment with a recommended "
            "fungicide reduces seed-borne carryover, which is a significant source of infection for this "
            "disease."
        ),
    },
    {
        "doc_id": "kb_240",
        "title": "FAO-56 / ICAR: Rice Crop Water Requirement (ET0 and Kc)",
        "reviewed_on": date(2025, 2, 12),
        "body": (
            "Reference evapotranspiration (ET0), calculated via the FAO-56 Penman-Monteith method, "
            "combined with crop coefficients (Kc) specific to each growth stage, gives the crop water "
            "requirement for paddy: crop water need = ET0 x Kc. Effective rainfall is then subtracted "
            "from the gross requirement to give the net irrigation need.\n\n"
            "For Samba-season paddy, Kc values typically rise through the vegetative stage, peak around "
            "the reproductive stage, and decline through ripening. Local weather station or gridded "
            "weather-service ET0 data (e.g. Open-Meteo, IMD) should be used rather than a single seasonal "
            "average, since day-to-day variation is significant.\n\n"
            "Over- or under-irrigating relative to this calculated requirement both carry cost: "
            "under-irrigation stresses the crop and can reduce yield, while over-irrigation wastes water "
            "and, as noted elsewhere, increases disease pressure by keeping humidity high."
        ),
    },
    {
        "doc_id": "kb_241",
        "title": "ICAR PoP: Rice — Nutrient Management Schedule (NPK)",
        "reviewed_on": date(2025, 1, 22),
        "body": (
            "A balanced NPK schedule for irrigated paddy typically splits nitrogen across basal, tillering, "
            "and panicle-initiation applications rather than a single dose, with phosphorus applied fully "
            "at basal and potassium split between basal and panicle initiation.\n\n"
            "Soil testing before the season is the most reliable way to set exact rates for a given field "
            "rather than relying on a blanket regional recommendation; zinc sulfate application is "
            "commonly needed on paddy soils showing zinc-deficiency symptoms (interveinal chlorosis on "
            "younger leaves).\n\n"
            "This schedule is primarily a yield and quality lever; see the BLB and disease-specific "
            "package-of-practices documents for how nitrogen timing also affects disease susceptibility."
        ),
    },
    {
        "doc_id": "kb_250",
        "title": "ICAR PoP: Paddy Post-Harvest Handling and Storage",
        "reviewed_on": date(2024, 12, 10),
        "body": (
            "Proper drying of harvested paddy to 12-14% moisture content before storage is essential to "
            "prevent fungal spoilage and insect infestation in storage. Sun-drying on a clean, raised "
            "surface, turned regularly, is the standard smallholder method; mechanical dryers give more "
            "consistent results where available.\n\n"
            "Store dried paddy in clean, dry, pest-proof containers or bags, off the ground, away from "
            "walls, in a well-ventilated store. Fumigate storage structures between seasons if past "
            "infestation has been an issue, following label safety precautions.\n\n"
            "This guidance covers the post-harvest phase and is unrelated to in-field disease management "
            "during the growing season."
        ),
    },
    {
        "doc_id": "kb_260",
        "title": "TNAU Crop Calendar: Samba Season Paddy, Tamil Nadu",
        "reviewed_on": date(2025, 6, 1),
        "body": (
            "Samba is the principal irrigated paddy season in the Cauvery delta and much of Tamil Nadu, "
            "with nursery sowing typically in August and transplanting in September, running through to "
            "harvest around January-February depending on the variety's duration.\n\n"
            "Land preparation, timely transplanting at 25-35 days seedling age, and maintaining the "
            "recommended spacing all support even crop stand establishment, which in turn supports more "
            "uniform disease and water management decisions across the field later in the season.\n\n"
            "This calendar is a general scheduling reference; consult stage-specific package-of-practices "
            "documents (irrigation, nutrient, and disease management) for what to do at each point on "
            "this calendar."
        ),
    },
]
