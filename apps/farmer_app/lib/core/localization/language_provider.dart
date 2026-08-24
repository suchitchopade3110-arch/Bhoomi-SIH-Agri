import 'package:flutter_riverpod/flutter_riverpod.dart';

/// Language configuration model for BHOOMI multi-lingual voice & text advisory
class LanguageOption {
  final String code;
  final String nativeName;
  final String englishName;
  final String greeting;
  final String buttonLabel;

  const LanguageOption({
    required this.code,
    required this.nativeName,
    required this.englishName,
    required this.greeting,
    required this.buttonLabel,
  });
}

/// All supported languages in Bhoomi Farmer App
const List<LanguageOption> kSupportedLanguages = [
  LanguageOption(
    code: 'en-IN',
    nativeName: 'English',
    englishName: 'English (Indian)',
    greeting: 'Hello & Welcome',
    buttonLabel: 'Continue to Setup',
  ),
  LanguageOption(
    code: 'te-IN',
    nativeName: 'తెలుగు',
    englishName: 'Telugu',
    greeting: 'నమస్కారం',
    buttonLabel: 'కొనసాగించండి (Continue)',
  ),
  LanguageOption(
    code: 'ta-IN',
    nativeName: 'தமிழ்',
    englishName: 'Tamil',
    greeting: 'வணக்கம்',
    buttonLabel: 'தொடரவும் (Continue)',
  ),
  LanguageOption(
    code: 'hi-IN',
    nativeName: 'हिंदी',
    englishName: 'Hindi',
    greeting: 'नमस्ते',
    buttonLabel: 'आगे बढ़ें (Continue)',
  ),
  LanguageOption(
    code: 'kn-IN',
    nativeName: 'ಕನ್ನಡ',
    englishName: 'Kannada',
    greeting: 'ನಮಸ್ಕಾರ',
    buttonLabel: 'ಮುಂದುವರಿಯಿರಿ (Continue)',
  ),
  LanguageOption(
    code: 'mr-IN',
    nativeName: 'मराठी',
    englishName: 'Marathi',
    greeting: 'नमस्कार',
    buttonLabel: 'पुढे सुरू ठेवा (Continue)',
  ),
  LanguageOption(
    code: 'ml-IN',
    nativeName: 'മലയാളം',
    englishName: 'Malayalam',
    greeting: 'നമസ്കാരം',
    buttonLabel: 'തുടരുക (Continue)',
  ),
  LanguageOption(
    code: 'pa-IN',
    nativeName: 'ਪੰਜਾਬੀ',
    englishName: 'Punjabi',
    greeting: 'ਸਤਿ ਸ੍ਰੀ ਅਕਾਲ',
    buttonLabel: 'ਜਾਰੀ ਰੱਖੋ (Continue)',
  ),
];

/// Global provider tracking the user's selected language (defaults to en-IN before selection)
final selectedLanguageProvider = StateProvider<String>((ref) => 'en-IN');
