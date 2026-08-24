# BHOOMI Dataset v4 to Existing System Mapping
**Document ID:** MAP-DATASET-V4-001  
**Dataset Location:** `data/external/Dataset_v4/`  
**Auditor:** Tharun (Agricultural Research + Voice Research Lead)  
**Date:** August 2026  
**Scope:** Structural, data model, and functional mapping of BHOOMI Dataset v4 against existing Bhoomi backend, ML, RAG, vision, and voice architecture.

---

## 1. Dataset v4 Inventory & Structure Overview

Dataset v4 is located at `data/external/Dataset_v4/` and comprises **28 total files** structured as follows:

```
data/external/Dataset_v4/
├── DATASET_CONTENTS.md               # Overview and file directory
├── IMAGE_DATASET_README.md           # Image provenance & rights note
├── SHA256SUMS.json                   # Cryptographic checksums (28 items)
├── image_manifest.csv                # Metadata for 17 images across 7 pests
├── pest_corpus_collection_plan.csv   # Target document collection plan
├── pest_records.csv                  # Tabular export of 8 pest records
├── pest_records.json                 # Structured JSON of 8 pest entities
├── severity_framework.json           # 3-tier severity framework definition
├── source_snapshot.json              # Dataset identity + 8 canonical docs
├── validation_roadmap.csv            # 13 prioritized validation tasks
├── vision_label_schema.json          # Vision annotation schema
└── images/                           # 8 pest folders (17 image files)
    ├── brown_planthopper/            # 3 images (adult, nymph, hopper burn)
    ├── earhead_bug/                  # 2 images (adult, field earhead bug)
    ├── gall_midge/                   # 2 images (adult fly, maggot)
    ├── green_leafhopper/             # 2 images (detail, symptom)
    ├── leaf_folder/                  # 3 images (adult, larva, scorched field)
    ├── stem_borer/                   # 3 images (dead heart, egg mass, adult)
    ├── thrips/                       # 2 images (nymph, adult PNG)
    └── whorl_maggot/                 # 0 images (directory exists, empty)
```

---

## 2. Component-by-Component Mapping Against Bhoomi Codebase

```
Classification Categories:
• READY: Compatible as-is or directly mappable with standard transformation
• NEEDS_METADATA: Content exists but lacks required Bhoomi schema fields/tags
• NEEDS_VALIDATION: Content present but requires agronomic / regulatory validation
• NEEDS_RESEARCH: Architectural framework present, but domain data must be researched
• INCOMPATIBLE: Structure or format cannot be consumed by current runtime systems
```

---

### A. RAG Ingestion Pipeline & Chunking

| Dataset v4 Component | Existing Bhoomi Target | Mapping Analysis | Classification |
|---|---|---|---|
| `source_snapshot.json` (`pest_corpus.records`) | `services/api/app/services/rag/ingest.py` & `corpus_data.py` | Dataset v4 provides 8 structured pest documents (`DOC-PEST-001` to `DOC-PEST-008`). Bhoomi's ingestion pipeline expects continuous prose (`CorpusDoc.body`) with markdown paragraph breaks (`\n\n`) for its greedy 600-char chunker (`app.domain.rag.chunking.chunk_text`). | `NEEDS_METADATA` |
| `pest_records.json` (`identification_cues`, `management.raw_summary`) | `services/api/app/domain/rag/chunking.py` | JSON arrays of distinguishing cues and raw summaries must be rendered into markdown sections (`## Identification`, `## Symptoms`, `## Management`, `## ETL`) before chunking. | `NEEDS_METADATA` |

---

### B. Database Schema & Vector Storage

| Dataset v4 Component | Existing Bhoomi Target | Mapping Analysis | Classification |
|---|---|---|---|
| `source_snapshot.json` (`document_id`, `title`, `last_reviewed`) | `app.models.kb_document.KBDocument` & `app.models.knowledge_chunk.KnowledgeChunk` | Schema fields match 1-to-1: `document_id` $\to$ `doc_id`, `title` $\to$ `title`, `last_reviewed` (`2026-08-24`) $\to$ `reviewed_on`. | `READY` |
| Dense Vector Space | `pgvector` HNSW (`KnowledgeChunk.embedding`, 1024 dimensions) | Text from Dataset v4 will generate 1024-dim vectors via `EmbeddingPort` matching existing schema and HNSW cosine index (`m=16, ef_construction=64`). | `READY` |

---

### C. Citation & Provenance Handling

