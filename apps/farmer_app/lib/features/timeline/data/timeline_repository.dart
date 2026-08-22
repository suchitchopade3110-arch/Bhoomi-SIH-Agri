import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'models/timeline_event.dart';
import 'timeline_api_service.dart';

final timelineRepositoryProvider = Provider<TimelineRepository>((ref) {
  final apiService = ref.watch(timelineApiServiceProvider);
  return TimelineRepository(apiService);
});

class TimelineRepository {
  final TimelineApiService _apiService;

  TimelineRepository(this._apiService);

  Future<FarmTimeline> getTimeline(String farmId) async {
    return await _apiService.getTimeline(farmId);
  }
}

