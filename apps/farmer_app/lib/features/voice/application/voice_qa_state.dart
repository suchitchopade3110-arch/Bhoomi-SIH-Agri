import 'dart:typed_data';

enum VoiceQaStep {
  idle,
  recording,
  uploading,
  thinking, // transcribing + retrieving + synthesizing on the backend
  speaking, // playing back the synthesized answer
  answered,
  error,
}

/// One turn of the speech-to-speech conversation, kept so the screen can
/// render a running transcript instead of only the latest exchange.
class VoiceQaTurn {
  final String transcript;
  final String answerText;
  final String audioResponseUrl;

  const VoiceQaTurn({
    required this.transcript,
    required this.answerText,
    required this.audioResponseUrl,
  });
}

class VoiceQaState {
  final VoiceQaStep step;
  final bool isRecording;
  final double uploadProgress;
  final Uint8List? recordedAudioBytes;
  final List<VoiceQaTurn> turns;
  final String? errorMessage;

  const VoiceQaState({
    this.step = VoiceQaStep.idle,
    this.isRecording = false,
    this.uploadProgress = 0.0,
    this.recordedAudioBytes,
    this.turns = const [],
    this.errorMessage,
  });

  bool get isIdle => step == VoiceQaStep.idle;
  bool get isBusy =>
      step == VoiceQaStep.uploading || step == VoiceQaStep.thinking;
  VoiceQaTurn? get lastTurn => turns.isEmpty ? null : turns.last;

  VoiceQaState copyWith({
    VoiceQaStep? step,
    bool? isRecording,
    double? uploadProgress,
    Uint8List? recordedAudioBytes,
    List<VoiceQaTurn>? turns,
    String? errorMessage,
  }) {
    return VoiceQaState(
      step: step ?? this.step,
      isRecording: isRecording ?? this.isRecording,
      uploadProgress: uploadProgress ?? this.uploadProgress,
      recordedAudioBytes: recordedAudioBytes ?? this.recordedAudioBytes,
      turns: turns ?? this.turns,
      // Same "always overwrite" convention as VoiceState.copyWith — omitting
      // the argument clears the error rather than sticking it forever.
      errorMessage: errorMessage,
    );
  }

  VoiceQaState appendTurn(VoiceQaTurn turn) => copyWith(turns: [...turns, turn]);
}
