---
doc_id: DOC-PEST-008
title: "ICAR Rice Insect Pest Management — Earhead Bug"
crop: "Rice (Oryza sativa)"
pest_name: "Earhead bug"
scientific_name: "Leptocorisa acuta"
pest_id: "PEST_008"
source_organization: "ICAR-IIRR"
source_type: "Technical Bulletin"
source_document: "ICAR Rice Insect Pest Management — Earhead Bug"
source_page: "Technical Bulletin / Grain Pests"
source_url: "https://iirr.icar.gov.in/"
citation: "ICAR Rice Insect Pest Management"
authority_level: "High"
source_date: "NOT EXPOSED IN SOURCE"
publication_date: null
publication_date_status: "not_exposed"
last_reviewed: 2026-08-24
verification_date: 2026-08-24
review_due: 2027-02-24
validation_status: "SOURCE_DERIVED_VALIDATED"
etl_validation_status: "SOURCE_SUPPORTED_WITH_CONTEXT"
severity_status: "MISSING_SOURCE_CUTOFFS"

etl_evidence:
  - record_id: "ETL-016"
    stage: "flowering"
    threshold:
      base:
        metric: "bugs_per_panicles"
        operator: ">="
        value: 5.0
        unit: "bugs/100_panicles"
      modifier: null
    status: "SOURCE_SUPPORTED"
    exact_source_text: "Flowering: 5 bugs/100 panicles"
  - record_id: "ETL-017"
    stage: "milking"
    threshold:
      base:
        metric: "bugs_per_panicles"
        operator: ">="
        value: 10.0
        unit: "bugs/100_panicles"
      modifier:
        condition: "hill_based_sampling_unit"
        adjusted_value_min: 1.0
        adjusted_value_max: 2.0
        adjusted_unit: "bugs/hill"
    status: "SOURCE_SUPPORTED_WITH_CONTEXT"
    exact_source_text: "Milking: 10 bugs/100 panicles"

chemical_prescriptions:
  - chemical: "Malathion"
    formulation: "50 EC"
    dose: "500 ml/ha"
    regulatory_status: "RESTRICTED"
    evidence_status: "SOURCE_DOCUMENTED_RESIDUE_RISK"
    notes: "Malathion is registered for rice earhead bug (500-1000 ml/ha), but application during grain milking carries high grain residue risk; strict PHI compliance (minimum 7-10 days before harvest) is mandatory."
---

# ICAR Rice Insect Pest Management: Earhead Bug

## 1. Overview & Crop Stages Affected
Rice earhead bug or gundhi bug (*Leptocorisa acuta*) attacks paddy specifically during the flowering, milking, and soft-dough stages of grain development.

Both adults and nymphs pierce the developing milky grains and suck the liquid contents, causing the grains to become partially filled, discolored, shriveled, or completely empty (chaffy). Heavy infestation imparts an unpleasant offensive odor to the field and significantly degrades grain market quality.

## 2. Distinguishing Field Identification Cues
- Slender, greenish-brown bug (15 to 20 mm long) with long legs and prominent antennae emitting a strong pungent odor.
- Greenish nymphs with black and white banded legs clustered on maturing panicles.
- Damaged grains displaying brownish puncture spots, shriveled hulls, or empty chaffy panicles.
- Apparent peak bug activity occurring during early morning and late evening hours.

## 3. Economic Threshold Levels (ETL)
Field interventions should be initiated when pest scouting reaches the following source-quoted action thresholds:
- **Flowering Stage**: 5 bugs per 100 panicles (`SOURCE_SUPPORTED`).
- **Milking / Grain-filling Stage**: 10 bugs per 100 panicles (`SOURCE_SUPPORTED_WITH_CONTEXT`). *Context Modifier: Equivalent to 1–2 bugs per hill in standard planting densities.*

## 4. Integrated Management & Control Practices
- **Cultural Control**: Synchronize planting across adjacent holdings to avoid staggered heading dates that sustain bug populations. Clear grassy weeds and wild grasses (*Echinochloa colona*, *Panicum repens*) from field borders.
- **Monitoring & Mechanical Control**: Set up light traps during night hours to monitor and trap adult bugs. Use net sweeps in early morning hours.
- **Chemical Control (Validated)**:
  - *Malathion 50 EC* @ 500–1000 ml/ha (`RESTRICTED` — high grain residue risk; spray during early morning or evening hours; strict minimum 7–10 days Pre-Harvest Interval required).

## 5. Regulatory & Validation Status
- Chemical Advice Status: Malathion 50 EC is **RESTRICTED** (mandatory PHI $\ge 7\text{–}10\text{ days}$).
- ETL Validation Status: **SOURCE_SUPPORTED_WITH_CONTEXT** (sampling unit duality documented).
- Publication Date: Not exposed in source web portal; review schedule maintained on a 6-month cycle.
