import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/api/api_client.dart';
import '../../../shared/constants/api_constants.dart';
import 'models/daily_brief_response.dart';

final dailyBriefApiServiceProvider = Provider<DailyBriefApiService>((ref) {
  return DailyBriefApiService(ApiClient());
});

class DailyBriefApiService {
  final ApiClient _apiClient;

  DailyBriefApiService(this._apiClient);

  Future<DailyBriefResponse> getDailyBrief(String farmId) async {
    final response = await _apiClient.get(
      ApiConstants.dailyBrief(farmId),
    );

    if (response.data is Map<String, dynamic>) {
      return DailyBriefResponse.fromJson(response.data as Map<String, dynamic>);
    }
    throw Exception('Invalid daily brief payload format.');
  }
}
