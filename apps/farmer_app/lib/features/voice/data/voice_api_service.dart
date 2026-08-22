import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/api/api_client.dart';
import '../../../core/api/api_exception.dart';
import '../../../shared/constants/api_constants.dart';
import 'models/synthesize_request.dart';
import 'models/synthesize_response.dart';
import 'models/transcribe_request.dart';
import 'models/transcribe_response.dart';

final voiceApiServiceProvider = Provider<VoiceApiService>((ref) {
  return VoiceApiService(ApiClient());
});

class VoiceApiService {
  final ApiClient _apiClient;

  VoiceApiService(this._apiClient);

  Future<TranscribeResponse> transcribe(TranscribeRequest request) async {
    try {
      final response = await _apiClient.post(
        ApiConstants.voiceTranscribe,
        data: request.toJson(),
      );

      if (response.data is Map<String, dynamic>) {
        return TranscribeResponse.fromJson(response.data as Map<String, dynamic>);
      }
      throw Exception('Invalid transcribe response format.');
    } on NetworkException {
      if (ApiConstants.enableMockFallback) {
        return const TranscribeResponse(
          text: 'Samba Paddy with yellow leaf discoloration along margins',
          lang: 'en-IN',
          confidence: 0.94,
          needsConfirmation: false,
        );
      }
      rethrow;
    }
  }

  Future<SynthesizeResponse> synthesize(SynthesizeRequest request) async {
    try {
      final response = await _apiClient.post(
        ApiConstants.voiceSynthesize,
        data: request.toJson(),
      );

      if (response.data is Map<String, dynamic>) {
        return SynthesizeResponse.fromJson(response.data as Map<String, dynamic>);
      }
      throw Exception('Invalid synthesize response format.');
    } on NetworkException {
      if (ApiConstants.enableMockFallback) {
        return const SynthesizeResponse(
          audioUrl: '',
          durationSeconds: 3.5,
        );
      }
      rethrow;
    }
  }
}
