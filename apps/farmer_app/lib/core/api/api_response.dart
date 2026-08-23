class ApiResponse<T> {
  final T? data;
  final bool isSuccess;
  final String? errorMessage;
  final int? statusCode;

  const ApiResponse({
    this.data,
    required this.isSuccess,
    this.errorMessage,
    this.statusCode,
  });

  factory ApiResponse.success(T data, {int? statusCode}) {
    return ApiResponse(
      data: data,
      isSuccess: true,
      statusCode: statusCode ?? 200,
    );
  }

  factory ApiResponse.failure(String message, {int? statusCode}) {
    return ApiResponse(
      isSuccess: false,
      errorMessage: message,
      statusCode: statusCode,
    );
  }
}
