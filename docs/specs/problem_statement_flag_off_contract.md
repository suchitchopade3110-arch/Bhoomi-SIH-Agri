# Flag-Off Contract: SIH26131-Only Endpoints

> **Document ID:** SPEC-FLAGOFF-001
> **Audience:** Frontend (Flutter `apps/farmer_app`, `apps/kvk_portal`)
> **Status:** Implemented — locked by `services/api/tests/unit/test_problem_statement_flag_off_contract.py`

## 1. What this covers

The backend serves one of two feature sets, selected by the
`PROBLEM_STATEMENT` environment flag:

| Value | Feature set |
| --- | --- |
| `sih26131` **(default, and what the demo runs)** | Pest surveillance: early-warning alerts + treatment efficacy |
| `sih25076` | Cadastral / resource planning; the alerts + efficacy endpoints are **not** part of the contract |

The flag is defined in `services/api/app/core/config.py` (re-exported from
`app/config.py`) with an explicit default of `"sih26131"`. It is never
undefined — an unset environment resolves to the default, and an
unrecognized value fails at startup rather than silently switching features
off.

This document defines the **exact response** you get from the SIH26131-only
endpoints when the server is *not* on `sih26131`.

## 2. Affected endpoints

| Method | Path | Feature id |
| --- | --- | --- |
| `GET` | `/api/v1/farms/{farm_id}/alerts` | `early_warning_alerts` |
| `POST` | `/api/v1/alerts/{alert_id}/acknowledge` | `early_warning_alerts` |
| `GET` | `/api/v1/treatments/{treatment_id}/efficacy` | `treatment_efficacy` |

> The efficacy endpoint's real path is `/treatments/{treatment_id}/efficacy`
> — sometimes referred to informally as "the `/efficacy` route".

## 3. The response

**HTTP status: `501 Not Implemented`.** Standard Bhoomi error envelope:

```json
{
  "error": {
    "code": "FEATURE_NOT_AVAILABLE",
    "message": "'early_warning_alerts' is not available under PROBLEM_STATEMENT=sih25076. It is part of the sih26131 feature set; set PROBLEM_STATEMENT=sih26131 to enable it.",
    "details": {
      "feature": "early_warning_alerts",
      "endpoint": "GET /api/v1/farms/{farm_id}/alerts",
      "active_problem_statement": "sih25076",
      "required_problem_statement": "sih26131"
    }
  }
}
```

Field guarantees:

| Field | Type | Guarantee |
| --- | --- | --- |
| `error.code` | `string` | Always exactly `"FEATURE_NOT_AVAILABLE"`. **Branch on this, not on the status code or the message.** |
| `error.message` | `string` | Human-readable, for logs and developer-facing surfaces. Wording may change; do not parse it. |
| `error.details.feature` | `string` | Stable id: `"early_warning_alerts"` or `"treatment_efficacy"`. Safe to branch on. |
| `error.details.endpoint` | `string` | The path template that was gated off. |
| `error.details.active_problem_statement` | `string` | What this deployment is running. |
| `error.details.required_problem_statement` | `string` | Always `"sih26131"`. |

`details` keys are additive-only: new keys may appear, existing ones will not
be removed or renamed without a version bump on this document.

### 3.1 What it is deliberately **not**

- **Not an empty `200`.** `{"active_alerts": []}` is indistinguishable from
  "this farm currently has no alerts", so the app would render a healthy
  empty state for a feature that does not exist on this server.
- **Not a `500`.** Nothing failed. A deployment configured for the other
  problem statement is a normal, expected state.
- **Not a bare `404`.** On `/farms/{farm_id}/alerts` a `404` cannot be told
  apart from "that farm id does not exist".

### 3.2 Authentication

The flag-off response is returned **before** authentication. A request with
no token, or an expired one, still gets `501 FEATURE_NOT_AVAILABLE` rather
than `401` — the answer does not depend on who is asking, and a client with a
stale token should learn the real reason the call will never succeed here.

Under `sih26131` the live routers apply normally: unauthenticated requests to
these paths get `401` as usual.

### 3.3 OpenAPI

Under `sih25076` these paths are **absent** from
`/api/v1/openapi.json`: the published schema describes only what the
deployment actually serves. Generated clients built from a `sih25076` schema
will not have these methods at all; a client built from the `sih26131` schema
and pointed at a `sih25076` server gets the `501` above.

## 4. Recommended client handling

```dart
// Flutter — pseudocode
if (response.statusCode == 501 &&
    body['error']?['code'] == 'FEATURE_NOT_AVAILABLE') {
  // Hide the Alerts / Efficacy entry point for this session.
  // Do NOT show an error toast, and do NOT retry — the answer is
  // deployment-configuration, stable for the lifetime of the server.
  featureRegistry.disable(body['error']['details']['feature']);
  return;
}
```

Cache the result per app session. Retrying, backing off, or surfacing a
"something went wrong" banner is wrong here: the response will not change
until the server is restarted with a different `PROBLEM_STATEMENT`.

To learn the active contract up front without probing a gated endpoint, call
`GET /` — it returns `{"contract": "SIH26131"}` (or `"SIH25076"`).

## 5. Where this lives in the backend

| Concern | File |
| --- | --- |
| Flag definition + default | `services/api/app/core/config.py` (`PROBLEM_STATEMENT`, `PROBLEM_STATEMENT_DEFAULT`) |
| Spec-path re-export | `services/api/app/config.py` |
| Error class (`501` / `FEATURE_NOT_AVAILABLE`) | `services/api/app/core/errors.py` (`FeatureNotAvailableError`) |
| Payload builder + `is_sih26131()` | `services/api/app/core/feature_flags.py` |
| Flag-off route stubs | `services/api/app/api/v1/feature_unavailable.py` |
| Router mounting | `services/api/app/api/v1/__init__.py` |
| Contract tests | `services/api/tests/unit/test_problem_statement_flag_off_contract.py` |
| Flag-definition tests | `services/api/tests/unit/test_problem_statement_flag_definition.py` |

Related: [`api_contract_sih26131_delta.md`](./api_contract_sih26131_delta.md)
(§1 gating strategy; note its §2.1/§2.3 supersession warning).
