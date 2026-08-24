---
pest_name: "Whorl maggot"
crop: "Rice (Oryza sativa)"
scientific_name: "Hydrellia philippina"
category: "Insect Pest"
tamil_name: "குருத்து ஈ"
aliases:
  - "Rice whorl maggot"
  - "இலை ஈ"
  - "Paddy whorl maggot"
  - "Hydrellia maggot"
source_organization: "TNAU / ICAR-IIRR"
source_title: "TNAU Whorl Maggot Management in Rice"
source_url: "https://agritech.tnau.ac.in/crop_protection/rice_pest.html"
review_date: "2026-08-24"
authority_level: "High (University Extension Bulletin - Authority Tier 8)"
---

# TNAU Whorl Maggot Management in Rice

## 1. Identification
The rice whorl maggot (*Hydrellia philippina*) is a semi-aquatic dipteran pest that attacks rice seedlings in wet nursery beds and newly transplanted paddy up to 30 days after transplanting (DAT) across Tamil Nadu and South India.

Farmers and scouts can identify the pest through its life stages:
- **Adult Fly**: Small, dull greyish-black fly (1.5 to 2.0 mm long) with smoky-grey wings, prominent golden-grey eyes, and silvery-white facial pubescence. The adults are frequently observed skimming actively over standing water surfaces in flooded paddy fields.
- **Egg**: Tiny, elongated, boat-shaped chalky-white eggs laid singly on the upper or lower surface of leaves floating on or close to the water level.
- **Maggot (Larva)**: Slender, legless, translucent-white to yellowish-white maggot (5 to 6 mm long when mature) with dark internal mouth hooks, found concealed inside the central unexpanded leaf whorl.
- **Pupa**: Light brown to dark brown, cylindrical, spindle-shaped puparium found attached to the outer leaf sheath near the water level.

## 2. Distinguishing Cues
Whorl maggot damage can be readily distinguished from leaf folders, stem borers, and mechanical hail damage by the following unique diagnostic symptoms:
- **Serrated, Broken Leaf Margins**: Maggot feeding occurs while the leaf is still rolled inside the central whorl. As the leaf expands and unfurls, the damaged areas appear as ragged, jagged, serrated margins with small chewed holes.
- **Transverse White Streaks**: Unfolded leaves exhibit distinct white to yellowish longitudinal feeding streaks running parallel to the midrib, often accompanied by pinched, constricted leaf blades that droop or break in the wind.
- **Absence of Dead Hearts or Silken Webs**: Unlike stem borer which kills the central shoot entirely, the central tiller survives whorl maggot attack, and unlike leaf folder, there are no silken threads stitching leaf margins together.

## 3. Symptoms and Field Signs
- **Ragged Leaf Unfolding**: Newly emerged central leaves exhibit yellow-white patches, pinholes, and torn, serrated leaf margins.
- **Stunted Early Tillering**: Continuous larval feeding on the unexpanded central leaves retards plant vigor, delaying tillering and vegetative canopy closure.
- **Water Skimming Flies**: Numerous tiny greyish flies skimming or darting across the water surface between hills during morning hours.

## 4. Life-Cycle and Relevant Biology
- **Oviposition**: Female flies lay 50 to 100 eggs singly on leaf surfaces close to the water. Incubation lasts 2 to 4 days.
- **Larval Habits**: Newly hatched maggots crawl down into the unexpanded central leaf whorl and feed on the developing mesophyll tissue. Larval stage lasts 10 to 12 days through 3 instars.
- **Pupation**: Maggots move to the outer leaf sheath near the water surface to pupate. Pupal period lasts 7 to 10 days.
- **Aquatic Dependency**: The pest requires continuous standing water to complete its life cycle; drying of the field causes high mortality of newly hatched maggots and pupae.

## 5. Vulnerable Growth Stages
Whorl maggot infests rice strictly during the early vegetative establishment window:
- **Nursery / Seedling Stage (1 to 20 Days After Sowing)**: Maggots attack tender seedlings in wet nursery beds.
- **Early Vegetative Stage (1 to 30 Days After Transplanting)**: Peak vulnerability window where active tiller initiation is retarded.
- **Late Vegetative & Reproductive Stages (Beyond 35 DAT)**: The crop naturally outgrows susceptibility as stems become tough and canopy closes; control measures beyond 35 DAT are unnecessary and economically unjustified.

## 6. Economic Threshold Level (ETL)
Field chemical interventions must be strictly based on the following source-quoted thresholds during the first 30 days of crop growth:
- **ETL Classification**: `NUMERIC_ETL`
- **Seedling / Nursery Stage**: $\ge 1\text{ to }2\text{ maggots per seedling}$ (`SOURCE_SUPPORTED`).
- **Vegetative Stage (Up to 30 DAT)**: $\ge 10\%\text{ damaged/ragged leaves}$ (`SOURCE_SUPPORTED`).
- *Distinction from Severity*: ETL sets the 30-day intervention boundary beyond which spraying is unviable. Severity tracks foliar laceration and tiller stunting.

