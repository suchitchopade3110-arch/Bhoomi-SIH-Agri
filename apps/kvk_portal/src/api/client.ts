import axios, { AxiosInstance } from 'axios';
import { env } from '../core/config/env';
import { authStore } from '../core/auth/auth_store';
import { KvkCase, ResolveCaseResponse } from '../features/cases/types/case.types';

export const apiClient: AxiosInstance = axios.create({
  baseURL: env.apiBaseUrl,
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to attach JWT token
apiClient.interceptors.request.use((config) => {
  const token = authStore.getToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Mock database for offline/demo reliability
let mockCases: KvkCase[] = [
  {
    case_id: 'case_kvk_701',
    farm_id: 'f_1',
    farmer_context: {
      farm_id: 'f_1',
      farmer_name: 'Muthusamy K.',
      district: 'Erode, Tamil Nadu',
      crop: 'Samba Paddy (CR 1009)',
      growth_stage: 'Vegetative (Day 45)',
      soil_type: 'Clay Loam',
      land_status: 'verified',
    },
    problem_description: 'Paddy leaf margins turning yellow with wavy grayish-white drying. Lesions spreading across 40% of tillers after heavy rainfall.',
    image_url: 'https://images.unsplash.com/photo-1586771107445-d3ca888129ff?auto=format&fit=crop&q=80&w=800',
    previous_ai_advisory: {
      possible_issue: 'Bacterial Leaf Blight (Xanthomonas oryzae pv. oryzae)',
      confidence_level: 'high',
      confidence_score: 0.88,
      actions: [
        'Drain excess standing water from the field for 2-3 days',
        'Avoid application of top-dressing nitrogen fertilizers during active disease',
        'Spray fresh cow dung slurry extract (20%) or certified copper bactericide',
      ],
      caution: 'High humidity and excessive nitrogen application increase disease spread.',
    },
    followup_notes: 'Drained standing water 2 days ago. Symptoms expanded to new upper leaves. Farmer requested KVK agronomist review.',
    escalation_reason: 'Persistent yellowing with bacterial ooze symptoms on leaf tips despite water drainage.',
    status: 'escalated_to_kvk',
    submission_timestamp: '2026-08-21T09:15:00Z',
  },
  {
    case_id: 'case_kvk_702',
    farm_id: 'f_2',
    farmer_context: {
      farm_id: 'f_2',
      farmer_name: 'Lakshmi Narayanan',
      district: 'Thanjavur, Tamil Nadu',
      crop: 'Kuruvai Paddy (ADT 43)',
      growth_stage: 'Tillering (Day 32)',
      soil_type: 'Alluvial',
      land_status: 'verified',
    },
    problem_description: 'Spindle-shaped spots with brownish borders and grayish centers on leaf blades. Few central leaves showing blast lesions.',
    image_url: 'https://images.unsplash.com/photo-1592982537447-7440770cbfc9?auto=format&fit=crop&q=80&w=800',
    previous_ai_advisory: {
      possible_issue: 'Rice Blast (Magnaporthe oryzae)',
      confidence_level: 'medium',
      confidence_score: 0.72,
      actions: [
        'Avoid applying excess nitrogenous fertilizer',
        'Spray Tricyclazole 75% WP @ 0.6 g/litre of water',
      ],
    },
    followup_notes: 'Need agronomist dosage verification for Kuruvai ADT 43 crop stage.',
    escalation_reason: 'Early blast detection during high dew condensation window.',
    status: 'under_review',
    submission_timestamp: '2026-08-21T08:00:00Z',
  },
  {
    case_id: 'case_kvk_703',
    farm_id: 'f_3',
    farmer_context: {
      farm_id: 'f_3',
      farmer_name: 'P. Sengottaiyan',
      district: 'Salem, Tamil Nadu',
      crop: 'Tapioca / Cassava',
      growth_stage: 'Tuber Initiation',
      soil_type: 'Red Sandy Loam',
      land_status: 'verified',
    },
    problem_description: 'Severe leaf curling, mosaic mottling, and stunted terminal shoot growth.',
    status: 'resolved',
    submission_timestamp: '2026-08-20T14:30:00Z',
    agronomist_advisory: 'Confirmed Cassava Mosaic Disease (CMD) transmitted by whiteflies (Bemisia tabaci). Rogue out infected plants and apply neem oil 3% formulation.',
    prescribed_actions: [
      'Rogue out severely infected plants and bury away from field',
      'Spray Yellow Sticky Traps @ 12 traps/acre to monitor whitefly vectors',
      'Apply Diafenthiuron 50 WP @ 1.25 g/litre',
    ],
    severity: 'high',
    resolved_at: '2026-08-21T07:30:00Z',
    agronomist: 'Dr. S. Sundaram (KVK Erode)',
  },
];

// Response fallback interceptor for contract-exact API operations
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    const url = error.config?.url || '';
    const method = error.config?.method?.toLowerCase() || '';

    // GET /api/v1/agronomist/queue or /api/v1/kvk/cases
    if ((url.includes('/api/v1/agronomist/queue') || (url.includes('/api/v1/kvk/cases') && !url.includes('/resolve'))) && method === 'get') {
      const segments = url.split('/');
      const lastSegment = segments[segments.length - 1];
      if (lastSegment !== 'cases' && lastSegment !== 'queue') {
        // Individual case
        const found = mockCases.find((c) => c.case_id === lastSegment);
        if (found) return Promise.resolve({ data: found, status: 200 });
      } else {
        // Queue list
        return Promise.resolve({ data: mockCases, status: 200 });
      }
    }

    // GET /api/v1/agronomist/case/{id}
    if (url.includes('/api/v1/agronomist/case/') && method === 'get') {
      const segments = url.split('/');
      const caseId = segments[segments.length - 1];
      const found = mockCases.find((c) => c.case_id === caseId) || mockCases[0];
      return Promise.resolve({ data: found, status: 200 });
    }

    // POST /api/v1/agronomist/resolve or /api/v1/kvk/cases/{id}/resolve
    if (url.includes('/resolve') && method === 'post') {
      const payload = typeof error.config?.data === 'string' ? JSON.parse(error.config?.data || '{}') : (error.config?.data || {});
      const caseId = payload.escalation_id || (url.includes('/cases/') ? url.split('/')[url.split('/').length - 2] : 'case_kvk_701');

      const target = mockCases.find((c) => c.case_id === caseId);
      if (target) {
        target.status = 'resolved';
        target.agronomist_advisory = payload.agronomist_advisory || payload.expert_advice;
        target.prescribed_actions = payload.prescribed_actions || payload.prescribed_inputs;
        target.severity = payload.severity || 'high';
        target.resolved_at = new Date().toISOString();
        target.agronomist = `${authStore.getCurrentAgronomist().name} (${authStore.getCurrentAgronomist().kvkCenter})`;
      }

      const response: ResolveCaseResponse = {
        case_id: caseId,
        status: 'resolved',
        resolved_at: new Date().toISOString(),
        agronomist: `${authStore.getCurrentAgronomist().name} (${authStore.getCurrentAgronomist().kvkCenter})`,
      };

      return Promise.resolve({ data: response, status: 200 });
    }

    return Promise.reject(error);
  }
);
