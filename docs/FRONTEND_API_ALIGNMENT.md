# BHOOMI — Frontend & Mobile API Alignment Specification

> **Specification Document:** `docs/FRONTEND_API_ALIGNMENT.md`
> **Status:** Partially aligned — see corrections below. Previous revision of
> this document asserted "Fully Integrated & Verified" for several rows that
> do not match the live backend or the actual client code; those rows are
> corrected in place rather than left to stand.
> **Target Environment:** Monorepo Ecosystem (`apps/farmer_app`, `apps/kvk_portal`, `apps/officer_portal`)
> **Base API Prefix:** `/api/v1`

---

## 1. Executive Summary

This document tracks the API contract alignment between the BHOOMI FastAPI
backend and its three clients:
1. **Farmer Mobile App** (`apps/farmer_app` — Flutter)
2. **KVK Agronomist Portal** (`apps/kvk_portal` — React + TypeScript)
3. **Revenue Officer Portal** (`apps/officer_portal` — React + TypeScript)

Every row below was checked directly against the live router source
(`services/api/app/api/v1/*.py`) and the actual client call sites — not
against a prior version of this document. Where a prior revision's claim
didn't hold up, the discrepancy is called out explicitly in §3 rather than
silently replaced, since another draft of this doc may already be in
someone else's hands.

---

## 2. Endpoint Alignment Registry

### SECTION A — LIVE ROUTE VERIFICATION MATRIX