## 7. Severity Indicators
- **A. Observable Severity Indicators**:
  - *Early Severity*: Small yellowish feeding streaks on newly expanded central leaves ($<5\%$ damaged leaves within 30 DAT); seedling vigor unaffected.
  - *Moderate Severity*: Ragged serrated leaf margins visible on multiple expanding leaves per hill ($6\%\text{–}15\%$ damaged leaves).
  - *Severe Severity*: Conspicuous broken serrated leaf blades and distorted central whorls across the plot ($16\%\text{–}30\%$ damaged leaves).
  - *Catastrophic*: $>30\%$ damaged leaves with severe seedling stunting and delayed canopy closure in flooded plots.
- **B. Quantitative Severity Thresholds**:
  - *TNAU Agritech Whorl Maggot Scale*:
    - SES 1–3 (Early): $<5\%$ damaged leaves within 30 DAT (`SOURCE_SUPPORTED`).
    - SES 5 (Moderate): $6\%\text{–}15\%$ damaged leaves (`SOURCE_SUPPORTED`).
    - SES 7 (Severe): $16\%\text{–}30\%$ damaged leaves (`SOURCE_SUPPORTED`).
    - SES 9 (Catastrophic): $>30\%$ damaged leaves with severe stunting (`SOURCE_SUPPORTED`).
  - *Threshold Status*: `SOURCE_SUPPORTED` (TNAU Extension Bulletin).
  - *Internal Engine Penalty Mapping*: Early = 30, Moderate = 55, Severe = 80 (`PROJECT_DERIVED_RULE` for Farm Health Score sub-index).

## 8. Cultural and Mechanical Management
- **Intermittent Field Drainage (AWD)**: Drain standing water from the field for 2 to 3 days periodically during the first 3 weeks after transplanting to expose eggs and maggots to desiccation and natural enemies.
- **Avoid Continuous Deep Flooding**: Maintain shallow water depth (2 to 3 cm) rather than deep standing water (5 to 10 cm) during the early tillering phase.
- **Neem Cake Incorporation**: Apply neem cake @ 250 kg/ha in nursery beds and @ 500 kg/ha in the main field during basal land preparation.
- **Timely Transplanting**: Transplant older, vigorous seedlings (25 to 30 days old) which establish rapidly and tolerate whorl maggot feeding better than very young tender seedlings.

## 9. Biological Management
- **Predatory Spiders & Flies**: Conserve ephydrid and dolichopodid predatory flies, as well as lycosid spiders hunting on the water surface.
- **Egg & Pupal Parasitoids**: Protect natural hymenopteran parasitoids (*Opius* spp., *Trichopria* spp.) that parasitize whorl maggot pupae.

## 10. Chemical Management
When pest damage exceeds 10% damaged leaves within 30 days after transplanting, apply approved treatments:
- **Fipronil 5 SC** @ 1000–1500 ml/ha in 500 L water (`VERIFIED_CURRENT`). Broad-spectrum systemic foliar spray; Pre-Harvest Interval (PHI): 32 days.
- **Carbofuran 3G** @ 33 kg/ha at planting (`RESTRICTED`). *Regulatory Warning: Class Ib high-toxicity carbamate under strict regulatory restriction in aquatic ecosystems due to high runoff and avian hazard; non-chemical field drainage and safer systemic alternatives strongly preferred.*

## 11. Monitoring Guidance
- **Visual Leaf Inspection**: Inspect 20 randomly selected hills across the field once every 4 days up to 30 DAT; count total leaves and leaves with ragged margins or yellow feeding streaks.
- **Water Surface Observation**: Observe 1 m² water patches in early morning for skimming adult flies.

## 12. Escalation and Decision Cues
Escalate immediately to the District Agriculture Extension Officer or KVK Agronomist if:
- **Severe Stunting Beyond 30 DAT**: Crop canopy fails to establish and tiller counts remain $<5\text{ tillers/hill}$ at 35 DAT.
- **Post-30 DAT Mistreatment**: Ensure farmers do not apply expensive insecticides after 35 DAT, as natural crop compensatory growth renders post-35 DAT spraying economically wasteful.

## 13. Source Citations
- **Primary Source**: Tamil Nadu Agricultural University (TNAU) Agritech Portal — Crop Protection / Rice Pest Management / Whorl Maggot (`https://agritech.tnau.ac.in/crop_protection/rice_pest.html`).
- **Secondary Source**: ICAR-Indian Institute of Rice Research (IIRR) Technical Bulletin on Rice Whorl Maggot.
- **Authority Level**: Tier 8 (State Agricultural University Extension Protocol).

## 14. Review Metadata
- **Last Review Date**: 2026-08-24
- **Verification Date**: 2026-08-24
- **Next Scheduled Review**: 2027-02-24 (6-Month Cycle)
- **Publication Date**: Not exposed in source web portal (marked `not_exposed`).
- **Validation Status**: `SOURCE_DERIVED_VALIDATED`
