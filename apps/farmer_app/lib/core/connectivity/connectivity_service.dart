import 'dart:async';
import 'package:connectivity_plus/connectivity_plus.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'network_state.dart';

final connectivityServiceProvider = Provider<ConnectivityService>((ref) {
  final service = ConnectivityService();
  ref.onDispose(() => service.dispose());
  return service;
});

final networkStateProvider = StateNotifierProvider<NetworkNotifier, NetworkState>((ref) {
  final service = ref.watch(connectivityServiceProvider);
  return NetworkNotifier(service);
});

class ConnectivityService {
  final Connectivity _connectivity;
  final StreamController<NetworkState> _controller = StreamController<NetworkState>.broadcast();

  ConnectivityService({Connectivity? connectivity})
      : _connectivity = connectivity ?? Connectivity() {
    _init();
  }

  Stream<NetworkState> get stream => _controller.stream;

  void _init() {
    _connectivity.onConnectivityChanged.listen(_handleConnectivityResults);
  }

  void _handleConnectivityResults(List<ConnectivityResult> results) {
    if (results.isEmpty || results.contains(ConnectivityResult.none)) {
      _controller.add(NetworkState.unavailable());
    } else if (results.contains(ConnectivityResult.bluetooth) || results.contains(ConnectivityResult.other)) {
      _controller.add(NetworkState.degraded());
    } else {
      _controller.add(NetworkState.online());
    }
  }

  Future<NetworkState> checkCurrentState() async {
    final results = await _connectivity.checkConnectivity();
    if (results.isEmpty || results.contains(ConnectivityResult.none)) {
      return NetworkState.unavailable();
    } else if (results.contains(ConnectivityResult.bluetooth) || results.contains(ConnectivityResult.other)) {
      return NetworkState.degraded();
    }
    return NetworkState.online();
  }

  void dispose() {
    _controller.close();
  }
}

class NetworkNotifier extends StateNotifier<NetworkState> {
  final ConnectivityService _service;
  StreamSubscription<NetworkState>? _subscription;

  NetworkNotifier(this._service) : super(NetworkState.online()) {
    _init();
  }

  void _init() async {
    final current = await _service.checkCurrentState();
    state = current;
    _subscription = _service.stream.listen((newState) {
      state = newState;
    });
  }

  void setDegraded(bool degraded) {
    if (degraded) {
      state = NetworkState.degraded();
    } else {
      state = NetworkState.online();
    }
  }

  @override
  void dispose() {
    _subscription?.cancel();
    super.dispose();
  }
}
