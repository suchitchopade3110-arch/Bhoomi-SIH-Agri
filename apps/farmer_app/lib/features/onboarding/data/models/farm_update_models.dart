class FarmUpdateRequest {
  final String? farmName;
  final String? primaryCrop;
  final String? growthStage;
  final String? region;
  final String? sowingDate;
  final String? soilType;
  final String? irrigationSource;

  const FarmUpdateRequest({
    this.farmName,
    this.primaryCrop,
    this.growthStage,
    this.region,
    this.sowingDate,
    this.soilType,
    this.irrigationSource,
  });

  Map<String, dynamic> toJson() => {
        if (farmName != null) 'farm_name': farmName,
        if (primaryCrop != null) 'primary_crop': primaryCrop,
        if (growthStage != null) 'growth_stage': growthStage,
        if (region != null) 'region': region,
        if (sowingDate != null) 'sowing_date': sowingDate,
        if (soilType != null) 'soil_type': soilType,
        if (irrigationSource != null) 'irrigation_source': irrigationSource,
      };
}

class ThinLandSubmissionRequest {
  final String surveyNumber;

  const ThinLandSubmissionRequest({required this.surveyNumber});

  Map<String, dynamic> toJson() => {
        'survey_number': surveyNumber,
      };
}

class ThinLandSubmissionResponse {
  final String farmId;
  final String surveyNumber;
  final String status;

  const ThinLandSubmissionResponse({
    required this.farmId,
    required this.surveyNumber,
    this.status = 'pending_verification',
  });

  factory ThinLandSubmissionResponse.fromJson(Map<String, dynamic> json) =>
      ThinLandSubmissionResponse(
        farmId: json['farm_id']?.toString() ?? '',
        surveyNumber: json['survey_number']?.toString() ?? '',
        status: json['status']?.toString() ?? 'pending_verification',
      );

  Map<String, dynamic> toJson() => {
        'farm_id': farmId,
        'survey_number': surveyNumber,
        'status': status,
      };
}
