class FollowupRequest {
  final String diagnosisId;
  final String outcome; // 'improved' | 'no_change' | 'got_worse'
  final String? notes;

  const FollowupRequest({
    required this.diagnosisId,
    required this.outcome,
    this.notes,
  });

  Map<String, dynamic> toJson() => {
        'diagnosis_id': diagnosisId,
        'outcome': outcome,
        if (notes != null) 'notes': notes,
      };
}

class FollowupResponse {
  final String followupId;
  final String diagnosisId;
  final String outcome;
  final String status;
  final String nextSteps;
  final bool escalationRecommended;
  final String recordedAt;

  const FollowupResponse({
    required this.followupId,
    required this.diagnosisId,
    required this.outcome,
    required this.status,
    required this.nextSteps,
    required this.escalationRecommended,
    required this.recordedAt,
  });

  factory FollowupResponse.fromJson(Map<String, dynamic> json) {
    return FollowupResponse(
      followupId: json['followup_id'] as String? ?? json['id'] as String? ?? '',
      diagnosisId: json['problem_id'] as String? ?? json['diagnosis_id'] as String? ?? '',
      outcome: json['response'] as String? ?? json['outcome'] as String? ?? 'improved',
      status: json['status'] as String? ?? (json['auto_escalated'] == true ? 'escalated' : 'recorded'),
      nextSteps: json['next_steps'] as String? ??
          (json['auto_escalated'] == true
              ? 'Case auto-escalated to KVK Agronomist for priority inspection.'
              : 'Continue field monitoring according to advisory schedule.'),
      escalationRecommended: json['auto_escalated'] as bool? ?? json['escalation_recommended'] as bool? ?? false,
      recordedAt: json['created_at'] as String? ?? json['recorded_at'] as String? ?? DateTime.now().toIso8601String(),
    );
  }

  Map<String, dynamic> toJson() => {
        'followup_id': followupId,
        'diagnosis_id': diagnosisId,
        'outcome': outcome,
        'status': status,
        'next_steps': nextSteps,
        'escalation_recommended': escalationRecommended,
        'recorded_at': recordedAt,
      };
}
