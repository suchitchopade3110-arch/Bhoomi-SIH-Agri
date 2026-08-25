// Runtime config for talking to the real Bhoomi backend. Mirrors the
// core/config/env.ts pattern used by kvk_portal and officer_portal.
export const env = {
  apiBaseUrl: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  enableLiveApi: import.meta.env.VITE_ENABLE_LIVE_API !== 'false',
  demo: {
    farmerPhone: import.meta.env.VITE_DEMO_FARMER_PHONE || '+919944400001',
    officerPhone: import.meta.env.VITE_DEMO_OFFICER_PHONE || '+919944400002',
    agronomistPhone: import.meta.env.VITE_DEMO_AGRONOMIST_PHONE || '+919944400003',
    password: import.meta.env.VITE_DEMO_PASSWORD || 'bhoomi123',
  },
};
