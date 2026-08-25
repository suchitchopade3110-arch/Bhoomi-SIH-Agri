import 'dart:typed_data';
import 'package:dio/dio.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../shared/constants/api_constants.dart';
import '../api/api_client.dart';

final assetUploadServiceProvider = Provider<AssetUploadService>((ref) {
  return AssetUploadService(ApiClient());
});

class PresignedAssetResult {
  final String assetId;
  final String uploadUrl;
  final Map<String, String> uploadHeaders;

  const PresignedAssetResult({
    required this.assetId,
    required this.uploadUrl,
    this.uploadHeaders = const {},
  });

  factory PresignedAssetResult.fromJson(Map<String, dynamic> json) {
    return PresignedAssetResult(
      assetId: json['asset_id'] as String? ?? json['id'] as String? ?? 'asset_default',
      uploadUrl: json['upload_url'] as String? ?? json['presigned_url'] as String? ?? '',
      uploadHeaders: json['upload_headers'] != null
          ? Map<String, String>.from(json['upload_headers'] as Map)
          : {},
    );
  }
}

class AssetUploadService {
  final ApiClient _apiClient;
  final Dio _uploadDio;

  AssetUploadService(this._apiClient, [Dio? uploadDio])
      : _uploadDio = uploadDio ?? Dio();

  Future<String> uploadAsset({
    required Uint8List bytes,
    required String contentType,
    String assetType = 'audio',
    void Function(double progress)? onProgress,
  }) async {
    try {
      // 1. Request presigned URL from backend
      final fileName = '${assetType}_${DateTime.now().millisecondsSinceEpoch}.${contentType.contains('jpeg') ? 'jpg' : contentType.contains('png') ? 'png' : contentType.contains('wav') ? 'wav' : 'bin'}';
      final presignResponse = await _apiClient.post(
        ApiConstants.assetsPresign,
        data: {
          'file_name': fileName,
          'content_type': contentType,
          'asset_kind': assetType == 'image' ? 'image' : assetType == 'document' ? 'document' : 'audio',
          'asset_type': assetType,
          'size_bytes': bytes.lengthInBytes,
        },
      );

      final presignedData = PresignedAssetResult.fromJson(
        presignResponse.data as Map<String, dynamic>,
      );

      // 2. Direct binary upload to presigned URL
      if (presignedData.uploadUrl.isNotEmpty) {
        await _uploadDio.put(
          presignedData.uploadUrl,
          data: Stream.fromIterable([bytes]),
          options: Options(
            headers: {
              'Content-Type': contentType,
              'Content-Length': bytes.lengthInBytes.toString(),
              ...presignedData.uploadHeaders,
            },
          ),
          onSendProgress: (sent, total) {
            if (total > 0 && onProgress != null) {
              onProgress(sent / total);
            }
          },
        );
      }

      // 3. Return the verified asset ID for subsequent API requests
      return presignedData.assetId;
    } catch (e) {
      if (ApiConstants.enableMockFallback) {
        return 'mock_asset_${DateTime.now().millisecondsSinceEpoch}';
      }
      rethrow;
    }
  }
}
