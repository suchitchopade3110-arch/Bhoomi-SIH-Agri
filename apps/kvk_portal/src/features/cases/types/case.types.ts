export type CaseStatus = 'escalated_to_kvk' | 'under_review' | 'resolved';

export interface TimelineMilestone {
  event_type?: string;
  title?: string;
  description?: string;
  timestamp?: string;
  severity?: string;
}

export interface FarmerContext {
  farm_id: string;
  farmer_name?: string;
  village?: string;
  district?: string;
  crop: string;
  growth_stage: string;
  soil_type?: string;
  land_status: string;
  land_verified?: boolean;
}

export interface PreviousAiAdvisory {
  possible_issue: string;
  confidence_level: string;
  confidence_score?: number;
  actions: string[];
  caution?: string;
}

export interface HealthSnapshot {
  farm_id: string;
  composite_score: number | null;
  health_band: string;
  environmental_suitability?: number;
  resource_adequacy?: number;
  crop_stage_progression?: number;
  active_problem_load?: number;
  monitoring_recency?: number;
  treatment_response?: number;
  computed_at?: string;
}

export interface KvkCase {
  case_id: string;
  farm_id: string;
  farmer_name?: string;
  village?: string;
  district?: string;
  crop?: string;
  growth_stage?: string;
  health_score?: number | null;
  land_verified?: boolean;
  farmer_context: FarmerContext;
  problem_description: string;
  image_url?: string;
  latest_images?: string[];
  previous_ai_advisory?: PreviousAiAdvisory;
  timeline_summary?: TimelineMilestone[];
  followup_notes?: string;
  escalation_reason?: string;
  status: CaseStatus;
  submission_timestamp: string;
  agronomist_advisory?: string;
  prescribed_actions?: string[];
  severity?: 'low' | 'moderate' | 'high' | 'critical' | 'early' | 'severe';
  resolved_at?: string;
  agronomist?: string;
  spoken_summary?: string;
}

export interface KvkCaseQueueResponse {
  cases: KvkCase[];
  next_cursor?: string | null;
  total?: number;
}

export interface ResolveCaseRequest {
  agronomist_advisory: string;
  prescribed_actions: string[];
  severity: 'low' | 'moderate' | 'high' | 'critical';
  status: 'resolved';
}

export interface ResolveCaseResponse {
  case_id: string;
  status: 'resolved';
  resolved_at: string;
  agronomist: string;
}

