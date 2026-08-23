import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../data/escalation_repository.dart';
import '../data/models/escalation_models.dart';

class EscalationState {
  final String reason;
  final bool isSubmitting;
  final EscalationResponse? response;
  final String? errorMessage;

  const EscalationState({
    this.reason = '',
    this.isSubmitting = false,
    this.response,
    this.errorMessage,
  });

  EscalationState copyWith({
    String? reason,
    bool? isSubmitting,
    EscalationResponse? response,
    String? errorMessage,
  }) {
    return EscalationState(
      reason: reason ?? this.reason,
      isSubmitting: isSubmitting ?? this.isSubmitting,
      response: response ?? this.response,
      errorMessage: errorMessage,
    );
  }
}

final escalationControllerProvider =
    StateNotifierProvider<EscalationController, EscalationState>((ref) {
  final repository = ref.watch(escalationRepositoryProvider);
  return EscalationController(repository);
});

class EscalationController extends StateNotifier<EscalationState> {
  final EscalationRepository _repository;

  EscalationController(this._repository) : super(const EscalationState());

  void setReason(String reason) {
    state = state.copyWith(reason: reason, errorMessage: null);
  }

  Future<EscalationResponse?> submitEscalation({
    required String farmId,
    required String diagnosisId,
    String? imageAssetId,
  }) async {
    if (state.isSubmitting) return null;

    state = state.copyWith(isSubmitting: true, errorMessage: null);

    try {
      final request = EscalationRequest(
        diagnosisId: diagnosisId,
        reason: state.reason.trim().isEmpty
            ? 'Crop symptoms persistent after recommended management. Requesting KVK agronomist review.'
            : state.reason.trim(),
        imageAssetId: imageAssetId,
      );

      final response = await _repository.submitEscalation(
        farmId: farmId,
        request: request,
      );

      state = state.copyWith(
        isSubmitting: false,
        response: response,
      );

      return response;
    } catch (e) {
      state = state.copyWith(
        isSubmitting: false,
        errorMessage: 'Unable to submit expert escalation. Please check your connection.',
      );
      return null;
    }
  }

  void reset() {
    state = const EscalationState();
  }
}
