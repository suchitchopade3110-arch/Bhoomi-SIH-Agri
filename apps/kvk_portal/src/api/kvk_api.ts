import { apiClient } from './client';
import {
  KvkCase,
  KvkCaseQueueResponse,
  ResolveCaseRequest,
  ResolveCaseResponse,
  HealthSnapshot,
} from '../features/cases/types/case.types';

function mapToKvkCase(item: any): KvkCase {
  const caseId = item.case_id || item.escalation_id || item.id || '';
  const farmId = item.farm_id || '';
  const farmerName = item.farmer_name || item.farmer_context?.farmer_name || 'Farmer';
  const village = item.village || item.farmer_context?.village || '';
  const district = item.district || item.farmer_context?.district || 'Erode, Tamil Nadu';
  const crop = item.crop || item.farmer_context?.crop || 'Samba Paddy';
  const growthStage = item.growth_stage || item.farmer_context?.growth_stage || 'Vegetative';
  const landVerified = item.land_verified ?? (item.land_status === 'verified' || item.farmer_context?.land_status === 'verified');
  const healthScore = item.health_score ?? (item.current_health_score !== undefined ? item.current_health_score : null);

  const images: string[] = Array.isArray(item.latest_images) && item.latest_images.length > 0
    ? item.latest_images
    : item.image_url
      ? [item.image_url]
      : ['https://images.unsplash.com/photo-1586771107445-d3ca888129ff?auto=format&fit=crop&q=80&w=800'];

  return {
    case_id: caseId,
    farm_id: farmId,
    farmer_name: farmerName,
    village: village,
    district: district,
    crop: crop,
    growth_stage: growthStage,
    health_score: healthScore,
    land_verified: landVerified,
    farmer_context: item.farmer_context || {
      farm_id: farmId,
      farmer_name: farmerName,
      village: village,
      district: village ? `${village}, ${district}` : district,
      crop: crop,
      growth_stage: growthStage,
      land_status: landVerified ? 'verified' : 'unverified',
      land_verified: landVerified,
    },
    problem_description:
      item.problem_summary ||
      item.problem_description ||
      'Crop anomaly reported by farmer requiring KVK agronomist review.',
    image_url: images[0],
    latest_images: images,
    previous_ai_advisory: item.previous_ai_advisory || {
      possible_issue: crop ? `${crop} Anomaly` : 'Observed Field Anomaly',
      confidence_level: 'medium',
      confidence_score: 0.68,
      actions: [
        'Drain excess standing water from field',
        'Avoid excessive nitrogen top-dressing',
      ],
      caution: 'Verify condition before applying chemical controls.',
    },
    timeline_summary: Array.isArray(item.timeline_summary) ? item.timeline_summary : [],
    followup_notes: item.followup_notes || (item.case_summary?.problem_summary ? item.case_summary.problem_summary : 'Referred for expert clinical review.'),
    escalation_reason: item.escalation_reason || (item.reason ? item.reason : 'Referred for expert KVK agronomist diagnosis and prescription.'),
    status: item.status === 'resolved' ? 'resolved' : item.status === 'under_review' ? 'under_review' : 'escalated_to_kvk',
    submission_timestamp: item.created_at || item.escalated_at || item.submission_timestamp || new Date().toISOString(),
    agronomist_advisory: item.agronomist_advisory || item.expert_advice || item.confirmed_diagnosis,
    prescribed_actions: item.prescribed_actions || item.prescribed_inputs,
    severity: item.severity === 'critical' ? 'critical' : item.severity === 'high' ? 'high' : item.severity === 'severe' ? 'high' : item.severity === 'moderate' ? 'moderate' : 'low',
    resolved_at: item.resolved_at || item.updated_at,
    agronomist: item.agronomist || item.agronomist_name || item.escalated_to,
    spoken_summary: item.spoken_summary,
  };
}

export const kvkApi = {
  getCaseQueue: async (params?: {
    cursor?: string;
    limit?: number;
  }): Promise<KvkCaseQueueResponse> => {
    let rawData: any;
    try {
      const res = await apiClient.get('/api/v1/agronomist/queue', { params });
      rawData = res.data;
    } catch {
      const res = await apiClient.get('/api/v1/kvk/cases', { params });
      rawData = res.data;
    }

    if (Array.isArray(rawData)) {
      const mapped = rawData.map(mapToKvkCase);
      return {
        cases: mapped,
        next_cursor: null,
        total: mapped.length,
      };
    }
    if (rawData && Array.isArray(rawData.cases)) {
      const mapped = rawData.cases.map(mapToKvkCase);
      return {
        cases: mapped,
        next_cursor: rawData.next_cursor || null,
        total: rawData.total || mapped.length,
      };
    }
    return {
      cases: [],
      next_cursor: null,
      total: 0,
    };
  },

  getCaseDetail: async (caseId: string): Promise<KvkCase> => {
    try {
      const res = await apiClient.get(`/api/v1/agronomist/case/${caseId}`);
      return mapToKvkCase(res.data);
    } catch {
      const res = await apiClient.get(`/api/v1/kvk/cases/${caseId}`);
      return mapToKvkCase(res.data);
    }
  },

  getFarmHealth: async (farmId: string): Promise<HealthSnapshot> => {
    const res = await apiClient.get<HealthSnapshot>(`/api/v1/health/${farmId}`);
    return res.data;
  },

  resolveCase: async (
    caseId: string,
    payload: ResolveCaseRequest
  ): Promise<ResolveCaseResponse> => {
    const agronomistPayload = {
      escalation_id: caseId,
      agronomist_id: 'agronomist_kvk_1',
      agronomist_name: 'Dr. S. Sundaram',
      confirmed_diagnosis: payload.agronomist_advisory,
      expert_advice: payload.agronomist_advisory,
      prescribed_inputs: payload.prescribed_actions,
      agronomist_advisory: payload.agronomist_advisory,
      prescribed_actions: payload.prescribed_actions,
      severity: payload.severity,
      status: 'resolved',
    };

    try {
      const res = await apiClient.post<any>(
        '/api/v1/agronomist/resolve',
        agronomistPayload
      );
      return {
        case_id: res.data.escalation_id || res.data.case_id || caseId,
        status: 'resolved',
        resolved_at: res.data.resolved_at || new Date().toISOString(),
        agronomist: res.data.agronomist || 'Dr. S. Sundaram (KVK Erode)',
      };
    } catch {
      const res = await apiClient.post<ResolveCaseResponse>(
        `/api/v1/kvk/cases/${caseId}/resolve`,
        payload
      );
      return res.data;
    }
  },
};

