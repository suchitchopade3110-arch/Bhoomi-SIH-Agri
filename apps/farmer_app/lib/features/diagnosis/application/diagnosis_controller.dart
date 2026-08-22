import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:image_picker/image_picker.dart';
import '../../../core/upload/asset_upload_service.dart';
import '../data/diagnosis_repository.dart';
import '../data/models/diagnose_request.dart';
import '../data/models/diagnosis_response.dart';
import 'diagnosis_state.dart';

final diagnosisControllerProvider =
    StateNotifierProvider<DiagnosisController, DiagnosisState>((ref) {
  final repository = ref.watch(diagnosisRepositoryProvider);
  final uploadService = ref.watch(assetUploadServiceProvider);
  return DiagnosisController(repository, uploadService);
});

class DiagnosisController extends StateNotifier<DiagnosisState> {
  final DiagnosisRepository _repository;
  final AssetUploadService _uploadService;
  final ImagePicker _picker = ImagePicker();

  DiagnosisController(this._repository, this._uploadService)
      : super(const DiagnosisState());

  void setProblemDescription(String text) {
    state = state.copyWith(problemDescription: text, errorMessage: null);
  }

  void setAudioAssetId(String assetId) {
    state = state.copyWith(audioAssetId: assetId);
  }

  Future<void> pickAndUploadImage(ImageSource source) async {
    try {
      state = state.copyWith(imageUploadStatus: ImageUploadStatus.selecting);
      final XFile? file = await _picker.pickImage(
        source: source,
        imageQuality: 85,
        maxWidth: 1920,
      );

      if (file == null) {
        state = state.copyWith(imageUploadStatus: ImageUploadStatus.none);
        return;
      }

      final bytes = await file.readAsBytes();
      state = state.copyWith(
        selectedImageBytes: bytes,
        selectedImagePath: file.path,
        imageUploadStatus: ImageUploadStatus.uploading,
        imageUploadProgress: 0.0,
      );

      // Upload directly to presigned URL
      final assetId = await _uploadService.uploadAsset(
        bytes: bytes,
        contentType: 'image/jpeg',
        assetType: 'image',
        onProgress: (progress) {
          state = state.copyWith(imageUploadProgress: progress);
        },
      );

      state = state.copyWith(
        imageAssetId: assetId,
        imageUploadStatus: ImageUploadStatus.uploaded,
      );
    } catch (e) {
      state = state.copyWith(
        imageUploadStatus: ImageUploadStatus.failed,
        errorMessage: 'Crop image upload failed. You may retry or submit text.',
      );
    }
  }

  Future<DiagnosisResponse?> submitDiagnosis(String farmId) async {
    if (!state.isValid || state.isDiagnosing) return null;

    state = state.copyWith(isDiagnosing: true, errorMessage: null);

    try {
      final request = DiagnoseRequest(
        problemDescription: state.problemDescription.trim().isEmpty
            ? 'Crop leaf discoloration and anomaly'
            : state.problemDescription.trim(),
        imageAssetId: state.imageAssetId,
        audioAssetId: state.audioAssetId,
      );

      final response = await _repository.diagnoseCrop(
        farmId: farmId,
        request: request,
      );

      state = state.copyWith(
        isDiagnosing: false,
        diagnosisResponse: response,
      );

      return response;
    } catch (e) {
      state = state.copyWith(
        isDiagnosing: false,
        errorMessage: 'Unable to complete crop diagnosis. Please check network and retry.',
      );
      return null;
    }
  }

  void reset() {
    state = const DiagnosisState();
  }
}
