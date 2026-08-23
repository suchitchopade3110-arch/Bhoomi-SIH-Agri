class AdvisorySource {
  final String title;
  final String organization;
  final String? url;

  const AdvisorySource({
    required this.title,
    required this.organization,
    this.url,
  });

  factory AdvisorySource.fromJson(Map<String, dynamic> json) {
    return AdvisorySource(
      title: json['title'] as String? ?? '',
      organization: json['organization'] as String? ?? 'Agricultural Extension',
      url: json['url'] as String?,
    );
  }

  Map<String, dynamic> toJson() => {
        'title': title,
        'organization': organization,
        if (url != null) 'url': url,
      };
}

class DiagnosisResponse {
  final String diagnosisId;
  final String farmId;
  final String possibleIssue;
  final String confidenceLevel; // 'high' | 'medium' | 'low' | 'uncertain'
  final double? confidenceScore;
  final List<String> symptomsToCheck;
  final List<String> actions;
  final String? caution;
  final List<AdvisorySource> sources;
  final bool canEscalate;
  final String? spokenSummary;
  final String createdAt;

  const DiagnosisResponse({
    required this.diagnosisId,
    required this.farmId,
    required this.possibleIssue,
    required this.confidenceLevel,
    this.confidenceScore,
    required this.symptomsToCheck,
    required this.actions,
    this.caution,
    this.sources = const [],
    this.canEscalate = true,
    this.spokenSummary,
    required this.createdAt,
  });

  bool get isHighConfidence => confidenceLevel.toLowerCase() == 'high';
  bool get isMediumConfidence => confidenceLevel.toLowerCase() == 'medium' || confidenceLevel.toLowerCase() == 'moderate';
  bool get isLowConfidence => confidenceLevel.toLowerCase() == 'low' || confidenceLevel.toLowerCase() == 'uncertain';

  factory DiagnosisResponse.fromJson(Map<String, dynamic> json) {
    final advisory = json['advisory'] as Map<String, dynamic>?;
    final diag = json['diagnosis'] as Map<String, dynamic>?;
    final citations = json['citations'] as List?;

    final confidenceVal = (diag?['confidence'] as num?)?.toDouble() ??
        (json['confidence_score'] as num?)?.toDouble();

    String calculatedLevel = 'medium';
    if (confidenceVal != null) {
      if (confidenceVal >= 0.70) {
        calculatedLevel = 'high';
      } else if (confidenceVal >= 0.40) {
        calculatedLevel = 'medium';
      } else {
        calculatedLevel = 'low';
      }
    } else if (json['confidence_level'] != null) {
      calculatedLevel = json['confidence_level'] as String;
    }

    List<String> checks = [];
    if (advisory?['what_to_check'] is List) {
      checks = List<String>.from(advisory!['what_to_check'] as List);
    } else if (json['symptoms_to_check'] is List) {
      checks = List<String>.from(json['symptoms_to_check'] as List);
    }

    List<String> nextActions = [];
    if (advisory?['what_to_do_next'] is List) {
      nextActions = List<String>.from(advisory!['what_to_do_next'] as List);
    } else if (json['actions'] is List) {
      nextActions = List<String>.from(json['actions'] as List);
    }

    List<AdvisorySource> sourceList = [];
    if (citations != null && citations.isNotEmpty) {
      sourceList = citations.map((c) {
        if (c is Map<String, dynamic>) {
          return AdvisorySource(
            title: c['title'] as String? ?? c['doc_id'] as String? ?? 'Agronomic Protocol',
            organization: c['reviewed_on'] != null ? 'Reviewed: ${c['reviewed_on']}' : 'ICAR / TNAU Advisory',
            url: c['url'] as String?,
          );
        }
        return const AdvisorySource(title: 'Agricultural Extension', organization: 'ICAR');
      }).toList();
    } else if (json['sources'] is List) {
      sourceList = (json['sources'] as List)
          .map((s) => AdvisorySource.fromJson(s as Map<String, dynamic>))
          .toList();
    }

    return DiagnosisResponse(
      diagnosisId: json['problem_id'] as String? ?? json['diagnosis_id'] as String? ?? json['id'] as String? ?? '',
      farmId: json['farm_id'] as String? ?? '',
      possibleIssue: advisory?['possible_issue'] as String? ??
          diag?['label'] as String? ??
          json['possible_issue'] as String? ??
          (json['above_gate'] == false ? 'Low Confidence Detection — Escalation Recommended' : 'Observed Field Anomaly'),
      confidenceLevel: calculatedLevel,
      confidenceScore: confidenceVal,
      symptomsToCheck: checks,
      actions: nextActions,
      caution: advisory?['what_to_avoid'] as String? ?? json['caution'] as String?,
      sources: sourceList,
      canEscalate: json['can_escalate'] as bool? ?? (json['above_gate'] != true || json['escalation'] != null),
      spokenSummary: json['spoken_summary'] as String?,
      createdAt: json['created_at'] as String? ?? DateTime.now().toIso8601String(),
    );
  }

  Map<String, dynamic> toJson() => {
        'diagnosis_id': diagnosisId,
        'farm_id': farmId,
        'possible_issue': possibleIssue,
        'confidence_level': confidenceLevel,
        if (confidenceScore != null) 'confidence_score': confidenceScore,
        'symptoms_to_check': symptomsToCheck,
        'actions': actions,
        if (caution != null) 'caution': caution,
        'sources': sources.map((s) => s.toJson()).toList(),
        'can_escalate': canEscalate,
        if (spokenSummary != null) 'spoken_summary': spokenSummary,
        'created_at': createdAt,
      };
}
