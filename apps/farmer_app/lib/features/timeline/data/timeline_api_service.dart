import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/api/api_client.dart';
import '../../../shared/constants/api_constants.dart';
import 'models/timeline_event.dart';

final timelineApiServiceProvider = Provider<TimelineApiService>((ref) {
  return TimelineApiService(ApiClient());
});

class TimelineApiService {
  final ApiClient _apiClient;

  TimelineApiService(this._apiClient);

  Future<FarmTimeline> getTimeline(String farmId) async {
    final response = await _apiClient.get(
      ApiConstants.farmTimeline(farmId),
    );

    if (response.data is Map<String, dynamic>) {
      return FarmTimeline.fromJson(response.data as Map<String, dynamic>);
    }
    throw Exception('Invalid timeline response format.');
  }
}
