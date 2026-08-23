import 'dart:typed_data';
import '../data/models/transcribe_response.dart';

enum VoiceFlowStep {
  idle,
  recording,
  uploading,
  transcribing,
  confirming,
  completed,
  error,
}

class VoiceState {
  final VoiceFlowStep step;
  final bool isRecording;
  final bool isUploading;
  final bool isTranscribing;
  final bool isSynthesizing;
  final bool isPlaying;
  final double uploadProgress;
  final Uint8List? recordedAudioBytes;
  final String? uploadedAssetId;
  final TranscribeResponse? transcription;
  final String? synthesizedAudioUrl;
  final String? errorMessage;

  const VoiceState({
    this.step = VoiceFlowStep.idle,
    this.isRecording = false,
    this.isUploading = false,
    this.isTranscribing = false,
    this.isSynthesizing = false,
    this.isPlaying = false,
    this.uploadProgress = 0.0,
    this.recordedAudioBytes,
    this.uploadedAssetId,
    this.transcription,
    this.synthesizedAudioUrl,
    this.errorMessage,
  });

  bool get isIdle => step == VoiceFlowStep.idle;
  bool get isConfirming => step == VoiceFlowStep.confirming;
  bool get isCompleted => step == VoiceFlowStep.completed;

  VoiceState copyWith({
    VoiceFlowStep? step,
    bool? isRecording,
    bool? isUploading,
    bool? isTranscribing,
    bool? isSynthesizing,
    bool? isPlaying,
    double? uploadProgress,
    Uint8List? recordedAudioBytes,
    String? uploadedAssetId,
    TranscribeResponse? transcription,
    String? synthesizedAudioUrl,
    String? errorMessage,
  }) {
    return VoiceState(
      step: step ?? this.step,
      isRecording: isRecording ?? this.isRecording,
      isUploading: isUploading ?? this.isUploading,
      isTranscribing: isTranscribing ?? this.isTranscribing,
      isSynthesizing: isSynthesizing ?? this.isSynthesizing,
      isPlaying: isPlaying ?? this.isPlaying,
      uploadProgress: uploadProgress ?? this.uploadProgress,
      recordedAudioBytes: recordedAudioBytes ?? this.recordedAudioBytes,
      uploadedAssetId: uploadedAssetId ?? this.uploadedAssetId,
      transcription: transcription ?? this.transcription,
      synthesizedAudioUrl: synthesizedAudioUrl ?? this.synthesizedAudioUrl,
      errorMessage: errorMessage,
    );
  }
}
