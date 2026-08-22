enum UploadStatus {
  idle,
  presigning,
  uploading,
  completed,
  error,
}

class UploadState {
  final UploadStatus status;
  final double progress; // 0.0 to 1.0
  final String? assetId;
  final String? errorMessage;

  const UploadState({
    this.status = UploadStatus.idle,
    this.progress = 0.0,
    this.assetId,
    this.errorMessage,
  });

  bool get isIdle => status == UploadStatus.idle;
  bool get isPresigning => status == UploadStatus.presigning;
  bool get isUploading => status == UploadStatus.uploading;
  bool get isCompleted => status == UploadStatus.completed;
  bool get isError => status == UploadStatus.error;

  UploadState copyWith({
    UploadStatus? status,
    double? progress,
    String? assetId,
    String? errorMessage,
  }) {
    return UploadState(
      status: status ?? this.status,
      progress: progress ?? this.progress,
      assetId: assetId ?? this.assetId,
      errorMessage: errorMessage,
    );
  }
}
