import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/api/api_exception.dart';
import '../../../core/storage/secure_storage_service.dart';
import '../data/farm_repository.dart';
import 'onboarding_state.dart';

final onboardingControllerProvider =
    StateNotifierProvider<OnboardingController, OnboardingState>((ref) {
  final repository = ref.watch(farmRepositoryProvider);
  final storageService = ref.watch(secureStorageServiceProvider);
  return OnboardingController(repository, storageService);
});

class OnboardingController extends StateNotifier<OnboardingState> {
  final FarmRepository _repository;
  final SecureStorageService _storageService;

  OnboardingController(this._repository, this._storageService)
      : super(const OnboardingState());

  void setCrop(String crop) {
    state = state.copyWith(crop: crop, errorMessage: null);
  }

  void setGrowthStage(String stage) {
    state = state.copyWith(growthStage: stage, errorMessage: null);
  }

  void setRegion(String region) {
    state = state.copyWith(region: region, errorMessage: null);
  }

  void setSoilType(String soilType) {
    state = state.copyWith(soilType: soilType, errorMessage: null);
  }

  void setIrrigationAccess(String irrigation) {
    state = state.copyWith(irrigationAccess: irrigation, errorMessage: null);
  }

  void setSeason(String season) {
    state = state.copyWith(season: season, errorMessage: null);
  }

  void nextStep() {
    if (state.currentStep < 2) {
      state = state.copyWith(currentStep: state.currentStep + 1);
    }
  }

  void previousStep() {
    if (state.currentStep > 0) {
      state = state.copyWith(currentStep: state.currentStep - 1);
    }
  }

  void goToStep(int step) {
    if (step >= 0 && step <= 2) {
      state = state.copyWith(currentStep: step);
    }
  }

  void startListening(String field) {
    state = state.copyWith(recordingField: field);
  }

  void stopListening() {
    state = state.copyWith(clearRecordingField: true);
  }

  void toggleListening([String? field]) {
    final targetField = field ?? (state.currentStep == 0 ? 'crop' : state.currentStep == 1 ? 'growth_stage' : 'region');
    if (state.isFieldRecording(targetField)) {
      stopListening();
    } else {
      startListening(targetField);
    }
  }

  void clearError() {
    state = state.copyWith(errorMessage: null);
  }

  Future<String?> submitFarm() async {
    if (state.isSubmitting) return null;

    state = state.copyWith(isSubmitting: true, errorMessage: null);

    try {
      final request = state.toRequest();
      final response = await _repository.createFarm(request);

      // Persist the returned farm ID locally
      await _storageService.saveFarmId(response.id);

      state = state.copyWith(
        isSubmitting: false,
        createdFarmResponse: response,
      );

      return response.id;
    } on ApiException catch (e) {
      state = state.copyWith(
        isSubmitting: false,
        errorMessage: e.message,
      );
      return null;
    } catch (e) {
      state = state.copyWith(
        isSubmitting: false,
        errorMessage: 'An unexpected error occurred while creating your farm. Please try again.',
      );
      return null;
    }
  }
}
