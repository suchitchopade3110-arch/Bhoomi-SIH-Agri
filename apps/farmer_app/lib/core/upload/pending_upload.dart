import 'dart:convert';
import 'dart:typed_data';

/// Per-item state for one entry in the offline upload queue (checklist §12.4).
///
/// ``queued`` covers both "never attempted yet" and "attempted, failed due
/// to connectivity, waiting to retry" — the queue auto-retries anything in
/// this state whenever the network comes back. ``failed`` is reserved for a
/// non-network error (e.g. the server rejected the upload) that retrying
/// on the same bytes won't fix on its own; the farmer can still retry it
/// manually.
enum PendingUploadStatus {
  queued,
  uploading,
  uploaded,
  failed,
}

class PendingUpload {
  final String id;
  final Uint8List bytes;
  final String contentType;
  final String assetType;
  final PendingUploadStatus status;
  final String? assetId;
  final String? errorMessage;
  final DateTime createdAt;
  final int attempts;

  const PendingUpload({
    required this.id,
    required this.bytes,
    required this.contentType,
    required this.assetType,
    this.status = PendingUploadStatus.queued,
    this.assetId,
    this.errorMessage,
    required this.createdAt,
    this.attempts = 0,
  });

  bool get isQueued => status == PendingUploadStatus.queued;
  bool get isUploading => status == PendingUploadStatus.uploading;
  bool get isUploaded => status == PendingUploadStatus.uploaded;
  bool get isFailed => status == PendingUploadStatus.failed;

  PendingUpload copyWith({
    PendingUploadStatus? status,
    String? assetId,
    String? errorMessage,
    int? attempts,
  }) {
    return PendingUpload(
      id: id,
      bytes: bytes,
      contentType: contentType,
      assetType: assetType,
      status: status ?? this.status,
      assetId: assetId ?? this.assetId,
      errorMessage: errorMessage,
      createdAt: createdAt,
      attempts: attempts ?? this.attempts,
    );
  }

  Map<String, dynamic> toJson() => {
        'id': id,
        'bytes_base64': base64Encode(bytes),
        'content_type': contentType,
        'asset_type': assetType,
        'status': status.name,
        'asset_id': assetId,
        'created_at': createdAt.toIso8601String(),
        'attempts': attempts,
      };

  factory PendingUpload.fromJson(Map<String, dynamic> json) {
    final statusName = json['status'] as String? ?? 'queued';
    return PendingUpload(
      id: json['id'] as String,
      bytes: base64Decode(json['bytes_base64'] as String? ?? ''),
      contentType: json['content_type'] as String? ?? 'application/octet-stream',
      assetType: json['asset_type'] as String? ?? 'image',
      // A row persisted mid-upload from a killed app restarts as queued,
      // not stuck "uploading" forever.
      status: statusName == 'uploading' ? PendingUploadStatus.queued : PendingUploadStatus.values.byName(statusName),
      assetId: json['asset_id'] as String?,
      createdAt: DateTime.tryParse(json['created_at'] as String? ?? '') ?? DateTime.now(),
      attempts: (json['attempts'] as num?)?.toInt() ?? 0,
    );
  }
}
