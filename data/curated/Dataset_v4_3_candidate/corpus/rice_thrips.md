---
doc_id: DOC-PEST-006
title: "KVK Rice Nursery Management — Thrips Control"
crop: "Rice (Oryza sativa)"
pest_name: "Thrips"
scientific_name: "Stenchaetothrips biformis"
pest_id: "PEST_006"
source_organization: "KVK"
source_type: "Extension Advisory"
source_document: "KVK Rice Nursery Management — Thrips Control"
source_page: "Extension Advisory / Nursery Protection"
source_url: "https://kvk.icar.gov.in/"
citation: "KVK Rice Nursery Management"
authority_level: "Medium-High"
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
  - record_id: "ETL-012"
    stage: "seedling"
    threshold:
      base:
        metric: "thrips_per_seedling"
        operator: ">="
        value: 5.0
        unit: "thrips/seedling"
      modifier: null
    status: "SOURCE_SUPPORTED"
    exact_source_text: "Seedling: 5 thrips/seedling"
  - record_id: "ETL-013"
    stage: "vegetative"
    threshold:
      base:
        metric: "thrips_per_hill"
        operator: ">="
        value: 25.0
        unit: "thrips/hill"
      modifier: null
    status: "SOURCE_SUPPORTED"
    exact_source_text: "Vegetative: 25 thrips/hill"

chemical_prescriptions:
  - chemical: "Thiamethoxam"
    formulation: "25 WG"
    dose: "100 g/ha"
    regulatory_status: "VERIFIED_CURRENT"
    evidence_status: "SOURCE_SUPPORTED_CIBRC_ALIGNED"
    notes: "CIBRC registered for rice thrips, stem borer, and GLH at 100 g/ha in 500 L water. PHI: 14 days. Suited for nursery and early vegetative foliar application."
---

# KVK Rice Nursery Management: Thrips Control

## 1. Overview & Crop Stages Affected
Rice thrips (*Stenchaetothrips biformis*) is a common nursery and early vegetative pest of paddy across Tamil Nadu. It causes severe leaf rolling and seedling stunting, particularly under dry nursery conditions and water deficit stress.

Both nymphs and adults lacerate the tender leaf surface and suck the plant sap, causing the leaf margins to curl inward and the tips to wither.

## 2. Distinguishing Field Identification Cues
- Minute, slender insects (1 to 2 mm long) with dark brown to black bodies and narrow fringed wings.
- Yellow to orange discoloration on upper leaf surfaces turning into silvery patches.
- Characteristic inward rolling or curling of leaf tips into needle-like shapes.
- Withered, dried leaf tips giving seedlings a burnt or scorched appearance.

## 3. Economic Threshold Levels (ETL)
Field interventions should be initiated when pest scouting reaches the following source-quoted action thresholds:
- **Seedling / Nursery Stage**: 5 thrips per seedling (`SOURCE_SUPPORTED`).
- **Vegetative (Tillering) Stage**: 25 thrips per hill (`SOURCE_SUPPORTED`).

*(Note: Severity cutoffs separating Early from Moderate/Severe infestations must be derived from vetted field evidence and are currently pending agronomist sign-off).*

## 4. Integrated Management & Control Practices
- **Cultural Control**: Submerge the nursery beds periodically with water to drown and dislodge feeding thrips. Avoid moisture stress in nursery. Maintain adequate standing water depth in the main field.
- **Monitoring**: Set up blue sticky traps above crop canopy level to monitor thrips population surges.
- **Chemical Control (Validated)**: Apply Thiamethoxam 25 WG @ 100 g/ha (`VERIFIED_CURRENT`, PHI: 14 days) in 500 L water/ha.

## 5. Regulatory & Validation Status
- Chemical Advice Status: Thiamethoxam 25 WG is **VERIFIED_CURRENT** (CIBRC registered on rice).
- ETL Validation Status: **SOURCE_SUPPORTED** (direct KVK/TNAU guideline).
- Publication Date: Not exposed in source web portal; review schedule maintained on a 6-month cycle.
