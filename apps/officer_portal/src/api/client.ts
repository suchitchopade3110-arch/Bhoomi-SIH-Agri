import axios, { AxiosInstance, AxiosResponse, InternalAxiosRequestConfig } from 'axios';
import { env } from '../core/config/env';
import { authStore } from '../core/auth/auth_store';
import { LandQueueItem, ReviewLandResponse } from '../features/land_review/types/land.types';

// Default contract-exact demo state for development & testability
let mockQueueStore: LandQueueItem[] = [
  {
    land_record_id: 'l_1',
    farm_id: 'f_1',
    farmer_stated: {
      survey_no: '142/3B',
      area_acres: 2.0,
    },
    boundary_geojson: {
      type: 'Polygon',
      coordinates: [
        [
          [77.7214, 11.3412],
          [77.7289, 11.3415],
          [77.7285, 11.3478],
          [77.7211, 11.3475],
          [77.7214, 11.3412],
        ],
      ],
    },
    submitted_at: '2026-08-21T08:30:00Z',
    status: 'pending_verification',
  },
  {
    land_record_id: 'l_2',
    farm_id: 'f_2',
    farmer_stated: {
      survey_no: '88/1A',
      area_acres: 3.5,
    },
    boundary_geojson: {
      type: 'Polygon',
      coordinates: [
        [
          [77.7410, 11.3520],
          [77.7490, 11.3522],
          [77.7485, 11.3590],
          [77.7408, 11.3588],
          [77.7410, 11.3520],
        ],
      ],
    },
    submitted_at: '2026-08-21T07:15:00Z',
    status: 'pending_verification',
  },
  {
    land_record_id: 'l_3',
    farm_id: 'f_3',
    farmer_stated: {
      survey_no: '204/C',
      area_acres: 1.0,
    },
    boundary_geojson: {
      type: 'Polygon',
      coordinates: [
        [
          [77.7110, 11.3320],
          [77.7160, 11.3322],
          [77.7155, 11.3370],
          [77.7108, 11.3368],
          [77.7110, 11.3320],
        ],
      ],
    },
    submitted_at: '2026-08-20T16:45:00Z',
    status: 'verified',
  },
];

export const apiClient: AxiosInstance = axios.create({
  baseURL: env.apiBaseUrl,
  timeout: 15000,
  headers: {
    'Content-Type': 'application/json',
  },
});

apiClient.interceptors.request.use((config: InternalAxiosRequestConfig) => {
  const token = authStore.getToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Resilient Fallback interceptor when backend is offline or unauthenticated in demo environment
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (env.enableMockFallback) {
      const { url, method } = error.config || {};

      // GET /api/v1/officer/queue or /api/v1/officer/land-queue
      if ((url?.includes('/officer/queue') || url?.includes('/officer/land-queue')) && method?.toLowerCase() === 'get') {
        return Promise.resolve({
          data: [...mockQueueStore],
          status: 200,
          statusText: 'OK',
          headers: {},
          config: error.config,
        } as AxiosResponse);
      }

      // POST /api/v1/officer/action
      if (url?.includes('/officer/action') && method?.toLowerCase() === 'post') {
        const payload = typeof error.config?.data === 'string' ? JSON.parse(error.config?.data || '{}') : (error.config?.data || {});
        const landId = payload.parcel_id || 'l_1';
        const isVerified = payload.action === 'verify' || payload.decision === 'verified';

        // Update local mock state
        mockQueueStore = mockQueueStore.map((item) =>
          item.land_record_id === landId
            ? { ...item, status: isVerified ? ('verified' as const) : ('rejected' as const) }
            : item
        );

        const responsePayload: ReviewLandResponse = {
          land_record_id: landId,
          status: isVerified ? 'verified' : 'rejected',
          verified_at: new Date().toISOString(),
          verifier: authStore.getCurrentOfficer().verifierTag,
        };

        return Promise.resolve({
          data: responsePayload,
          status: 200,
          statusText: 'OK',
          headers: {},
          config: error.config,
        } as AxiosResponse);
      }
    }

    return Promise.reject(error);
  }
);
