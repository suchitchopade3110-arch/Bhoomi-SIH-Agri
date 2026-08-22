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

  Future<void> playUrl(String url) async {
    try {
      await _player.setUrl(url);
      await _player.play();
    } catch (_) {
      // Audio playback enhancement fails gracefully without crashing the UI
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
