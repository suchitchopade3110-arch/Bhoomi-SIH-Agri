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

--- Pest entries (kb_p3xx) ---------------------------------------------
The pest entries below are a deliberately *partial* ingestion of the
real, sourced dataset at ``data/curated/Dataset_v4_validated/corpus/``
(TNAU / ICAR-IIRR / IRRI / KVK extension material, 8 docs). Every source
doc there carries ``chemical_prescriptions`` (specific product/dose pairs,
some ``regulatory_status: RESTRICTED``) and a "Regulatory & Validation
Status" section discussing them, plus a manifest-level
``chemical_advice_status: UNVERIFIED`` at the corpus level. Neither the
chemical-control bullets nor the regulatory-status sections are
reproduced here: only Overview, Field Identification Cues, Economic
Threshold Levels (ETL), and the Cultural/Biological/physical control
practices are carried over. This lets pest diagnosis compose grounded,
non-fabricated advice for identification and non-chemical management,
while a query needing chemical-specific guidance still finds nothing to
ground on and correctly escalates (PRD §5.9 "never fabricate") — see
README.md §9 for the product decision behind this split.
"""

from datetime import date
from typing import NotRequired, TypedDict


class CorpusDoc(TypedDict, total=False):
    doc_id: str
    content_type: str  # "disease" | "pest" — real retrieval-scoping metadata (checklist §4.1),
    # not inferred from doc_id naming; see knowledge_chunks.content_type / crop.
    crop: str
    title: str
    reviewed_on: date
    body: str
    distinguishing_cues: NotRequired[str]


CORPUS_DOCS: list[CorpusDoc] = [
    {
        "doc_id": "kb_211",
        "content_type": "disease",
        "crop": "paddy",
        "title": "ICAR PoP: Rice — Bacterial Leaf Blight",
        "reviewed_on": date(2025, 11, 2),
        "distinguishing_cues": (
            "Early morning milky bacterial ooze on lesion surfaces with characteristic wavy margin, "
            "diagnostic for BLB and distinguishing it from fungal leaf diseases; distinct 'Kresek' wilting in seedlings."
        ),
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
        "content_type": "disease",
        "crop": "paddy",
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
        "content_type": "disease",
        "crop": "paddy",
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
        "content_type": "disease",
        "crop": "paddy",
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
        "content_type": "disease",
        "crop": "paddy",
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
        "content_type": "disease",
        "crop": "paddy",
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
        "content_type": "disease",
        "crop": "paddy",
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
        "content_type": "disease",
        "crop": "paddy",
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
        "content_type": "disease",
        "crop": "paddy",
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
        "content_type": "disease",
        "crop": "paddy",
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
        "content_type": "disease",
        "crop": "paddy",
        "title": "ICAR PoP: Rice — Blast Disease (Magnaporthe oryzae)",
        "reviewed_on": date(2025, 4, 18),
        "distinguishing_cues": (
            "Spindle-shaped leaf lesions with gray-white center and reddish-brown margin, distinct from vein-following BLB lesions; "
            "neck blast attacks panicle base causing completely empty, chaffy grain."
        ),
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
        "content_type": "disease",
        "crop": "paddy",
        "title": "ICAR PoP: Rice — Sheath Blight (Rhizoctonia solani)",
        "reviewed_on": date(2025, 4, 18),
        "distinguishing_cues": (
            "Irregular greenish-gray lesions with straw-colored center on leaf sheath near waterline climbing upward, "
            "distinct from leaf-blade lesions of BLB and blast."
        ),
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
        "content_type": "disease",
        "crop": "paddy",
        "title": "ICAR PoP: Rice — Brown Spot Disease",
        "reviewed_on": date(2025, 3, 5),
        "distinguishing_cues": (
            "Small, oval, brown lesions scattered across leaf blade, typically associated with potassium/soil "
            "nutrient deficiencies rather than nitrogen excess."
        ),
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
        "content_type": "disease",
        "crop": "paddy",
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
        "content_type": "disease",
        "crop": "paddy",
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
        "content_type": "disease",
        "crop": "paddy",
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
        "content_type": "disease",
        "crop": "paddy",
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
    {
        "doc_id": "kb_p301",
        "content_type": "pest",
        "crop": "paddy",
        "title": "TNAU Rice Pest Management Guide — Stem Borer (Identification & Non-Chemical Control)",
        "reviewed_on": date(2026, 8, 24),
        "distinguishing_cues": (
            "Egg masses with buff-colored hairs on tender leaf tips; brown-headed larvae boring lower stem; "
            "central shoot 'dead hearts' pulling out easily; erect white chaffy earheads at reproductive stage."
        ),
        "body": (
            "Stem borer (Scirpophaga incertulas) is one of the major insect pests of paddy across Tamil "
            "Nadu and South India, attacking rice at all growth stages. During the vegetative stage, "
            "larval feeding inside the stem causes the central shoot to dry up and die, producing the "
            "classic 'dead heart' symptom. During the reproductive stage, feeding at the base of the "
            "panicle results in completely empty, chaffy, erect white panicles known as 'white earhead.'\n\n"
            "Field identification cues: egg masses covered with buff-colored hairs laid near the tips of "
            "tender leaves; larvae with a brown head and dirty-white body boring inside the lower stem; "
            "adult moths with silvery-white to yellowish-brown wings bearing prominent black spots on the "
            "forewings; dead hearts where the central tiller pulls out easily when tugged; and white "
            "earheads in the flowering to grain-filling phase.\n\n"
            "Field interventions should be initiated when scouting reaches these thresholds: vegetative "
            "stage — 1 egg mass per square meter or 10% dead hearts; reproductive stage — 1 egg mass per "
            "square meter or 5% white ears.\n\n"
            "Cultural and varietal control: cultivate moderately resistant or tolerant rice varieties "
            "recommended for the region, such as CO 51 and ADT 43. Regularly scout the nursery and main "
            "field to hand-pick and destroy egg masses before larvae hatch. Biological control: release "
            "egg parasitoids (Trichogramma japonicum) at 50,000 per hectare when moth activity is "
            "detected, and conserve native predatory spiders and parasitoids."
        ),
    },
    {
        "doc_id": "kb_p302",
        "content_type": "pest",
        "crop": "paddy",
        "title": "IRRI Rice Knowledge Bank — Brown Planthopper (Identification & Non-Chemical Control)",
        "reviewed_on": date(2026, 8, 24),
        "distinguishing_cues": (
            "Small brownish insects with distinct white mid-dorsal abdominal band near waterline; circular scorched "
            "hopper-burn patches; copious sticky honeydew with black sooty mold at plant base."
        ),
        "body": (
            "Brown planthopper (Nilaparvata lugens) is a destructive sap-sucking pest affecting rice "
            "across Tamil Nadu and South India, infesting crops at all growth stages with damage peaking "
            "between tillering and flowering. Both nymphs and adults gather at the base of rice tillers "
            "near the water line, sucking plant sap; heavy infestation leads to extensive yellowing and "
            "rapid drying of crops in characteristic circular patches known as 'hopper burn.'\n\n"
            "Field identification cues: small brownish insect with distinct white bands across the "
            "mid-dorsal abdomen; wings held roof-like over the body at rest, in both long-winged and "
            "short-winged forms; young nymphs with white waxy filaments gathering densely at the plant "
            "base; circular scorched or dried-up hopper-burn patches spreading rapidly across the field; "
            "and copious sticky honeydew at the base of tillers leading to black sooty mold growth.\n\n"
            "Field interventions should be initiated when scouting reaches these thresholds: seedling "
            "stage — 1 to 2 nymphs per hill; vegetative stage — 5 to 10 nymphs per hill (rising to 10-15 "
            "per hill where mirid bug or wolf-spider predators are present at 1 or more per hill); "
            "reproductive stage — 10 to 20 nymphs per hill (upper limit applies when natural biological "
            "control is intact).\n\n"
            "Cultural and varietal control: grow resistant paddy varieties such as ADT 36 and ASD 16; "
            "avoid excessive nitrogen application, especially late top-dressing; maintain intermittent "
            "irrigation (alternate wetting and drying) with 2 to 5 cm water depth rather than continuous "
            "deep flooding. Biological control: conserve beneficial natural predators including the mirid "
            "bug (Cyrtorhinus lividipennis), predatory spiders (Lycosa pseudoannulata), and water striders."
        ),
    },
    {
        "doc_id": "kb_p303",
        "content_type": "pest",
        "crop": "paddy",
        "title": "TNAU Rice Pest Management Guide — Leaf Folder (Identification & Non-Chemical Control)",
        "reviewed_on": date(2026, 8, 24),
        "distinguishing_cues": (
            "Leaves folded lengthwise with fine silken threads and green caterpillar inside; longitudinal white papery "
            "streaks where mesophyll is scraped; whitish scorched canopy appearance from a distance."
        ),
        "body": (
            "Rice leaf folder (Cnaphalocrocis medinalis) is a widespread foliage feeder of paddy across "
            "Tamil Nadu, damaging crops primarily from the vegetative stage through boot leaf and panicle "
            "emergence. The larva folds the leaf blade longitudinally using silken threads and feeds on "
            "the green mesophyll tissue from within the protective roll, leaving transparent white streaks "
            "and impairing photosynthesis.\n\n"
            "Field identification cues: leaves folded lengthwise with fine silken threads holding the "
            "margins together; greenish-translucent caterpillar actively feeding inside the folded leaf "
            "blade; longitudinal white, papery streaks where chlorophyll has been scraped; adult moth with "
            "golden-yellow wings and distinct wavy dark borders; severely infested fields show a whitish, "
            "scorched appearance from a distance.\n\n"
            "Field interventions should be initiated when scouting reaches these thresholds: vegetative "
            "stage — 1 larva per hill or 10% folded leaves; reproductive stage — 2 larvae per hill or 20% "
            "folded leaves, tightening to 5-10% damaged flag leaves during flag leaf emergence and booting "
            "given its critical role in grain carbohydrate supply.\n\n"
            "Cultural control: avoid excessively close planting, maintain wider row spacing to facilitate "
            "light penetration, and clear grassy weeds (Echinochloa, Leersia) from field bunds since they "
            "serve as alternate hosts. Physical and biological control: install light traps to monitor and "
            "trap adult moths, and conserve natural egg parasitoids such as Trichogramma chilonis."
        ),
    },
    {
        "doc_id": "kb_p304",
        "content_type": "pest",
        "crop": "paddy",
        "title": "ICAR Rice Production Manual — Green Leafhopper (Identification & Non-Chemical Control)",
        "reviewed_on": date(2026, 8, 24),
        "distinguishing_cues": (
            "Slender bright-green wedge-shaped insect with black markings on head and forewings; agile jumping/flying; "
            "foliage yellowing extending downward from tips; stunting with orange-yellow discoloration from Rice Tungro Virus."
        ),
        "body": (
            "Green leafhopper (Nephotettix virescens) infests paddy across all growth stages. Direct "
            "feeding causes foliage yellowing, but its primary economic significance is as the active "
            "vector transmitting Rice Tungro Virus (RTV), making early management in the nursery and "
            "vegetative stages critical.\n\n"
            "Field identification cues: slender, bright-green wedge-shaped insect with distinct black "
            "markings on the head and forewings; extreme jumping and flying agility when disturbed in the "
            "canopy; foliage yellowing beginning from leaf tips and extending downwards along margins; "
            "stunted plant growth with orange-yellow leaf discoloration if Rice Tungro Virus is "
            "co-transmitted.\n\n"
            "Field interventions should be initiated when scouting reaches these thresholds: seedling "
            "stage — 5 hoppers per hill, dropping to 1-2 per hill in Rice Tungro Virus endemic tracts; "
            "vegetative stage — 10 to 15 hoppers per hill, dropping to 2 per hill if active virus infection "
            "is present in neighboring plots; reproductive stage — 20 hoppers per hill once virus "
            "transmission risk has diminished post-heading.\n\n"
            "Cultural and varietal control: adopt resistant rice cultivars like CO 51 and remove collateral "
            "weed hosts (Leersia hexandra, Cyperus) along bunds and irrigation channels. Preventive "
            "management: apply neem-based insecticidal formulations (Azadirachtin) as a preventive "
            "repellant."
        ),
    },
    {
        "doc_id": "kb_p305",
        "content_type": "pest",
        "crop": "paddy",
        "title": "TNAU Gall Midge Management in Rice (Identification & Non-Chemical Control)",
        "reviewed_on": date(2026, 8, 24),
        "distinguishing_cues": (
            "Tubular 'silver shoots' or 'onion shoots' at tiller base; stunted tillers with reddish-brown pupal cases "
            "protruding from gall tips; small mosquito-like fly."
        ),
        "body": (
            "Rice gall midge (Orseolia oryzae) is an internal feeder causing severe damage primarily "
            "during the tillering stage, endemic in the Cauvery delta and coastal districts of Tamil Nadu. "
            "The maggot feeds at the growing apical tip of the tiller, causing the leaf sheath to "
            "transform into a hollow, tubular elongation resembling an onion leaf or silver shoot, "
            "rendering the tiller sterile and incapable of producing a panicle.\n\n"
            "Field identification cues: characteristic tubular 'silver shoots' or 'onion shoots' at the "
            "base of tillers; stunted tillers with galls at the base containing feeding maggots; reddish-"
            "brown pupal cases protruding from the tip of the gall tube prior to adult emergence; adult is "
            "a small, mosquito-like fly with long, slender legs and antennae.\n\n"
            "Field interventions should be initiated when scouting reaches this threshold at the "
            "vegetative (tillering) stage: 5% silver shoots or 1 adult fly per 100 net sweeps.\n\n"
            "Cultural and varietal control: grow resistant paddy cultivars such as Kavya and Surekha in "
            "endemic tracts; conduct deep summer plowing to expose and destroy overwintering pupae in "
            "stubble; avoid delayed transplanting in gall-midge-prone seasons. Biological control: "
            "conserve natural larval parasitoids such as Platygaster oryzae."
        ),
    },
    {
        "doc_id": "kb_p306",
        "content_type": "pest",
        "crop": "paddy",
        "title": "KVK Rice Nursery Management — Thrips (Identification & Non-Chemical Control)",
        "reviewed_on": date(2026, 8, 24),
        "distinguishing_cues": (
            "Minute slender dark insects (1 to 2 mm) with narrow fringed wings; yellow to orange discoloration on upper leaf surfaces; "
            "inward needle-like leaf tip curling and withered scorched appearance."
        ),
        "body": (
            "Rice thrips (Stenchaetothrips biformis) is a common nursery and early vegetative pest of "
            "paddy across Tamil Nadu, causing severe foliage rolling and seedling stunting, particularly "
            "under dry nursery conditions and moisture-stressed seedbeds. Both nymphs and adults lacerate "
            "the tender leaf surface and suck plant sap, causing the foliage margins to curl inward and "
            "wither at the edges.\n\n"
            "Field identification cues: minute, slender insects (1 to 2 mm long) with dark brown to black "
            "bodies and narrow fringed wings; yellow to orange discoloration on upper leaf surfaces turning "
            "into silvery patches; characteristic inward rolling or curling of leaf tips into needle-like "
            "shapes; withered, dried leaf tips giving seedlings a burnt or scorched appearance.\n\n"
            "Field interventions should be initiated when scouting reaches these thresholds: seedling / "
            "nursery stage — 5 thrips per seedling; vegetative (tillering) stage — 25 thrips per hill.\n\n"
            "Cultural control: submerge nursery beds periodically with water to drown and dislodge feeding "
            "thrips; avoid moisture stress in the nursery; maintain adequate standing water depth in the "
            "main field. Monitoring: set up blue sticky traps above crop canopy level to monitor thrips "
            "population surges."
        ),
    },
    {
        "doc_id": "kb_p307",
        "content_type": "pest",
        "crop": "paddy",
        "title": "TNAU Whorl Maggot Management in Rice (Identification & Non-Chemical Control)",
        "reviewed_on": date(2026, 8, 24),
        "distinguishing_cues": (
            "Yellowish-white feeding streaks and ragged, serrated margins on newly unfolding leaves; translucent whitish-yellow "
            "maggots inside unexpanded central leaf whorl."
        ),
        "body": (
            "Rice whorl maggot (Hydrellia philippina) attacks seedlings in nursery beds and newly "
            "transplanted rice up to 30 days after transplanting. The maggot enters the unexpanded central "
            "leaf whorl and feeds on the inner margin of the developing leaf; when the leaf expands, "
            "damaged portions appear as conspicuous yellowish-white streaks and ragged, serrated leaf "
            "margins.\n\n"
            "Field identification cues: white to yellowish feeding marks and ragged, broken margins on "
            "newly unfolded leaves; tiny, translucent whitish-yellow maggots inside the central leaf whorl; "
            "small greyish-black flies with smoky wings skimming over standing water surfaces in flooded "
            "fields; tiny elongated white eggs laid singly on the leaf surface close to the water level.\n\n"
            "Field interventions should be initiated when scouting reaches these thresholds: seedling / "
            "nursery stage — 1 to 2 maggots per seedling; vegetative stage — 10% damaged leaves within 30 "
            "days after transplanting.\n\n"
            "Cultural control: drain standing water from the field periodically for 2 to 3 days to expose "
            "maggots and eggs to sunlight and natural predators, and avoid continuous deep flooding during "
            "the first month after transplanting. Organic amendments: incorporate neem cake at 250 kg/ha "
            "in the nursery bed at sowing."
        ),
    },
    {
        "doc_id": "kb_p308",
        "content_type": "pest",
        "crop": "paddy",
        "title": "ICAR Rice Insect Pest Management — Earhead Bug (Identification & Non-Chemical Control)",
        "reviewed_on": date(2026, 8, 24),
        "distinguishing_cues": (
            "Slender greenish-brown bug (15-20 mm) emitting strong pungent odor; punctured, brownish-spotted, shriveled hulls "
            "and empty chaffy panicles during milking/soft-dough stage."
        ),
        "body": (
            "Rice earhead bug or gundhi bug (Leptocorisa acuta) attacks paddy specifically during the "
            "flowering, milking, and soft-dough stages of grain development. Both adults and nymphs "
            "pierce the developing milky grains and suck the liquid contents, causing grains to become "
            "partially filled, discolored, shriveled, or completely empty (chaffy); heavy infestation "
            "imparts an unpleasant odor to the field and degrades grain market quality.\n\n"
            "Field identification cues: slender, greenish-brown bug (15 to 20 mm long) with long legs and "
            "prominent antennae emitting a strong pungent odor; greenish nymphs with black and white "
            "banded legs clustered on maturing panicles; damaged grains with brownish puncture spots, "
            "shriveled hulls, or empty chaffy panicles; peak bug activity during early morning and late "
            "evening hours.\n\n"
            "Field interventions should be initiated when scouting reaches these thresholds: flowering "
            "stage — 5 bugs per 100 panicles; milking / grain-filling stage — 10 bugs per 100 panicles, "
            "equivalent to 1-2 bugs per hill in standard planting densities.\n\n"
            "Cultural control: synchronize planting across adjacent holdings to avoid staggered heading "
            "dates that sustain bug populations, and clear grassy weeds and wild grasses (Echinochloa "
            "colona, Panicum repens) from field borders. Monitoring and mechanical control: set up light "
            "traps during night hours to monitor and trap adult bugs, and use net sweeps in early morning "
            "hours."
        ),
    },
]
