---
doc_id: DOC-PEST-001
title: "TNAU Rice Pest Management Guide — Stem Borer"
crop: "Rice (Oryza sativa)"
pest_name: "Stem borer"
scientific_name: "Scirpophaga incertulas"
pest_id: "PEST_001"
source_organization: "TNAU"
source_type: "Extension Bulletin"
source_document: "TNAU Rice Pest Management Guide — Stem Borer"
source_page: "Crop Protection / Rice Pest / Stem Borer"
source_url: "https://agritech.tnau.ac.in/crop_protection/rice_pest.html"
citation: "TNAU Agritech Portal, Rice Pest Management"
authority_level: "High"
source_date: "NOT EXPOSED IN SOURCE"
publication_date: null
publication_date_status: "not_exposed"
last_reviewed: 2026-08-24
verification_date: 2026-08-24
review_due: 2027-02-24
validation_status: "SOURCE_DERIVED_VALIDATED"
etl_validation_status: "SOURCE_SUPPORTED"
severity_status: "MISSING_SOURCE_CUTOFFS"

etl_evidence:
  - record_id: "ETL-001"
    stage: "vegetative"
    threshold:
      base:
        primary_metric: "egg_masses_per_sq_meter"
        operator: ">="
        value: 1.0
        unit: "egg_mass/m2"
        alternative_metric: "dead_heart_pct"
        alternative_operator: ">="
        alternative_value: 10.0
        alternative_unit: "percent"
      modifier: null
    status: "SOURCE_SUPPORTED"
    exact_source_text: "Vegetative: 1 egg mass/m² or 10% dead hearts"
  - record_id: "ETL-002"
    stage: "reproductive"
    threshold:
      base:
        primary_metric: "egg_masses_per_sq_meter"
        operator: ">="
        value: 1.0
        unit: "egg_mass/m2"
        alternative_metric: "white_ear_pct"
        alternative_operator: ">="
        alternative_value: 5.0
        alternative_unit: "percent"
      modifier: null
    status: "SOURCE_SUPPORTED"
    exact_source_text: "Reproductive: 1 egg mass/m² or 5% white ears"

chemical_prescriptions:
  - chemical: "Carbofuran"
    formulation: "3G"
    dose: "33 kg/ha at planting"
    regulatory_status: "RESTRICTED"
    evidence_status: "SOURCE_DOCUMENTED_RESTRICTED"
    notes: "Class Ib high-toxicity carbamate under state-level restrictions/bans in India; requires agronomist warning."
  - chemical: "Chlorantraniliprole"
    formulation: "18.5 SC"
    dose: "150 ml/ha if ETL exceeded"
    regulatory_status: "VERIFIED_CURRENT"
    evidence_status: "SOURCE_SUPPORTED_CIBRC_ALIGNED"
    notes: "CIBRC approved label claim for Yellow Stem Borer on rice. Dilution: 150 ml in 500 L water/ha. PHI: 47 days."
---

# TNAU Rice Pest Management Guide: Stem Borer

## 1. Overview & Crop Stages Affected
Stem borer is one of the major insect pests of paddy across Tamil Nadu and South India. It attacks rice crops across all growth stages, with distinct symptoms manifesting during the vegetative and reproductive phases.

During the vegetative stage, larval feeding inside the stem causes the central shoot to dry up and die, producing the classic "dead heart" symptom. During the reproductive stage, feeding at the base of the panicle results in completely empty, chaffy, erect white panicles known as "white earhead" or "white ear."

## 2. Distinguishing Field Identification Cues
- Egg masses covered with buff-colored hairs laid near the tips of tender leaves.
- Larvae characterized by a brown head and dirty-white body boring inside the lower stem.
- Adult moths with silvery-white to yellowish-brown wings bearing prominent black spots on the forewings.
- Presence of "dead hearts" in the vegetative phase where the central tiller pulls out easily when tugged.
- Presence of "white earheads" (empty panicles) in the flowering to grain-filling phase.

## 3. Economic Threshold Levels (ETL)
Field interventions should be initiated when pest scouting reaches the following source-quoted action thresholds:
- **Vegetative Stage**: 1 egg mass per square meter OR 10% dead hearts (`SOURCE_SUPPORTED`).
- **Reproductive Stage**: 1 egg mass per square meter OR 5% white ears (`SOURCE_SUPPORTED`).

*(Note: Severity cutoffs separating Early from Moderate/Severe infestations must be derived from vetted field evidence and are currently pending agronomist sign-off).*

## 4. Integrated Management & Control Practices
- **Cultural & Varietal Control**: Cultivate moderately resistant or tolerant rice varieties recommended for the region, such as CO 51 and ADT 43. Regularly scout nursery and main field to hand-pick and destroy egg masses before larvae hatch.
- **Biological Control**: Release egg parasitoids (*Trichogramma japonicum*) @ 50,000 per hectare when moth activity is detected. Conserve native predatory spiders and parasitoids.
- **Chemical Control (Validated)**:
  - *Chlorantraniliprole 18.5 SC* @ 150 ml/ha in 500 L water/ha (`VERIFIED_CURRENT`, PHI: 47 days).
  - *Carbofuran 3G* @ 33 kg/ha (`RESTRICTED` — high mammalian/wildlife toxicity; subject to state bans).

## 5. Regulatory & Validation Status
- Chemical Advice Status: Chlorantraniliprole 18.5 SC is **VERIFIED_CURRENT** (CIBRC registered for rice); Carbofuran 3G is **RESTRICTED**.
- ETL Validation Status: **SOURCE_SUPPORTED** (direct TNAU guideline).
- Publication Date: Not exposed in source web portal; review schedule maintained on a 6-month cycle.
