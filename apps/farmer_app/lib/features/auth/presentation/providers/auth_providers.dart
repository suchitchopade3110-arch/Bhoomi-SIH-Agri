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

  AuthNotifier(this._repository) : super(const AsyncValue.loading()) {
    checkInitialAuth();
  }

  Future<void> checkInitialAuth() async {
    try {
      final token = await _repository.getPersistedToken();
      if (token != null && token.isNotEmpty) {
        state = AsyncValue.data(TokenResponse(
          accessToken: token,
          tokenType: 'bearer',
          expiresIn: 3600,
          userId: '',
          role: 'farmer',
        ));
      } else {
        state = const AsyncValue.data(null);
      }
    } catch (_) {
      state = const AsyncValue.data(null);
    }
  }

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
      rethrow;
    }
  }

  Future<void> register(UserRegisterRequest request) async {
    state = const AsyncValue.loading();
    try {
      await _repository.register(request);
      state = const AsyncValue.data(null);
    } catch (e, st) {
      state = AsyncValue.error(e, st);
      rethrow;
    }
  }

  Future<void> verifyOtp(OtpVerifyRequest request) async {
    state = const AsyncValue.loading();
    try {
      final res = await _repository.verifyOtp(request);
      state = AsyncValue.data(res);
    } catch (e, st) {
      state = AsyncValue.error(e, st);
      rethrow;
    }
  }

  Future<void> logout() async {
    await _repository.logout();
    state = const AsyncValue.data(null);
  }
}
