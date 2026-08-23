export interface GeoJSONPolygon {
  type: 'Polygon';
  coordinates: number[][][];
}

export interface FarmerStatedDetails {
  survey_no: string;
  area_acres: number;
}

export type LandVerificationStatus = 'pending_verification' | 'submitted' | 'under_review' | 'verified' | 'rejected';

export interface LandQueueItem {
  land_record_id: string;
  farm_id: string;
  farmer_stated: FarmerStatedDetails;
  boundary_geojson?: GeoJSONPolygon | null;
  submitted_at: string;
  status: LandVerificationStatus;
  rejection_reason?: string;
  verifier?: string;
  verified_at?: string;
}

export interface LandQueueResponse {
  items: LandQueueItem[];
  next_cursor?: string | null;
  total?: number;
}

export interface ReviewLandRequest {
  decision: 'verified' | 'rejected';
  reason?: string;
  boundary_geojson?: GeoJSONPolygon | null;
}

export interface ReviewLandResponse {
  land_record_id: string;
  status: 'verified' | 'rejected';
  verified_at?: string;
  verifier: string;
  rejection_reason?: string;
}
