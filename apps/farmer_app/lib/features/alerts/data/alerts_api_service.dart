import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/api/api_client.dart';
import '../../../core/api/api_exception.dart';
import '../../../shared/constants/api_constants.dart';
import 'models/alert_models.dart';

final alertsApiServiceProvider = Provider<AlertsApiService>((ref) {
  return AlertsApiService(ApiClient());
});

class AlertsApiService {
  final ApiClient _apiClient;

  AlertsApiService(this._apiClient);

  Future<FarmAlertsResponseModel> getFarmAlerts(String farmId) async {
    try {
      final response = await _apiClient.get(
        ApiConstants.farmAlerts(farmId),
      );

      if (response.data is Map<String, dynamic>) {
        return FarmAlertsResponseModel.fromJson(response.data as Map<String, dynamic>);
      }
      throw Exception('Invalid farm alerts response payload.');
    } on NetworkException {
      if (ApiConstants.enableMockFallback) {
        return FarmAlertsResponseModel(
          farmId: farmId,
          activeAlerts: [
            AlertItemModel(
              alertId: 'alert_blb_erode_01',
              pathogenName: 'Bacterial Leaf Blight',
              severity: 'warning',
              triggerReason: 'High humidity (>85%) and spatial cluster outbreak in 5km radius.',
              preventativeAction: 'Drain standing water and reduce nitrogen fertilizer.',
              inspectionTasks: const [
                'Check field border rows for water-soaked leaf lesions.',
                'Inspect 20 random hills across diagonal walk.',
              ],
              spokenSummary: 'BLB alert in your area. Please inspect border rows.',
              createdAt: DateTime.now().toIso8601String(),
              expiresAt: DateTime.now().add(const Duration(days: 3)).toIso8601String(),
            ),
          ],
        );
      }
      rethrow;
    }
  }

  Future<AlertAcknowledgeResponse> acknowledgeAlert(
    String alertId,
    AlertAcknowledgeRequest request,
  ) async {
    try {
      final response = await _apiClient.post(
        ApiConstants.alertAcknowledge(alertId),
        data: request.toJson(),
      );

      if (response.data is Map<String, dynamic>) {
        return AlertAcknowledgeResponse.fromJson(response.data as Map<String, dynamic>);
      }
      throw Exception('Invalid alert acknowledge response payload.');
    } on NetworkException {
      if (ApiConstants.enableMockFallback) {
        return AlertAcknowledgeResponse(
          status: 'acknowledged',
          alertId: alertId,
        );
      }
      rethrow;
    }
  }
}
