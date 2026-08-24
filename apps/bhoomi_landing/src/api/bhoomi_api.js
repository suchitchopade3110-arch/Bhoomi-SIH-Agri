// Typed(ish) calls against the real Bhoomi API, one per landing-page
// feature. Every function returns `null` on any failure (network down,
// backend not running, empty demo DB) instead of throwing, so callers can
// do `const live = await getX(); setState(live ?? LOCAL_FALLBACK)` and the
// page keeps working standalone.
import { apiRequest, loginDemo } from './client';
import { env } from './env';

async function safe(fn) {
  try {
    return await fn();
  } catch (err) {
    console.warn('[bhoomi_api] falling back to local demo data:', err.message);
    return null;
  }
}

/** The seeded farmer's first farm, or null if the API/DB isn't available. */
export async function getDemoFarm() {
  return safe(async () => {
    const farms = await apiRequest('farmer', '/api/v1/farms');
    return farms && farms.length > 0 ? farms[0] : null;
  });
}

export async function getFarmSummary(farmId) {
  return safe(() => apiRequest('farmer', `/api/v1/farms/${farmId}/summary`));
}

export async function getFarmHealth(farmId) {
  return safe(() => apiRequest('farmer', `/api/v1/farms/${farmId}/health`));
}

export async function getFarmTimeline(farmId) {
  return safe(() => apiRequest('farmer', `/api/v1/timeline/${farmId}`));
}

/** Grounded 5-point advisory for the "Ask Bhoomi" voice demo. */
export async function askAdvisory(farmId, queryText, lang = 'ta-IN') {
  return safe(() =>
    apiRequest('farmer', '/api/v1/advisory/query', {
      method: 'POST',
      body: JSON.stringify({ farm_id: farmId, query_text: queryText, lang }),
    })
  );
}

export async function getOfficerQueue() {
  return safe(() => apiRequest('officer', '/api/v1/officer/queue'));
}

export async function submitOfficerAction(parcelId, action, notes) {
  return safe(() =>
    apiRequest('officer', '/api/v1/officer/action', {
      method: 'POST',
      body: JSON.stringify({
        parcel_id: parcelId,
        action,
        officer_notes: notes,
      }),
    })
  );
}

export async function getAgronomistQueue() {
  return safe(() => apiRequest('agronomist', '/api/v1/agronomist/queue'));
}

export async function resolveAgronomistCase({ escalationId, diagnosis, advice, prescribedInputs }) {
  return safe(async () => {
    // The demo agronomist's own name/id come from /auth/me so the case
    // record shows a real, logged-in-as identity rather than a placeholder.
    const token = await loginDemo('agronomist');
    const me = await fetch(`${env.apiBaseUrl}/api/v1/auth/me`, {
      headers: { Authorization: `Bearer ${token}` },
    }).then((r) => r.json());

    return apiRequest('agronomist', '/api/v1/agronomist/resolve', {
      method: 'POST',
      body: JSON.stringify({
        escalation_id: escalationId,
        agronomist_id: me.id,
        agronomist_name: me.full_name,
        confirmed_diagnosis: diagnosis,
        expert_advice: advice,
        prescribed_inputs: prescribedInputs,
      }),
    });
  });
}
