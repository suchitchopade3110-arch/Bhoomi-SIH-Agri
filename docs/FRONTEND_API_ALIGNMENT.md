# BHOOMI — Frontend & Mobile API Alignment Specification

> **Specification Document:** `docs/FRONTEND_API_ALIGNMENT.md`  
> **Status:** Fully Integrated & Verified  
> **Target Environment:** Monorepo Ecosystem (`apps/farmer_app`, `apps/kvk_portal`, `apps/officer_portal`)  
> **Base API Prefix:** `/api/v1`

---

## 1. Executive Summary

This document details the complete end-to-end API contract reconciliation between the BHOOMI FastAPI backend intelligence layer and all three frontend applications:
1. **Farmer Mobile App** (`apps/farmer_app` — Flutter)
2. **KVK Agronomist Portal** (`apps/kvk_portal` — React + TypeScript)
3. **Revenue Officer Portal** (`apps/officer_portal` — React + TypeScript)

All endpoints, models, enums, status code branches, confidence gates, and fallback behaviors are reconciled and validated without modifying any backend code.

---

## 2. API Contract Alignment Table

| Endpoint | Method | Frontend App | Service File | Request Model | Response Model | Status | Notes / Reconciliation |
|---|---|---|---|---|---|---|---|
| `/api/v1/auth/otp/request` | `POST` | `farmer_app` | `auth_api_service.dart` | `{ phone }` | `OtpRequestResponse` | **VERIFIED** | Request 6-digit OTP for farmer phone login. |
| `/api/v1/auth/otp/verify` | `POST` | `farmer_app` | `auth_api_service.dart` | `{ phone, otp, session_id }` | `AuthTokenResponse` | **VERIFIED** | Stores JWT token securely in `flutter_secure_storage`. |
| `/api/v1/assets/presigned-url` | `POST` | `farmer_app` | `asset_upload_service.dart` | `PresignedUploadRequest` | `PresignedAssetResult` | **VERIFIED** | Pre-signs S3 URL; client uploads binary via direct `PUT`. |
| `/api/v1/voice/transcribe` | `POST` | `farmer_app` | `voice_api_service.dart` | `TranscribeRequest` | `TranscribeResponse` | **VERIFIED** | Handles `transcript`/`text`, `needs_confirmation`, BCP-47 `lang`. |
| `/api/v1/voice/synthesize` | `POST` | `farmer_app` | `voice_api_service.dart` | `SynthesizeRequest` | `SynthesizeResponse` | **VERIFIED** | Synthesizes backend `spoken_summary` into audio bytes. |
| `/api/v1/farms/` | `POST` | `farmer_app` | `farm_api_service.dart` | `CreateFarmRequest` | `FarmIdentity` | **VERIFIED** | Registers farm with crop, tillable area, soil type, and location. |
| `/api/v1/farms/{id}/summary` | `GET` | `farmer_app` | `farm_summary_api_service.dart`| — | `FarmSummary` | **VERIFIED** | Fetches composite health, active advisories, and plan references. |
| `/api/v1/land/verify` | `POST` | `farmer_app` | `land_api_service.dart` | `LandSubmissionRequest` | `LandRecordResponse` | **VERIFIED** | Supports HTTP 200 (auto-verified) & 202 (queued for officer review). |
| `/api/v1/land/{id}` | `GET` | `farmer_app` | `land_api_service.dart` | — | `LandRecordResponse` | **VERIFIED** | Polls verification status, confirmed area, and officer notes. |
| `/api/v1/farms/{id}/health` | `GET` | `farmer_app` | `health_api_service.dart` | — | `HealthSnapshot` | **VERIFIED** | Supports object map & array subindices; handles `score: null` (unrated). |
| `/api/v1/farms/{id}/health/history` | `GET` | `farmer_app` | `health_api_service.dart` | — | `HealthHistoryResponse` | **VERIFIED** | Renders score trajectory with triggering audit factor. |
| `/api/v1/diagnose/{id}` | `POST` | `farmer_app` | `diagnosis_api_service.dart` | `DiagnoseRequest` | `DiagnosisResponse` | **VERIFIED** | Enforces confidence gate (Rule 1 & 2); prioritizes `spoken_summary`. |
| `/api/v1/resource-plan/{id}` | `POST` | `farmer_app` | `resource_plan_api_service.dart`| — | `ResourcePlan` | **VERIFIED** | Deserializes FAO-56 `irrigation_plan` (`et0_mm_day`, `kc_factor`, `daily_liters_total`). |
| `/api/v1/resource-plan/{id}` | `GET` | `farmer_app` | `resource_plan_api_service.dart`| — | `ResourcePlan` | **VERIFIED** | Fetches latest computed irrigation and seed requirement. |
| `/api/v1/schemes/match` | `POST` | `farmer_app` | `schemes_api_service.dart` | `{ farm_id }` | `List<SchemeSummary>` | **VERIFIED** | Handles HTTP 409 `LAND_NOT_VERIFIED` with dedicated guided state. |
| `/api/v1/schemes/{id}` | `GET` | `farmer_app` | `schemes_api_service.dart` | — | `SchemeDetail` | **VERIFIED** | Displays benefits, subsidies, eligibility, and required documents. |
| `/api/v1/timeline/{id}` | `GET` | `farmer_app` | `timeline_api_service.dart` | — | `FarmTimeline` | **VERIFIED** | Displays chronological lifecycle activities with status tags. |
| `/api/v1/followup/checkin` | `POST` | `farmer_app` | `followup_api_service.dart` | `FollowupRequest` | `FollowupResponse` | **VERIFIED** | Check-in (`improved`/`no_change`/`got_worse`); auto-escalates. |
| `/api/v1/escalation/create` | `POST` | `farmer_app` | `escalation_api_service.dart` | `EscalationRequest` | `EscalationResponse` | **VERIFIED** | Submits farm case to assigned KVK agronomist center. |
| `/api/v1/agronomist/queue` | `GET` | `kvk_portal` | `kvk_api.ts` | `{ cursor, limit }` | `KvkCaseQueueResponse` | **VERIFIED** | Supports cursor pagination (`next_cursor`, `total`, `cases[]`). |
| `/api/v1/agronomist/case/{id}`| `GET` | `kvk_portal` | `kvk_api.ts` | — | `KvkCase` | **VERIFIED** | Fetches full multimodal case summary, AI advisory, and photos. |
| `/api/v1/agronomist/resolve` | `POST` | `kvk_portal` | `kvk_api.ts` | `ResolveCaseRequest` | `ResolveCaseResponse` | **VERIFIED** | Submits agronomist prescription and resolves escalation. |
| `/api/v1/officer/queue` | `GET` | `officer_portal` | `officer_api.ts` | `{ cursor, limit }` | `LandQueueResponse` | **VERIFIED** | Supports cursor pagination (`next_cursor`, `items[]`) & GeoJSON. |
| `/api/v1/officer/action` | `POST` | `officer_portal` | `officer_api.ts` | `OfficerActionRequest` | `ReviewLandResponse` | **VERIFIED** | Records revenue officer boundary approval/rejection with notes. |

