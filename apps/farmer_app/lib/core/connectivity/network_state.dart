enum NetworkStatus {
  online,
  degraded,
  unavailable,
}

class NetworkState {
  final NetworkStatus status;
  final String? message;

  const NetworkState({
    required this.status,
    this.message,
  });

  bool get isOnline => status == NetworkStatus.online;
  bool get isDegraded => status == NetworkStatus.degraded;
  bool get isUnavailable => status == NetworkStatus.unavailable;

  factory NetworkState.online() => const NetworkState(status: NetworkStatus.online);
  
  factory NetworkState.degraded({String? message}) => NetworkState(
        status: NetworkStatus.degraded,
        message: message ?? "Weak connection. We'll keep the experience lightweight.",
      );

  factory NetworkState.unavailable({String? message}) => NetworkState(
        status: NetworkStatus.unavailable,
        message: message ?? 'No network connection. Please check your signal and retry.',
      );
}
