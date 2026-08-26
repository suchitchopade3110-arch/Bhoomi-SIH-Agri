import 'dart:typed_data';
import '../data/models/diagnosis_response.dart';

enum ImageUploadStatus {
  none,
  selecting,
  uploading,
  uploaded,
  failed,
  // Offline upload queue (checklist §12.4): the image couldn't reach the
  // server right now but is queued locally and will upload automatically
  // once connectivity returns.
  queued,
}

class DiagnosisState {
  final String problemDescription;
  final Uint8List? selectedImageBytes;
  final String? selectedImagePath;
  final String? imageAssetId;
  final ImageUploadStatus imageUploadStatus;
  final double imageUploadProgress;
  final String? audioAssetId;
  final bool isDiagnosing;
  final DiagnosisResponse? diagnosisResponse;
  final String? errorMessage;

  const DiagnosisState({
    this.problemDescription = '',
    this.selectedImageBytes,
    this.selectedImagePath,
    this.imageAssetId,
    this.imageUploadStatus = ImageUploadStatus.none,
    this.imageUploadProgress = 0.0,
    this.audioAssetId,
    this.isDiagnosing = false,
    this.diagnosisResponse,
    this.errorMessage,
  });

  // A real, presigned image is mandatory: the backend's diagnosis contract
  // requires image_asset_id unconditionally (services/api/app/schemas/
  // diagnosis.py — no default) and, since the §2.5 asset-provenance fix,
  // rejects anything that isn't a real presigned asset. Text/audio alone
  // was never actually a supported submission path server-side, even
  // though this previously let it through with a fake placeholder id.
  bool get isValid => imageAssetId != null;

  DiagnosisState copyWith({
    String? problemDescription,
    Uint8List? selectedImageBytes,
    String? selectedImagePath,
    String? imageAssetId,
    ImageUploadStatus? imageUploadStatus,
    double? imageUploadProgress,
    String? audioAssetId,
    bool? isDiagnosing,
    DiagnosisResponse? diagnosisResponse,
    String? errorMessage,
  }) {
    return DiagnosisState(
      problemDescription: problemDescription ?? this.problemDescription,
      selectedImageBytes: selectedImageBytes ?? this.selectedImageBytes,
      selectedImagePath: selectedImagePath ?? this.selectedImagePath,
      imageAssetId: imageAssetId ?? this.imageAssetId,
      imageUploadStatus: imageUploadStatus ?? this.imageUploadStatus,
      imageUploadProgress: imageUploadProgress ?? this.imageUploadProgress,
      audioAssetId: audioAssetId ?? this.audioAssetId,
      isDiagnosing: isDiagnosing ?? this.isDiagnosing,
      diagnosisResponse: diagnosisResponse ?? this.diagnosisResponse,
      errorMessage: errorMessage,
    );
  }
}
