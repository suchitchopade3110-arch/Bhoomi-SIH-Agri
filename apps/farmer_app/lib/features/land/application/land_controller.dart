import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../onboarding/data/farm_repository.dart';
import '../../onboarding/data/models/farm_update_models.dart';
import '../data/land_repository.dart';
import '../data/models/land_record_response.dart';
import '../data/models/land_submission_request.dart';

class LandState {
  final String surveyNo;
  final double areaAcres;
  final GeoJsonPolygonData? boundaryGeojson;
  final bool isSubmitting;
  final bool isLoading;
  final LandRecordResponse? currentRecord;
  final String? errorMessage;

  const LandState({
    this.surveyNo = '',
    this.areaAcres = 2.0,
    this.boundaryGeojson,
    this.isSubmitting = false,
    this.isLoading = false,
    this.currentRecord,
    this.errorMessage,
  });

  bool get isValid => surveyNo.trim().isNotEmpty && areaAcres > 0;

  LandState copyWith({
    String? surveyNo,
    double? areaAcres,
    GeoJsonPolygonData? boundaryGeojson,
    bool? isSubmitting,
    bool? isLoading,
    LandRecordResponse? currentRecord,
    String? errorMessage,
  }) {
    return LandState(
      surveyNo: surveyNo ?? this.surveyNo,
      areaAcres: areaAcres ?? this.areaAcres,
      boundaryGeojson: boundaryGeojson ?? this.boundaryGeojson,
      isSubmitting: isSubmitting ?? this.isSubmitting,
      isLoading: isLoading ?? this.isLoading,
      currentRecord: currentRecord ?? this.currentRecord,
      errorMessage: errorMessage,
    );
  }
}

final landControllerProvider =
    StateNotifierProvider<LandController, LandState>((ref) {
  final repository = ref.watch(landRepositoryProvider);
  return LandController(repository, ref);
});

class LandController extends StateNotifier<LandState> {
  final LandRepository _repository;
  final Ref _ref;

  LandController(this._repository, this._ref) : super(const LandState());

  void setSurveyNo(String surveyNo) {
    state = state.copyWith(surveyNo: surveyNo, errorMessage: null);
  }

  void setAreaAcres(double acres) {
    state = state.copyWith(areaAcres: acres, errorMessage: null);
  }

  void setBoundaryGeojson(GeoJsonPolygonData geojson) {
    state = state.copyWith(boundaryGeojson: geojson, errorMessage: null);
  }

  Future<LandRecordResponse?> submitLand(String farmId) async {
    if (!state.isValid || state.isSubmitting) return null;

    state = state.copyWith(isSubmitting: true, errorMessage: null);

    try {
      final request = LandSubmissionRequest(
        surveyNo: state.surveyNo,
        areaAcres: state.areaAcres,
        boundaryGeojson: state.boundaryGeojson ?? _defaultPolygon(),
      );

      final response = await _repository.submitLand(
        farmId: farmId,
        request: request,
      );

      // Link land to farm in background
      try {
        final farmRepo = _ref.read(farmRepositoryProvider);
        await farmRepo.submitFarmLand(farmId, ThinLandSubmissionRequest(surveyNumber: state.surveyNo));
      } catch (_) {}

      state = state.copyWith(
        isSubmitting: false,
        currentRecord: response,
      );
      return response;
    } catch (e) {
      state = state.copyWith(
        isSubmitting: false,
        errorMessage: 'Unable to submit land record. Please try again.',
      );
      return null;
    }
  }

  Future<void> fetchLandRecord(String farmId) async {
    state = state.copyWith(isLoading: true, errorMessage: null);
    try {
      final response = await _repository.getLandRecord(farmId);
      state = state.copyWith(
        isLoading: false,
        currentRecord: response,
      );
    } catch (e) {
      state = state.copyWith(
        isLoading: false,
        errorMessage: 'Unable to fetch verification status.',
      );
    }
  }

  GeoJsonPolygonData _defaultPolygon() {
    return const GeoJsonPolygonData(
      coordinates: [
        [
          [77.7214, 11.3412],
          [77.7289, 11.3415],
          [77.7285, 11.3478],
          [77.7211, 11.3475],
          [77.7214, 11.3412],
        ],
      ],
    );
  }
}
