import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/storage/secure_storage_service.dart';
import 'auth_api_service.dart';
import 'models/auth_models.dart';

final authRepositoryProvider = Provider<AuthRepository>((ref) {
  final apiService = ref.watch(authApiServiceProvider);
  final storageService = SecureStorageService();
  return AuthRepository(apiService, storageService);
});

class AuthRepository {
  final AuthApiService _apiService;
  final SecureStorageService _storageService;

  AuthRepository(this._apiService, this._storageService);

  Future<UserResponse> register(UserRegisterRequest request) async {
    return await _apiService.register(request);
  }

  Future<TokenResponse> login(UserLoginRequest request) async {
    final token = await _apiService.login(request);
    await _storageService.saveAuthToken(token.accessToken);
    return token;
  }

  Future<UserResponse> getMe() async {
    return await _apiService.getMe();
  }

  Future<OtpRequestResponse> requestOtp(String phoneNumber) async {
    return await _apiService.requestOtp(OtpRequestRequest(phoneNumber: phoneNumber));
  }

  Future<TokenResponse> verifyOtp(OtpVerifyRequest request) async {
    final token = await _apiService.verifyOtp(request);
    await _storageService.saveAuthToken(token.accessToken);
    return token;
  }

  Future<void> logout() async {
    await _storageService.deleteAuthToken();
  }

  Future<String?> getPersistedToken() async {
    return await _storageService.getAuthToken();
  }
}
