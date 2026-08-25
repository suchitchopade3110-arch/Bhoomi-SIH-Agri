class CaseSummaryBundleModel {
  final String crop;
  final String region;
  final String growthStage;
  final List<dynamic> problemHistory;
  final List<dynamic> images;
  final List<String> treatmentsTried;
  final String? followupTrend;
  final String? currentAdvisory;

  const CaseSummaryBundleModel({
    required this.crop,
    required this.region,
    required this.growthStage,
    this.problemHistory = const [],
    this.images = const [],
    this.treatmentsTried = const [],
    this.followupTrend,
    this.currentAdvisory,
  });

  factory CaseSummaryBundleModel.fromJson(Map<String, dynamic> json) =>
      CaseSummaryBundleModel(
        crop: json['crop']?.toString() ?? '',
        region: json['region']?.toString() ?? '',
        growthStage: json['growth_stage']?.toString() ?? '',
        problemHistory: json['problem_history'] as List? ?? const [],
        images: json['images'] as List? ?? const [],
        treatmentsTried: (json['treatments_tried'] as List?)
                ?.map((e) => e.toString())
                .toList() ??
            const [],
        followupTrend: json['followup_trend']?.toString(),
        currentAdvisory: json['current_advisory']?.toString(),
      );

  Map<String, dynamic> toJson() => {
        'crop': crop,
        'region': region,
        'growth_stage': growthStage,
        'problem_history': problemHistory,
        'images': images,
        'treatments_tried': treatmentsTried,
        if (followupTrend != null) 'followup_trend': followupTrend,
        if (currentAdvisory != null) 'current_advisory': currentAdvisory,
      };
}

class CasePDFPayloadModel {
  final String caseId;
  final String farmId;
  final String farmerName;
  final String village;
  final String district;
  final String? assignedKvk;
  final String severity;
  final String status;
  final String generatedAt;
  final CaseSummaryBundleModel bundle;
  final String summaryHeadline;
  final String? prescribedActionsSummary;
  final String? shareUrl;

  const CasePDFPayloadModel({
    required this.caseId,
    required this.farmId,
    this.farmerName = 'Farmer',
    this.village = '',
    this.district = '',
    this.assignedKvk,
    required this.severity,
    required this.status,
    required this.generatedAt,
    required this.bundle,
    required this.summaryHeadline,
    this.prescribedActionsSummary,
    this.shareUrl,
  });

  factory CasePDFPayloadModel.fromJson(Map<String, dynamic> json) =>
      CasePDFPayloadModel(
        caseId: json['case_id']?.toString() ?? '',
        farmId: json['farm_id']?.toString() ?? '',
        farmerName: json['farmer_name']?.toString() ?? 'Farmer',
        village: json['village']?.toString() ?? '',
        district: json['district']?.toString() ?? '',
        assignedKvk: json['assigned_kvk']?.toString(),
        severity: json['severity']?.toString() ?? 'early',
        status: json['status']?.toString() ?? 'escalated',
        generatedAt: json['generated_at']?.toString() ?? '',
        bundle: json['bundle'] is Map<String, dynamic>
            ? CaseSummaryBundleModel.fromJson(json['bundle'] as Map<String, dynamic>)
            : const CaseSummaryBundleModel(
                crop: '',
                region: '',
                growthStage: '',
              ),
        summaryHeadline: json['summary_headline']?.toString() ?? '',
        prescribedActionsSummary: json['prescribed_actions_summary']?.toString(),
        shareUrl: json['share_url']?.toString(),
      );

  Map<String, dynamic> toJson() => {
        'case_id': caseId,
        'farm_id': farmId,
        'farmer_name': farmerName,
        'village': village,
        'district': district,
        if (assignedKvk != null) 'assigned_kvk': assignedKvk,
        'severity': severity,
        'status': status,
        'generated_at': generatedAt,
        'bundle': bundle.toJson(),
        'summary_headline': summaryHeadline,
        if (prescribedActionsSummary != null)
          'prescribed_actions_summary': prescribedActionsSummary,
        if (shareUrl != null) 'share_url': shareUrl,
      };
}
