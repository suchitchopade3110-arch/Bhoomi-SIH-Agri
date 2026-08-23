import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/api/api_client.dart';
import '../../../core/api/api_exception.dart';
import '../../../shared/constants/api_constants.dart';
import 'models/scheme_summary.dart';

final schemesApiServiceProvider = Provider<SchemesApiService>((ref) {
  return SchemesApiService(ApiClient());
});

class SchemesApiService {
  final ApiClient _apiClient;

  SchemesApiService(this._apiClient);

  Future<List<SchemeSummary>> getSchemes(String farmId) async {
    try {
      final response = await _apiClient.post(
        ApiConstants.schemesMatch,
        data: {'farm_id': farmId},
      );

      if (response.data is List) {
        return (response.data as List)
            .map((s) => SchemeSummary.fromJson(s as Map<String, dynamic>))
            .toList();
      } else if (response.data is Map<String, dynamic>) {
        final map = response.data as Map<String, dynamic>;
        final list = map['matched_schemes'] ?? map['schemes'] ?? map['items'];
        if (list is List) {
          return list
              .map((s) => SchemeSummary.fromJson(s as Map<String, dynamic>))
              .toList();
        }
      }
      throw Exception('Invalid schemes payload format.');
    } on NetworkException {
      if (ApiConstants.enableMockFallback) {
        return const [
          SchemeSummary(
            schemeId: 'pm_kisan',
            title: 'PM-KISAN Samman Nidhi',
            shortDescription: 'Direct income support of ₹6,000 per year in three equal installments to landholding farmer families.',
            matchStatus: 'likely_relevant',
            matchExplanation: 'Verified landholding size of 2.0 acres satisfies small/marginal farmer eligibility criteria.',
            missingRequirements: [],
            benefitSummary: '₹6,000 / year direct benefit transfer',
          ),
          SchemeSummary(
            schemeId: 'pmfby_crop_insurance',
            title: 'Pradhan Mantri Fasal Bima Yojana (PMFBY)',
            shortDescription: 'Comprehensive crop insurance covering non-preventable natural risks from pre-sowing to post-harvest.',
            matchStatus: 'likely_relevant',
            matchExplanation: 'Samba Paddy in Erode notified under PMFBY seasonal coverage.',
            missingRequirements: ['Sowing Certificate'],
            benefitSummary: 'Up to ₹35,000 / acre sum insured',
          ),
        ];
      }
      rethrow;
    }
  }

  Future<SchemeDetail> getSchemeDetail(String schemeId) async {
    try {
      final response = await _apiClient.get(
        ApiConstants.schemeDetail(schemeId),
      );

      if (response.data is Map<String, dynamic>) {
        return SchemeDetail.fromJson(response.data as Map<String, dynamic>);
      }
      throw Exception('Invalid scheme detail format.');
    } on NetworkException {
      if (ApiConstants.enableMockFallback) {
        return const SchemeDetail(
          schemeId: 'pm_kisan',
          title: 'PM-KISAN Samman Nidhi',
          department: 'Ministry of Agriculture & Farmers Welfare',
          description: 'Financial assistance for all landholding farmer families with cultivable land.',
          matchExplanation: 'Verified landholding size of 2.0 acres satisfies small/marginal farmer criteria.',
          benefits: [
            '₹6,000 per year transferred directly to Aadhaar-linked bank account',
            'Paid in three 4-monthly installments of ₹2,000 each',
          ],
          eligibilityCriteria: [
            'All landholding farmer families with cultivable land parcel records',
            'Excludes institutional landholders and high-income tax payees',
          ],
          requiredDocuments: [
            'Aadhaar Card',
            'Verified Land Ownership Record (Patta / Chitta / RoR)',
            'Bank Account Passbook',
          ],
          officialUrl: 'https://pmkisan.gov.in',
          helpline: '155261 / 011-24300606',
        );
      }
      rethrow;
    }
  }

  Future<SchemeDetail> submitRequirements({
    required String farmId,
    required String schemeId,
    required Map<String, dynamic> additionalData,
  }) async {
    try {
      final response = await _apiClient.post(
        ApiConstants.schemeRequirements(farmId, schemeId),
        data: {'additional_data': additionalData},
      );

      if (response.data is Map<String, dynamic>) {
        return SchemeDetail.fromJson(response.data as Map<String, dynamic>);
      }
      throw Exception('Invalid submission response.');
    } on NetworkException {
      if (ApiConstants.enableMockFallback) {
        return await getSchemeDetail(schemeId);
      }
      rethrow;
    }
  }
}