---

## 3. Key Feature Reconciliations

### 3.1 Diagnosis `spoken_summary` Integration
- **Model:** `DiagnosisResponse.spokenSummary` maps `json['spoken_summary']`.
- **UI Execution:** `DiagnosisResultScreen` uses `response.spokenSummary ?? fallbackGeneratedSummary`.
- **TTS Delivery:** Spoken agricultural advice is dispatched directly to `voiceController.synthesizeAndSpeak(speechSummary)`.

### 3.2 Daily Brief Conversational Summary
- **Model:** `DailyBriefResponse.spokenSummary` maps `json['spoken_summary']`.
- **Audio Action:** Home and daily brief audio buttons speak the backend-generated conversational brief.

### 3.3 Land Verification Gating on Government Schemes
- **HTTP 409 & Error Code:** `SchemesScreen` catches `LAND_NOT_VERIFIED` and HTTP 409 conflicts.
- **Guided UI:** Displays the "Land Verification Required" prompt with a primary CTA button navigating directly to `/land/$farmId/boundary`.
- **Normal Flow:** Verified farms display the full matched subsidies list without obstruction.

### 3.4 Cursor-Based Queue Pagination
- **KVK Portal (`CaseQueue`):** Supports `KvkCaseQueueResponse` with `next_cursor` tracking, loading skeletons, error retry, and "Load More Cases" actions.
- **Officer Portal (`LandQueueList`):** Supports `LandQueueResponse` with `next_cursor` tracking, filter tabs (`All`, `Pending`, `Verified`), and "Load More Records" actions.

### 3.5 Health Subindices Compatibility
- **Dual Format Ingestion:** `HealthSubIndices.fromJson` normalizes both:
  1. Object Map: `{ environmental_suitability: 0.85, resource_adequacy: 0.78, ... }`
  2. Array of Subindices: `[ { key: "environmental_suitability", value: 0.85, weight: 0.20, contribution: 17.0 }, ... ]`
- **Unrated Handling:** `score: null` / `band: "unrated"` displays "Unrated — Not enough data yet".

### 3.6 Degraded Bandwidth & Offline Resilience
- **Network State:** `ConnectivityService` monitors signal quality and emits `online`, `degraded`, or `unavailable`.
- **Banner UI:** `DegradedNetworkBanner` alerts the farmer with non-intrusive status when network connectivity is constrained.
