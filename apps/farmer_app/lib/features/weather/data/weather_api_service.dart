import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../core/api/api_client.dart';
import '../../../core/api/api_exception.dart';
import '../../../shared/constants/api_constants.dart';
import 'models/weather_data.dart';

final weatherApiServiceProvider = Provider<WeatherApiService>((ref) {
  return WeatherApiService(ApiClient());
});

class WeatherApiService {
  final ApiClient _apiClient;

  WeatherApiService(this._apiClient);

  Future<WeatherData> getWeather(String farmId) async {
    try {
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
    } on NetworkException {
      if (ApiConstants.enableMockFallback) {
        return const WeatherData(
          temperatureC: 28.5,
          humidityPct: 72,
          rainfallMm: 0.0,
          rainfallProbPct: 10,
          condition: 'Partly Cloudy',
          forecastSummary: 'Dry conditions favorable for scheduled fieldwork and irrigation.',
          dailyForecast: [
            DailyForecastItem(day: 'Today', tempMaxC: 32, tempMinC: 24, condition: 'Partly Cloudy'),
            DailyForecastItem(day: 'Tomorrow', tempMaxC: 33, tempMinC: 24, condition: 'Sunny'),
            DailyForecastItem(day: 'Thu', tempMaxC: 31, tempMinC: 23, condition: 'Scattered Clouds'),
            DailyForecastItem(day: 'Fri', tempMaxC: 30, tempMinC: 23, condition: 'Light Rain'),
          ],
        );
      }
      rethrow;
    }
  }
}
