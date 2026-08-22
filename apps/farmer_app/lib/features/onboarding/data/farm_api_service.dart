import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/api/api_client.dart';
import '../../../core/api/api_exception.dart';
import '../../../shared/constants/api_constants.dart';
import 'models/create_farm_request.dart';
import 'models/create_farm_response.dart';

final farmApiServiceProvider = Provider<FarmApiService>((ref) {
  return FarmApiService(ApiClient());
});

class FarmApiService {
  final ApiClient _apiClient;

  FarmApiService(this._apiClient);

  Future<CreateFarmResponse> createFarm(CreateFarmRequest request) async {
    try {
      final response = await _apiClient.post(
        ApiConstants.farms,
        data: request.toJson(),
      );

      if (response.data is Map<String, dynamic>) {
        return CreateFarmResponse.fromJson(response.data as Map<String, dynamic>);
      } else {
        throw Exception('Unexpected response format from farm creation API.');
      }
    } on NetworkException {
      if (ApiConstants.enableMockFallback) {
        return const CreateFarmResponse(
          id: 'farm_tamilnadu_001',
          landStatus: 'pending_verification',
          health: FarmHealthInitial(band: 'unrated', score: null),
        );
      }
      rethrow;
    }
  }
}
