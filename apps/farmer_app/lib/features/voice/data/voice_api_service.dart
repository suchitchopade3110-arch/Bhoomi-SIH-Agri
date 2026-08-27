import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/api/api_client.dart';
import '../../../core/api/api_exception.dart';
import '../../../shared/constants/api_constants.dart';
import 'models/confirm_field_models.dart';
import 'models/synthesize_request.dart';
import 'models/synthesize_response.dart';
import 'models/transcribe_request.dart';
import 'models/transcribe_response.dart';
import 'models/voice_query_request.dart';
import 'models/voice_query_response.dart';

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

  Future<ConfirmFieldResponse> confirmField(ConfirmFieldRequest request) async {
    try {
      final response = await _apiClient.post(
        ApiConstants.voiceConfirm,
        data: request.toJson(),
      );

      if (response.data is Map<String, dynamic>) {
        return ConfirmFieldResponse.fromJson(response.data as Map<String, dynamic>);
      }
      throw Exception('Invalid confirm field response format.');
    } on NetworkException {
      if (ApiConstants.enableMockFallback) {
        return ConfirmFieldResponse(
          status: request.isConfirmed ? 'committed' : 'retry_prompt',
          field: request.field,
          finalValue: request.confirmedValue,
          message: request.isConfirmed ? 'மதிப்பு சேமிக்கப்பட்டது.' : 'மீண்டும் சொல்லவும்.',
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

  /// End-to-end speech-to-speech: audio in, spoken answer out
  /// (`POST /api/v1/voice/query`).
  Future<VoiceQueryResponse> query(VoiceQueryRequest request) async {
    try {
      final response = await _apiClient.post(
        ApiConstants.voiceQuery,
        data: request.toJson(),
      );

      if (response.data is Map<String, dynamic>) {
        return VoiceQueryResponse.fromJson(response.data as Map<String, dynamic>);
      }
      throw Exception('Invalid voice query response format.');
    } on NetworkException {
      if (ApiConstants.enableMockFallback) {
        return const VoiceQueryResponse(
          transcript: 'Why are my paddy leaves turning yellow?',
          answerText:
              "I don't have reliable information for this right now. Should I send it to an expert?",
          audioResponseUrl: '',
          spokenSummary:
              "I don't have reliable information for this. Should I send it to an expert?",
        );
      }
      rethrow;
    }
  }
}
