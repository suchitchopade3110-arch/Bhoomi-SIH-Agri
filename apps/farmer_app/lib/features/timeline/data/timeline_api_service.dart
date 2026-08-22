import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/api/api_client.dart';
import '../../../core/api/api_exception.dart';
import '../../../shared/constants/api_constants.dart';
import 'models/timeline_event.dart';

final timelineApiServiceProvider = Provider<TimelineApiService>((ref) {
  return TimelineApiService(ApiClient());
});

class TimelineApiService {
  final ApiClient _apiClient;

  TimelineApiService(this._apiClient);

  Future<FarmTimeline> getTimeline(String farmId) async {
    try {
      final response = await _apiClient.get(
        ApiConstants.farmTimeline(farmId),
      );

      if (response.data is Map<String, dynamic>) {
        return FarmTimeline.fromJson(response.data as Map<String, dynamic>);
      }
      throw Exception('Invalid timeline response format.');
    } on NetworkException {
      if (ApiConstants.enableMockFallback) {
        return FarmTimeline(
          farmId: farmId,
          events: const [
            TimelineEvent(
              eventId: 'evt_1',
              eventType: 'onboarding',
              title: 'Farm Profile Created',
              summary: 'Registered 2.0 acres of Samba Paddy in Erode district.',
              timestamp: '2026-08-14T10:00:00Z',
              status: 'completed',
            ),
            TimelineEvent(
              eventId: 'evt_2',
              eventType: 'land_verification',
              title: 'Cadastral Boundary Verified',
              summary: 'Official revenue parcel FMB matched 2.0 acres.',
              timestamp: '2026-08-18T10:00:00Z',
              status: 'completed',
            ),
            TimelineEvent(
              eventId: 'evt_3',
              eventType: 'diagnosis',
              title: 'Bacterial Leaf Blight Advisory',
              summary: 'Bio-control treatment and drainage protocol issued.',
              timestamp: '2026-08-21T10:00:00Z',
              status: 'action_required',
            ),
          ],
        );
      }
      rethrow;
    }
  }
}
