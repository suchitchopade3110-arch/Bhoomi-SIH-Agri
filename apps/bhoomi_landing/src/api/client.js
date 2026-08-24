// Minimal fetch wrapper for the Bhoomi FastAPI backend + a demo-login
// helper. The landing page is a public pitch deck, not an authenticated
// app, so "login" here just means: obtain a JWT for one of the three
// seeded demo accounts (farmer/officer/agronomist) so we can show real
// data behind each portal preview. Every call is wrapped by the callers
// in bhoomi_api.js so a network failure quietly falls back to the local
// demo data in src/data/ instead of breaking the page.
import { env } from './env';

const TOKEN_CACHE_KEY = 'bhoomi_landing_demo_tokens';

function readTokenCache() {
  try {
    return JSON.parse(sessionStorage.getItem(TOKEN_CACHE_KEY) || '{}');
  } catch {
    return {};
  }
}

function writeTokenCache(cache) {
  try {
    sessionStorage.setItem(TOKEN_CACHE_KEY, JSON.stringify(cache));
  } catch {
    // sessionStorage unavailable (private mode, SSR, etc.) — fine, just
    // means we re-login next call instead of caching.
  }
}

async function request(path, options = {}) {
  const res = await fetch(`${env.apiBaseUrl}${path}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...(options.headers || {}),
    },
  });

  if (!res.ok) {
    const body = await res.text().catch(() => '');
    throw new Error(`${options.method || 'GET'} ${path} -> ${res.status}: ${body}`);
  }

  if (res.status === 204) return null;
  return res.json();
}

/**
 * Logs in as one of the three seeded demo accounts and returns a bearer
 * token, caching it for the tab session so repeated modal opens don't
 * re-authenticate every time.
 */
export async function loginDemo(role) {
  const cache = readTokenCache();
  if (cache[role]) return cache[role];

  const phone = {
    farmer: env.demo.farmerPhone,
    officer: env.demo.officerPhone,
    agronomist: env.demo.agronomistPhone,
  }[role];

  if (!phone) throw new Error(`Unknown demo role: ${role}`);

  const data = await request('/api/v1/auth/login', {
    method: 'POST',
    body: JSON.stringify({ phone_number: phone, password: env.demo.password }),
  });

  cache[role] = data.access_token;
  writeTokenCache(cache);
  return data.access_token;
}

/** Authenticated GET/POST against the live API as a given demo role. */
export async function apiRequest(role, path, options = {}) {
  if (!env.enableLiveApi) throw new Error('Live API disabled (VITE_ENABLE_LIVE_API=false)');
  const token = await loginDemo(role);
  return request(path, {
    ...options,
    headers: {
      Authorization: `Bearer ${token}`,
      ...(options.headers || {}),
    },
  });
}