| Application | Feature | Method | Live Backend Route | Client Call Site | Status | Notes |
|---|---|---|---|---|---|---|
| `farmer_app` | Register Farm | `POST` | `/api/v1/farms` | `ApiConstants.farms` | **LIVE** | No trailing slash; returns 201 Created |
| `farmer_app` | Get Farm Details | `GET` | `/api/v1/farms/{farm_id}` | `ApiConstants.farmDetail(id)` | **LIVE** | Core farm identity |
| `farmer_app` | Update Farm Profile | `PUT` | `/api/v1/farms/{farm_id}` | — | **NOT WIRED** | Backend route exists (`farms.py`). `ApiClient` has no `.put()` method at all and no call site exists — `farmDetail(id)` is only ever used for `GET`. See §3.1. |
| `farmer_app` | Farm Summary | `GET` | `/api/v1/farms/{farm_id}/summary` | `ApiConstants.farmSummary(id)` | **LIVE** | Daily brief, weather, and farm identity |
| `farmer_app` | Farm Risk Score | `GET` | `/api/v1/farms/{farm_id}/risk` | `ApiConstants.farmHealth(id)` | **LIVE** | Composite risk score & subindices. Route is `/risk`, not `/health` — see §3.2 |
| `farmer_app` | Risk History | `GET` | `/api/v1/farms/{farm_id}/risk/history` | `ApiConstants.farmHealthHistory(id)` | **LIVE** | Ordered risk-snapshot history |
| `farmer_app` | Risk Recompute | `POST` | `/api/v1/farms/{farm_id}/risk/recompute` | `ApiConstants.farmHealthRecompute(id)` | **LIVE** | Force risk score recompute |
| `farmer_app` | Crop Diagnosis | `POST` | `/api/v1/farms/{farm_id}/diagnose` | `ApiConstants.farmDiagnose(id)` | **LIVE** | Confidence-gated diagnosis & advisory |
| `farmer_app` | Advisory Query | `POST` | `/api/v1/advisory/query` | `ApiConstants.advisoryQuery` | **LIVE** | Direct RAG knowledge query |
| `farmer_app` | Farm Timeline | `GET` | `/api/v1/timeline/{farm_id}` | `ApiConstants.farmTimeline(id)` | **LIVE** | Chronological farm events |
| `farmer_app` | Timeline Events | `POST` | `/api/v1/timeline/events` | `ApiConstants.timelineEvents` | **LIVE** | Log timeline event |
| `farmer_app` | Follow-up Check-in | `POST` | `/api/v1/followup/checkin` | `ApiConstants.followupCheckin` | **LIVE** | Follow-up outcome reporting |
| `farmer_app` | Create Escalation | `POST` | `/api/v1/escalation/create` | `ApiConstants.escalationCreate` | **LIVE** | Forward case to KVK center |
| `farmer_app` | Escalation Detail | `GET` | `/api/v1/escalation/{escalation_id}` | `ApiConstants.escalationRecord(id)` | **LIVE** | Escalation status by ID |
| `farmer_app` | Cadastral Lookup | — | *(no such route)* | — | **DOES NOT EXIST** | Deliberately cut from scope — `land.py`'s own module docstring: "HITL-only — no automated cadastral lookup (SIH26131 feature checklist §13.3: 'cut')." The `ApiConstants.landCadastralLookup` constant that pointed at this was removed. See §3.3. |
| `farmer_app` | Land Verification | `POST` | `/api/v1/land/verify` | `ApiConstants.landVerify` | **LIVE** | Submits `survey_number` + optional `patta_passbook_asset_id` only — **no GeoJSON polygon field exists** on this request. See §3.3. |
| `farmer_app` | Farm Land Status | `GET` | `/api/v1/land/{farm_id}` | `ApiConstants.farmLand(id)` | **LIVE** | Retrieves verification status |
| `farmer_app` | Calculate Resource Plan | `POST` | `/api/v1/resource-plan/{farm_id}` | `ApiConstants.resourcePlan(id)` | **LIVE** | FAO-56 irrigation calculation |
| `farmer_app` | Get Resource Plan | `GET` | `/api/v1/resource-plan/{farm_id}` | `ApiConstants.latestResourcePlan(id)` | **LIVE** | Retrieves latest plan |
| `farmer_app` | Schemes Match | `POST` | `/api/v1/schemes/match` | `ApiConstants.schemesMatch` | **LIVE** | Matches government subsidies |
| `farmer_app` | Scheme Detail | `GET` | `/api/v1/schemes/{scheme_id}` | `ApiConstants.schemeDetail(id)` | **LIVE** | Eligibility guidelines & application link |
| `farmer_app` | Farm-scoped Schemes | `GET` | `/api/v1/farms/{farm_id}/schemes` | — | **NOT WIRED** | Route exists (`farms.py`); no Flutter constant or call site. App only uses the generic `schemesMatch`/`schemeDetail`. |
| `farmer_app` | Presigned URL | `POST` | `/api/v1/assets/presigned-url` | `ApiConstants.assetsPresign` | **LIVE** | S3 / MinIO / local upload link (see `STORAGE_BACKEND`) |
| `farmer_app` | Asset Detail | `GET` | `/api/v1/assets/{asset_id}` | `ApiConstants.assetDetail(id)` | **LIVE** | Retrieve uploaded asset metadata |
| `farmer_app` | Voice Transcribe | `POST` | `/api/v1/voice/transcribe` | `ApiConstants.voiceTranscribe` | **LIVE** | ASR speech-to-text |
| `farmer_app` | Voice Confirm | `POST` | `/api/v1/voice/confirm` | — | **NOT WIRED** | Read-back confirmation step (PRD §5.1 / feature checklist §1: "reads back each field for confirmation before saving") — route exists, nothing calls it. |
| `farmer_app` | Voice Synthesize | `POST` | `/api/v1/voice/synthesize` | `ApiConstants.voiceSynthesize` | **LIVE** | TTS text-to-speech |
| `farmer_app` | Voice Query (e2e) | `POST` | `/api/v1/voice/query` | `ApiConstants.voiceQuery` | **LIVE** | End-to-end voice query |
| `farmer_app` | Auth Register/Login/OTP | `POST`/`GET` | `/api/v1/auth/*` | — | **NOT WIRED** | No auth/OTP call site anywhere in `apps/farmer_app/lib`. Not tracked in `FEATURE_CHECKLIST.md` either — see §5. |
| `farmer_app` | Guidance Cards | `GET` | `/api/v1/guidance`, `/api/v1/guidance/{crop}` | — | **NOT WIRED** | Tracked as a pending checklist item (§7, "interim guidance card — C") but has no constant or call site yet. |
| `farmer_app` | Alerts | `GET`/`POST` | `/api/v1/farms/{farm_id}/alerts`, `/api/v1/alerts/{alert_id}/acknowledge` | — | **NOT WIRED** | Whole feature checklist §9 (early-warning alerts) unimplemented on the client. |
| `farmer_app` | Treatment Efficacy | `GET` | `/api/v1/treatments/{treatment_id}/efficacy` | — | **NOT WIRED** | Checklist §11 — scope itself still marked undecided in the checklist. |
| `officer_portal`| Land Queue | `GET` | `/api/v1/officer/queue` | `officerApi.getLandQueue` | **LIVE** | Parcels pending HITL review |
| `officer_portal`| Officer Review Detail | `GET` | `/api/v1/officer/review/{parcel_id}` | — | **NOT CALLED** | Backend route exists (`OfficerReviewDetail` schema); `officer_portal` never calls it — it renders parcel detail from the queue list response instead. |
| `officer_portal`| Officer Action | `POST` | `/api/v1/officer/action` | `officerApi.reviewLand` | **LIVE, WITH CAVEAT** | Client sends `confirmed_boundary_geojson`, `officer_id`, `officer_name` in the payload; `OfficerActionRequest` only defines `parcel_id`/`action`/`officer_notes` — the extra fields are silently ignored server-side (Pydantic's default `extra="ignore"`), not an error, but not persisted either. Matches the "no boundary correction UI" cut (`FEATURE_CHECKLIST.md` §10.2) — the client-side polygon UI has nothing on the backend to receive it. |
| `kvk_portal` | Agronomist Queue | `GET` | `/api/v1/agronomist/queue` | `kvkApi.getCaseQueue` | **LIVE** | Escalated farmer cases |
| `kvk_portal` | Agronomist Case Detail | `GET` | `/api/v1/agronomist/case/{escalation_id}` | `kvkApi.getCaseDetail` | **LIVE** | Living case file bundle |
| `kvk_portal` | Agronomist Resolve Case | `POST` | `/api/v1/agronomist/resolve` | `kvkApi.resolveCase` | **LIVE** | Dispatches clinical diagnosis |
| `kvk_portal` | Farm Risk (labelled "Health") | `GET` | `/api/v1/farms/{farm_id}/risk` | `kvkApi.getFarmHealth` | **LIVE** | Client already calls the correct `/risk` path despite the `getFarmHealth` name — see §3.2 |
| `kvk_portal` | Case PDF Payload | `GET` | `/api/v1/agronomist/case/{escalation_id}/pdf-payload` | — | **NOT WIRED** | Checklist §7: "Case PDF: backend payload + Flutter share sheet — C". Route exists; no portal or app call site yet. |

---

## 3. Corrections to the Prior Revision of This Document

The previous version of this file marked every row above "LIVE VERIFIED"
regardless of whether that held up. These are the specific claims that
didn't:

1. **"Update Farm Profile" was never actually wired.** The prior doc listed
   `PUT /api/v1/farms/{farm_id}` as verified via `ApiConstants.farmDetail(id)`.
   In reality `farmDetail(id)` is a `GET`-only constant, and
   `apps/farmer_app/lib/core/api/api_client.dart`'s `ApiClient` doesn't
   define a `.put()` method at all — there is no way the app could have
   made this call. No farm-edit flow exists on the client today.

2. **The health/risk route name was "resolved" to the wrong path.** The
   prior doc's §3 claimed the fix was renaming the frontend constant to
   `/api/v1/farms/{farm_id}/health` and called that the "correct backend
   route." The actual live router (`services/api/app/api/v1/health.py`)
   mounts this under `/farms/{farm_id}/risk`, tagged "Farm Risk Score" —
   there is no `/health` path on this router at all. `kvk_portal`'s
   `kvkApi.getFarmHealth` already (correctly) calls `/risk`; only this
   document had the path wrong.

3. **"Cadastral Lookup" and "GeoJSON polygon" describe a feature that was
   deliberately cut, not implemented.** `POST /api/v1/land/cadastral-lookup`
   does not exist anywhere in `services/api/app/api/v1/land.py`, whose own
   docstring states auto-lookup was cut from SIH26131 scope in favor of
   HITL-only survey-number submission (feature checklist §10.1/§13.2/§13.3).
   `LandVerifyRequest` (`app/schemas/land.py`) has exactly two fields —
   `survey_number` and an optional `patta_passbook_asset_id` — no boundary
   geometry field exists to submit a polygon through. The dead
   `ApiConstants.landCadastralLookup` constant (never called from anywhere
   in the app) has since been removed from `apps/farmer_app`.

4. **Unverifiable toolchain claims.** The prior §4 stated `flutter analyze`,
   `flutter test`, and both portals' `npm run build` "passed cleanly." Given
   the discrepancies above — including a claimed-verified call site that
   the `ApiClient` has no method to make — those results could not have
   reflected the current alignment. This revision does not restate that
   claim; re-run those checks locally before trusting a "clean" status here
   again.

Everything else in the original registry (asset presign, voice
transcribe/synthesize, timeline, follow-up, escalation, resource-plan,
schemes match/detail, officer queue/action, agronomist queue/case/resolve)
was checked against the live router source for this revision and held up.

---

## 4. Verification Method

- **Route source of truth**: `services/api/app/api/v1/*.py` (the routers
  actually mounted by `services/api/app/main.py` via
  `services/api/app/api/v1/__init__.py`) — not `services/api/app/routers/`,
  a similarly-named directory that exists but is never imported by `main.py`.
- **Client call sites**: grepped directly in `apps/farmer_app/lib`,
  `apps/officer_portal/src`, `apps/kvk_portal/src` rather than assumed from
  constant names — a defined constant is not the same as a call site (see
  the `farmDetail`/`PUT` case above).
- **Schema fields**: checked against `services/api/app/schemas/*.py`
  directly, not inferred from endpoint names.

---

## 5. Known Gaps Not Yet Tracked Anywhere

`docs/FEATURE_CHECKLIST.md` already tracks most of §2's "NOT WIRED" rows as
pending checklist items (guidance cards §7, alerts §9, treatment efficacy
§11, land/schemes side-features §10, voice read-back confirmation §1, case
PDF §7). One gap is tracked in **neither** document: **auth/OTP
login/registration has no client call site and no checklist entry** —
`/api/v1/auth/register`, `/login`, `/me`, `/otp/request`, `/otp/verify` all
exist on the backend with nothing referencing them from
`apps/farmer_app/lib`, and `FEATURE_CHECKLIST.md` doesn't mention
authentication at all, including in its §13 "explicitly not in scope" list.
Worth a decision on whether this is intentionally deferred (e.g. a single
demo account) or a genuine oversight, so it either gets a checklist line or
gets documented as an explicit cut.
