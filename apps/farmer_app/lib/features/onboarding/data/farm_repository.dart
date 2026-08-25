import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'farm_api_service.dart';
import 'models/create_farm_request.dart';
import 'models/create_farm_response.dart';
import 'models/farm_update_models.dart';

final farmRepositoryProvider = Provider<FarmRepository>((ref) {
  final apiService = ref.watch(farmApiServiceProvider);
  return FarmRepository(apiService);
});

class FarmRepository {
  final FarmApiService _apiService;

  FarmRepository(this._apiService);

  Future<CreateFarmResponse> createFarm(CreateFarmRequest request) async {
    return await _apiService.createFarm(request);
  }

  Future<Map<String, dynamic>> updateFarm(String farmId, FarmUpdateRequest request) async {
    return await _apiService.updateFarm(farmId, request);
  }

  Future<ThinLandSubmissionResponse> submitFarmLand(String farmId, ThinLandSubmissionRequest request) async {
    return await _apiService.submitFarmLand(farmId, request);
  }
}