| Dataset v4 Component | Existing Bhoomi Target | Mapping Analysis | Classification |
|---|---|---|---|
| `source_snapshot.json` (`citation`, `source_url`, `authority_level`, `organization`) | `app.domain.rag.prompt.build_grounding_prompt` & `app.domain.rag.advisory.AdvisoryCitation` | Dataset v4 contains complete provenance tracking (TNAU, ICAR-IRRI, ICAR-IIRR, KVK). Publication dates are marked `"NOT EXPOSED IN SOURCE"`, but `last_reviewed: 2026-08-24` satisfies Bhoomi's `reviewed_on` constraint. | `READY` |

---

### D. Pest & Disease Knowledge Data

| Dataset v4 Component | Existing Bhoomi Target | Mapping Analysis | Classification |
|---|---|---|---|
| 8 Rice Insect Pests (`Stem borer`, `BPH`, `Leaf folder`, `GLH`, `Gall midge`, `Thrips`, `Whorl maggot`, `Earhead bug`) | `services/api/corpus/` & `services/api/app/services/rag/corpus_data.py` | **Major Addition**: Fills the entire missing insect pest void in Bhoomi (which previously had only fungal/bacterial diseases). Covers all major rice entomological threats in Tamil Nadu. | `NEEDS_VALIDATION` |
| Disease Data | `services/api/corpus/` (BLB, Blast, Brown Spot) | Dataset v4 contains metadata counters for diseases (`core_disease_classes: 3`) but 0 disease records in `pest_records.json`. Existing Bhoomi disease corpus remains the sole source for diseases. | `NEEDS_RESEARCH` (for non-rice diseases) |
| BLB (Bacterial Leaf Blight) | `services/api/corpus/rice_blb.md` | Dataset v4 has 0 BLB records (strictly insect pests). Existing Bhoomi BLB implementation (`kb_211`–`kb_220`) is retained. | `READY` (in existing codebase) |

---

### E. Severity & Health Scoring Engine

| Dataset v4 Component | Existing Bhoomi Target | Mapping Analysis | Classification |
|---|---|---|---|
| `severity_framework.json` | `app.domain.health.constants.SEVERITY_PENALTY` (`EARLY`: 30, `MODERATE`: 55, `SEVERE`: 80) | Dataset v4 formalizes 3 tiers (`early`, `moderate`, `severe_spreading`) matching Bhoomi's 3-tier severity enum. However, pest records state `severity: { tier: null, status: "MISSING" }` and `numeric_cutoff: "Do not invent"`. | `NEEDS_RESEARCH` |
| `active_problem_load` Sub-Index | `app.domain.health.subindices.active_problem_load` | Once pest severity criteria are quantified, pest diagnoses can directly deduct from Sub-index #4 without modifying scoring logic. | `READY` (Logic ready, needs pest criteria) |

---

### F. ETL & Outbreak Alert Systems

| Dataset v4 Component | Existing Bhoomi Target | Mapping Analysis | Classification |
|---|---|---|---|
| `pest_records.json` (`threshold.raw`) | `docs/specs/early_warning_alert_spec.md` (Hybrid Outbreak Trigger) | Dataset v4 captures official source-quoted ETLs (e.g., BPH: *5–10 nymphs/hill in vegetative*; Stem Borer: *10% dead hearts*). These are currently unparsed text strings and lack meteorological incubation rules ($RH \ge 85\%$, Temp bands). | `NEEDS_VALIDATION` |

---

### G. Crop-Stage & Resource Planning (FAO-56)

| Dataset v4 Component | Existing Bhoomi Target | Mapping Analysis | Classification |
|---|---|---|---|
| `growth_stage` text in pest records | `app.domain.health.subindices.crop_stage_progression` & `app.core.enums.GrowthStage` | Dataset v4 describes stage vulnerability (e.g. *Nursery and early vegetative*, *Flowering to grain filling*). Requires mapping to canonical Bhoomi stage enums (`seedling`, `vegetative`, `reproductive`, `ripening`). | `NEEDS_METADATA` |
| FAO-56 $K_c$ & Seed Rates | `app.domain.farm_reference_data.py` & `app.domain.fao56.py` | Dataset v4 contains 0 FAO-56 / $K_c$ tables or water requirement data (entomology focus only). | `NEEDS_RESEARCH` |

---

### H. Vision & Image Diagnosis Pipeline

