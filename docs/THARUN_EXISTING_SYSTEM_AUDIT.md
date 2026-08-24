# Agricultural Research & Voice Systems: Comprehensive Audit
**Bhoomi SIH25076 Platform**
**Auditor Role:** Tharun (Agricultural Research + Voice Research)
**Audit Date:** August 2026
**Scope:** Backend API, ML Services, Domain Logic, Knowledge Repositories, Voice Processing, Vision Gate, and Testing Suites.

---

## Executive Summary

This audit establishes the baseline technical and scientific state of the Bhoomi platform across all 22 functional areas under the **Agricultural Research & Voice Research** portfolio.

The platform architecture rigorously follows hexagonal/clean architecture with clear separation between ports, domain logic, and persistence. The mathematical and deterministic frameworks (FAO-56 resource calculations, 6-index health scoring engine, confidence gating, and RAG grounding) are fully wired and backed by 248+ passing automated tests.

However, the agronomic and linguistic knowledge bases currently operate on bounded seed datasets (specifically centered on Samba Paddy and Bacterial Leaf Blight). Transitioning from a hackathon demonstration slice to a robust production system requires substantial domain research contributions: expanding the ICAR Package of Practices corpus across multiple crops, establishing crop-specific physiological calendars and $K_c$ coefficients, codifying pathogen meteorological risk models, and enriching Tamil agricultural dialect vocabularies.

---

## Detailed System Audit (22 Areas)

```
Classification Categories:
• ALREADY_IMPLEMENTED
• PARTIALLY_IMPLEMENTED
• MISSING
• NEEDS_VALIDATION
• NOT_RELEVANT_TO_MY_ROLE
```

---

### 1. RAG Ingestion Pipeline
- **File Path:** `services/api/app/services/rag/ingest.py`, `services/api/scripts/load_corpus.py`
- **What it currently does:** Idempotently parses curated document text into paragraph-aware overlapping chunks, computes dense vector embeddings using `EmbeddingPort`, and persists them into the PostgreSQL `knowledge_chunks` table with cosine HNSW indexing.
- **Data it consumes:** `CorpusDoc` list (`app.services.rag.corpus_data.CORPUS_DOCS`) or Markdown files with YAML frontmatter from `services/api/corpus/`.
- **Data it produces:** Rows in the `knowledge_chunks` table containing document ID, title, review date, chunk index, text body, and 1024-dim embedding vector.
- **Current Status:** `ALREADY_IMPLEMENTED`
- **Needs Research Contribution:** Yes. The ingestion engine is fully functional, but requires an expanded corpus of curated ICAR / TNAU documents beyond the 8 seed documents.
- **Missing Data:** Ingestion scripts for tabular agronomic data, multi-lingual documents (Tamil parallel corpus), and automated validation of frontmatter schema.
- **Validation Required:** Chunking boundary validation to ensure that dosage instructions and chemical application steps are not split across chunk windows.

---

### 2. RAG Document / Chunk Schema
- **File Path:** `services/api/app/models/knowledge_chunk.py`, `services/api/app/models/kb_document.py`
- **What it currently does:** Defines SQLAlchemy ORM entities for knowledge documents and chunks. `KnowledgeChunk` denormalizes `doc_id`, `title`, and `reviewed_on` to allow single-query citation assembly during vector retrieval.
- **Data it consumes:** Chunk text, parent document metadata (`KBDocument`), 1024-dimensional float vector.
- **Data it produces:** Database schema mapping for pgvector table with HNSW index (`m=16`, `ef_construction=64`, `vector_cosine_ops`).
- **Current Status:** `ALREADY_IMPLEMENTED`
- **Needs Research Contribution:** Yes. The schema currently lacks structured domain taxonomy fields (e.g., target crop, pathogen type, growth stage tag, agro-climatic zone).
- **Missing Data:** Metadata tagging specifications for hierarchical filtering (e.g., `crop_id`, `disease_id`, `intervention_type: chemical | cultural | biological`).
- **Validation Required:** Verification that index parameters (`m=16, ef_construction=64`) maintain sub-20ms retrieval latency as chunk count scales from 50 to 10,000+.

---

