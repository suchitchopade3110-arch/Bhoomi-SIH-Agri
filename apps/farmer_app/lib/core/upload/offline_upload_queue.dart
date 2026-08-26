import 'dart:async';
import 'dart:convert';
import 'dart:typed_data';
import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../api/api_exception.dart';
import '../connectivity/connectivity_service.dart';
import '../storage/secure_storage_service.dart';
import 'asset_upload_service.dart';
import 'pending_upload.dart';

/// Offline upload queue with per-item state (checklist §12.4).
///
/// A crop photo or voice note whose upload fails with a connectivity error
/// is queued here instead of just being dropped with a generic "upload
/// failed" message. Each item's state is individually tracked
/// (queued/uploading/uploaded/failed) and persisted, so it survives an app
/// restart, and the whole queue auto-retries whenever [networkStateProvider]
/// reports the connection is back.
final offlineUploadQueueProvider =
    StateNotifierProvider<OfflineUploadQueueNotifier, List<PendingUpload>>((ref) {
  final notifier = OfflineUploadQueueNotifier(
    uploadService: ref.watch(assetUploadServiceProvider),
    storage: ref.watch(secureStorageServiceProvider),
  );
  ref.listen<NetworkState>(networkStateProvider, (previous, next) {
    if (next.isOnline && previous?.isOnline != true) {
      notifier.retryAllQueued();
    }
  });
  return notifier;
});

class OfflineUploadQueueNotifier extends StateNotifier<List<PendingUpload>> {
  static const _storageKey = 'bhoomi_offline_upload_queue';

  final AssetUploadService _uploadService;
  final SecureStorageService _storage;
  bool _loaded = false;

  OfflineUploadQueueNotifier({
    required AssetUploadService uploadService,
    required SecureStorageService storage,
  })  : _uploadService = uploadService,
        _storage = storage,
        super(const []) {
    _restore();
  }

  Future<void> _restore() async {
    final raw = await _storage.readRaw(_storageKey);
    if (raw == null || raw.isEmpty) {
      _loaded = true;
      return;
    }
    try {
      final decoded = jsonDecode(raw) as List<dynamic>;
      state = decoded.map((e) => PendingUpload.fromJson(e as Map<String, dynamic>)).toList();
    } catch (_) {
      // Corrupt/unreadable queue — start clean rather than crash the app
      // over a persisted upload record.
      state = const [];
    }
    _loaded = true;
    // Pick up anything left queued from a previous session.
    unawaited(retryAllQueued());
  }

  Future<void> _persist() async {
    if (!_loaded) return;
    final json = jsonEncode(state.map((u) => u.toJson()).toList());
    await _storage.writeRaw(_storageKey, json);
  }

  /// Enqueues [bytes] for upload and returns the local pending id
  /// immediately — the actual upload (and any retries) happen in the
  /// background. Call [waitFor] with the returned id to await the result.
  String enqueue({
    required Uint8List bytes,
    required String contentType,
    required String assetType,
  }) {
    final id = 'pending_${DateTime.now().microsecondsSinceEpoch}';
    final item = PendingUpload(
      id: id,
      bytes: bytes,
      contentType: contentType,
      assetType: assetType,
      createdAt: DateTime.now(),
    );
    state = [...state, item];
    unawaited(_persist());
    unawaited(_attempt(id));
    return id;
  }

  /// Resolves once the item finishes (uploaded or terminally failed).
  /// Resolves immediately if it has already finished by the time this is
  /// called.
  Future<PendingUpload> waitFor(String id) async {
    final existing = _find(id);
    if (existing == null || existing.isUploaded || existing.isFailed) {
      return existing ?? _missing(id);
    }

    final completer = Completer<PendingUpload>();
    // Simple polling avoids wiring a second stream just for this — the
    // queue only ever has a handful of in-flight items at once.
    final timer = Timer.periodic(const Duration(milliseconds: 300), (t) {
      final current = _find(id);
      if (current == null || current.isUploaded || current.isFailed) {
        if (!completer.isCompleted) completer.complete(current ?? _missing(id));
      }
    });
    final result = await completer.future;
    timer.cancel();
    return result;
  }

  PendingUpload? _find(String id) {
    for (final u in state) {
      if (u.id == id) return u;
    }
    return null;
  }

  PendingUpload _missing(String id) => PendingUpload(
        id: id,
        bytes: Uint8List(0),
        contentType: '',
        assetType: '',
        status: PendingUploadStatus.failed,
        errorMessage: 'Upload record not found.',
        createdAt: DateTime.now(),
      );

  Future<void> retryAllQueued() async {
    final queuedIds = state.where((u) => u.isQueued).map((u) => u.id).toList();
    for (final id in queuedIds) {
      await _attempt(id);
    }
  }

  Future<void> retry(String id) => _attempt(id);

  Future<void> _attempt(String id) async {
    final item = _find(id);
    if (item == null || item.isUploading || item.isUploaded) return;

    _update(id, (u) => u.copyWith(status: PendingUploadStatus.uploading));

    try {
      final assetId = await _uploadService.uploadAsset(
        bytes: item.bytes,
        contentType: item.contentType,
        assetType: item.assetType,
      );
      _update(
        id,
        (u) => u.copyWith(status: PendingUploadStatus.uploaded, assetId: assetId, attempts: u.attempts + 1),
      );
    } on NetworkException {
      // Stays queued — the connectivity listener (or a manual retry) will
      // pick it up again. Not a terminal failure.
      _update(id, (u) => u.copyWith(status: PendingUploadStatus.queued, attempts: u.attempts + 1));
    } on DioException catch (e) {
      // The direct-to-presigned-URL binary PUT (asset_upload_service.dart)
      // uses a raw Dio instance, not ApiClient, so a connectivity failure
      // there surfaces as DioException rather than NetworkException.
      // Treat the same connection-shaped error types as retryable.
      const retryableTypes = {
        DioExceptionType.connectionTimeout,
        DioExceptionType.sendTimeout,
        DioExceptionType.receiveTimeout,
        DioExceptionType.connectionError,
        DioExceptionType.unknown,
      };
      if (retryableTypes.contains(e.type)) {
        _update(id, (u) => u.copyWith(status: PendingUploadStatus.queued, attempts: u.attempts + 1));
      } else {
        _update(
          id,
          (u) => u.copyWith(status: PendingUploadStatus.failed, errorMessage: e.toString(), attempts: u.attempts + 1),
        );
      }
    } catch (e) {
      _update(
        id,
        (u) => u.copyWith(
          status: PendingUploadStatus.failed,
          errorMessage: e.toString(),
          attempts: u.attempts + 1,
        ),
      );
    }
    unawaited(_persist());
  }

  void _update(String id, PendingUpload Function(PendingUpload) transform) {
    state = [
      for (final u in state) if (u.id == id) transform(u) else u,
    ];
  }

  /// Drops a completed or terminally-failed item from the visible queue
  /// (e.g. once its diagnosis form has consumed the asset id).
  void dismiss(String id) {
    state = state.where((u) => u.id != id).toList();
    unawaited(_persist());
  }
}
