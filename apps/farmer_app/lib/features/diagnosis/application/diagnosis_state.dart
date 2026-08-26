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

  bool get isValid => problemDescription.trim().isNotEmpty || imageAssetId != null || audioAssetId != null;

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
