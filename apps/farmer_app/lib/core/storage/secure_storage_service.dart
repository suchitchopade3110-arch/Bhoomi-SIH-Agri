import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

final secureStorageServiceProvider = Provider<SecureStorageService>((ref) {
  return SecureStorageService();
});

class SecureStorageService {
  final FlutterSecureStorage _storage;

  static const String _keyFarmId = 'bhoomi_current_farm_id';
  static const String _keyAuthToken = 'bhoomi_auth_token';

  SecureStorageService({FlutterSecureStorage? storage})
      : _storage = storage ??
            const FlutterSecureStorage(
              aOptions: AndroidOptions(encryptedSharedPreferences: true),
              iOptions: IOSOptions(accessibility: KeychainAccessibility.first_unlock),
            );

  Future<void> saveFarmId(String farmId) async {
    await _storage.write(key: _keyFarmId, value: farmId);
  }

  Future<String?> getFarmId() async {
    return await _storage.read(key: _keyFarmId);
  }

  Future<void> deleteFarmId() async {
    await _storage.delete(key: _keyFarmId);
  }

  Future<void> saveAuthToken(String token) async {
    await _storage.write(key: _keyAuthToken, value: token);
  }

  Future<String?> getAuthToken() async {
    return await _storage.read(key: _keyAuthToken);
  }

  Future<void> deleteAuthToken() async {
    await _storage.delete(key: _keyAuthToken);
  }

  Future<void> clearAll() async {
    await _storage.deleteAll();
  }
}
