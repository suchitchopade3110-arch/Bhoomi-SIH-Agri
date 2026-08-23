import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/audio/audio_playback_service.dart';
import '../../../core/audio/audio_recording_service.dart';
import '../../../core/upload/asset_upload_service.dart';
import '../data/models/transcribe_response.dart';
import '../data/voice_repository.dart';
import 'voice_state.dart';

final voiceControllerProvider =
    StateNotifierProvider<VoiceController, VoiceState>((ref) {
  final recordingService = ref.watch(audioRecordingServiceProvider);
  final playbackService = ref.watch(audioPlaybackServiceProvider);
  final uploadService = ref.watch(assetUploadServiceProvider);
  final repository = ref.watch(voiceRepositoryProvider);

  return VoiceController(
    recordingService: recordingService,
    playbackService: playbackService,
    uploadService: uploadService,
    repository: repository,
  );
});

class VoiceController extends StateNotifier<VoiceState> {
  final AudioRecordingService _recordingService;
  final AudioPlaybackService _playbackService;
  final AssetUploadService _uploadService;
  final VoiceRepository _repository;

  VoiceController({
    required AudioRecordingService recordingService,
    required AudioPlaybackService playbackService,
    required AssetUploadService uploadService,
    required VoiceRepository repository,
  })  : _recordingService = recordingService,
        _playbackService = playbackService,
        _uploadService = uploadService,
        _repository = repository,
        super(const VoiceState());

  Future<void> startRecording() async {
    try {
      await _recordingService.startRecording();
      state = state.copyWith(
        step: VoiceFlowStep.recording,
        isRecording: true,
        errorMessage: null,
      );
    } catch (e) {
      state = state.copyWith(
        step: VoiceFlowStep.error,
        errorMessage: 'Microphone access is required to speak with BHOOMI.',
      );
    }
  }

  Future<TranscribeResponse?> stopAndProcessAudio({String lang = 'en-IN'}) async {
    if (!state.isRecording) return null;

    try {
      // 1. Stop recording and retrieve binary audio bytes
      final audioBytes = await _recordingService.stopRecording();
      if (audioBytes == null || audioBytes.isEmpty) {
        state = state.copyWith(
          step: VoiceFlowStep.error,
          isRecording: false,
          errorMessage: 'No audio recorded. Please tap and speak again.',
        );
        return null;
      }

      state = state.copyWith(
        step: VoiceFlowStep.uploading,
        isRecording: false,
        isUploading: true,
        recordedAudioBytes: audioBytes,
        uploadProgress: 0.0,
      );

      // 2. Direct upload to presigned URL (Never send large files directly to API)
      final assetId = await _uploadService.uploadAsset(
        bytes: audioBytes,
        contentType: 'audio/aac',
        assetType: 'audio',
        onProgress: (progress) {
          state = state.copyWith(uploadProgress: progress);
        },
      );

      // 3. Request transcription with asset_id
      state = state.copyWith(
        step: VoiceFlowStep.transcribing,
        isUploading: false,
        isTranscribing: true,
        uploadedAssetId: assetId,
      );

      final transcription = await _repository.transcribe(assetId, lang: lang);

      // 4. Handle confidence and confirmation requirements
      if (transcription.isLowConfidence) {
        state = state.copyWith(
          step: VoiceFlowStep.error,
          isTranscribing: false,
          transcription: transcription,
          errorMessage: "We couldn't clearly understand that. Please try again or select an option.",
        );
        return transcription;
      }

      state = state.copyWith(
        step: transcription.needsConfirmation ? VoiceFlowStep.confirming : VoiceFlowStep.completed,
        isTranscribing: false,
        transcription: transcription,
      );

      return transcription;
    } catch (e) {
      state = state.copyWith(
        step: VoiceFlowStep.error,
        isRecording: false,
        isUploading: false,
        isTranscribing: false,
        errorMessage: 'Unable to process speech at this moment. Please try again.',
      );
      return null;
    }
  }

  Future<void> synthesizeAndSpeak(String text, {String lang = 'en-IN'}) async {
    if (text.trim().isEmpty) return;

    try {
      state = state.copyWith(isSynthesizing: true);
      final response = await _repository.synthesize(text, lang: lang);
      state = state.copyWith(
        isSynthesizing: false,
        synthesizedAudioUrl: response.audioUrl,
        isPlaying: true,
      );

      await _playbackService.playUrl(response.audioUrl);
      state = state.copyWith(isPlaying: false);
    } catch (e) {
      state = state.copyWith(
        isSynthesizing: false,
        isPlaying: false,
      );
      // Graceful fallback without breaking text experience
    }
  }

  void stopPlayback() {
    _playbackService.stop();
    state = state.copyWith(isPlaying: false);
  }

  void reset() {
    _recordingService.cancelRecording();
    _playbackService.stop();
    state = const VoiceState();
  }
}