### 3. pgvector Metadata
- **File Path:** `services/api/app/models/knowledge_chunk.py`, `services/api/app/repositories/knowledge_chunk_repository.py`
- **What it currently does:** Executes approximate nearest neighbor (ANN) vector similarity searches using PostgreSQL pgvector cosine distance operator (`<=>`). Calculates relevance score as `1.0 - cosine_distance`.
- **Data it consumes:** 1024-dimensional query embedding vector, `top_k` integer, optional document ID filter.
- **Data it produces:** List of `(KnowledgeChunk, similarity_score)` tuples sorted by descending cosine similarity.
- **Current Status:** `ALREADY_IMPLEMENTED`
- **Needs Research Contribution:** Yes. Research is needed to determine whether hybrid search (combining vector distance with lexical BM25 / PostgreSQL full-text search) improves recall for technical chemical names (e.g., *Streptocycline*, *Tricyclazole*).
- **Missing Data:** Field-level metadata indices for pre-filtering retrieval by crop or geographic region.
- **Validation Required:** Cosine distance metric calibration against real BGE-M3 embeddings.

---

### 4. BGE-M3 Embedding Pipeline
- **File Path:** `services/api/app/adapters/dependencies.py`, `services/api/app/ports/embeddings.py`, `services/api/app/adapters/stubs.py`, `services/ml/app/embeddings.py`
- **What it currently does:** Defines the `EmbeddingPort` interface expecting 1024-dimensional dense vectors. In testing/stub mode, uses `StubEmbeddingAdapter` (token-level feature hashing trick with stopword filtering).
- **Data it consumes:** Query string or batch of document chunk strings.
- **Data it produces:** 1024-dimensional float vector normalized to unit length.
- **Current Status:** `PARTIALLY_IMPLEMENTED`
- **Needs Research Contribution:** Yes. `services/ml/app/embeddings.py` is currently an unpopulated stub. Tharun must evaluate real BGE-M3 performance on Tamil-English cross-lingual retrieval (matching a farmer's Tamil spoken query to an English ICAR PoP chunk).
- **Missing Data:** Deployed BGE-M3 inference pipeline / container and cross-lingual similarity evaluation benchmarks.
- **Validation Required:** Verify semantic similarity score distribution on agricultural query pairs to validate the `RAG_RELEVANCE_THRESHOLD = 0.60` threshold.

---

### 5. Source / Citation Handling
- **File Path:** `services/api/app/domain/rag/prompt.py`, `services/api/app/domain/rag/advisory.py`, `services/api/app/domain/rag/constants.py`
- **What it currently does:** Enforces strict provenance in LLM prompts. The system prompt commands the LLM to emit responses exclusively from retrieved chunks, citing `doc_id`, `title`, and `reviewed_on`. The domain parser validates that every citation in the response matches a retrieved chunk.
- **Data it consumes:** Retrieved chunk metadata dictionaries and LLM JSON output.
- **Data it produces:** Validated `AdvisoryCitation` objects or triggers `INSUFFICIENT_CONTEXT` fallback if citations are missing.
- **Current Status:** `ALREADY_IMPLEMENTED`
- **Needs Research Contribution:** Yes. Ensure real-world ICAR/TNAU publication authorities, bulletin serials, and agronomist reviewer names replace placeholder demo citations.
- **Missing Data:** Official bibliographic metadata for state agricultural university Package of Practices.
- **Validation Required:** Verification that LLM cannot hallucinate or emit phantom citations.

---

### 6. Existing Agricultural Knowledge Records
- **File Path:** `services/api/app/services/rag/corpus_data.py`, `services/api/corpus/*.md`
- **What it currently does:** Provides 8 curated seed documents:
  1. `kb_211`: *ICAR PoP: Rice — Bacterial Leaf Blight (BLB)*
  2. `kb_212`: *ICAR PoP: Rice — BLB Causal Agent & Disease Cycle*
  3. `kb_213`: *ICAR PoP: Rice — BLB Favorable Environmental Conditions*
  4. `kb_214`: *ICAR PoP: Rice — BLB Cultural Control Measures*
  5. `kb_215`: *ICAR PoP: Rice — BLB Chemical Control*
  6. `kb_216`: *ICAR PoP: Rice — BLB-Resistant Varieties*
  7. `kb_217`: *ICAR PoP: Rice — Field Drainage & Water Management*
  8. `kb_218`: *ICAR PoP: Rice — Nitrogen Management & Disease Susceptibility*
  (Additional adjacent docs in `corpus_data.py`: `kb_219`, `kb_220`, `kb_230` Blast, `kb_231` Sheath Blight, `kb_232` Brown Spot).
- **Data it consumes:** Raw text and frontmatter.
- **Data it produces:** Ingested corpus chunks.
- **Current Status:** `PARTIALLY_IMPLEMENTED`
- **Needs Research Contribution:** Yes. The current knowledge base is restricted to Rice/Paddy diseases. Tharun must research and assemble comprehensive knowledge documents for Tomato, Groundnut, Sugarcane, and Banana.
- **Missing Data:** Knowledge packs for non-paddy crops, nutrient deficiency keys, organic farming practices, and weed management.
- **Validation Required:** Agronomic validation of dosages, spray timings, and safety intervals against the TNAU Crop Production Guide.

---

### 7. Existing Pest Data
- **File Path:** `services/api/app/services/rag/corpus_data.py`, `docs/specs/early_warning_alert_spec.md`
- **What it currently does:** References pest management conceptually in architectural specifications, but contains zero dedicated insect pest records in the active corpus.
- **Data it consumes:** N/A.
- **Data it produces:** N/A.
- **Current Status:** `MISSING`
- **Needs Research Contribution:** Yes. Tharun must compile comprehensive entomological data: major insect pests (Brown Planthopper, Yellow Stem Borer, Gall Midge, Leaf Folder, Fall Armyworm), lifecycle stages, scouting methods, ETL thresholds, and integrated pest management (IPM) strategies.
- **Missing Data:** Insect pest knowledge base docs, pest diagnosis image classes, ETL values, and pheromone trap / biocontrol recommendations.
- **Validation Required:** Field threshold validation according to Directorate of Plant Protection, Quarantine & Storage (DPPQS) guidelines.

---

### 8. Existing Disease Data
- **File Path:** `services/api/app/services/rag/corpus_data.py`, `services/api/app/services/gate_service.py`
- **What it currently does:** Covers 4 rice fungal/bacterial diseases in RAG corpus (BLB, Blast, Sheath Blight, Brown Spot) and 5 strings in `SUPPORTED_DIAGNOSIS_LABELS` (`bacterial_leaf_blight`, `early_blight`, `late_blight`, `leaf_curl_virus`, `powdery_mildew`).
- **Data it consumes:** Symptom descriptions, pathogen biology, treatment protocols.
- **Data it produces:** Diagnostic classes and grounding text.
- **Current Status:** `PARTIALLY_IMPLEMENTED`
- **Needs Research Contribution:** Yes. Need full pathology profiles for horticultural crops (Tomato Early/Late Blight, Leaf Curl Virus, Powdery Mildew) and major pulse/oilseed diseases.
- **Missing Data:** Treatment protocols, chemical compatibility charts, and fungicide resistance management guidelines.
- **Validation Required:** Verification that symptom descriptions distinguish look-alike physiological disorders from biotic diseases.

---

### 9. BLB (Bacterial Leaf Blight) Data
- **File Path:** `services/api/app/services/rag/corpus_data.py` (`kb_211`–`kb_220`), `services/api/corpus/rice_blb.md`
- **What it currently does:** Provides deep coverage for *Xanthomonas oryzae pv. oryzae*: symptoms (water-soaked lesions, wavy margins, milky ooze, Kresek seedling wilt), environmental triggers (25–34°C, RH >70%), cultural controls (field drainage, AWD, withholding top-dress N, balanced K), chemical controls (Copper Oxychloride 50% WP @ 2.5 g/L, Streptocycline @ 100–200 ppm), and resistant varieties.
- **Data it consumes:** ICAR package of practices data.
- **Data it produces:** Chunks that ground BLB queries and provide diagnosis recommendations.
- **Current Status:** `ALREADY_IMPLEMENTED`
- **Needs Research Contribution:** Yes. Minor updates required: add specific TNAU released varieties (e.g., ADT 53, CO 51, CR 1009 Sub1) and bio-control protocols (*Pseudomonas fluorescens* seed & foliar treatment).
- **Missing Data:** Localized variety resistance ratings across Tamil Nadu agro-climatic zones.
- **Validation Required:** Compliance of chemical recommendations with Central Insecticide Board & Registration Committee (CIBRC).

---

### 10. Existing ETL / Threshold Data
- **File Path:** `docs/specs/early_warning_alert_spec.md`, `services/api/app/domain/health/constants.py`
- **What it currently does:** Outlines the mathematical logic for hybrid meteorological-geospatial early warning triggers (e.g., sustained $RH \ge 80\%$, $Temp \in [25^\circ C, 32^\circ C]$ for $\ge 48\text{ hours}$ combined with spatial cluster density).
- **Data it consumes:** Weather history from `WeatherPort` and spatial cluster queries from PostGIS.
- **Data it produces:** Risk alerts (`INFO`, `WARNING`, `EMERGENCY`).
- **Current Status:** `NEEDS_VALIDATION`
- **Needs Research Contribution:** Yes. Tharun must formulate the complete **Pathogen Risk Threshold Matrix** specifying the exact thermal, humidity, and rainfall incubation windows for each target disease and pest.
- **Missing Data:** Empirical threshold tables for Blast, Brown Spot, Early Blight, and insect pest degree-day models.
- **Validation Required:** Multi-year historical weather vs outbreak validation in Tamil Nadu delta districts.

---

### 11. Existing Severity Logic
- **File Path:** `services/api/app/domain/health/constants.py`, `services/api/app/domain/health/subindices.py`
- **What it currently does:** Translates discrete problem severity levels into deterministic health score deductions:
  - `ProblemSeverity.EARLY`: 30 penalty points
  - `ProblemSeverity.MODERATE`: 55 penalty points
  - `ProblemSeverity.SEVERE`: 80 penalty points
- **Data it consumes:** `OpenProblemInput(severity=...)`.
- **Data it produces:** `active_problem_load` sub-index score (`100 - sum(penalties)` clamped to `[0, 100]`).
- **Current Status:** `ALREADY_IMPLEMENTED`
- **Needs Research Contribution:** Yes. Tharun must define the standardized field evaluation rubric mapping physical crop symptoms (% leaf area infected, % tillers damaged, canopy height reduction) to `EARLY`, `MODERATE`, and `SEVERE`.
- **Missing Data:** Standard Evaluation System (SES) 1–9 scale mapping to the 3-tier severity enum.
- **Validation Required:** Agronomist agreement on severity transition thresholds.

---

### 12. Existing Crop-Stage Data
- **File Path:** `services/api/app/domain/farm_reference_data.py` (`GROWTH_STAGE_EXPECTED_DAY`), `services/api/app/domain/health/subindices.py`
- **What it currently does:** Maps growth stages to expected days-since-planting:
  - `initial`: Day 10
  - `vegetative`: Day 30
  - `mid_season`: Day 75
  - `late_season`: Day 110
  Penalizes stage deviation at `2.0` points per day difference between actual and expected schedule.
- **Data it consumes:** `days_since_planting` (integer), `growth_stage` (string).
- **Data it produces:** `crop_stage_progression` sub-index score (0–100).
- **Current Status:** `PARTIALLY_IMPLEMENTED`
- **Needs Research Contribution:** Yes. The current implementation uses a single hardcoded calendar calibrated for medium-duration Samba paddy. Tharun must provide physiological stage calendars for short-, medium-, and long-duration paddy varieties, as well as horticultural crops.
- **Missing Data:** Crop-specific calendars for Kuruvai paddy (105 days), Thaladi/Samba paddy (135–150 days), Tomato (120 days), Groundnut (105–120 days).
- **Validation Required:** Field validation across varied sowing dates and thermal time (Growing Degree Days / GDD).

---

### 13. Existing FAO-56 / Kc Inputs
- **File Path:** `services/api/app/domain/farm_reference_data.py` (`CROP_KC_TABLE`, `SEED_RATE_KG_PER_ACRE`), `services/api/app/domain/fao56.py`
- **What it currently does:** Implements the standard FAO-56 Penman-Monteith crop water calculation:
  $$\text{Net Irrigation (mm)} = \max(0, (\text{ET}_0 \times K_c) - \text{Effective Rainfall})$$
  $$\text{Total Daily Liters} = \text{Net Irrigation (mm)} \times \text{Area (acres)} \times 4046.8564$$
  Provides inspectable breakdown including 5HP pump runtime hours (at 12,000 L/hr) and seed rate calculations.
- **Data it consumes:** `crop`, `growth_stage`, `area_acres`, `et0_mm_day`, `effective_rainfall_mm`.
- **Data it produces:** `Fao56CalculateResponse` with exact formula, liter breakdown, and spoken Tamil explanation.
- **Current Status:** `PARTIALLY_IMPLEMENTED`
- **Needs Research Contribution:** Yes. `CROP_KC_TABLE` only contains Samba paddy coefficients (`initial: 1.10`, `vegetative: 1.05`, `mid_season: 1.20`, `late_season: 0.90`) with fallback `0.95`. `SEED_RATE_KG_PER_ACRE` only contains `samba_paddy: 30.0` with fallback `20.0`. Tharun must provide verified $K_c$ stages and seed rates for all supported crops.
- **Missing Data:** Stage-specific $K_c$ values for Tomato, Groundnut, Sugarcane, Banana, and direct-seeded vs transplanted rice. Soil water retention multipliers for sandy, clay loam, and red soils.
- **Validation Required:** Irrigation volume validation against local KVK and ICAR Water Technology Centre field guidelines.

---

### 14. Existing Health-Score Agricultural Inputs
- **File Path:** `services/api/app/domain/farm_reference_data.py` (`DEFAULT_CROP_IDEAL`), `services/api/app/domain/health/inputs.py`, `services/api/app/domain/health/subindices.py`
- **What it currently does:** Evaluates environmental suitability against `DEFAULT_CROP_IDEAL`:
  - `temp_min_c`: 25.0°C, `temp_max_c`: 35.0°C (penalty: 2.0 pts / °C deviation)
  - `humidity_min_pct`: 60.0%, `humidity_max_pct`: 80.0% (penalty: 1.25 pts / % deviation)
  - `soil_moisture_min_pct`: 65.0% (penalty: 2.0 pts / % deficit)
- **Data it consumes:** Live weather readings, soil moisture %, delivered irrigation, open problems, scan recency, follow-up history.
- **Data it produces:** Comprehensive 6-index health snapshot with overall score (0–100) and health band (`good`, `watch`, `poor`, `critical`).
- **Current Status:** `PARTIALLY_IMPLEMENTED`
- **Needs Research Contribution:** Yes. The ideal environmental envelope is currently global and static. Tharun must define stage-specific physiological temperature, humidity, and soil moisture envelopes per crop (e.g., rice flowering requires temp < 35°C to avoid spikelet sterility).
- **Missing Data:** Per-crop, per-stage `CropIdealConditions` reference table.
- **Validation Required:** Sensitivity analysis of penalty coefficients to avoid score over-penalization under normal diurnal fluctuations.

---

### 15. Existing Image / Vision Datasets
- **File Path:** `services/ml/app/image_model.py` (empty), `services/api/app/adapters/image_diagnosis_real.py`, `services/api/app/adapters/stubs.py`
- **What it currently does:** Real adapter routes requests to `http://ml-service/diagnose`. In stub mode, `StubImageDiagnosisAdapter` returns mock predictions with configurable confidence.
- **Data it consumes:** Image asset IDs / presigned URLs.
- **Data it produces:** `(label, confidence, metadata)`.
- **Current Status:** `MISSING`
- **Needs Research Contribution:** Yes. The ML vision inference service has no underlying dataset or weights in the repository. Tharun must curate and source labeled image datasets for Indian agricultural conditions (e.g., PlantVillage, ICAR-CRIDA, field photos) for the target crop-disease matrix.
- **Missing Data:** Curated training, validation, and benchmark test image splits with bounding boxes/class labels.
- **Validation Required:** Model accuracy, precision, recall, and calibration on field images with variable illumination and complex backgrounds.

---

### 16. Existing Image Labels and Metadata
- **File Path:** `services/api/app/services/gate_service.py` (`SUPPORTED_DIAGNOSIS_LABELS`)
- **What it currently does:** Restricts acceptable model outputs to a closed set:
  `{"bacterial_leaf_blight", "early_blight", "late_blight", "leaf_curl_virus", "powdery_mildew"}`. Any prediction outside this set is deemed out-of-scope and escalates automatically.
- **Data it consumes:** Predicted label string from vision model.
- **Data it produces:** Boolean `in_scope` flag feeding `domain.gate.decide`.
- **Current Status:** `PARTIALLY_IMPLEMENTED`
- **Needs Research Contribution:** Yes. Tharun must define the complete multi-crop diagnostic taxonomy aligning vision class labels, RAG knowledge document keys, and KVK diagnosis categories.
- **Missing Data:** Explicit crop-prefixed canonical labels (e.g., `rice__bacterial_leaf_blight`, `rice__blast`, `tomato__early_blight`, `healthy`).
- **Validation Required:** Alignment across ML class indices, API contract enums, and database problem types.

---

### 17. Existing Tamil Terminology / Normalization
- **File Path:** `services/api/app/services/intent_parser.py`, `services/api/app/services/confirmation.py`
- **What it currently does:** Provides keyword-based extraction and normalization for Tamil script and transliterated Roman text:
  - Crops (`நெல்`, `சம்பா`, `தக்காளி`, `நிலக்கடலை`, `கரும்பு`, `வாழை`)
  - Soils (`களிமண்`, `மணல்`, `செம்மண்`, `வண்டல்`, `கருப்பு மண்`)
  - Stages (`நாற்று`, `நாற்றங்கால்`, `வளர்ச்சி`, `பூக்கும்`, `கதிர்`, `முதிர்வு`, `அறுவடை`)
  - Irrigation (`கால்வாய்`, `ஆழ்குழாய்`, `ஆழ்துளை`, `கிணறு`, `மழை`)
  - Follow-up responses (`சரியாகிவிட்டது`, `மேம்பட்டது`, `மாற்றமில்லை`, `மோசமாகிவிட்டது`)
  - Tamil number words (`ஒரு` $\to 1.0$, `இரண்டு` $\to 2.0$, `அரை` $\to 0.5$, etc.)
  - Acre/Hectare conversion ($1\text{ ha} \to 2.471\text{ acres}$).
- **Data it consumes:** Spoken transcript strings from ASR.
- **Data it produces:** `ParsedIntent` objects with normalized values and Tamil read-back prompt generation strings.
- **Current Status:** `PARTIALLY_IMPLEMENTED`
- **Needs Research Contribution:** Yes. Tharun must enrich the lexicon with Tamil regional farming dialects (Kongu Tamil, Cauvery Delta Tamil, Southern TN vernacular), colloquial pest/disease names (*vengayam noi*, *surul poochi*, *manjal thevai*), and regional land measurement units (*kuzhi*, *maa*, *cent*, *kandagam*).
- **Missing Data:** Dialectal synonym dictionary and agricultural entity normalization tables.
- **Validation Required:** Field audio trial testing with native Tamil farmers across different districts.

---

### 18. Existing ASR / TTS Implementation
- **File Path:** `services/api/app/adapters/bhashini_asr.py`, `services/api/app/adapters/whisper_asr.py`, `services/api/app/adapters/gtts_adapter.py`, `services/api/app/ports/asr_tts.py`
- **What it currently does:** Implements speech recognition and synthesis with fallback hierarchy:
  - Primary: Bhashini ULCA API (`https://dhruva-api.bhashini.gov.in/services/inference/pipeline`)
  - Fallback: OpenAI Whisper API (`https://api.openai.com/v1/audio/transcriptions`)
  - Local/Testing: `StubAsrTtsAdapter` returning context-specific Tamil transcripts.
- **Data it consumes:** Audio asset URI / audio binary data, Bhashini credentials.
- **Data it produces:** `(transcription_text, confidence_score)`, `(audio_asset_id, audio_url)`.
- **Current Status:** `ALREADY_IMPLEMENTED`
- **Needs Research Contribution:** Yes. Benchmark Word Error Rate (WER) and Character Error Rate (CER) on noisy rural field audio recordings (wind, water pump noise, tractor engine background).
- **Missing Data:** Audio benchmark test dataset in rural acoustic environments.
- **Validation Required:** End-to-end latency and recognition accuracy on domain-specific agricultural vocabulary.

---

### 19. Existing Voice Onboarding Flow
- **File Path:** `services/api/app/api/v1/voice.py`, `services/api/app/services/voice_service.py`, `services/api/app/services/confirmation.py`, `apps/farmer_app/lib/features/onboarding/`
- **What it currently does:** Coordinates spoken onboarding dialog. Transcribes input $\to$ parses structured fields $\to$ evaluates if confirmation is required $\to$ generates spoken Tamil read-back confirmation for consequential numeric fields (land area, crop type, growth stage) before committing to database.
- **Data it consumes:** Voice audio recordings from Flutter client.
- **Data it produces:** `VoiceTranscribeResponse` with parsed intents and `readback_text` (`"நீங்கள் சொன்னது 2 ஏக்கர் நிலம், சரிதானா?"`).
- **Current Status:** `ALREADY_IMPLEMENTED`
- **Needs Research Contribution:** Yes. Design conversational error recovery prompts and clarification flows when the farmer's response is ambiguous or outside known vocabulary.
- **Missing Data:** Multi-turn conversational fallback trees in Tamil.
- **Validation Required:** Usability trials with semi-literate farmer focus groups.

---

### 20. Existing RAG Evaluation Tests
- **File Path:** `services/api/tests/rag/test_advisory_service.py`, `services/api/tests/rag/test_ingest.py`, `services/api/tests/domain/test_rag_prompt.py`, `services/api/tests/domain/test_rag_chunking.py`, `services/api/tests/domain/test_rag_similarity.py`
- **What it currently does:** Comprehensive test suite validating:
  - Ingestion and chunk generation idempotency
  - Token-level hashing and cosine similarity computation
  - Strict 5-point prompt assembly and negative constraints
  - Fallback to `insufficient_context` on low relevance scores
  - Citation parsing and validation
- **Data it consumes:** Synthetic query strings, mock and pgvector repositories.
- **Data it produces:** Test assertions passing across all suites.
- **Current Status:** `ALREADY_IMPLEMENTED`
- **Needs Research Contribution:** Yes. Tharun must create a **Golden Agricultural Q&A Benchmark Dataset** (100+ real farmer questions with ground truth ICAR citations and expected 5-point advisories) for formal RAG Triad benchmarking.
- **Missing Data:** Golden evaluation query-document pairs across all target crops.
- **Validation Required:** Empirical verification of `RAG_RELEVANCE_THRESHOLD = 0.60` against real BGE-M3 embeddings.

---

### 21. Existing Voice / ASR Tests
- **File Path:** `services/api/tests/unit/test_voice.py`
- **What it currently does:** Tests ASR transcription handling, intent parsing across contexts (`onboarding`, `diagnosis`, `followup`), numeric land area extraction, Tamil number word conversion, and verbal read-back confirmation prompt generation.
- **Data it consumes:** Synthetic transcription strings and context flags.
- **Data it produces:** Unit test verification results.
- **Current Status:** `ALREADY_IMPLEMENTED`
- **Needs Research Contribution:** Yes. Supply real-world transcript test vectors including code-switching (Tamil + English words like *"2 acres paddy potturukken"*), phonetic misspellings from ASR outputs, and fractional land units.
- **Missing Data:** Test fixtures for noisy/imperfect speech transcripts.
- **Validation Required:** Robustness of `IntentParser` against unexpected punctuation and filler words.

---

### 22. Existing Vision Tests
- **File Path:** `services/api/tests/rag/test_diagnosis_service.py`, `services/api/tests/domain/test_gate.py`
- **What it currently does:** Tests the confidence gate orchestration:
  - Confidence $\ge 0.70$ and in-scope $\to$ `ADVISE`
  - Confidence $< 0.70$ $\to$ `ESCALATE_DIAGNOSIS_CONFIDENCE`
  - Out-of-scope label $\to$ `ESCALATE_UNSUPPORTED_CROP`
  - Low retrieval relevance $\to$ `ESCALATE_NO_RELEVANT_KNOWLEDGE`
- **Data it consumes:** Mock diagnosis adapter with settable confidence and labels.
- **Data it produces:** Unit and integration test assertions.
- **Current Status:** `ALREADY_IMPLEMENTED`
- **Needs Research Contribution:** Yes. When real vision models are trained, Tharun must provide test image suites representing true field conditions (under-exposed, motion-blurred, multiple co-occurring diseases) to evaluate calibration and false positive rates.
- **Missing Data:** Physical image fixture files for end-to-end vision model evaluation.
- **Validation Required:** Calibration curve validation to confirm model confidence matches true posterior probability.

---

## Summary Matrix

| # | Item | Current Status | Tharun's Research Required? |
|---|---|---|---|
| 1 | RAG Ingestion Pipeline | `ALREADY_IMPLEMENTED` | Yes (Provide full corpus) |
| 2 | RAG Document/Chunk Schema | `ALREADY_IMPLEMENTED` | Yes (Define taxonomy metadata) |
| 3 | pgvector Metadata | `ALREADY_IMPLEMENTED` | Yes (Metadata filtering specifications) |
| 4 | BGE-M3 Embedding Pipeline | `PARTIALLY_IMPLEMENTED` | Yes (Cross-lingual benchmark & weights) |
| 5 | Source / Citation Handling | `ALREADY_IMPLEMENTED` | Yes (Real ICAR bibliographic data) |
| 6 | Existing Agricultural Knowledge Records | `PARTIALLY_IMPLEMENTED` | Yes (Expand to 5 crops & pests) |
| 7 | Existing Pest Data | `MISSING` | Yes (Complete pest & IPM catalog) |
| 8 | Existing Disease Data | `PARTIALLY_IMPLEMENTED` | Yes (Expand non-paddy disease profiles) |
| 9 | BLB (Bacterial Leaf Blight) Data | `ALREADY_IMPLEMENTED` | Yes (TNAU releases & biocontrol updates) |
| 10 | Existing ETL / Threshold Data | `NEEDS_VALIDATION` | Yes (Pathogen risk threshold matrix) |
| 11 | Existing Severity Logic | `ALREADY_IMPLEMENTED` | Yes (SES visual scoring rubric) |
| 12 | Existing Crop-Stage Data | `PARTIALLY_IMPLEMENTED` | Yes (Crop calendars by duration) |
| 13 | Existing FAO-56 / Kc Inputs | `PARTIALLY_IMPLEMENTED` | Yes (Complete Kc tables & soil factors) |
| 14 | Existing Health-Score Agronomic Inputs | `PARTIALLY_IMPLEMENTED` | Yes (Stage-specific environmental envelopes) |
| 15 | Existing Image / Vision Datasets | `MISSING` | Yes (Curate labeled Indian farm images) |
| 16 | Existing Image Labels and Metadata | `PARTIALLY_IMPLEMENTED` | Yes (Canonical crop-pathogen taxonomy) |
| 17 | Existing Tamil Terminology / Normalization | `PARTIALLY_IMPLEMENTED` | Yes (Dialectal lexicons & local units) |
| 18 | Existing ASR / TTS Implementation | `ALREADY_IMPLEMENTED` | Yes (Field WER/CER evaluation) |
| 19 | Existing Voice Onboarding Flow | `ALREADY_IMPLEMENTED` | Yes (Conversational error dialogs) |
| 20 | Existing RAG Evaluation Tests | `ALREADY_IMPLEMENTED` | Yes (100+ Golden Q&A evaluation set) |
| 21 | Existing Voice / ASR Tests | `ALREADY_IMPLEMENTED` | Yes (Tanglish & noisy transcript fixtures) |
| 22 | Existing Vision Tests | `ALREADY_IMPLEMENTED` | Yes (Field test image fixture sets) |
