# BHOOMI Dataset v4 Curated Working Staging Report
**Location:** `data/curated/Dataset_v4_validated/`  
**Status:** `STAGING_CURATED — NOT_PRODUCTION_READY`  
**Curator:** Tharun BL (Agricultural Research + Voice Research Lead)  
**Date:** August 2026

---

## 1. Executive Summary & Working Directory Structure

The curated working directory `data/curated/Dataset_v4_validated/` has been prepared using `data/external/Dataset_v4/` as the baseline ground-of-truth.

```
data/curated/Dataset_v4_validated/
├── CORPUS_MANIFEST.json             # Root copy of document and artifact manifest
├── SOURCE_REGISTRY.csv              # Root copy of authority source registry
├── DATASET_VALIDATION_STATUS.md     # Comprehensive status report (this file)
├── corpus/                          # 8 Standardized Markdown RAG documents
│   ├── rice_stem_borer.md           # DOC-PEST-001
│   ├── rice_brown_planthopper.md    # DOC-PEST-002
│   ├── rice_leaf_folder.md          # DOC-PEST-003
│   ├── rice_green_leafhopper.md     # DOC-PEST-004
│   ├── rice_gall_midge.md           # DOC-PEST-005
│   ├── rice_thrips.md               # DOC-PEST-006
│   ├── rice_whorl_maggot.md         # DOC-PEST-007
│   └── rice_earhead_bug.md          # DOC-PEST-008
├── evidence/                        # Structured quantitative evidence
│   └── ETL_EVIDENCE.jsonl           # 17 structured numerical threshold records
├── tamil/                           # Tamil linguistic assets
│   └── TAMIL_PEST_LEXICON.csv       # 23 canonical names & dialectal variants
├── images/                          # 17 reference images preserved unchanged
│   ├── brown_planthopper/           # 3 images
│   ├── earhead_bug/                 # 2 images
│   ├── gall_midge/                  # 2 images
│   ├── green_leafhopper/            # 2 images
│   ├── leaf_folder/                 # 3 images
│   ├── stem_borer/                  # 3 images
│   ├── thrips/                      # 2 images
│   └── whorl_maggot/                # 0 images
├── manifests/                       # Schemas and registries
│   ├── CORPUS_MANIFEST.json         # Document catalog and metadata
│   ├── SOURCE_REGISTRY.csv          # Authority organizations and URLs
│   ├── image_manifest.csv           # Image-level provenance and hashes
│   ├── vision_label_schema.json     # Vision annotation schema
│   └── pest_corpus_collection_plan.csv
└── validation/                      # Governance and audit trackers
    ├── PEST_VALIDATION_TRACKER.csv  # 8-pest readiness checklist
    └── CHEMICAL_VALIDATION_REQUIRED.csv # 9 chemical prescriptions requiring audit
```

---

## 2. Records Prepared (8 Canonical Pests)

| Doc ID | Pest Name | Source Org | Stage Focus | Evidence Records | Images | Markdown Path |
|---|---|---|---|---|---|---|
| `DOC-PEST-001` | Stem borer | TNAU | Vegetative & Reproductive | 2 | 3 | `corpus/rice_stem_borer.md` |
| `DOC-PEST-002` | Brown planthopper (BPH) | ICAR-IRRI | Seedling, Vegetative, Reproductive | 3 | 3 | `corpus/rice_brown_planthopper.md` |
| `DOC-PEST-003` | Leaf folder | TNAU | Vegetative & Boot Leaf | 2 | 3 | `corpus/rice_leaf_folder.md` |
| `DOC-PEST-004` | Green leafhopper (GLH) | ICAR-IIRR | All Stages (Tungro Vector) | 3 | 2 | `corpus/rice_green_leafhopper.md` |
| `DOC-PEST-005` | Gall midge | TNAU | Tillering Stage | 1 | 2 | `corpus/rice_gall_midge.md` |
| `DOC-PEST-006` | Thrips | KVK | Nursery & Early Vegetative | 2 | 2 | `corpus/rice_thrips.md` |
| `DOC-PEST-007` | Whorl maggot | TNAU | Nursery & Newly Transplanted | 2 | 0 | `corpus/rice_whorl_maggot.md` |
| `DOC-PEST-008` | Earhead bug | ICAR-IIRR | Flowering & Grain Milking | 2 | 2 | `corpus/rice_earhead_bug.md` |

---

## 3. Claims & Regulatory Audits Requiring Verification

### A. Chemical Recommendations Requiring Verification (9 Total)
All chemical management advice is currently tagged as **`UNVERIFIED`** in both YAML frontmatter and `CHEMICAL_VALIDATION_REQUIRED.csv`:

1. **Carbofuran 3G @ 33 kg/ha** (Stem borer, Gall midge, Whorl maggot): High priority regulatory audit required. Carbofuran is banned/restricted in several Indian states and faces tight CIBRC restrictions.
2. **Chlorantraniliprole 18.5 SC @ 150 ml/ha** (Stem borer, Leaf folder): Modern diamide; verify water dilution rates and label claims on paddy.
3. **Buprofezin 25 SC @ 400 ml/ha** (BPH): Insect growth regulator; verify spray targeting (base of tillers) and Pre-Harvest Interval (PHI).
4. **Imidacloprid 17.8 SL @ 100 ml/ha** (GLH): Neonicotinoid; verify safety intervals relative to flowering.
5. **Thiamethoxam 25 WG @ 100 g/ha** (Thrips): Verify foliar nursery dosage.
6. **Malathion 50 EC @ 500 ml/ha** (Earhead bug): Applied during grain milking; severe grain residue risk. Requires maximum residue limit (MRL) and PHI verification.

### B. Structured ETL Evidence Records (17 Total)
17 discrete numeric ETL action thresholds were extracted and formatted into `evidence/ETL_EVIDENCE.jsonl` without inventing unstated values. Every record preserves exact source citation and verbatim text.

### C. Severity Cutoffs (8 Pests Missing Discrete Cutoffs)
The 3-tier severity framework (`early`, `moderate`, `severe_spreading`) is defined in `severity_framework.json`, but specific numeric cutoff thresholds (% damage, insect counts) remain unassigned. They are explicitly flagged as `MISSING_SOURCE_CUTOFFS` to prevent artificial scoring distortion.

### D. Tamil Linguistic Terms (23 Total Terms)
- **16 Terms Marked `VERIFIED`**: Canonical names (e.g. *தண்டு துளைப்பான்*, *புகையான்*, *இலை சுருட்டு புழு*, *ஆணைக்கொம்பன்*, *இலைப்பேன்*) and standard symptom phrases (*வெண்கதிர்*, *வெள்ளிக்குருத்து*).
- **7 Terms Marked `NEEDS_REVIEW`**: Colloquial regional aliases (e.g. *குருத்துப் பூச்சி*, *பச்சை புழு*, *துங்ரோ பூச்சி*, *சாற்றுப்பூச்சி*, *குந்தி பூச்சி*) awaiting dialectal validation with local farming groups.

### E. Images Retained (17 Total)
17 reference images copied from Dataset v4 with complete cryptographic integrity (SHA-256 verified) and manifest metadata (`image_manifest.csv`). Tagged for UI display in the KVK portal rather than model training due to resolution and sample size constraints.

---

## 4. Production Integration Constraints Honored

- **No pgvector Ingestion**: Raw data has not been ingested into the live `knowledge_chunks` table.
- **No Code Modifications**: `gate_service.py`, `intent_parser.py`, and domain services remain untouched.
- **Zero Fabrication**: Missing severity cutoffs and unexposed publication dates are preserved as explicit placeholders rather than filled with synthetic assumptions.
