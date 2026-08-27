import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/audio/audio_playback_service.dart';
import '../../../core/audio/audio_recording_service.dart';
import '../../../core/upload/asset_upload_service.dart';
import '../data/voice_repository.dart';
import 'voice_qa_state.dart';

final voiceQaControllerProvider =
    StateNotifierProvider.autoDispose<VoiceQaController, VoiceQaState>((ref) {
  final recordingService = ref.watch(audioRecordingServiceProvider);
  final playbackService = ref.watch(audioPlaybackServiceProvider);
  final uploadService = ref.watch(assetUploadServiceProvider);
  final repository = ref.watch(voiceRepositoryProvider);

  return VoiceQaController(
    recordingService: recordingService,
    playbackService: playbackService,
    uploadService: uploadService,
    repository: repository,
  );
});

/// Drives the full speech-to-speech loop for one screen: record -> upload
/// -> ask (transcribe + grounded answer, server-side) -> play the spoken
/// answer back. Deliberately separate from [VoiceController], which drives
/// the record -> transcribe -> confirm-and-fill-a-form flow used elsewhere
/// (Ask BHOOMI's problem-description field) — the two flows return
/// different response shapes and end differently (a form value vs. an
/// audio answer to play), so sharing one state/controller would just
/// couple two unrelated flows together.
class VoiceQaController extends StateNotifier<VoiceQaState> {
  final AudioRecordingService _recordingService;
  final AudioPlaybackService _playbackService;
  final AssetUploadService _uploadService;
  final VoiceRepository _repository;

  VoiceQaController({
    required AudioRecordingService recordingService,
    required AudioPlaybackService playbackService,
    required AssetUploadService uploadService,
    required VoiceRepository repository,
  })  : _recordingService = recordingService,
        _playbackService = playbackService,
        _uploadService = uploadService,
        _repository = repository,
        super(const VoiceQaState());

  Future<void> startRecording() async {
    try {
      await _recordingService.startRecording();
      state = state.copyWith(
        step: VoiceQaStep.recording,
        isRecording: true,
        errorMessage: null,
      );
    } catch (e) {
      state = state.copyWith(
        step: VoiceQaStep.error,
        errorMessage: 'Microphone access is required to ask BHOOMI.',
      );
    }
  }

  /// Stops recording, uploads the clip, and runs it through the full
  /// speech-to-speech pipeline, then auto-plays the spoken answer.
  Future<void> stopAndAsk({required String farmId, String lang = 'en-IN'}) async {
    if (!state.isRecording) return;

    try {
      final audioBytes = await _recordingService.stopRecording();
      if (audioBytes == null || audioBytes.isEmpty) {
        state = state.copyWith(
          step: VoiceQaStep.error,
          isRecording: false,
          errorMessage: 'No audio recorded. Please tap and speak again.',
        );
        return;
      }

      state = state.copyWith(
        step: VoiceQaStep.uploading,
        isRecording: false,
        recordedAudioBytes: audioBytes,
        uploadProgress: 0.0,
      );

      final assetId = await _uploadService.uploadAsset(
        bytes: audioBytes,
        contentType: 'audio/aac',
        assetType: 'audio',
        onProgress: (progress) {
          state = state.copyWith(uploadProgress: progress);
        },
      );

      state = state.copyWith(step: VoiceQaStep.thinking);

      final response = await _repository.askQuestion(
        audioAssetId: assetId,
        farmId: farmId,
        lang: lang,
      );

      state = state.appendTurn(
        VoiceQaTurn(
          transcript: response.transcript,
          answerText: response.answerText,
          audioResponseUrl: response.audioResponseUrl,
        ),
      );

      if (response.audioResponseUrl.isNotEmpty) {
        state = state.copyWith(step: VoiceQaStep.speaking);
        final played = await _playbackService.playUrl(response.audioResponseUrl);
        state = state.copyWith(
          step: VoiceQaStep.answered,
          errorMessage: played ? null : 'Got an answer, but audio playback failed — read it below.',
        );
      } else {
        state = state.copyWith(step: VoiceQaStep.answered);
      }
    } catch (e) {
      state = state.copyWith(
        step: VoiceQaStep.error,
        isRecording: false,
        errorMessage: 'Unable to process your question right now. Please try again.',
      );
    }
  }

  Future<void> replayLastAnswer() async {
    final url = state.lastTurn?.audioResponseUrl;
    if (url == null || url.isEmpty) return;
    await _playbackService.playUrl(url);
  }

  void reset() {
    _recordingService.cancelRecording();
    _playbackService.stop();
    state = const VoiceQaState();
  }

  @override
  void dispose() {
    _playbackService.stop();
    super.dispose();
  }
}
