sealed class ApiException implements Exception {
  final String message;
  final String? code;
  final int? statusCode;
  final dynamic data;
  final Map<String, dynamic>? details;

  const ApiException({
    required this.message,
    this.code,
    this.statusCode,
    this.data,
    this.details,
  });

  @override
  String toString() => code != null ? '[$code] $message' : message;
}

class NetworkException extends ApiException {
  const NetworkException({
    super.message = 'Unable to connect to BHOOMI servers. Please check your connection.',
    super.code = 'NETWORK_UNAVAILABLE',
    super.statusCode,
    super.data,
    super.details,
  });
}

class UnauthorizedException extends ApiException {
  const UnauthorizedException({
    super.message = 'Session expired or unauthorized. Please sign in again.',
    super.code = 'UNAUTHENTICATED',
    super.statusCode = 401,
    super.data,
    super.details,
  });
}

class ValidationException extends ApiException {
  final List<String> missingFields;

  const ValidationException({
    super.message = 'Some farm details are missing or invalid.',
    this.missingFields = const [],
    super.code = 'VALIDATION_FAILED',
    super.statusCode = 422,
    super.data,
    super.details,
  });
}

class ServerException extends ApiException {
  const ServerException({
    super.message = 'A server error occurred. Please try again shortly.',
    super.code = 'SERVER_ERROR',
    super.statusCode = 500,
    super.data,
    super.details,
  });
}

class DomainException extends ApiException {
  const DomainException({
    required super.message,
    required super.code,
    super.statusCode = 400,
    super.data,
    super.details,
  });
}

class UnexpectedException extends ApiException {
  const UnexpectedException({
    super.message = 'An unexpected error occurred. Please try again.',
    super.code,
    super.statusCode,
    super.data,
    super.details,
  });
}
