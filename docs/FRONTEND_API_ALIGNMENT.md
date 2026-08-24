# BHOOMI — Frontend & Mobile API Alignment Specification

> **Specification Document:** `docs/FRONTEND_API_ALIGNMENT.md`  
> **Status:** Fully Integrated & Verified with Live Backend Routing  
> **Target Environment:** Monorepo Ecosystem (`apps/farmer_app`, `apps/kvk_portal`, `apps/officer_portal`)  
> **Base API Prefix:** `/api/v1`

---

## 1. Executive Summary

This document details the end-to-end API contract alignment between the BHOOMI FastAPI backend intelligence layer and all frontend/mobile applications:
1. **Farmer Mobile App** (`apps/farmer_app` — Flutter)
2. **KVK Agronomist Portal** (`apps/kvk_portal` — React + TypeScript)
3. **Revenue Officer Portal** (`apps/officer_portal` — React + TypeScript)

All endpoints, methods, and URL structures have been audited against the live FastAPI routes (`/api/v1/openapi.json`).

---

## 2. Endpoint Alignment Registry

### SECTION A — LIVE ROUTE VERIFICATION MATRIX

| Application | Feature | Method | Live Backend Route | Client Call Site | Status | Notes |
|---|---|---|---|---|---|---|
| `farmer_app` | Register Farm | `POST` | `/api/v1/farms` | `ApiConstants.farms` | **LIVE VERIFIED** | No trailing slash; returns 201 Created |
| `farmer_app` | Get Farm Details | `GET` | `/api/v1/farms/{farm_id}` | `ApiConstants.farmDetail(id)` | **LIVE VERIFIED** | Core farm identity |
| `farmer_app` | Update Farm Profile | `PUT` | `/api/v1/farms/{farm_id}` | `ApiConstants.farmDetail(id)` | **LIVE VERIFIED** | PUT method per backend `farms.py` |
| `farmer_app` | Farm Summary | `GET` | `/api/v1/farms/{farm_id}/summary` | `ApiConstants.farmSummary(id)` | **LIVE VERIFIED** | Daily brief, weather, and farm identity |
| `farmer_app` | Farm Health Snapshot | `GET` | `/api/v1/farms/{farm_id}/health` | `ApiConstants.farmHealth(id)` | **LIVE VERIFIED** | Composite health score & subindices |
| `farmer_app` | Health History | `GET` | `/api/v1/farms/{farm_id}/health/history` | `ApiConstants.farmHealthHistory(id)` | **LIVE VERIFIED** | Ordered cursor-paginated health logs |
| `farmer_app` | Health Recompute | `POST` | `/api/v1/farms/{farm_id}/health/recompute` | `ApiConstants.farmHealthRecompute(id)` | **LIVE VERIFIED** | Force health score recompute |
| `farmer_app` | Crop Diagnosis | `POST` | `/api/v1/farms/{farm_id}/diagnose` | `ApiConstants.farmDiagnose(id)` | **LIVE VERIFIED** | Confidence-gated diagnosis & advisory |
| `farmer_app` | Advisory Query | `POST` | `/api/v1/advisory/query` | `ApiConstants.advisoryQuery` | **LIVE VERIFIED** | Direct RAG knowledge query |
| `farmer_app` | Farm Timeline | `GET` | `/api/v1/timeline/{farm_id}` | `ApiConstants.farmTimeline(id)` | **LIVE VERIFIED** | Chronological farm events |
| `farmer_app` | Timeline Events | `POST` | `/api/v1/timeline/events` | `ApiConstants.timelineEvents` | **LIVE VERIFIED** | Log timeline event |
| `farmer_app` | Follow-up Check-in | `POST` | `/api/v1/followup/checkin` | `ApiConstants.followupCheckin` | **LIVE VERIFIED** | Follow-up outcome reporting |
| `farmer_app` | Create Escalation | `POST` | `/api/v1/escalation/create` | `ApiConstants.escalationCreate` | **LIVE VERIFIED** | Forward case to KVK center |
| `farmer_app` | Escalation Detail | `GET` | `/api/v1/escalation/{escalation_id}` | `ApiConstants.escalationRecord(id)` | **LIVE VERIFIED** | Escalation status by ID |
| `farmer_app` | Cadastral Lookup | `POST` | `/api/v1/land/cadastral-lookup` | `ApiConstants.landCadastralLookup` | **LIVE VERIFIED** | Automated boundary search |
| `farmer_app` | Land Verification | `POST` | `/api/v1/land/verify` | `ApiConstants.landVerify` | **LIVE VERIFIED** | Submits survey number & GeoJSON polygon |
| `farmer_app` | Farm Land Status | `GET` | `/api/v1/land/{farm_id}` | `ApiConstants.farmLand(id)` | **LIVE VERIFIED** | Retrieves verification status |
| `farmer_app` | Calculate Resource Plan | `POST` | `/api/v1/resource-plan/{farm_id}` | `ApiConstants.resourcePlan(id)` | **LIVE VERIFIED** | FAO-56 irrigation calculation |
| `farmer_app` | Get Resource Plan | `GET` | `/api/v1/resource-plan/{farm_id}` | `ApiConstants.latestResourcePlan(id)` | **LIVE VERIFIED** | Retrieves latest plan |
| `farmer_app` | Schemes Match | `POST` | `/api/v1/schemes/match` | `ApiConstants.schemesMatch` | **LIVE VERIFIED** | Matches government subsidies |
| `farmer_app` | Scheme Detail | `GET` | `/api/v1/schemes/{scheme_id}` | `ApiConstants.schemeDetail(id)` | **LIVE VERIFIED** | Eligibility guidelines & application link |
| `farmer_app` | Presigned URL | `POST` | `/api/v1/assets/presigned-url` | `ApiConstants.assetsPresign` | **LIVE VERIFIED** | S3 / MinIO upload link |
| `farmer_app` | Asset Detail | `GET` | `/api/v1/assets/{asset_id}` | `ApiConstants.assetDetail(id)` | **LIVE VERIFIED** | Retrieve uploaded asset metadata |
| `farmer_app` | Voice Transcribe | `POST` | `/api/v1/voice/transcribe` | `ApiConstants.voiceTranscribe` | **LIVE VERIFIED** | ASR speech-to-text |
| `farmer_app` | Voice Synthesize | `POST` | `/api/v1/voice/synthesize` | `ApiConstants.voiceSynthesize` | **LIVE VERIFIED** | TTS text-to-speech |
| `officer_portal`| Land Queue | `GET` | `/api/v1/officer/queue` | `officerApi.getLandQueue` | **LIVE VERIFIED** | Parcels pending HITL review |
| `officer_portal`| Officer Review Detail | `GET` | `/api/v1/officer/review/{parcel_id}` | `officerApi` | **LIVE VERIFIED** | Inspect parcel cadastral overlay |
| `officer_portal`| Officer Action | `POST` | `/api/v1/officer/action` | `officerApi.reviewLand` | **LIVE VERIFIED** | Approve / Reject with confirmed GeoJSON |
| `kvk_portal` | Agronomist Queue | `GET` | `/api/v1/agronomist/queue` | `kvkApi.getCaseQueue` | **LIVE VERIFIED** | Escalated farmer cases |
| `kvk_portal` | Agronomist Case Detail | `GET` | `/api/v1/agronomist/case/{escalation_id}` | `kvkApi.getCaseDetail` | **LIVE VERIFIED** | Living case file bundle |
| `kvk_portal` | Agronomist Resolve Case | `POST` | `/api/v1/agronomist/resolve` | `kvkApi.resolveCase` | **LIVE VERIFIED** | Dispatches clinical diagnosis |
| `kvk_portal` | Farm Treatment Health | `GET` | `/api/v1/farms/{farm_id}/health` | `kvkApi.getFarmHealth` | **LIVE VERIFIED** | Live health score recovery tracking |

