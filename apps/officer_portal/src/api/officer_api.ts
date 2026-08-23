import { apiClient } from './client';
import {
  LandQueueItem,
  LandQueueResponse,
  ReviewLandRequest,
  ReviewLandResponse,
} from '../features/land_review/types/land.types';

function mapToLandQueueItem(item: any): LandQueueItem {
  const parcelId = item.parcel_id || item.land_record_id || item.id || '';
  const farmId = item.farm_id || '';

  return {
    land_record_id: parcelId,
    farm_id: farmId,
    farmer_stated: {
      survey_no: item.survey_no || item.survey_number || item.farmer_stated?.survey_no || '142/3B',
      area_acres: item.area_acres || item.total_area_acres || item.farmer_stated?.area_acres || 2.4,
    },
    boundary_geojson: item.suggested_boundary || item.boundary_geojson || item.confirmed_boundary_geojson || null,
    submitted_at: item.created_at || item.submitted_at || new Date().toISOString(),
    status: item.status === 'verified' ? 'verified' : item.status === 'rejected' ? 'rejected' : 'pending_verification',
    rejection_reason: item.rejection_reason || item.officer_notes,
    verifier: item.verifier || item.officer_name,
    verified_at: item.verified_at || item.updated_at,
  };
}

export const officerApi = {
  getLandQueue: async (params?: {
    cursor?: string;
    limit?: number;
  }): Promise<LandQueueResponse> => {
    let rawData: any;
    try {
      const res = await apiClient.get('/api/v1/officer/queue', { params });
      rawData = res.data;
    } catch {
      const res = await apiClient.get('/api/v1/officer/land-queue', { params });
      rawData = res.data;
    }

    if (Array.isArray(rawData)) {
      const mapped = rawData.map(mapToLandQueueItem);
      return {
        items: mapped,
        next_cursor: null,
        total: mapped.length,
      };
    }
    if (rawData && Array.isArray(rawData.items)) {
      const mapped = rawData.items.map(mapToLandQueueItem);
      return {
        items: mapped,
        next_cursor: rawData.next_cursor || null,
        total: rawData.total || mapped.length,
      };
    }
    return {
      items: [],
      next_cursor: null,
      total: 0,
    };
  },

  reviewLand: async (
    landRecordId: string,
    payload: ReviewLandRequest
  ): Promise<ReviewLandResponse> => {
    const actionPayload = {
      parcel_id: landRecordId,
      action: payload.decision === 'verified' ? 'verify' : 'reject',
      confirmed_boundary_geojson: payload.boundary_geojson,
      officer_notes: payload.reason,
      officer_id: 'officer_erode_1',
      officer_name: 'M. Radhakrishnan (Tahsildar Erode)',
    };

    try {
      const res = await apiClient.post<any>('/api/v1/officer/action', actionPayload);
      return {
        land_record_id: res.data.parcel_id || landRecordId,
        status: res.data.status === 'verified' ? 'verified' : 'rejected',
        verified_at: res.data.updated_at || new Date().toISOString(),
        verifier: 'M. Radhakrishnan (Tahsildar Erode)',
        rejection_reason: res.data.officer_notes || payload.reason,
      };
    } catch {
      const res = await apiClient.post<ReviewLandResponse>(
        `/api/v1/officer/land/${landRecordId}/review`,
        payload
      );
      return res.data;
    }
  },
};
