import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'models/weather_data.dart';
import 'weather_api_service.dart';

final weatherRepositoryProvider = Provider<WeatherRepository>((ref) {
  final apiService = ref.watch(weatherApiServiceProvider);
  return WeatherRepository(apiService);
});

class WeatherRepository {
  final WeatherApiService _apiService;

  WeatherRepository(this._apiService);

  Future<WeatherData> getWeather(String farmId) async {
    return await _apiService.getWeather(farmId);
  }
}

final farmWeatherProvider =
    FutureProvider.family<WeatherData, String>((ref, farmId) async {
  final repository = ref.watch(weatherRepositoryProvider);
  return await repository.getWeather(farmId);
});
