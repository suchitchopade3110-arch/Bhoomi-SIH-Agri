import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'land_api_service.dart';
import 'models/land_record_response.dart';
import 'models/land_submission_request.dart';

final landRepositoryProvider = Provider<LandRepository>((ref) {
  final apiService = ref.watch(landApiServiceProvider);
  return LandRepository(apiService);
});

class LandRepository {
  final LandApiService _apiService;

  LandRepository(this._apiService);

  Future<LandRecordResponse> submitLand({
    required String farmId,
    required LandSubmissionRequest request,
  }) async {
    return await _apiService.submitLand(farmId: farmId, request: request);
  }

  Future<LandRecordResponse> getLandRecord(String landId) async {
    return await _apiService.getLandRecord(landId);
  }
}
