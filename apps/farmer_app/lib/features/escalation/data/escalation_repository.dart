import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'escalation_api_service.dart';
import 'models/escalation_models.dart';

final escalationRepositoryProvider = Provider<EscalationRepository>((ref) {
  final apiService = ref.watch(escalationApiServiceProvider);
  return EscalationRepository(apiService);
});

class EscalationRepository {
  final EscalationApiService _apiService;

  EscalationRepository(this._apiService);

  Future<EscalationResponse> submitEscalation({
    required String farmId,
    required EscalationRequest request,
  }) async {
    return await _apiService.submitEscalation(farmId: farmId, request: request);
  }

  Future<EscalationResponse> getEscalationStatus(String caseId) async {
    return await _apiService.getEscalationStatus(caseId);
  }
}
