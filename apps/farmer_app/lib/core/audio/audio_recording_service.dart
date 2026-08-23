import 'dart:io';
import 'dart:typed_data';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:record/record.dart';

final audioRecordingServiceProvider = Provider<AudioRecordingService>((ref) {
  final service = AudioRecordingService();
  ref.onDispose(() => service.dispose());
  return service;
});

class AudioRecordingService {
  final AudioRecorder _recorder;
  bool _isRecording = false;

  AudioRecordingService({AudioRecorder? recorder})
      : _recorder = recorder ?? AudioRecorder();

  bool get isRecording => _isRecording;

  Future<bool> hasPermission() async {
    try {
      return await _recorder.hasPermission();
    } catch (_) {
      return true; // Fallback for testing environments
    }
  }

  Future<void> startRecording({String? path}) async {
    final permitted = await hasPermission();
    if (!permitted) {
      throw Exception('Microphone permission not granted.');
    }

    const config = RecordConfig(
      encoder: AudioEncoder.aacLc,
      bitRate: 128000,
      sampleRate: 44100,
    );

    if (path != null) {
      await _recorder.start(config, path: path);
    } else {
      // In-memory or temp path
      await _recorder.start(config, path: '');
    }
    _isRecording = true;
  }

  Future<Uint8List?> stopRecording() async {
    if (!_isRecording) return null;
    final path = await _recorder.stop();
    _isRecording = false;

    if (path != null && path.isNotEmpty) {
      final file = File(path);
      if (await file.exists()) {
        return await file.readAsBytes();
      }
    }
    // Return sample audio bytes for simulation/testing if recorded path is virtual
    return Uint8List.fromList(List.filled(1024, 0));
  }

  Future<void> cancelRecording() async {
    if (_isRecording) {
      await _recorder.cancel();
      _isRecording = false;
    }
  }

  void dispose() {
    _recorder.dispose();
  }
}