| Dataset v4 Component | Existing Bhoomi Target | Mapping Analysis | Classification |
|---|---|---|---|
| 17 Reference Images in `images/` | `services/ml/app/image_model.py` & `app.adapters.image_diagnosis_real.py` | 17 images across 7 pests (Stem borer: 3, BPH: 3, Leaf folder: 3, GLH: 2, Gall midge: 2, Thrips: 2, Earhead bug: 2, Whorl maggot: 0). Resolutions range from 79x103 to 283x264. | `NEEDS_METADATA` / `INCOMPATIBLE` (Reference only) |
| `image_manifest.csv` | `services/ml/` (Dataset splits & training) | Manifest contains SHA-256 hashes, source URLs, dimensions, and label types (`adult`, `nymph`, `damage_symptom`, `hopper_burn`, `dead_heart`). Fields `expert_verified: false` and `dataset_split: unassigned` prevent direct ML training. | `NEEDS_VALIDATION` |
| `vision_label_schema.json` | `app.services.gate_service.SUPPORTED_DIAGNOSIS_LABELS` | Current Bhoomi vision gate only supports 5 disease labels (`bacterial_leaf_blight`, `early_blight`, `late_blight`, `leaf_curl_virus`, `powdery_mildew`). Adding the 8 pests requires expanding the gate's whitelist. | `NEEDS_METADATA` |

---

### I. Voice, ASR & Tamil Normalization

| Dataset v4 Component | Existing Bhoomi Target | Mapping Analysis | Classification |
|---|---|---|---|
| Pest Names & Symptoms | `app.services.intent_parser.py` & `app.services.confirmation.py` | Dataset v4 is English-only. Lacks Tamil pest names (e.g., Stem Borer $\to$ தண்டு துளைப்பான், BPH $\to$ புகையான், Leaf folder $\to$ இலை சுருட்டு புழு, Gall midge $\to$ ஆணைக்கொம்பன், Thrips $\to$ இலைப்பேன், Earhead bug $\to$ கதிர் நாவாய்ப்பூச்சி). | `NEEDS_RESEARCH` |
| Spoken Read-Back Templates | `app.services.confirmation.ConfirmationService` | Read-back templates for confirmed pest diagnosis need Tamil translations before voice playback. | `NEEDS_RESEARCH` |

---

## 3. Summary Mapping Table

| Component | Dataset v4 Status | Existing BHOOMI Support | Gap | Priority | Recommended Action |
|---|---|---|---|---|---|
| **Pest Knowledge (RAG)** | 8 structured records with ETL & management | Ingestion pipeline, pgvector, citation parser ready | Structured JSON not converted to Markdown prose | **P0** | Compile 8 Markdown documents with YAML frontmatter and ingest into `knowledge_chunks`. |
| **Pest Citations** | Complete source metadata (TNAU, IRRI, ICAR) | Strict 5-point citation contract supported | Publication date not exposed in web sources | **P1** | Retain `last_reviewed: 2026-08-24` and mark publication date as unexposed. |
| **Pest Severity Cutoffs** | 3-tier framework defined; records missing cutoffs | Severity penalties (-30, -55, -80) implemented | Exact field population cutoffs not quantified per pest | **P0** | Define SES damage percentage and population cutoffs for each of the 8 pests. |
| **ETL Thresholds** | Text ETL strings present for all 8 pests | Early warning alert spec ready | ETLs not parsed into structured numerical triggers | **P1** | Extract numeric ETL thresholds and combine with weather incubation rules. |
| **Reference Images** | 17 images across 7 pests with manifest & hashes | Vision gate and image adapter wired | Low sample size, no splits, unverified license | **P1** | Treat as reference fixtures for KVK portal verification; expand dataset for ML training. |
| **Vision Gate Labels** | 8 pest classes defined in manifest | Gate whitelist restricted to 5 diseases | Pests not included in `SUPPORTED_DIAGNOSIS_LABELS` | **P0** | Update gate enum and whitelist with the 8 canonical pest labels. |
| **Tamil Pest Lexicon** | English names only in records | `IntentParser` keyword matching ready | Tamil names, synonyms, and dialect terms missing | **P0** | Add Tamil pest keywords and symptoms to `_CROP_KEYWORDS` / `_PEST_KEYWORDS`. |
| **Disease Data** | 0 disease records (entomology focus) | 8 ICAR disease documents in production | Non-rice diseases (Tomato, Groundnut) missing | **P0** | Research and add Tomato and Groundnut disease profiles in separate package. |
| **FAO-56 / $K_c$** | Not present in Dataset v4 | FAO-56 calculation engine fully functional | Multi-crop $K_c$ coefficients missing | **P1** | Research and supply $K_c$ tables for non-paddy crops. |
| **Validation Status** | All records flagged `validation_required` | Strict no-fabrication architecture enforced | Chemical advice not validated against CIBRC 2026 | **P0** | Validate chemical dosages against CIBRC and TNAU 2025–2026 guide before RAG release. |
