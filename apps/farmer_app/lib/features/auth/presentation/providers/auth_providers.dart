import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../data/auth_repository.dart';
import '../../data/models/auth_models.dart';

final currentUserProvider = FutureProvider<UserResponse>((ref) async {
  final repository = ref.watch(authRepositoryProvider);
  return await repository.getMe();
});

final authStateProvider = StateNotifierProvider<AuthNotifier, AsyncValue<TokenResponse?>>((ref) {
  final repository = ref.watch(authRepositoryProvider);
  return AuthNotifier(repository);
});

class AuthNotifier extends StateNotifier<AsyncValue<TokenResponse?>> {
  final AuthRepository _repository;

  AuthNotifier(this._repository) : super(const AsyncValue.data(null));

  Future<void> login(String phoneNumber, String password) async {
    state = const AsyncValue.loading();
    try {
      final res = await _repository.login(UserLoginRequest(
        phoneNumber: phoneNumber,
        password: password,
      ));
      state = AsyncValue.data(res);
    } catch (e, st) {
      state = AsyncValue.error(e, st);
    }
  }

  Future<void> verifyOtp(OtpVerifyRequest request) async {
    state = const AsyncValue.loading();
    try {
      final res = await _repository.verifyOtp(request);
      state = AsyncValue.data(res);
    } catch (e, st) {
      state = AsyncValue.error(e, st);
    }
  }

  Future<void> logout() async {
    await _repository.logout();
    state = const AsyncValue.data(null);
  }
}
