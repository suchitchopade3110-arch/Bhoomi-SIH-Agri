# Contract Freeze Changelog — Phase 1 (SIH26131)

> **Document ID:** CHANGELOG-FREEZE-001  
> **Status:** Frozen (Hours 0–2)  
> **Target Release:** SIH26131 Core Intelligence Layer

---

## 1. Frozen Shapes & Rationales

| Frozen Shape / Model | Schema Location | One-Line Rationale |
| :--- | :--- | :--- |
| **`GateObject`** | [`app.schemas.gate.GateObject`](file:///c:/Users/SUCHIT%20CHOPADE/OneDrive/Desktop/Bhoomi-SIH-Agri/services/api/app/schemas/gate.py) | Standardizes confidence gate decision object returned in `/diagnose` across both answer and escalation paths (`above_gate`, `confidence`, `threshold`, `reason_code`, `alternatives`). |
| **`FivePointAdvisory` (Reordered)** | [`app.schemas.advisory.FivePointAdvisory`](file:///c:/Users/SUCHIT%20CHOPADE/OneDrive/Desktop/Bhoomi-SIH-Agri/services/api/app/schemas/advisory.py) | Promotes `what_to_avoid` before `what_to_do_next` to align with farmer persona research leading with harm prevention. |
| **`FIVE_POINT_FIELDS` (Reordered)** | [`app.domain.rag.constants.FIVE_POINT_FIELDS`](file:///c:/Users/SUCHIT%20CHOPADE/OneDrive/Desktop/Bhoomi-SIH-Agri/services/api/app/domain/rag/constants.py) | Locks tuple ordering `("possible_issue", "what_to_check", "what_to_avoid", "what_to_do_next", "expert_triggers")` for RAG parser and prompts. |
| **`FarmRiskTrendResponse`** | [`app.schemas.farm.FarmRiskTrendResponse`](file:///c:/Users/SUCHIT%20CHOPADE/OneDrive/Desktop/Bhoomi-SIH-Agri/services/api/app/schemas/farm.py) | Freezes qualitative advisory string plus trend indicator for `/farms/{id}/risk` without numeric sub-index breakdown. |
| **`FarmSummaryTrendResponse`** | [`app.schemas.farm.FarmSummaryTrendResponse`](file:///c:/Users/SUCHIT%20CHOPADE/OneDrive/Desktop/Bhoomi-SIH-Agri/services/api/app/schemas/farm.py) | Freezes high-level summary card for `/farms/{id}/summary` returning qualitative advisory and trend trajectory. |
| **`LandStatus` (Thin Enum)** | [`app.core.enums.LandStatus`](file:///c:/Users/SUCHIT%20CHOPADE/OneDrive/Desktop/Bhoomi-SIH-Agri/services/api/app/core/enums.py) | Enforces thin land verification status `pending_verification \| verified \| rejected` without cadastral geometry dependencies. |
| **`ThinLandVerification`** | [`app.schemas.land.ThinLandVerification`](file:///c:/Users/SUCHIT%20CHOPADE/OneDrive/Desktop/Bhoomi-SIH-Agri/services/api/app/schemas/land.py) | Strips deprecated geometry and area verification fields for thin land verification in SIH26131. |
| **`SchemeResponse` & `SchemeListResponse`** | [`app.schemas.schemes.SchemeResponse`](file:///c:/Users/SUCHIT%20CHOPADE/OneDrive/Desktop/Bhoomi-SIH-Agri/services/api/app/schemas/schemes.py) | Freezes static subsidy list with explicit `last_verified` date and active status flag. |
