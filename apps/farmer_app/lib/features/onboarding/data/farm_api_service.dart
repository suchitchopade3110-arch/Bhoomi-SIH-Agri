import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/api/api_client.dart';
import '../../../core/api/api_exception.dart';
import '../../../shared/constants/api_constants.dart';
import 'models/create_farm_request.dart';
import 'models/create_farm_response.dart';
import 'models/farm_update_models.dart';

final farmApiServiceProvider = Provider<FarmApiService>((ref) {
  return FarmApiService(ApiClient());
});

class FarmApiService {
  final ApiClient _apiClient;

  FarmApiService(this._apiClient);

  /// GET /farms — every farm owned by the authenticated user. The router's
  /// post-login/post-OTP-verify redirect uses this to find a real farm_id
  /// instead of navigating to a hardcoded one that won't exist server-side.
  Future<List<Map<String, dynamic>>> listMyFarms() async {
    final response = await _apiClient.get(ApiConstants.farms);
    if (response.data is List) {
      return (response.data as List).cast<Map<String, dynamic>>();
    }
    throw Exception('Unexpected response format from farm listing API.');
  }

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

  Future<Map<String, dynamic>> updateFarm(String farmId, FarmUpdateRequest request) async {
    final response = await _apiClient.put(
      ApiConstants.updateFarm(farmId),
      data: request.toJson(),
    );

    if (response.data is Map<String, dynamic>) {
      return response.data as Map<String, dynamic>;
    }
    throw Exception('Unexpected response format from farm update API.');
  }

  Future<ThinLandSubmissionResponse> submitFarmLand(String farmId, ThinLandSubmissionRequest request) async {
    final response = await _apiClient.post(
      ApiConstants.farmLandLink(farmId),
      data: request.toJson(),
    );

    if (response.data is Map<String, dynamic>) {
      return ThinLandSubmissionResponse.fromJson(response.data as Map<String, dynamic>);
    }
    throw Exception('Unexpected response format from farm land submission API.');
  }
}
