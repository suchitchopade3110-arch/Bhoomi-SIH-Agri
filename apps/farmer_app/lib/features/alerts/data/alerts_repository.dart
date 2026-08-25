import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'alerts_api_service.dart';
import 'models/alert_models.dart';

final alertsRepositoryProvider = Provider<AlertsRepository>((ref) {
  final apiService = ref.watch(alertsApiServiceProvider);
  return AlertsRepository(apiService);
});

class AlertsRepository {
  final AlertsApiService _apiService;

  AlertsRepository(this._apiService);

  Future<FarmAlertsResponseModel> getFarmAlerts(String farmId) async {
    return await _apiService.getFarmAlerts(farmId);
  }

  Future<AlertAcknowledgeResponse> acknowledgeAlert({
    required String alertId,
    required String farmId,
    String reason = 'action_taken',
  }) async {
    return await _apiService.acknowledgeAlert(
      alertId,
      AlertAcknowledgeRequest(farmId: farmId, reason: reason),
    );
  }
}
