---
doc_id: DOC-PEST-005
title: "TNAU Gall Midge Management in Rice"
crop: "Rice (Oryza sativa)"
pest_name: "Gall midge"
scientific_name: "Orseolia oryzae"
pest_id: "PEST_005"
source_organization: "TNAU"
source_type: "Extension Bulletin"
source_document: "TNAU Gall Midge Management in Rice"
source_page: "Crop Protection / Rice Pest / Gall Midge"
source_url: "https://agritech.tnau.ac.in/crop_protection/rice_pest.html"
citation: "TNAU Gall Midge Management"
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
  - record_id: "ETL-011"
    stage: "vegetative"
    threshold:
      base:
        primary_metric: "silver_shoot_pct"
        operator: ">="
        value: 5.0
        unit: "percent"
        alternative_metric: "adults_per_sweeps"
        alternative_operator: ">="
        alternative_value: 1.0
        alternative_unit: "adult/100_sweeps"
      modifier: null
    status: "SOURCE_SUPPORTED"
    exact_source_text: "Vegetative: 5% silver shoots or 1 adult/100 sweeps"

chemical_prescriptions:
  - chemical: "Carbofuran"
    formulation: "3G"
    dose: "33 kg/ha at planting"
    regulatory_status: "RESTRICTED"
    evidence_status: "SOURCE_DOCUMENTED_RESTRICTED"
    notes: "Carbofuran 3G application in standing water is restricted due to environmental/mammalian toxicity. Non-chemical controls (resistant varieties, summer plowing) preferred."
---

# TNAU Gall Midge Management in Rice

## 1. Overview & Crop Stages Affected
Rice gall midge (*Orseolia oryzae*) is an internal feeder causing severe damage primarily during the tillering stage. It is endemic in the Cauvery delta and coastal districts of Tamil Nadu.

The maggot feeds at the growing apical tip of the tiller, causing the leaf sheath to transform into a hollow, tubular elongation resembling an onion leaf or silver shoot, rendering the tiller sterile and incapable of producing a panicle.

## 2. Distinguishing Field Identification Cues
- Formation of characteristic tubular "silver shoots" or "onion shoots" at the base of tillers.
- Stunted tillers with galls at the base containing feeding maggots.
- Presence of reddish-brown pupal cases protruding from the tip of the gall tube prior to adult emergence.
- Adult is a small, mosquito-like fly with long, slender legs and antennae.

## 3. Economic Threshold Levels (ETL)
Field interventions should be initiated when pest scouting reaches the following source-quoted action thresholds:
- **Vegetative (Tillering) Stage**: 5% silver shoots OR 1 adult fly per 100 net sweeps (`SOURCE_SUPPORTED`).

*(Note: Severity cutoffs separating Early from Moderate/Severe infestations must be derived from vetted field evidence and are currently pending agronomist sign-off).*

## 4. Integrated Management & Control Practices
- **Cultural & Varietal Control**: Grow resistant paddy cultivars such as Kavya and Surekha in endemic tracts. Conduct deep summer plowing to expose and destroy overwintering pupae in stubble. Avoid delayed transplanting in gall midge prone seasons.
- **Biological Control**: Conserve natural larval parasitoids such as *Platygaster oryzae* (*Platygaster orseoliae*).
- **Chemical Control (Validated)**:
  - *Carbofuran 3G* @ 33 kg/ha at planting (`RESTRICTED` — high toxicity; subject to state restrictions and regulatory caution).

## 5. Regulatory & Validation Status
- Chemical Advice Status: Carbofuran 3G is **RESTRICTED** (Class Ib toxicant).
- ETL Validation Status: **SOURCE_SUPPORTED** (direct TNAU guideline).
- Publication Date: Not exposed in source web portal; review schedule maintained on a 6-month cycle.
