import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/api/api_client.dart';
import '../../../shared/constants/api_constants.dart';
import 'models/scheme_summary.dart';

final schemesApiServiceProvider = Provider<SchemesApiService>((ref) {
  return SchemesApiService(ApiClient());
});

class SchemesApiService {
  final ApiClient _apiClient;

  SchemesApiService(this._apiClient);

  Future<List<SchemeSummary>> getSchemes(String farmId) async {
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
  }

  Future<SchemeDetail> getSchemeDetail(String schemeId) async {
    final response = await _apiClient.get(
      ApiConstants.schemeDetail(schemeId),
    );

    if (response.data is Map<String, dynamic>) {
      return SchemeDetail.fromJson(response.data as Map<String, dynamic>);
    }
    throw Exception('Invalid scheme detail format.');
  }

  Future<SchemeDetail> submitRequirements({
    required String farmId,
    required String schemeId,
    required Map<String, dynamic> additionalData,
  }) async {
    final response = await _apiClient.post(
      ApiConstants.schemeRequirements(farmId, schemeId),
      data: {'additional_data': additionalData},
    );

    if (response.data is Map<String, dynamic>) {
      return SchemeDetail.fromJson(response.data as Map<String, dynamic>);
    }
    throw Exception('Invalid scheme requirements response format.');
  }
}
