class UserRegisterRequest {
  final String phoneNumber;
  final String fullName;
  final String role;
  final String preferredLanguage;
  final String password;

  const UserRegisterRequest({
    required this.phoneNumber,
    required this.fullName,
    this.role = 'farmer',
    this.preferredLanguage = 'ta',
    required this.password,
  });

  Map<String, dynamic> toJson() => {
        'phone_number': phoneNumber,
        'full_name': fullName,
        'role': role,
        'preferred_language': preferredLanguage,
        'password': password,
      };
}

class UserLoginRequest {
  final String phoneNumber;
  final String password;

  const UserLoginRequest({
    required this.phoneNumber,
    required this.password,
  });

  Map<String, dynamic> toJson() => {
        'phone_number': phoneNumber,
        'password': password,
      };
}

class TokenResponse {
  final String accessToken;
  final String tokenType;
  final int expiresIn;
  final String userId;
  final String role;

  const TokenResponse({
    required this.accessToken,
    required this.tokenType,
    required this.expiresIn,
    required this.userId,
    required this.role,
  });

  factory TokenResponse.fromJson(Map<String, dynamic> json) => TokenResponse(
        accessToken: json['access_token']?.toString() ?? '',
        tokenType: json['token_type']?.toString() ?? 'bearer',
        expiresIn: (json['expires_in'] as num?)?.toInt() ?? 0,
        userId: json['user_id']?.toString() ?? '',
        role: json['role']?.toString() ?? 'farmer',
      );

  Map<String, dynamic> toJson() => {
        'access_token': accessToken,
        'token_type': tokenType,
        'expires_in': expiresIn,
        'user_id': userId,
        'role': role,
      };
}

class UserResponse {
  final String id;
  final String phoneNumber;
  final String fullName;
  final String role;
  final String preferredLanguage;
  final String? createdAt;

  const UserResponse({
    required this.id,
    required this.phoneNumber,
    required this.fullName,
    required this.role,
    required this.preferredLanguage,
    this.createdAt,
  });

  factory UserResponse.fromJson(Map<String, dynamic> json) => UserResponse(
        id: json['id']?.toString() ?? '',
        phoneNumber: json['phone_number']?.toString() ?? '',
        fullName: json['full_name']?.toString() ?? '',
        role: json['role']?.toString() ?? 'farmer',
        preferredLanguage: json['preferred_language']?.toString() ?? 'ta',
        createdAt: json['created_at']?.toString(),
      );

  Map<String, dynamic> toJson() => {
        'id': id,
        'phone_number': phoneNumber,
        'full_name': fullName,
        'role': role,
        'preferred_language': preferredLanguage,
        if (createdAt != null) 'created_at': createdAt,
      };
}

class OtpRequestRequest {
  final String phoneNumber;

  const OtpRequestRequest({required this.phoneNumber});

  Map<String, dynamic> toJson() => {
        'phone_number': phoneNumber,
      };
}

class OtpRequestResponse {
  final String message;
  final int expiresIn;
  final String? debugOtp;

  const OtpRequestResponse({
    required this.message,
    required this.expiresIn,
    this.debugOtp,
  });

  factory OtpRequestResponse.fromJson(Map<String, dynamic> json) =>
      OtpRequestResponse(
        message: json['message']?.toString() ?? 'OTP sent.',
        expiresIn: (json['expires_in'] as num?)?.toInt() ?? 300,
        debugOtp: json['debug_otp']?.toString(),
      );

  Map<String, dynamic> toJson() => {
        'message': message,
        'expires_in': expiresIn,
        if (debugOtp != null) 'debug_otp': debugOtp,
      };
}

class OtpVerifyRequest {
  final String phoneNumber;
  final String otp;
  final String? fullName;
  final String preferredLanguage;

  const OtpVerifyRequest({
    required this.phoneNumber,
    required this.otp,
    this.fullName,
    this.preferredLanguage = 'ta',
  });

  Map<String, dynamic> toJson() => {
        'phone_number': phoneNumber,
        'otp': otp,
        if (fullName != null) 'full_name': fullName,
        'preferred_language': preferredLanguage,
      };
}
