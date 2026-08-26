import 'dart:async';
import 'dart:typed_data';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:image_picker/image_picker.dart';
import '../../../core/upload/asset_upload_service.dart';
import '../../../core/upload/offline_upload_queue.dart';
import '../data/diagnosis_repository.dart';
import '../data/models/diagnose_request.dart';
import '../data/models/diagnosis_response.dart';
import 'diagnosis_state.dart';

final diagnosisControllerProvider =
    StateNotifierProvider<DiagnosisController, DiagnosisState>((ref) {
  final repository = ref.watch(diagnosisRepositoryProvider);
  final uploadService = ref.watch(assetUploadServiceProvider);
  final uploadQueue = ref.watch(offlineUploadQueueProvider.notifier);
  return DiagnosisController(repository, uploadService, uploadQueue);
});

class DiagnosisController extends StateNotifier<DiagnosisState> {
  final DiagnosisRepository _repository;
  final AssetUploadService _uploadService;
  final OfflineUploadQueueNotifier _uploadQueue;
  final ImagePicker _picker = ImagePicker();

  DiagnosisController(this._repository, this._uploadService, this._uploadQueue)
      : super(const DiagnosisState());

  void setProblemDescription(String text) {
    state = state.copyWith(problemDescription: text, errorMessage: null);
  }

  void setAudioAssetId(String assetId) {
    state = state.copyWith(audioAssetId: assetId);
  }

  Future<void> pickAndUploadImage(ImageSource source) async {
    Uint8List? bytes;
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

      bytes = await file.readAsBytes();
      state = state.copyWith(
        selectedImageBytes: bytes,
        selectedImagePath: file.path,
        imageUploadStatus: ImageUploadStatus.uploading,
        imageUploadProgress: 0.0,
      );
    } catch (e) {
      // Failed before we even had image bytes (picker/permission error) —
      // nothing to queue, just surface it.
      state = state.copyWith(
        imageUploadStatus: ImageUploadStatus.failed,
        errorMessage: 'Could not access the photo. Please try again.',
      );
      return;
    }

    try {
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
      // Offline upload queue (checklist §12.4): rather than dropping the
      // photo on a connectivity failure, queue it locally — it uploads
      // automatically once the network is back, and the farmer can still
      // submit the rest of the diagnosis in the meantime.
      final pendingId = _uploadQueue.enqueue(
        bytes: bytes,
        contentType: 'image/jpeg',
        assetType: 'image',
      );
      state = state.copyWith(imageUploadStatus: ImageUploadStatus.queued);
      unawaited(_awaitQueuedUpload(pendingId));
    }
  }

  Future<void> _awaitQueuedUpload(String pendingId) async {
    final result = await _uploadQueue.waitFor(pendingId);
    if (!mounted) return;
    if (result.isUploaded && result.assetId != null) {
      state = state.copyWith(imageAssetId: result.assetId, imageUploadStatus: ImageUploadStatus.uploaded);
    } else {
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
