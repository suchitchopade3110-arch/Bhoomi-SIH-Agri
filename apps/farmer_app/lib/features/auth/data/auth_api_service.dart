import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/api/api_client.dart';
import '../../../shared/constants/api_constants.dart';
import 'models/auth_models.dart';

final authApiServiceProvider = Provider<AuthApiService>((ref) {
  return AuthApiService(ApiClient());
});

class AuthApiService {
  final ApiClient _apiClient;

  AuthApiService(this._apiClient);

  Future<UserResponse> register(UserRegisterRequest request) async {
    final response = await _apiClient.post(
      ApiConstants.authRegister,
      data: request.toJson(),
    );

    if (response.data is Map<String, dynamic>) {
      return UserResponse.fromJson(response.data as Map<String, dynamic>);
    }
    throw Exception('Invalid register response payload.');
  }

  Future<TokenResponse> login(UserLoginRequest request) async {
    final response = await _apiClient.post(
      ApiConstants.authLogin,
      data: request.toJson(),
    );

    if (response.data is Map<String, dynamic>) {
      return TokenResponse.fromJson(response.data as Map<String, dynamic>);
    }
    throw Exception('Invalid login response payload.');
  }

  Future<UserResponse> getMe() async {
    final response = await _apiClient.get(
      ApiConstants.authMe,
    );

    if (response.data is Map<String, dynamic>) {
      return UserResponse.fromJson(response.data as Map<String, dynamic>);
    }
    throw Exception('Invalid user profile response payload.');
  }

  Future<OtpRequestResponse> requestOtp(OtpRequestRequest request) async {
    final response = await _apiClient.post(
      ApiConstants.authOtpRequest,
      data: request.toJson(),
    );

    if (response.data is Map<String, dynamic>) {
      return OtpRequestResponse.fromJson(response.data as Map<String, dynamic>);
    }
    throw Exception('Invalid OTP request response payload.');
  }

  Future<TokenResponse> verifyOtp(OtpVerifyRequest request) async {
    final response = await _apiClient.post(
      ApiConstants.authOtpVerify,
      data: request.toJson(),
    );

    if (response.data is Map<String, dynamic>) {
      return TokenResponse.fromJson(response.data as Map<String, dynamic>);
    }
    throw Exception('Invalid OTP verify response payload.');
  }
}
