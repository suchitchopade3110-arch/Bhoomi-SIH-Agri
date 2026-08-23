import 'dart:io';
import 'package:dio/dio.dart';
import '../../shared/constants/api_constants.dart';
import '../storage/secure_storage_service.dart';
import 'api_exception.dart';

class ApiClient {
  final Dio _dio;
  final SecureStorageService _storageService;

  ApiClient({
    Dio? dio,
    SecureStorageService? storageService,
  })  : _dio = dio ?? Dio(),
        _storageService = storageService ?? SecureStorageService() {
    _dio.options = BaseOptions(
      baseUrl: ApiConstants.baseApiUrl,
      connectTimeout: ApiConstants.connectTimeout,
      receiveTimeout: ApiConstants.receiveTimeout,
      sendTimeout: ApiConstants.sendTimeout,
      headers: {
        ApiConstants.contentTypeHeader: ApiConstants.applicationJson,
      },
    );

    _dio.interceptors.add(
      InterceptorsWrapper(
        onRequest: (options, handler) async {
          final token = await _storageService.getAuthToken();
          if (token != null && token.isNotEmpty) {
            options.headers[ApiConstants.authorizationHeader] = 'Bearer $token';
          }
          return handler.next(options);
        },
        onError: (DioException error, handler) {
          return handler.next(error);
        },
      ),
    );
  }

  Future<Response<T>> get<T>(
    String path, {
    Map<String, dynamic>? queryParameters,
    Options? options,
  }) async {
    try {
      return await _dio.get<T>(
        path,
        queryParameters: queryParameters,
        options: options,
      );
    } on DioException catch (e) {
      throw _handleDioError(e);
    } catch (e) {
      throw UnexpectedException(message: e.toString());
    }
  }

  Future<Response<T>> post<T>(
    String path, {
    dynamic data,
    Map<String, dynamic>? queryParameters,
    Options? options,
  }) async {
    try {
      return await _dio.post<T>(
        path,
        data: data,
        queryParameters: queryParameters,
        options: options,
      );
    } on DioException catch (e) {
      throw _handleDioError(e);
    } catch (e) {
      throw UnexpectedException(message: e.toString());
    }
  }

  ApiException _handleDioError(DioException error) {
    switch (error.type) {
      case DioExceptionType.connectionTimeout ||
          DioExceptionType.sendTimeout ||
          DioExceptionType.receiveTimeout ||
          DioExceptionType.connectionError ||
          DioExceptionType.badCertificate ||
          DioExceptionType.transformTimeout:
        return const NetworkException(
          message: 'Connection timed out or network is unreachable. Please try again.',
        );
      case DioExceptionType.badResponse:
        final statusCode = error.response?.statusCode;
        final responseData = error.response?.data;

        String? errCode;
        String? errMsg;
        Map<String, dynamic>? errDetails;

        if (responseData is Map) {
          if (responseData['error'] is Map) {
            final errObj = responseData['error'] as Map;
            errCode = errObj['code']?.toString();
            errMsg = errObj['message']?.toString();
            if (errObj['details'] is Map) {
              errDetails = Map<String, dynamic>.from(errObj['details'] as Map);
            }
          } else if (responseData['detail'] != null) {
            errMsg = responseData['detail'].toString();
          } else if (responseData['message'] != null) {
            errMsg = responseData['message'].toString();
          }
        }

        if (statusCode == 401 || statusCode == 403) {
          return UnauthorizedException(
            message: errMsg ?? (statusCode == 401 ? 'Session expired or unauthorized. Please sign in again.' : 'Access forbidden.'),
            code: errCode ?? (statusCode == 401 ? 'UNAUTHENTICATED' : 'FORBIDDEN'),
            statusCode: statusCode,
            data: responseData,
            details: errDetails,
          );
        }

        if (errCode != null && errCode.isNotEmpty) {
          return DomainException(
            message: errMsg ?? 'Domain operation rejected: $errCode',
            code: errCode,
            statusCode: statusCode ?? 400,
            data: responseData,
            details: errDetails,
          );
        }

        if (statusCode == 422 || statusCode == 400) {
          List<String> missing = [];
          if (responseData is Map && responseData.containsKey('missing_fields')) {
            missing = List<String>.from(responseData['missing_fields']);
          }
          return ValidationException(
            message: errMsg ?? 'Invalid request data.',
            missingFields: missing,
            code: errCode ?? 'VALIDATION_FAILED',
            statusCode: statusCode,
            data: responseData,
            details: errDetails,
          );
        }

        if (statusCode != null && statusCode >= 500) {
          return ServerException(
            message: errMsg ?? 'Server error ($statusCode). Please try again shortly.',
            statusCode: statusCode,
            data: responseData,
            details: errDetails,
          );
        }

        return UnexpectedException(
          message: errMsg ?? 'Error occurred: ${error.message}',
          code: errCode,
          statusCode: statusCode,
          data: responseData,
          details: errDetails,
        );

      case DioExceptionType.cancel:
        return const UnexpectedException(message: 'Request was cancelled.');

      case DioExceptionType.unknown:
        if (error.error is SocketException) {
          return const NetworkException(
            message: 'No internet connection detected.',
          );
        }
        return UnexpectedException(message: error.message ?? 'Unknown error occurred.');
    }
  }
}
