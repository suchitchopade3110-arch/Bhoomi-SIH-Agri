import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'followup_api_service.dart';
import 'models/followup_models.dart';

final followupRepositoryProvider = Provider<FollowupRepository>((ref) {
  final apiService = ref.watch(followupApiServiceProvider);
  return FollowupRepository(apiService);
});

class FollowupRepository {
  final FollowupApiService _apiService;

  FollowupRepository(this._apiService);

  Future<FollowupResponse> submitFollowup({
    required String farmId,
    required FollowupRequest request,
  }) async {
    return await _apiService.submitFollowup(farmId: farmId, request: request);
  }
}
