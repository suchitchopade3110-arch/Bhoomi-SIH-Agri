class SchemeSummary {
  final String schemeId;
  final String title;
  final String shortDescription;
  final String matchStatus; // 'likely_relevant' | 'more_info_needed' | 'available'
  final String? matchExplanation;
  final List<String> missingRequirements;
  final String? benefitSummary;

  const SchemeSummary({
    required this.schemeId,
    required this.title,
    required this.shortDescription,
    required this.matchStatus,
    this.matchExplanation,
    this.missingRequirements = const [],
    this.benefitSummary,
  });

  bool get isLikelyRelevant => matchStatus.toLowerCase() == 'likely_relevant';
  bool get isMoreInfoNeeded => matchStatus.toLowerCase() == 'more_info_needed';

  factory SchemeSummary.fromJson(Map<String, dynamic> json) {
    return SchemeSummary(
      schemeId: json['scheme_id'] as String? ?? json['id'] as String? ?? '',
      title: json['title'] as String? ?? json['name'] as String? ?? '',
      shortDescription: json['short_description'] as String? ?? json['description'] as String? ?? '',
      matchStatus: json['match_status'] as String? ?? (json['status'] != null ? json['status'].toString() : 'likely_relevant'),
      matchExplanation: json['match_explanation'] as String?,
      missingRequirements: json['missing_requirements'] != null
          ? List<String>.from(json['missing_requirements'] as List)
          : [],
      benefitSummary: json['benefit_summary'] as String? ?? json['benefits'] as String?,
    );
  }

  Map<String, dynamic> toJson() => {
        'scheme_id': schemeId,
        'title': title,
        'short_description': shortDescription,
        'match_status': matchStatus,
        if (matchExplanation != null) 'match_explanation': matchExplanation,
        'missing_requirements': missingRequirements,
        if (benefitSummary != null) 'benefit_summary': benefitSummary,
      };
}

class SchemeDetail {
  final String schemeId;
  final String title;
  final String department;
  final String description;
  final String? matchExplanation;
  final List<String> benefits;
  final List<String> eligibilityCriteria;
  final List<String> requiredDocuments;
  final String? officialUrl;
  final String? helpline;

  const SchemeDetail({
    required this.schemeId,
    required this.title,
    required this.department,
    required this.description,
    this.matchExplanation,
    this.benefits = const [],
    this.eligibilityCriteria = const [],
    this.requiredDocuments = const [],
    this.officialUrl,
    this.helpline,
  });

  factory SchemeDetail.fromJson(Map<String, dynamic> json) {
    List<String> parsedBenefits = [];
    if (json['benefits'] is List) {
      parsedBenefits = List<String>.from(json['benefits'] as List);
    } else if (json['benefits'] is String) {
      parsedBenefits = [(json['benefits'] as String)];
    }

    List<String> parsedEligibility = [];
    if (json['eligibility_criteria'] is List) {
      parsedEligibility = List<String>.from(json['eligibility_criteria'] as List);
    } else if (json['eligibility_criteria'] is Map) {
      parsedEligibility = (json['eligibility_criteria'] as Map)
          .entries
          .map((e) => '${e.key}: ${e.value}')
          .toList();
    } else if (json['eligibility_criteria'] is String) {
      parsedEligibility = [(json['eligibility_criteria'] as String)];
    }

    return SchemeDetail(
      schemeId: json['scheme_id'] as String? ?? json['id'] as String? ?? '',
      title: json['title'] as String? ?? json['name'] as String? ?? '',
      department: json['department'] as String? ?? json['ministry'] as String? ?? 'Ministry of Agriculture & Farmers Welfare',
      description: json['description'] as String? ?? '',
      matchExplanation: json['match_explanation'] as String?,
      benefits: parsedBenefits,
      eligibilityCriteria: parsedEligibility,
      requiredDocuments: json['required_documents'] != null
          ? List<String>.from(json['required_documents'] as List)
          : [],
      officialUrl: json['official_url'] as String? ?? json['portal_url'] as String?,
      helpline: json['helpline'] as String?,
    );
  }

  Map<String, dynamic> toJson() => {
        'scheme_id': schemeId,
        'title': title,
        'department': department,
        'description': description,
        if (matchExplanation != null) 'match_explanation': matchExplanation,
        'benefits': benefits,
        'eligibility_criteria': eligibilityCriteria,
        'required_documents': requiredDocuments,
        if (officialUrl != null) 'official_url': officialUrl,
        if (helpline != null) 'helpline': helpline,
      };
}
