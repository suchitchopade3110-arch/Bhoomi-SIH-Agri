import '../data/models/create_farm_request.dart';
import '../data/models/create_farm_response.dart';

class OnboardingState {
  final String crop;
  final double areaAcresSelfReported;
  final String growthStage;
  final String soilType;
  final String irrigationAccess;
  final String season;

  final int currentStep;
  final bool isListening;
  final bool isSubmitting;
  final String? errorMessage;
  final CreateFarmResponse? createdFarmResponse;
  final Map<String, String> validationErrors;

  const OnboardingState({
    this.crop = 'samba_paddy',
    this.areaAcresSelfReported = 2.0,
    this.growthStage = 'vegetative',
    this.soilType = 'clay_loam',
    this.irrigationAccess = 'canal',
    this.season = 'samba',
    this.currentStep = 0,
    this.isListening = false,
    this.isSubmitting = false,
    this.errorMessage,
    this.createdFarmResponse,
    this.validationErrors = const {},
  });

  bool get isCurrentStepValid {
    switch (currentStep) {
      case 0:
        return crop.trim().isNotEmpty;
      case 1:
        return areaAcresSelfReported > 0;
      case 2:
        return growthStage.trim().isNotEmpty;
      case 3:
        return soilType.trim().isNotEmpty;
      case 4:
        return irrigationAccess.trim().isNotEmpty;
      case 5:
        return season.trim().isNotEmpty;
      default:
        return true;
    }
  }

  bool get isProfileComplete {
    return crop.isNotEmpty &&
        areaAcresSelfReported > 0 &&
        growthStage.isNotEmpty;
  }

  CreateFarmRequest toRequest() {
    return CreateFarmRequest(
      crop: crop,
      areaAcresSelfReported: areaAcresSelfReported,
      growthStage: growthStage,
      soilType: soilType,
      irrigationAccess: irrigationAccess,
      season: season,
    );
  }

  OnboardingState copyWith({
    String? crop,
    double? areaAcresSelfReported,
    String? growthStage,
    String? soilType,
    String? irrigationAccess,
    String? season,
    int? currentStep,
    bool? isListening,
    bool? isSubmitting,
    String? errorMessage,
    CreateFarmResponse? createdFarmResponse,
    Map<String, String>? validationErrors,
  }) {
    return OnboardingState(
      crop: crop ?? this.crop,
      areaAcresSelfReported: areaAcresSelfReported ?? this.areaAcresSelfReported,
      growthStage: growthStage ?? this.growthStage,
      soilType: soilType ?? this.soilType,
      irrigationAccess: irrigationAccess ?? this.irrigationAccess,
      season: season ?? this.season,
      currentStep: currentStep ?? this.currentStep,
      isListening: isListening ?? this.isListening,
      isSubmitting: isSubmitting ?? this.isSubmitting,
      errorMessage: errorMessage,
      createdFarmResponse: createdFarmResponse ?? this.createdFarmResponse,
      validationErrors: validationErrors ?? this.validationErrors,
    );
  }
}

