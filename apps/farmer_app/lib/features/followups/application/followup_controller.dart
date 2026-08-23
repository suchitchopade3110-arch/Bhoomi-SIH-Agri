import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../data/followup_repository.dart';
import '../data/models/followup_models.dart';

class FollowupState {
  final String? selectedOutcome; // 'improved' | 'no_change' | 'got_worse'
  final String notes;
  final bool isSubmitting;
  final FollowupResponse? response;
  final String? errorMessage;

  const FollowupState({
    this.selectedOutcome,
    this.notes = '',
    this.isSubmitting = false,
    this.response,
    this.errorMessage,
  });

  FollowupState copyWith({
    String? selectedOutcome,
    String? notes,
    bool? isSubmitting,
    FollowupResponse? response,
    String? errorMessage,
  }) {
    return FollowupState(
      selectedOutcome: selectedOutcome ?? this.selectedOutcome,
      notes: notes ?? this.notes,
      isSubmitting: isSubmitting ?? this.isSubmitting,
      response: response ?? this.response,
      errorMessage: errorMessage,
    );
  }
}

final followupControllerProvider =
    StateNotifierProvider<FollowupController, FollowupState>((ref) {
  final repository = ref.watch(followupRepositoryProvider);
  return FollowupController(repository);
});

class FollowupController extends StateNotifier<FollowupState> {
  final FollowupRepository _repository;

  FollowupController(this._repository) : super(const FollowupState());

  void selectOutcome(String outcome) {
    state = state.copyWith(selectedOutcome: outcome, errorMessage: null);
  }

  void setNotes(String notes) {
    state = state.copyWith(notes: notes);
  }

  Future<FollowupResponse?> submitFollowup({
    required String farmId,
    required String diagnosisId,
  }) async {
    if (state.selectedOutcome == null || state.isSubmitting) return null;

    state = state.copyWith(isSubmitting: true, errorMessage: null);

    try {
      final request = FollowupRequest(
        diagnosisId: diagnosisId,
        outcome: state.selectedOutcome!,
        notes: state.notes.trim().isEmpty ? null : state.notes.trim(),
      );

      final response = await _repository.submitFollowup(
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
        errorMessage: 'Unable to submit follow-up status. Please check your connection.',
      );
      return null;
    }
  }

  void reset() {
    state = const FollowupState();
  }
}
