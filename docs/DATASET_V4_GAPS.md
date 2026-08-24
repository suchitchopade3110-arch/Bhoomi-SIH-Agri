# BHOOMI Dataset v4: Comprehensive Gap Analysis
**Document ID:** GAP-DATASET-V4-001  
**Auditor:** Tharun (Agricultural Research + Voice Research Lead)  
**Date:** August 2026  
**Target:** Pre-Ingestion Quality Assurance & Research Roadmap

---

## 1. Gap Summary Table

| Component | Dataset v4 Status | Existing BHOOMI Support | Gap | Priority | Recommended Action |
|---|---|---|---|---|---|
| **Pest Knowledge Prose Formatting** | Structured JSON with management summaries | RAG chunker expects continuous paragraph markdown | Raw JSON not formatted into prose with frontmatter | **P0** | Transform JSON into 8 Markdown documents with YAML metadata for ingestion. |
| **Pest Severity Numerical Cutoffs** | 3-tier framework defined; records state `MISSING` | Severity penalty system (-30, -55, -80) implemented | Discrete visual damage & population cutoffs unassigned | **P0** | Quantify SES damage % and count thresholds for Early, Moderate, and Severe tiers. |
| **Tamil Pest Terminology & Normalization** | English text only | `IntentParser` and confirmation service ready | Tamil pest names, dialect terms, and symptoms missing | **P0** | Build Tamil keyword dictionaries for all 8 pests with spoken phonetic variants. |
| **Chemical Advice Label Validation** | Source-quoted chemicals (e.g. Carbofuran 3G) | Advisory service citations enforce strict grounding | Historical vs current 2026 CIBRC registration status unverified | **P0** | Audit all active ingredients against current CIBRC banned/restricted pesticide lists. |
| **Vision Gate Whitelist Alignment** | 8 pest classes defined in manifest | Gate whitelist restricted to 5 diseases | Pests rejected as out-of-scope by confidence gate | **P0** | Add the 8 pest label keys to `SUPPORTED_DIAGNOSIS_LABELS` in `gate_service.py`. |
| **Structured Numerical ETL Rules** | Text strings in `threshold.raw` | Early Warning Alert specification drafted | Outbreak weather incubation rules ($RH \ge 85\%$, Temp) absent | **P1** | Formulate quantitative ETL data structures and meteorological outbreak rules. |
| **Vision Training Dataset & Model Weights** | 17 reference images across 7 pests (Whorl maggot: 0) | Real image adapter expects hosted ML service | Small sample size, low resolution, unverified license, no splits | **P1** | Retain as reference images for KVK portal; source 500+ field images/class for ML training. |
| **Growth Stage Canonical Mapping** | Text growth stage descriptions | GrowthStage enum (`seedling`, `vegetative`, etc.) | Unstandardized strings not mapped to canonical enum | **P1** | Create mapping table connecting pest vulnerability phrases to canonical growth stages. |
| **Source Publication Dates** | Flagged as `"NOT EXPOSED IN SOURCE"` | `reviewed_on` date supported | Original publication year/month not traceable to static PDF | **P1** | Attempt deep archival lookup for original bulletin dates or maintain explicit unexposed flag. |
| **Non-Rice Crop & Disease Coverage** | Zero non-rice pests; zero disease records | Disease RAG corpus for Rice BLB/Blast/Brown Spot | No entomology or pathology data for Tomato, Groundnut, Sugarcane | **P0** | Expand Dataset v5 to cover major horticultural and commercial crop pests/diseases. |

---

## 2. Detailed Gap Specifications

---

### Gap 1: Unformatted Prose & Ingestion Impediment
- **What is missing:** Markdown text files (`.md`) with standard YAML frontmatter for the 8 insect pests. Dataset v4 stores pest knowledge as structured JSON keys (`identification_cues`, `threshold.raw`, `management.raw_summary`).
- **Why it matters:** Bhoomi's RAG chunking algorithm (`app.domain.rag.chunking.chunk_text`) operates on prose paragraphs separated by `\n\n`. Passing raw JSON leads to fragmented chunks and awkward LLM grounding prompts.
- **Blocks RAG:** **YES** (Direct ingestion blocked until prose transformation is completed).
- **Blocks Vision:** No.
- **Blocks Voice:** No.
- **Priority:** **P0**
- **What Tharun must provide:** Formatted Markdown files in `services/api/corpus/` (e.g., `rice_stem_borer.md`, `rice_bph.md`, `rice_leaf_folder.md`, etc.) with `doc_id`, `title`, `source`, `reviewed_on`, and structured subheadings.

---

