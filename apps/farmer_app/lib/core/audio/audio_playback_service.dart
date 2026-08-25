import 'package:flutter/foundation.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:just_audio/just_audio.dart';

final audioPlaybackServiceProvider = Provider<AudioPlaybackService>((ref) {
  final service = AudioPlaybackService();
  ref.onDispose(() => service.dispose());
  return service;
});

class AudioPlaybackService {
  final AudioPlayer _player;
  bool _isPlaying = false;

  AudioPlaybackService({AudioPlayer? player}) : _player = player ?? AudioPlayer() {
    _player.playerStateStream.listen((state) {
      _isPlaying = state.playing;
    });
  }

  bool get isPlaying => _isPlaying;
  Stream<PlayerState> get playerStateStream => _player.playerStateStream;

  /// Loads and plays [url]. Returns `true` on success, `false` if playback
  /// couldn't start — the caller decides how (or whether) to surface that
  /// to the user; this only guarantees the failure isn't invisible.
  Future<bool> playUrl(String url) async {
    try {
      await _player.setUrl(url);
      await _player.play();
      return true;
    } catch (e) {
      debugPrint('AudioPlaybackService: failed to play $url — $e');
      return false;
    }
  }

  Future<void> stop() async {
    await _player.stop();
  }

  Future<void> pause() async {
    await _player.pause();
  }

  void dispose() {
    _player.dispose();
  }
}
