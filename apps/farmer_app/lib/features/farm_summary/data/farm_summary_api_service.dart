import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/api/api_client.dart';
import '../../../shared/constants/api_constants.dart';
import 'models/farm_summary.dart';

final farmSummaryApiServiceProvider = Provider<FarmSummaryApiService>((ref) {
  return FarmSummaryApiService(ApiClient());
});

class FarmSummaryApiService {
  final ApiClient _apiClient;

  FarmSummaryApiService(this._apiClient);

  Future<FarmSummary> getFarmSummary(String farmId) async {
    final response = await _apiClient.get(
      ApiConstants.farmSummary(farmId),
    );

    if (response.data is Map<String, dynamic>) {
      return FarmSummary.fromJson(response.data as Map<String, dynamic>);
    } else {
      throw Exception('Invalid summary response payload format.');
    }
  }
}
