import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/api/api_client.dart';
import '../../../shared/constants/api_constants.dart';
import 'models/weather_data.dart';

final weatherApiServiceProvider = Provider<WeatherApiService>((ref) {
  return WeatherApiService(ApiClient());
});

class WeatherApiService {
  final ApiClient _apiClient;

  WeatherApiService(this._apiClient);

  Future<WeatherData> getWeather(String farmId) async {
    final response = await _apiClient.get(
      ApiConstants.farmWeather(farmId),
    );

    if (response.data is Map<String, dynamic>) {
      final map = response.data as Map<String, dynamic>;
      final weatherMap = map['weather_summary'] is Map<String, dynamic>
          ? map['weather_summary'] as Map<String, dynamic>
          : map;
      return WeatherData.fromJson(weatherMap);
    }
    throw Exception('Invalid weather response payload format.');
  }
}
