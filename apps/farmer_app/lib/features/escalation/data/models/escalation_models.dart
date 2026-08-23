class EscalationRequest {
  final String diagnosisId;
  final String reason;
  final String? imageAssetId;

  const EscalationRequest({
    required this.diagnosisId,
    required this.reason,
    this.imageAssetId,
  });

  Map<String, dynamic> toJson() => {
        'diagnosis_id': diagnosisId,
        'reason': reason,
        if (imageAssetId != null) 'image_asset_id': imageAssetId,
      };
}

class EscalationResponse {
  final String caseId;
  final String farmId;
  final String status; // 'escalated_to_kvk' | 'under_review' | 'resolved'
  final String submissionTimestamp;
  final String kvkCenter;
  final String estimatedReview;
  final String? expertResolution;
  final String? resolvedAt;
  final String? agronomist;

  const EscalationResponse({
    required this.caseId,
    required this.farmId,
    required this.status,
    required this.submissionTimestamp,
    required this.kvkCenter,
    required this.estimatedReview,
    this.expertResolution,
    this.resolvedAt,
    this.agronomist,
  });

  bool get isResolved => status.toLowerCase() == 'resolved';

  factory EscalationResponse.fromJson(Map<String, dynamic> json) {
    final caseSummary = json['case_summary'] as Map<String, dynamic>?;
    return EscalationResponse(
      caseId: json['escalation_id'] as String? ?? json['case_id'] as String? ?? json['id'] as String? ?? '',
      farmId: json['farm_id'] as String? ?? '',
      status: json['status'] as String? ?? 'escalated_to_kvk',
      submissionTimestamp: json['created_at'] as String? ?? json['submission_timestamp'] as String? ?? DateTime.now().toIso8601String(),
      kvkCenter: json['assigned_kvk_center'] as String? ?? json['kvk_center'] as String? ?? 'ICAR-KVK Erode Center',
      estimatedReview: json['estimated_review'] as String? ?? 'Within 24 business hours',
      expertResolution: caseSummary?['problem_summary'] as String? ?? json['expert_resolution'] as String?,
      resolvedAt: json['resolved_at'] as String?,
      agronomist: caseSummary?['escalated_to'] as String? ?? json['agronomist'] as String?,
    );
  }

  Map<String, dynamic> toJson() => {
        'case_id': caseId,
        'farm_id': farmId,
        'status': status,
        'submission_timestamp': submissionTimestamp,
        'kvk_center': kvkCenter,
        'estimated_review': estimatedReview,
        if (expertResolution != null) 'expert_resolution': expertResolution,
        if (resolvedAt != null) 'resolved_at': resolvedAt,
        if (agronomist != null) 'agronomist': agronomist,
      };
}