### Gap 2: Unquantified Severity Cutoffs per Pest
- **What is missing:** Specific numerical boundaries (e.g., % dead hearts, nymphs per hill, % leaf area folded) defining when a pest infestation is `EARLY`, `MODERATE`, or `SEVERE`. `pest_records.json` explicitly states: `severity: { tier: null, criteria: null, status: "MISSING" }`.
- **Why it matters:** Bhoomi's transparent health scoring engine relies on `active_problem_load` which deducts -30 (Early), -55 (Moderate), or -80 (Severe). Without objective criteria, agronomists and AI cannot calibrate score movement.
- **Blocks RAG:** No.
- **Blocks Vision:** No (Vision outputs class label and confidence; severity is assessed via symptoms).
- **Blocks Voice:** No.
- **Priority:** **P0**
- **What Tharun must provide:** Standard Evaluation System (SES) mapping for each of the 8 pests:
  - *Stem borer*: Early (<5% dead hearts), Moderate (5–10%), Severe (>10% dead hearts or >5% white ears).
  - *BPH*: Early (<5 nymphs/hill), Moderate (5–10 nymphs/hill), Severe (>10 nymphs/hill or hopper burn patches).
  - *Leaf folder*: Early (<5% folded leaves), Moderate (5–10%), Severe (>10% folded leaves).

---

### Gap 3: Missing Tamil Nomenclature & Spoken Variants
- **What is missing:** Unicode Tamil and transliterated Roman keywords for the 8 insect pests and their diagnostic field symptoms.
- **Why it matters:** Bhoomi is a voice-first platform for Tamil farmers. If a farmer says *"தண்டு துளைப்பான் தாக்கியுள்ளது"* (Stem borer has attacked) or *"இலையில சுருட்டு புழு இருக்கு"* (Leaf folder is present), `IntentParser` currently fails to extract the problem entity.
- **Blocks RAG:** No (RAG query can be English-translated or dense embedded).
- **Blocks Vision:** No.
- **Blocks Voice:** **YES** (Blocks voice query intent extraction and Tamil read-back confirmation).
- **Priority:** **P0**
- **What Tharun must provide:** Tamil keyword mapping dictionary for `app/services/intent_parser.py`:
  - Stem borer: `தண்டு துளைப்பான்`, `குருத்து பூச்சி`, `dead heart`, `வெண்கதிர்`
  - BPH: `புகையான்`, `பழுப்பு தத்துப்பூச்சி`, `hopper burn`, `சாறு உறிஞ்சும் பூச்சி`
  - Leaf folder: `இலை சுருட்டு புழு`, `சுருட்டு புழு`, `பச்சை புழு`
  - Gall midge: `ஆணைக்கொம்பன்`, `வெள்ளிக்குருத்து`, `silver shoot`
  - Green leafhopper: `பச்சை தத்துப்பூச்சி`, `துங்ரோ பூச்சி`
  - Thrips: `இலைப்பேன்`, `சுருள் பேன்`
  - Whorl maggot: `குருத்து ஈ`, `இலை ஈ`
  - Earhead bug: `கதிர் நாவாய்ப்பூச்சி`, `சாறு பூச்சி`

---

### Gap 4: Chemical Advice Regulatory & Label Claim Validation
- **What is missing:** Statutory review of recommended chemical treatments against the 2026 Central Insecticide Board and Registration Committee (CIBRC) approved list.
- **Why it matters:** Dataset v4 includes recommendations such as *Carbofuran 3G @ 33 kg/ha* (Stem borer / Gall midge / Whorl maggot) and *Malathion 50 EC* (Earhead bug). Carbofuran and certain synthetic insecticides face bans or strict restrictions under Indian pesticide safety regulations. Recommending banned chemicals violates Bhoomi's core safety mandate.
- **Blocks RAG:** **YES** (Safety risk to release unvalidated chemical prescriptions).
- **Blocks Vision:** No.
- **Blocks Voice:** No.
- **Priority:** **P0**
- **What Tharun must provide:** Regulatory audit table certifying active ingredients, label dosages, waiting periods (Pre-Harvest Interval / PHI), and approved biological/green-chemistry alternatives (e.g. *Chlorantraniliprole 18.5 SC*, *Flubendiamide 39.35 SC*, *Azadirachtin 10,000 ppm*, *Trichogramma japonicum* egg parasitoids).

---

### Gap 5: Confidence Gate Whitelist Mismatch
- **What is missing:** The 8 pest label identifiers are missing from `SUPPORTED_DIAGNOSIS_LABELS` in `services/api/app/services/gate_service.py`.
- **Why it matters:** The confidence gate currently only permits:
  `{"bacterial_leaf_blight", "early_blight", "late_blight", "leaf_curl_virus", "powdery_mildew"}`. Any vision prediction predicting a pest (e.g., `stem_borer`) will be classified as `out_of_scope` and trigger `ESCALATE_UNSUPPORTED_CROP` regardless of confidence.
