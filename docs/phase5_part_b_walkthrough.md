# Phase 5 Part B — Risk Model Rewrite & SIH26131 Alignment Walkthrough

## Summary of Changes

Phase 5 Part B realigns the intelligence layer with the SIH26131 4-subindex risk model, cleans up routing inconsistencies, deletes drift-prone legacy packages, and validates the entire test suite.

### 1. Deleted Legacy Packages & Duplicates
- **`packages/shared/`**: Removed via `git rm -r packages/shared`. All runtime components import canonical enums from `app.core.enums` / `app.domain.enums`.
- **Duplicate Route Removed**: Deleted duplicate `GET /{farm_id}/risk` from `app/api/v1/farms.py`. The canonical scoring engine endpoint is mounted in `app/api/v1/health.py`.

### 2. Four-Subindex Risk Engine (`WEIGHTS_VERSION = "v2-sih26131"`)
- `SubIndexKey` now contains strictly the four SIH26131 sub-indices:
  1. `active_problem_severity` (Weight: `0.40`, Penalties: Early `30`, Moderate `55`, Severe `80`)
  2. `environmental_risk` (Weight: `0.25`, Temp penalty: `2.0/°C`, Humidity penalty: `1.25/%`)
  3. `monitoring_recency` (Weight: `0.15`, Recency penalty: `5.0/day`, Default `70`, Expert verified `90` / `95`)
  4. `treatment_response` (Weight: `0.20`, Default `70`, `got_worse`: `40`, `no_change`: `50`, `improved`: `90`, `resolved`: `95`)
- Obsolete formulas dropped: `resource_adequacy`, `crop_stage_progression`, `SOIL_MOISTURE_DEFICIT_PENALTY_PER_PCT`, `STAGE_DEVIATION_PENALTY_PER_DAY`.
- Updated `HealthScoreInputs`, `_missing_fields`, and `compute_all_subindices` in `app/domain/health/`.
- Updated Tamil health score delta reason mapping in `app/services/health_reason.py`.

### 3. API Surface & Route Gating
- `/farms/{farm_id}/health*` routes replaced with `/farms/{farm_id}/risk*` (`/risk`, `/risk/history`, `/risk/recompute`).
- Default `PROBLEM_STATEMENT` configured to `"sih26131"` in `app/core/config.py`.
- Under `sih26131`: `land_router`, `officer_router`, `schemes_router`, `alerts_router` and all core intelligence routers mount. `resource_plan_router` remains unmounted (`404`).
- `GET /farms/{id}/summary` returns qualitative condition trend card without numeric score or band.

### 4. Tests & Acceptance Verification
- `tests/domain/test_health_score.py`: Added pure unit test `test_sih26131_reconciliation` verifying the exact 82 → 73 → 57 → 91 score walk and breakdown contributions:
  - **Step 1 (Baseline)**: Active=100 (40.0), Env=70 (17.5), Recency=70 (10.5), Treatment=70 (14.0) = **82** (`HealthBand.GOOD`)
  - **Step 2 (Diagnosis - Early Stem Borer detected)**: Active=70 (28.0), Env=70 (17.5), Recency=90 (13.5), Treatment=70 (14.0) = **73** (`HealthBand.WATCH`)
  - **Step 3 (Follow-up - Got Worse)**: Active=45 (18.0), Env=70 (17.5), Recency=90 (13.5), Treatment=40 (8.0) = **57** (`HealthBand.POOR`)
  - **Step 4 (Resolution - Case Resolved)**: Active=100 (40.0), Env=70 (17.5), Recency=95 (14.25), Treatment=95 (19.0) = **91** (`HealthBand.EXCELLENT`)
- `tests/e2e/test_runbook.py`: End-to-end integration test updated and verified for the 82 → 73 → 57 → 91 walk.
- Full test suite passed: **415 passed in 10.41s**.

---

## Verification Evidence

### Runtime SubIndexKey Enum Check
```bash
python -c "from app.core.enums import SubIndexKey; print(sorted(e.value for e in SubIndexKey))"
# Output:
# ['active_problem_severity', 'environmental_risk', 'monitoring_recency', 'treatment_response']
```

### Pytest Full Suite Run
```
============================== test session starts ===============================
platform win32 -- Python 3.14.3, pytest-9.1.1, pluggy-1.6.0
rootdir: Bhoomi-SIH-Agri\services\api
configfile: pyproject.toml
plugins: anyio-4.12.1, langsmith-0.7.24, asyncio-1.4.0
collected 415 items

...
415 passed, 1794 warnings in 10.41s
==================================================================================
```
