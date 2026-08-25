import '../data/models/create_farm_request.dart';
import '../data/models/create_farm_response.dart';

class OnboardingState {
  final String crop;
  final String growthStage;
  final String region;
  final String soilType;
  final String irrigationAccess;
  final String season;

  final int currentStep;
  final String? recordingField;
  final bool isSubmitting;
  final String? errorMessage;
  final CreateFarmResponse? createdFarmResponse;
  final Map<String, String> validationErrors;

  const OnboardingState({
    this.crop = 'samba_paddy',
    this.growthStage = 'vegetative',
    this.region = 'Cauvery Delta',
    this.soilType = 'Clay Loam',
    this.irrigationAccess = 'Borewell',
    this.season = 'samba',
    this.currentStep = 0,
    this.recordingField,
    this.isSubmitting = false,
    this.errorMessage,
    this.createdFarmResponse,
    this.validationErrors = const {},
  });

  bool isFieldRecording(String field) => recordingField == field;
  bool get isListening => recordingField != null;

  bool get isCurrentStepValid {
    switch (currentStep) {
      case 0:
        return crop.trim().isNotEmpty;
      case 1:
        return growthStage.trim().isNotEmpty;
      case 2:
        return region.trim().isNotEmpty;
      default:
        return true;
    }
  }

  bool get isProfileComplete {
    return crop.isNotEmpty &&
        growthStage.isNotEmpty &&
        region.isNotEmpty;
  }

  CreateFarmRequest toRequest() {
    return CreateFarmRequest(
      crop: crop,
      growthStage: growthStage,
      region: region,
      soilType: soilType,
      irrigationAccess: irrigationAccess,
      season: season,
    );
  }

  OnboardingState copyWith({
    String? crop,
    String? growthStage,
    String? region,
    String? soilType,
    String? irrigationAccess,
    String? season,
    int? currentStep,
    String? recordingField,
    bool clearRecordingField = false,
    bool? isSubmitting,
    String? errorMessage,
    CreateFarmResponse? createdFarmResponse,
    Map<String, String>? validationErrors,
  }) {
    return OnboardingState(
      crop: crop ?? this.crop,
      growthStage: growthStage ?? this.growthStage,
      region: region ?? this.region,
      soilType: soilType ?? this.soilType,
      irrigationAccess: irrigationAccess ?? this.irrigationAccess,
      season: season ?? this.season,
      currentStep: currentStep ?? this.currentStep,
      recordingField: clearRecordingField ? null : (recordingField ?? this.recordingField),
      isSubmitting: isSubmitting ?? this.isSubmitting,
      errorMessage: errorMessage,
      createdFarmResponse: createdFarmResponse ?? this.createdFarmResponse,
      validationErrors: validationErrors ?? this.validationErrors,
    );
  }
}