---

## 3. Discrepancies Resolved in this Audit

1. **Health Score URL Path Mismatch**:
   - **Incorrect frontend constant**: `/api/v1/health/{farm_id}`
   - **Correct backend route**: `/api/v1/farms/{farm_id}/health` (under prefix `/farms`)
   - **Resolution**: Updated `ApiConstants.farmHealth`, `farmHealthHistory`, `farmHealthRecompute` in `farmer_app` and `kvkApi.getFarmHealth` in `kvk_portal`.

2. **Crop Diagnosis URL Path Mismatch**:
   - **Incorrect frontend constant**: `/api/v1/diagnose/{farm_id}`
   - **Correct backend route**: `/api/v1/farms/{farm_id}/diagnose` (under prefix `/farms`)
   - **Resolution**: Updated `ApiConstants.farmDiagnose` in `farmer_app`.

3. **Farm Registration Trailing Slash**:
   - **Incorrect frontend constant**: `/api/v1/farms/`
   - **Correct backend route**: `/api/v1/farms`
   - **Resolution**: Removed trailing slash to prevent HTTP 307 redirects on POST requests.

4. **Dead Fallback Routes in Portals**:
   - `officer_portal`: Removed dead fallback calls to `/api/v1/officer/land-queue` and `/api/v1/officer/land/{id}/review`.
   - `kvk_portal`: Removed dead fallback calls to `/api/v1/kvk/cases` and `/api/v1/kvk/cases/{id}/resolve`.

5. **Explicit Problem Statement Feature Flag Documentation**:
   - Documented `PROBLEM_STATEMENT=sih25076` in `.env.example` at root and in `services/api/.env.example`.
   - Under `sih25076` (demo default): `land`, `officer`, `resource_plan`, and `schemes` routers are mounted alongside core intelligence.

---

## 4. Verification Check Log

- **Live Route Dump**: Verified against `GET /api/v1/openapi.json`
- **End-to-End Live HTTP Tests**:
  - `GET /api/v1/farms/{farm_id}/health` -> Non-404 verified (HTTP 200)
  - `POST /api/v1/farms/{farm_id}/diagnose` -> Non-404 verified (HTTP 200)
  - `GET /api/v1/officer/queue` -> Non-404 verified (HTTP 200)
  - `GET /api/v1/agronomist/queue` -> Non-404 verified (HTTP 200)
- **Compilers / Linters**:
  - `flutter analyze` & `flutter test` in `apps/farmer_app` passed cleanly.
  - `npm run build` in `apps/kvk_portal` passed cleanly.
  - `npm run build` in `apps/officer_portal` passed cleanly.
