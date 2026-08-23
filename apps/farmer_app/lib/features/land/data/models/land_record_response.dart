import 'land_submission_request.dart';

class FarmerStatedLand {
  final String surveyNo;
  final double areaAcres;

  const FarmerStatedLand({
    required this.surveyNo,
    required this.areaAcres,
  });

  factory FarmerStatedLand.fromJson(Map<String, dynamic> json) {
    return FarmerStatedLand(
      surveyNo: json['survey_no'] as String? ?? '',
      areaAcres: (json['area_acres'] as num?)?.toDouble() ?? 0.0,
    );
  }

  Map<String, dynamic> toJson() => {
        'survey_no': surveyNo,
        'area_acres': areaAcres,
      };
}

class LandRecordResponse {
  final String landRecordId;
  final String farmId;
  final FarmerStatedLand farmerStated;
  final GeoJsonPolygonData? boundaryGeojson;
  final String submittedAt;
  final String status; // 'submitted' | 'under_review' | 'pending_verification' | 'verified' | 'rejected'
  final String? verifier;
  final String? verifiedAt;
  final String? rejectionReason;

  const LandRecordResponse({
    required this.landRecordId,
    required this.farmId,
    required this.farmerStated,
    this.boundaryGeojson,
    required this.submittedAt,
    required this.status,
    this.verifier,
    this.verifiedAt,
    this.rejectionReason,
  });

  bool get isVerified => status == 'verified';
  bool get isPending => status == 'pending_verification' || status == 'submitted' || status == 'under_review';
  bool get isRejected => status == 'rejected';

  factory LandRecordResponse.fromJson(Map<String, dynamic> json) {
    return LandRecordResponse(
      landRecordId: json['land_record_id'] as String? ?? json['parcel_id'] as String? ?? json['id'] as String? ?? '',
      farmId: json['farm_id'] as String? ?? '',
      farmerStated: FarmerStatedLand.fromJson(
        json['farmer_stated'] as Map<String, dynamic>? ?? {},
      ),
      boundaryGeojson: json['boundary_geojson'] != null
          ? GeoJsonPolygonData.fromJson(json['boundary_geojson'] as Map<String, dynamic>)
          : json['suggested_boundary'] != null
              ? GeoJsonPolygonData.fromJson(json['suggested_boundary'] as Map<String, dynamic>)
              : null,
      submittedAt: json['submitted_at'] as String? ?? '',
      status: json['status'] as String? ?? 'pending_verification',
      verifier: json['verifier'] as String?,
      verifiedAt: json['verified_at'] as String?,
      rejectionReason: json['officer_notes'] as String? ?? json['rejection_reason'] as String? ?? json['reason'] as String?,
    );
  }

  Map<String, dynamic> toJson() => {
        'land_record_id': landRecordId,
        'farm_id': farmId,
        'farmer_stated': farmerStated.toJson(),
        if (boundaryGeojson != null) 'boundary_geojson': boundaryGeojson!.toJson(),
        'submitted_at': submittedAt,
        'status': status,
        if (verifier != null) 'verifier': verifier,
        if (verifiedAt != null) 'verified_at': verifiedAt,
        if (rejectionReason != null) 'rejection_reason': rejectionReason,
      };
}
