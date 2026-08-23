export type CaseStatus = 'escalated_to_kvk' | 'under_review' | 'resolved';

export interface FarmerContext {
  farm_id: string;
  farmer_name?: string;
  district?: string;
  crop: string;
  growth_stage: string;
  soil_type?: string;
  land_status: string;
}

export interface PreviousAiAdvisory {
  possible_issue: string;
  confidence_level: string;
  confidence_score?: number;
  actions: string[];
  caution?: string;
}

export interface KvkCase {
  case_id: string;
  farm_id: string;
  farmer_context: FarmerContext;
  problem_description: string;
  image_url?: string;
  previous_ai_advisory?: PreviousAiAdvisory;
  followup_notes?: string;
  escalation_reason?: string;
  status: CaseStatus;
  submission_timestamp: string;
  agronomist_advisory?: string;
  prescribed_actions?: string[];
  severity?: 'low' | 'moderate' | 'high' | 'critical';
  resolved_at?: string;
  agronomist?: string;
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
