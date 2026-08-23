import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'farm_api_service.dart';
import 'models/create_farm_request.dart';
import 'models/create_farm_response.dart';

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
}