- **Blocks RAG:** No.
- **Blocks Vision:** **YES** (Directly blocks vision diagnosis routing for pests).
- **Blocks Voice:** No.
- **Priority:** **P0**
- **What Tharun must provide:** Standardized lowercase enum string list for pest labels: `["paddy__stem_borer", "paddy__brown_planthopper", "paddy__leaf_folder", "paddy__green_leafhopper", "paddy__gall_midge", "paddy__thrips", "paddy__whorl_maggot", "paddy__earhead_bug"]`.

---

### Gap 6: Structured ETL & Meteorological Outbreak Models
- **What is missing:** Machine-readable numerical ETL threshold parameters and multi-day meteorological incubation conditions for pest outbreaks.
- **Why it matters:** The SIH26131 Early-Warning Alert System (`early_warning_alert_spec.md`) requires quantitative triggers (e.g., 48-hour temperature/humidity windows and spatial case cluster thresholds) to generate proactive alerts before visual damage occurs.
- **Blocks RAG:** No.
- **Blocks Vision:** No.
- **Blocks Voice:** No.
- **Priority:** **P1**
- **What Tharun must provide:** Pathogen and pest risk threshold matrix matching pest biology with weather parameters (e.g., BPH favors $Temp \in [28^\circ\text{C}, 32^\circ\text{C}]$, $RH > 80\%$, continuous waterlogging; Gall midge favors high rainfall and cloudiness during tillering).

---

### Gap 7: Image Dataset Volume, Quality & License Status
- **What is missing:** High-resolution field training images with expert annotations, train/val/test splits, and confirmed redistribution licenses. Dataset v4 has 17 images across 7 classes (Whorl maggot has 0 images), small thumbnail resolutions (e.g. 79x103 px), and unverified license status.
- **Why it matters:** 17 thumbnail images are insufficient to train or fine-tune a robust Vision Transformer (ViT) or CNN classifier.
- **Blocks RAG:** No.
- **Blocks Vision:** **YES** (Blocks training a real production vision model; does NOT block using images as reference thumbnails in KVK agronomist portal).
- **Blocks Voice:** No.
- **Priority:** **P1**
- **What Tharun must provide:** Sourcing plan for at least 500 field-captured images per class with varied lighting and leaf damage stages, alongside rights verification from TNAU / ICAR.

---

### Gap 8: Growth Stage Canonical Standardization
- **What is missing:** Mapping between free-text descriptions in `pest_records.json` (e.g., *"All stages; dead heart in vegetative, white earhead in reproductive"*) and Bhoomi's canonical `GrowthStage` enum values (`seedling`, `vegetative`, `reproductive`, `ripening`).
- **Why it matters:** Resource planning and health score calculations filter recommendations by active crop growth stage.
- **Blocks RAG:** No.
- **Blocks Vision:** No.
- **Blocks Voice:** No.
- **Priority:** **P1**
- **What Tharun must provide:** Discrete stage vulnerability mapping array:
  `{"stem_borer": ["vegetative", "reproductive"], "bph": ["vegetative", "reproductive"], "thrips": ["seedling", "vegetative"], "earhead_bug": ["reproductive", "ripening"]}`.

---

### Gap 9: Traceable Publication Dates for Web-Sourced Bulletins
- **What is missing:** Explicit publication years for TNAU Agritech portal pages, which are dynamically updated web guides without printed publication dates (`"publication_date_status": "not_exposed"`).
- **Why it matters:** Bhoomi requires citations to carry a `reviewed_on` date to prevent stale agronomic advice.
- **Blocks RAG:** No (`last_reviewed: 2026-08-24` satisfies the database constraint).
- **Blocks Vision:** No.
- **Blocks Voice:** No.
- **Priority:** **P1**
- **What Tharun must provide:** Formal review sign-off date establishing the 6-month review cycle (`review_due: 2027-02-24`).

---

### Gap 10: Non-Rice Crop & Disease Domain Coverage
- **What is missing:** Entomology and plant pathology records for non-paddy crops (Tomato, Groundnut, Sugarcane, Banana). Dataset v4 is exclusively focused on Rice Pests.
- **Why it matters:** Bhoomi's target scope encompasses 5 major Tamil Nadu cropping systems. Queries for Tomato Early Blight or Groundnut Tikka Leaf Spot currently return no relevant sources.
- **Blocks RAG:** **YES** (for non-rice queries).
- **Blocks Vision:** **YES** (for non-rice crops).
- **Blocks Voice:** No.
- **Priority:** **P0**
- **What Tharun must provide:** Formulation of Dataset v5 expanding knowledge coverage to Tomato, Groundnut, Sugarcane, and Banana.
