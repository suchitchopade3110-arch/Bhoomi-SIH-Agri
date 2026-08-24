import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/api/api_client.dart';
import '../../../core/api/api_exception.dart';
import '../../../shared/constants/api_constants.dart';
import 'models/land_record_response.dart';
import 'models/land_submission_request.dart';

final landApiServiceProvider = Provider<LandApiService>((ref) {
  return LandApiService(ApiClient());
});

class LandApiService {
  final ApiClient _apiClient;

  LandApiService(this._apiClient);

  Future<LandRecordResponse> submitLand({
    required String farmId,
    required LandSubmissionRequest request,
  }) async {
    final payload = {
      'farm_id': farmId,
      'survey_number': request.surveyNo,
      'survey_no': request.surveyNo,
      'area_acres': request.areaAcres,
      if (request.boundaryGeojson != null) 'suggested_boundary': request.boundaryGeojson!.toJson(),
      if (request.boundaryGeojson != null) 'boundary_geojson': request.boundaryGeojson!.toJson(),
    };

    try {
      final response = await _apiClient.post(
        ApiConstants.landVerify,
        data: payload,
      );

      if (response.data is Map<String, dynamic>) {
        final map = Map<String, dynamic>.from(response.data as Map);
        if (response.statusCode == 202 && !map.containsKey('status')) {
          map['status'] = 'pending_verification';
        }
        if (!map.containsKey('farm_id')) map['farm_id'] = farmId;
        if (!map.containsKey('farmer_stated')) {
          map['farmer_stated'] = {
            'survey_no': request.surveyNo,
            'area_acres': request.areaAcres,
          };
        }
        return LandRecordResponse.fromJson(map);
      }
      throw Exception('Invalid land submission response payload.');
    } on NetworkException {
      if (ApiConstants.enableMockFallback) {
        return LandRecordResponse(
          landRecordId: 'parcel_erode_142',
          farmId: farmId,
          farmerStated: FarmerStatedLand(
            surveyNo: request.surveyNo,
            areaAcres: request.areaAcres,
          ),
          boundaryGeojson: request.boundaryGeojson,
          status: 'verified',
          submittedAt: DateTime.now().toIso8601String(),
          verifiedAt: DateTime.now().toIso8601String(),
          verifier: 'Taluk Revenue Officer (Erode)',
        );
      }
      rethrow;
    }
  }

  Future<LandRecordResponse> getLandRecord(String farmId) async {
    try {
      final response = await _apiClient.get(
        ApiConstants.farmLand(farmId),
      );

      if (response.data is Map<String, dynamic>) {
        return LandRecordResponse.fromJson(response.data as Map<String, dynamic>);
      }
      throw Exception('Invalid land record response payload.');
    } on NetworkException {
      if (ApiConstants.enableMockFallback) {
        return LandRecordResponse(
          landRecordId: 'parcel_erode_142',
          farmId: farmId,
          farmerStated: const FarmerStatedLand(
            surveyNo: '142/3B',
            areaAcres: 2.0,
          ),
          status: 'verified',
          submittedAt: DateTime.now().toIso8601String(),
          verifiedAt: DateTime.now().toIso8601String(),
          verifier: 'Taluk Revenue Officer (Erode)',
        );
      }
      rethrow;
    }
  }
}
