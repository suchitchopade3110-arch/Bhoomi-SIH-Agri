import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'language_provider.dart';

class BhoomiStrings {
  final String languageCode;

  const BhoomiStrings(this.languageCode);

  // App Bar / Branding
  String get appTitle => 'BHOOMI';
  String get appSubtitle => _t({
    'en-IN': 'AI-Powered Farmer Companion',
    'te-IN': 'రైతులకు AI మిత్రుడు',
    'ta-IN': 'விவசாயிகளுக்கான AI தோழன்',
    'hi-IN': 'किसानों का AI साथी',
    'kn-IN': 'ರೈತರಿಗೆ AI ಒಡನಾಡಿ',
    'mr-IN': 'शेतकऱ्यांचा AI मित्र',
    'ml-IN': 'കർഷകർക്കുള്ള AI സഹായി',
    'pa-IN': 'ਕਿਸਾਨਾਂ ਦਾ AI ਸਾਥੀ',
  });

  // Welcome Screen (always English base, but accessible here too)
  String get welcomeTitle => 'BHOOMI';
  String get welcomeSubtitle => 'AI-Powered Farmer Companion';
  String get welcomeDesc =>
      'Your trusted digital farming partner for land verification, crop health, and intelligent farm assistance.';
  String get getStarted => 'Get Started';
  String get hackathonBadge => 'Smart India Hackathon SIH25076';

  // Language Selection Screen
  String get chooseLanguageTitle => _t({
    'en-IN': 'Choose Your Language',
    'te-IN': 'మీ భాషను ఎంచుకోండి',
    'ta-IN': 'உங்கள் மொழியைத் தேர்ந்தெடுக்கவும்',
    'hi-IN': 'अपनी भाषा चुनें',
    'kn-IN': 'ನಿಮ್ಮ ಭಾಷೆಯನ್ನು ಆಯ್ಕೆಮಾಡಿ',
    'mr-IN': 'तुमची भाषा निवडा',
    'ml-IN': 'നിങ്ങളുടെ ഭാഷ തിരഞ്ഞെടുക്കുക',
    'pa-IN': 'ਆਪਣੀ ਭਾਸ਼ਾ ਚੁਣੋ',
  });
  String get chooseLanguageDesc => _t({
    'en-IN': 'BHOOMI will speak, listen, and provide intelligent farm advisories in your preferred language.',
    'te-IN': 'భూమి మీ ప్రాధాన్య భాషలోనే మాట్లాడుతుంది, వింటుంది మరియు తెలివైన వ్యవసాయ సలహాలను అందిస్తుంది.',
    'ta-IN': 'பூமி உங்கள் விருப்ப மொழியிலேயே பேசும், கேட்கும் மற்றும் நுண்ணறிவு பண்ணை ஆலோசனைகளை வழங்கும்.',
    'hi-IN': 'भूमि आपकी पसंदीदा भाषा में बोलेगी, सुनेगी और सटीक कृषि सलाह प्रदान करेगी।',
    'kn-IN': 'ಭೂಮಿ ನಿಮ್ಮ ಆದ್ಯತೆಯ ಭಾಷೆಯಲ್ಲಿ ಮಾತನಾಡುತ್ತದೆ, ಕೇಳುತ್ತದೆ ಮತ್ತು ಕೃಷಿ ಸಲಹೆಗಳನ್ನು ನೀಡುತ್ತದೆ.',
    'mr-IN': 'भूमी तुमच्या पसंतीच्या भाषेत बोलेल, ऐकेल आणि अचूक शेतीविषयक सल्ला देईल.',
    'ml-IN': 'ഭൂമി നിങ്ങളുടെ ഇഷ്ട ഭാഷയിൽ സംസാരിക്കുകയും കേൾക്കുകയും കൃഷി ഉപദേശങ്ങൾ നൽകുകയും ചെയ്യും.',
    'pa-IN': 'ਭੂਮੀ ਤੁਹਾਡੀ ਪਸੰਦੀਦਾ ਭਾਸ਼ਾ ਵਿੱਚ ਬੋਲੇਗੀ, ਸੁਣੇਗੀ ਅਤੇ ਖੇਤੀ ਸਲਾਹ ਪ੍ਰਦਾਨ ਕਰੇਗੀ।',
  });

  // Onboarding Screen
  String get onboardingTitle => _t({
    'en-IN': 'Tell us about your farm',
    'te-IN': 'మీ పొలం వివరాలు తెలియజేయండి',
    'ta-IN': 'உங்கள் பண்ணை விவரங்களை தெரிவியுங்கள்',
    'hi-IN': 'अपने खेत के बारे में बताएं',
    'kn-IN': 'ನಿಮ್ಮ ಕೃಷಿ ವಿವರಗಳನ್ನು ತಿಳಿಸಿ',
    'mr-IN': 'तुमच्या शेतीबद्दल सांगा',
    'ml-IN': 'നിങ്ങളുടെ കൃഷിയിടത്തെക്കുറിച്ച് പറയുക',
    'pa-IN': 'ਆਪਣੇ ਖੇਤ ਬਾਰੇ ਦੱਸੋ',
  });

  // Step 1: Crop
  String get cropStepTitle => _t({
    'en-IN': 'What crop are you growing?',
    'te-IN': 'మీరు ఏ పంట పండిస్తున్నారు?',
    'ta-IN': 'நீங்கள் என்ன பயிர் செய்கிறீர்கள்?',
    'hi-IN': 'आप कौन सी फसल उगा रहे हैं?',
    'kn-IN': 'ನೀವು ಯಾವ ಬೆಳೆ ಬೆಳೆಯುತ್ತಿದ್ದೀರಿ?',
    'mr-IN': 'तुम्ही कोणते पीक घेत आहात?',
    'ml-IN': 'നിങ്ങൾ ഏത് വിളയാണ് വളർത്തുന്നത്?',
    'pa-IN': 'ਤੁਸੀਂ ਕਿਹੜੀ ਫਸਲ ਉਗਾ ਰਹੇ ਹੋ?',
  });
  String get cropStepSub => _t({
    'en-IN': 'Speak clearly or select your crop from the list below',
    'te-IN': 'స్పష్టంగా మాట్లాడండి లేదా క్రింది జాబితా నుండి మీ పంటను ఎంచుకోండి',
    'ta-IN': 'தெளிவாகப் பேசவும் அல்லது கீழேயுள்ள பட்டியலிலிருந்து தேர்ந்தெடுக்கவும்',
    'hi-IN': 'स्पष्ट बोलें या नीचे दी गई सूची से अपनी फसल चुनें',
    'kn-IN': 'ಸ್ಪಷ್ಟವಾಗಿ ಮಾತನಾಡಿ ಅಥವಾ ಕೆಳಗಿನ ಪಟ್ಟಿಯಿಂದ ನಿಮ್ಮ ಬೆಳೆಯನ್ನು ಆಯ್ಕೆಮಾಡಿ',
    'mr-IN': 'स्पष्ट बोला किंवा खालील यादीतून तुमचे पीक निवडा',
    'ml-IN': 'വ്യക്തമായി സംസാരിക്കുക അല്ലെങ്കിൽ താഴെയുള്ള പട്ടികയിൽ നിന്ന് തിരഞ്ഞെടുക്കുക',
    'pa-IN': 'ਸਪੱਸ਼ਟ ਬੋਲੋ ਜਾਂ ਹੇਠਾਂ ਦਿੱਤੀ ਸੂਚੀ ਵਿੱਚੋਂ ਆਪਣੀ ਫਸਲ ਚੁਣੋ',
  });
  String get cropVoicePrompt => _t({
    'en-IN': 'Tap to speak your crop',
    'te-IN': 'మీ పంట పేరు చెప్పడానికి తాకండి',
    'ta-IN': 'உங்கள் பயிரைப் பேச தட்டவும்',
    'hi-IN': 'अपनी फसल बोलने के लिए टैप करें',
    'kn-IN': 'ನಿಮ್ಮ ಬೆಳೆ ಹೆಸರು ಹೇಳಲು ಟ್ಯಾಪ್ ಮಾಡಿ',
    'mr-IN': 'तुमचे पीक सांगण्यासाठी टॅप करा',
    'ml-IN': 'വിളയുടെ പേര് പറയാൻ ടാപ്പ് ചെയ്യുക',
    'pa-IN': 'ਆਪਣੀ ਫਸਲ ਬੋਲਣ ਲਈ ਟੈਪ ਕਰੋ',
  });
  String get quickSelectOptions => _t({
    'en-IN': 'Quick Selection Options',
    'te-IN': 'శీఘ్ర ఎంపికలు',
    'ta-IN': 'விரைவுத் தேர்வுகள்',
    'hi-IN': 'त्वरित चयन विकल्प',
    'kn-IN': 'ತ್ವರಿತ ಆಯ್ಕೆಗಳು',
    'mr-IN': 'द्रुत निवड पर्याय',
    'ml-IN': 'പെട്ടെന്നുള്ള തിരഞ്ഞെടുപ്പുകൾ',
    'pa-IN': 'ਤੁਰੰਤ ਚੋਣ ਵਿਕਲਪ',
  });

  // Crops Names
  String cropName(String cropId) {
    switch (cropId) {
      case 'samba_paddy':
        return _t({
          'en-IN': 'Samba Paddy',
          'te-IN': 'సాంబ వరి',
          'ta-IN': 'சம்பா நெல்',
          'hi-IN': 'सांबा धान',
          'kn-IN': 'ಸಾಂಬಾ ಭತ್ತ',
          'mr-IN': 'सांबा भात',
          'ml-IN': 'സാമ്പ നെല്ല്',
          'pa-IN': 'ਸਾਂਬਾ ਝੋਨਾ',
        });
      case 'kuruvai_paddy':
        return _t({
          'en-IN': 'Kuruvai Paddy',
          'te-IN': 'కురువై వరి',
          'ta-IN': 'குறுவை நெல்',
          'hi-IN': 'कुरुवई धान',
          'kn-IN': 'ಕುರುವೈ ಭತ್ತ',
          'mr-IN': 'कुरुवई भात',
          'ml-IN': 'കുറുവായ് നെല്ല്',
          'pa-IN': 'ਕੁਰੂਵਈ ਝੋਨਾ',
        });
      case 'sugarcane':
        return _t({
          'en-IN': 'Sugarcane',
          'te-IN': 'చెరకు',
          'ta-IN': 'கரும்பு',
          'hi-IN': 'गन्ना',
          'kn-IN': 'ಕಬ್ಬು',
          'mr-IN': 'ऊस',
          'ml-IN': 'കരിമ്പ്',
          'pa-IN': 'ਗੰਨਾ',
        });
      case 'cotton':
        return _t({
          'en-IN': 'Cotton',
          'te-IN': 'పత్తి',
          'ta-IN': 'பருத்தி',
          'hi-IN': 'कपास',
          'kn-IN': 'ಹತ್ತಿ',
          'mr-IN': 'कापूस',
          'ml-IN': 'പരുത്തി',
          'pa-IN': 'ਕਪਾਹ',
        });
      case 'banana':
        return _t({
          'en-IN': 'Banana',
          'te-IN': 'అరటి',
          'ta-IN': 'வாழை',
          'hi-IN': 'केला',
          'kn-IN': 'ಬಾಳೆ',
          'mr-IN': 'केळी',
          'ml-IN': 'വാഴ',
          'pa-IN': 'ਕੇਲਾ',
        });
      case 'maize':
        return _t({
          'en-IN': 'Maize (Corn)',
          'te-IN': 'మొక్కజొన్న',
          'ta-IN': 'மக்காச்சோளம்',
          'hi-IN': 'मक्का',
          'kn-IN': 'ಮೆಕ್ಕೆಜೋಳ',
          'mr-IN': 'मका',
          'ml-IN': 'ചോളം',
          'pa-IN': 'ਮੱਕੀ',
        });
      default:
        return cropId.replaceAll('_', ' ').toUpperCase();
    }
  }

  String cropSubtitle(String cropId) {
    switch (cropId) {
      case 'samba_paddy':
        return _t({
          'en-IN': 'Traditional long-duration rice',
          'te-IN': 'సాంప్రదాయ దీర్ఘకాలిక వరి పంట',
          'ta-IN': 'பாரம்பரிய நீண்ட கால நெல்',
          'hi-IN': 'पारंपरिक लंबी अवधि का धान',
          'kn-IN': 'ಸಾಂಪ್ರದಾಯಿಕ ದೀರ್ಘಾವಧಿ ಭತ್ತ',
          'mr-IN': 'पारंपारिक दीर्घ मुदतीचा भात',
          'ml-IN': 'പരമ്പരാഗത ദീർഘകാല നെല്ല്',
          'pa-IN': 'ਰਵਾਇਤੀ ਲੰਬੇ ਸਮੇਂ ਦਾ ਝੋਨਾ',
        });
      case 'kuruvai_paddy':
        return _t({
          'en-IN': 'Short-duration summer crop',
          'te-IN': 'స్వల్పకాలిక వేసవి వరి పంట',
          'ta-IN': 'குறுகிய கால கோடைப் பயிர்',
          'hi-IN': 'अल्पकालिक ग्रीष्मकालीन फसल',
          'kn-IN': 'ಅಲ್ಪಾವಧಿ ಬೇಸಿಗೆ ಬೆಳೆ',
          'mr-IN': 'अल्पकालीन उन्हाळी पीक',
          'ml-IN': 'ഹ്രസ്വകാല വേനൽക്കാല വിള',
          'pa-IN': 'ਥੋੜ੍ਹੇ ਸਮੇਂ ਦੀ ਗਰਮੀਆਂ ਦੀ ਫਸਲ',
        });
      case 'sugarcane':
        return _t({
          'en-IN': 'Commercial perennial crop',
          'te-IN': 'వాణిజ్య బహువార్షిక పంట',
          'ta-IN': 'வணிக பல்லாண்டுப் பயிர்',
          'hi-IN': 'व्यावसायिक बारहमासी फसल',
          'kn-IN': 'ವಾಣಿಜ್ಯ ದೀರ್ಘಕಾಲೀನ ಬೆಳೆ',
          'mr-IN': 'व्यावसायिक बारमाही पीक',
          'ml-IN': 'വാണിജ്യ ബഹുവർഷ വിള',
          'pa-IN': 'ਵਪਾਰਕ ਸਾਲਾਨਾ ਫਸਲ',
        });
      case 'cotton':
        return _t({
          'en-IN': 'Cash fiber crop',
          'te-IN': 'వాణిజ్య నూలు పంట',
          'ta-IN': 'பணப்பயிர் இழை',
          'hi-IN': 'नकदी रेशा फसल',
          'kn-IN': 'ವಾಣಿಜ್ಯ ನಾರು ಬೆಳೆ',
          'mr-IN': 'नगदी फायबर पीक',
          'ml-IN': 'നാണ്യ ഫൈബർ വിള',
          'pa-IN': 'ਨਕਦੀ ਫਾਈਬਰ ਫਸਲ',
        });
      case 'banana':
        return _t({
          'en-IN': 'Fruit plantation',
          'te-IN': 'పండ్ల తోట పంట',
          'ta-IN': 'பழத்தோட்டம்',
          'hi-IN': 'फल बागान',
          'kn-IN': 'ಹಣ್ಣಿನ ತೋಟ',
          'mr-IN': 'फळबाग लागवड',
          'ml-IN': 'ഫലവൃക്ഷ തോട്ടം',
          'pa-IN': 'ਫਲਾਂ ਦਾ ਬਾਗ',
        });
      case 'maize':
        return _t({
          'en-IN': 'Nutrient-rich grain',
          'te-IN': 'పోషకాలు కలిగిన ధాన్యం',
          'ta-IN': 'சத்து நிறைந்த தானியம்',
          'hi-IN': 'पोषक तत्वों से भरपूर अनाज',
          'kn-IN': 'ಪೌಷ್ಟಿಕ ಧಾನ್ಯ',
          'mr-IN': 'पौष्टिक धान्य',
          'ml-IN': 'പോഷക സമ്പുഷ്ടമായ ധാന്യം',
          'pa-IN': 'ਪੌਸ਼ਟਿਕ ਅਨਾਜ',
        });
      default:
        return '';
    }
  }

  // Step 2: Land Area
  String get areaStepTitle => _t({
    'en-IN': 'How much land are you farming?',
    'te-IN': 'మీ సాగు విస్తీర్ణం ఎంత?',
    'ta-IN': 'எவ்வளவு நிலத்தில் விவசாயம் செய்கிறீர்கள்?',
    'hi-IN': 'आपकी खेती की भूमि कितनी है?',
    'kn-IN': 'ನಿಮ್ಮ ಕೃಷಿ ಭೂಮಿ ಎಷ್ಟು?',
    'mr-IN': 'तुमची शेती किती एकर आहे?',
    'ml-IN': 'എത്രത്തോളം സ്ഥലത്താണ് കൃഷി ചെയ്യുന്നത്?',
    'pa-IN': 'ਤੁਹਾਡੀ ਕਿੰਨੀ ਜ਼ਮੀਨ ਹੈ?',
  });
  String get areaStepSub => _t({
    'en-IN': 'Self-reported area in acres for official verification',
    'te-IN': 'అధికారిక ధృవీకరణ కోసం ఎకరాలలో విస్తీర్ణం',
    'ta-IN': 'அதிகாரப்பூர்வ சரிபார்ப்பிற்கான பரப்பளவு (ஏக்கர்)',
    'hi-IN': 'आधिकारिक सत्यापन के लिए एकड़ में क्षेत्र',
    'kn-IN': 'ಅಧಿಕೃತ ಪರಿಶೀಲನೆಗಾಗಿ ಎಕರೆಗಳಲ್ಲಿ ವಿಸ್ತೀರ್ಣ',
    'mr-IN': 'अधिकृत पडताळणीसाठी एकर क्षेत्र',
    'ml-IN': 'ഔദ്യോഗിക പരിശോധനയ്ക്കായി ഏക്കർ കണക്ക്',
    'pa-IN': 'ਅਧਿਕਾਰਤ ਪੁਸ਼ਟੀ ਲਈ ਏਕੜ ਰਕਬਾ',
  });
  String get areaVoicePrompt => _t({
    'en-IN': 'Tap to speak your farm size',
    'te-IN': 'పొలం విస్తీర్ణం చెప్పడానికి తాకండి',
    'ta-IN': 'நிலப்பரப்பைப் பேச தட்டவும்',
    'hi-IN': 'खेत का आकार बोलने के लिए टैप करें',
    'kn-IN': 'ಭೂಮಿಯ ವಿಸ್ತೀರ್ಣ ಹೇಳಲು ಟ್ಯಾಪ್ ಮಾಡಿ',
    'mr-IN': 'शेताचे क्षेत्र सांगण्यासाठी टॅप करा',
    'ml-IN': 'വലിപ്പം പറയാൻ ടാപ്പ് ചെയ്യുക',
    'pa-IN': 'ਰਕਬਾ ਬੋਲਣ ਲਈ ਟੈਪ ਕਰੋ',
  });
  String get selectFarmAreaTitle => _t({
    'en-IN': 'Select Farm Area (Acres)',
    'te-IN': 'పొలం విస్తీర్ణాన్ని ఎంచుకోండి (ఎకరాలు)',
    'ta-IN': 'பண்ணை பரப்பளவைத் தேர்ந்தெடுக்கவும் (ஏக்கர்)',
    'hi-IN': 'खेत का क्षेत्रफल चुनें (एकड़)',
    'kn-IN': 'ಕೃಷಿ ಪ್ರದೇಶ ಆಯ್ಕೆಮಾಡಿ (ಎಕರೆ)',
    'mr-IN': 'शेतीचे क्षेत्र निवडा (एकर)',
    'ml-IN': 'വിസ്തൃതി തിരഞ്ഞെടുക്കുക (ഏക്കർ)',
    'pa-IN': 'ਖੇਤ ਦਾ ਰਕਬਾ ਚੁਣੋ (ਏਕੜ)',
  });
  String formatAcres(double acres) {
    final acresUnit = _t({
      'en-IN': acres == 1.0 ? 'Acre' : 'Acres',
      'te-IN': 'ఎకరాలు',
      'ta-IN': 'ஏக்கர்',
      'hi-IN': 'एकड़',
      'kn-IN': 'ಎಕರೆ',
      'mr-IN': 'एकर',
      'ml-IN': 'ഏക്കർ',
      'pa-IN': 'ਏਕੜ',
    });
    return '$acres $acresUnit';
  }

  // Step 3: Growth Stage
  String get growthStepTitle => _t({
    'en-IN': 'What stage is your crop in?',
    'te-IN': 'మీ పంట ప్రస్తుతం ఏ దశలో ఉంది?',
    'ta-IN': 'உங்கள் பயிர் எந்த நிலையில் உள்ளது?',
    'hi-IN': 'आपकी फसल किस चरण में है?',
    'kn-IN': 'ನಿಮ್ಮ ಬೆಳೆ ಯಾವ ಹಂತದಲ್ಲಿದೆ?',
    'mr-IN': 'तुमचे पीक कोणत्या टप्प्यावर आहे?',
    'ml-IN': 'നിങ്ങളുടെ വിള ഏത് ഘട്ടത്തിലാണ്?',
    'pa-IN': 'ਤੁਹਾਡੀ ਫਸਲ ਕਿਸ ਪੜਾਅ \'ਤੇ ਹੈ?',
  });
  String get growthStepSub => _t({
    'en-IN': 'Helps track growth phase and land readiness',
    'te-IN': 'పంట పెరుగుదల దశ మరియు నీటి అవసరాలను ట్రాక్ చేయడానికి',
    'ta-IN': 'வளர்ச்சி நிலை மற்றும் தேவைகளைக் கண்காணிக்க உதவுகிறது',
    'hi-IN': 'विकास चरण और पानी की जरूरतों को ट्रैक करने में मदद करता है',
    'kn-IN': 'ಬೆಳವಣಿಗೆಯ ಹಂತ ತಿಳಿಯಲು ನೆರವಾಗುತ್ತದೆ',
    'mr-IN': 'वाढीचा टप्पा ट्रॅक करण्यास मदत करते',
    'ml-IN': 'വളർച്ചാ ഘട്ടം നിരീക്ഷിക്കാൻ സഹായിക്കുന്നു',
    'pa-IN': 'ਵਿਕਾਸ ਪੜਾਅ ਨੂੰ ਟਰੈਕ ਕਰਨ ਵਿੱਚ ਮਦਦ ਕਰਦਾ ਹੈ',
  });
  String get growthVoicePrompt => _t({
    'en-IN': 'Tap to speak current stage',
    'te-IN': 'ప్రస్తుత దశను చెప్పడానికి తాకండి',
    'ta-IN': 'தற்போதைய நிலையைப் பேச தட்டவும்',
    'hi-IN': 'वर्तमान चरण बोलने के लिए टैप करें',
    'kn-IN': 'ಪ್ರಸ್ತುತ ಹಂತ ಹೇಳಲು ಟ್ಯಾಪ್ ಮಾಡಿ',
    'mr-IN': 'सद्य स्थिती सांगण्यासाठी टॅप करा',
    'ml-IN': 'നിലവിലെ ഘട്ടം പറയാൻ ടാപ്പ് ചെയ്യുക',
    'pa-IN': 'ਮੌਜੂਦਾ ਪੜਾਅ ਬੋਲਣ ਲਈ ਟੈਪ ਕਰੋ',
  });
  String get selectGrowthStageTitle => _t({
    'en-IN': 'Select Current Stage',
    'te-IN': 'ప్రస్తుత దశను ఎంచుకోండి',
    'ta-IN': 'தற்போதைய நிலையைத் தேர்ந்தெடுக்கவும்',
    'hi-IN': 'वर्तमान चरण चुनें',
    'kn-IN': 'ಪ್ರಸ್ತುತ ಹಂತ ಆಯ್ಕೆಮಾಡಿ',
    'mr-IN': 'सद्य स्थिती निवडा',
    'ml-IN': 'ഘട്ടം തിരഞ്ഞെടുക്കുക',
    'pa-IN': 'ਮੌਜੂਦਾ ਪੜਾਅ ਚੁਣੋ',
  });

  String stageName(String stageId) {
    switch (stageId) {
      case 'vegetative':
        return _t({
          'en-IN': 'Vegetative',
          'te-IN': 'శాఖీయ దశ (ఆకులు/కొమ్మలు)',
          'ta-IN': 'பயிர் வளர்ச்சி நிலை',
          'hi-IN': 'वानस्पतिक अवस्था',
          'kn-IN': 'ಸಸ್ಯಕ ಬೆಳವಣಿಗೆ ಹಂತ',
          'mr-IN': 'शाकीय वाढ अवस्था',
          'ml-IN': 'സസ്യ വളർച്ചാ ഘട്ടം',
          'pa-IN': 'ਬਨਸਪਤੀ ਪੜਾਅ',
        });
      case 'flowering':
        return _t({
          'en-IN': 'Flowering',
          'te-IN': 'పూత దశ',
          'ta-IN': 'பூக்கும் நிலை',
          'hi-IN': 'फूल आने की अवस्था',
          'kn-IN': 'ಹೂಬಿಡುವ ಹಂತ',
          'mr-IN': 'फुलधारणा अवस्था',
          'ml-IN': 'പൂവിടൽ ഘട്ടം',
          'pa-IN': 'ਫੁੱਲ ਪੈਣ ਦਾ ਪੜਾਅ',
        });
      case 'grain_filling':
        return _t({
          'en-IN': 'Grain Filling',
          'te-IN': 'గింజ పాలుపోసుకునే దశ',
          'ta-IN': 'தானியம் உருவாகும் நிலை',
          'hi-IN': 'दाना भरने की अवस्था',
          'kn-IN': 'ಕಾಳು ಕಟ್ಟುವ ಹಂತ',
          'mr-IN': 'दाणे भरणे अवस्था',
          'ml-IN': 'ധാന്യ രൂപീകരണ ഘട്ടം',
          'pa-IN': 'ਦਾਣਾ ਭਰਨ ਦਾ ਪੜਾਅ',
        });
      case 'maturity':
        return _t({
          'en-IN': 'Maturity',
          'te-IN': 'పక్వ దశ (ముదిరిన పంట)',
          'ta-IN': 'முதிர்ச்சி நிலை',
          'hi-IN': 'परिपक्व अवस्था',
          'kn-IN': 'ಪಕ್ವತೆಯ ಹಂತ',
          'mr-IN': 'पक्वता अवस्था',
          'ml-IN': 'വിളവെടുപ്പ് പാകം',
          'pa-IN': 'ਪੱਕਣ ਦਾ ਪੜਾਅ',
        });
      case 'harvest_ready':
        return _t({
          'en-IN': 'Harvest Ready',
          'te-IN': 'కోతకు సిద్ధం',
          'ta-IN': 'அறுவடைக்கு தயார்',
          'hi-IN': 'कटाई के लिए तैयार',
          'kn-IN': 'ಕೊಯ್ಲಿಗೆ ಸಿದ್ಧ',
          'mr-IN': 'काढणीस तयार',
          'ml-IN': 'വിളവെടുക്കാൻ തയ്യാർ',
          'pa-IN': 'ਵਾਢੀ ਲਈ ਤਿਆਰ',
        });
      default:
        return stageId.replaceAll('_', ' ');
    }
  }

  String stageSubtitle(String stageId) {
    switch (stageId) {
      case 'vegetative':
        return _t({
          'en-IN': 'Leaf & stem rapid growth stage',
          'te-IN': 'ఆకులు మరియు కాండం వేగంగా పెరిగే దశ',
          'ta-IN': 'இலை மற்றும் தண்டு விரைவான வளர்ச்சி',
          'hi-IN': 'पत्ती और तने के तेजी से विकास का चरण',
          'kn-IN': 'ಎಲೆ ಮತ್ತು ಕಾಂಡದ ವೇಗದ ಬೆಳವಣಿಗೆ',
          'mr-IN': 'पाने आणि खोडाची जलद वाढ',
          'ml-IN': 'ഇലകളും തണ്ടും വേഗത്തിൽ വളരുന്ന ഘട്ടം',
          'pa-IN': 'ਪੱਤੇ ਅਤੇ ਤਣੇ ਦਾ ਤੇਜ਼ੀ ਨਾਲ ਵਿਕਾਸ',
        });
      case 'flowering':
        return _t({
          'en-IN': 'Bloom and pollination active',
          'te-IN': 'పూత మరియు పరాగ సంపర్క దశ',
          'ta-IN': 'மலர்ச்சி மற்றும் மகரந்தச் சேர்க்கை',
          'hi-IN': 'फूल और परागण सक्रिय',
          'kn-IN': 'ಹೂ ಮತ್ತು ಪರಾಗಸ್ಪರ್ಶ ಕ್ರಿಯೆ',
          'mr-IN': 'फुले आणि परागीभवन सक्रिय',
          'ml-IN': 'പൂക്കളും പരാഗണവും സജീവം',
          'pa-IN': 'ਫੁੱਲ ਅਤੇ ਪਰਾਗਣ ਸਰਗਰਮ',
        });
      case 'grain_filling':
        return _t({
          'en-IN': 'Panicle & grain development',
          'te-IN': 'కంకి మరియు గింజలు అభివృద్ధి చెందే దశ',
          'ta-IN': 'கதிர் மற்றும் தானிய வளர்ச்சி',
          'hi-IN': 'बाली और दाने का विकास',
          'kn-IN': 'ತೆನೆ ಮತ್ತು ಧಾನ್ಯ ಬೆಳವಣಿಗೆ',
          'mr-IN': 'कणीस आणि दाण्यांचा विकास',
          'ml-IN': 'കതിരും ധാന്യവും വികസിക്കുന്നു',
          'pa-IN': 'ਸਿੱਟਾ ਅਤੇ ਦਾਣੇ ਦਾ ਵਿਕਾਸ',
        });
      case 'maturity':
        return _t({
          'en-IN': 'Crop turning golden / ripening',
          'te-IN': 'పంట పక్వానికి వచ్చి బంగారు రంగులోకి మారుతుంది',
          'ta-IN': 'பயிர் பொன்னிறமாக மாறும் நிலை',
          'hi-IN': 'फसल सुनहरी / पकने की ओर',
          'kn-IN': 'ಬೆಳೆ ಬಂಗಾರದ ಬಣ್ಣಕ್ಕೆ ತಿರುಗುತ್ತಿದೆ',
          'mr-IN': 'पीक पिवळे/पक्व होत आहे',
          'ml-IN': 'വിള പാകമായി സ്വർണ്ണ നിറമാകുന്നു',
          'pa-IN': 'ਫਸਲ ਸੁਨਹਿਰੀ / ਪੱਕ ਰਹੀ ਹੈ',
        });
      case 'harvest_ready':
        return _t({
          'en-IN': 'Ready for cutting and yield collection',
          'te-IN': 'కోత కోసి దిగుబడిని సేకరించడానికి సిద్ధంగా ఉంది',
          'ta-IN': 'அறுவடை மற்றும் மகசூல் சேகரிப்புக்கு தயார்',
          'hi-IN': 'कटाई और उपज एकत्र करने के लिए तैयार',
          'kn-IN': 'ಕಟಾವು ಮತ್ತು ಇಳುವರಿ ಸಂಗ್ರಹಕ್ಕೆ ಸಿದ್ಧ',
          'mr-IN': 'कापणी आणि उत्पादन गोळा करण्यासाठी सज्ज',
          'ml-IN': 'വിളവെടുപ്പിനും ശേഖരണത്തിനും തയ്യാർ',
          'pa-IN': 'ਕਟਾਈ ਅਤੇ ਝਾੜ ਇਕੱਠਾ ਕਰਨ ਲਈ ਤਿਆਰ',
        });
      default:
        return '';
    }
  }

  // Confirm Profile Screen
  String get confirmProfileTitle => _t({
    'en-IN': 'Confirm Farm Profile',
    'te-IN': 'పొలం ప్రొఫైల్ నిర్ధారించండి',
    'ta-IN': 'பண்ணை சுயவிவரத்தை உறுதிப்படுத்தவும்',
    'hi-IN': 'खेत प्रोफ़ाइल की पुष्टि करें',
    'kn-IN': 'ಕೃಷಿ ಪ್ರೊಫೈಲ್ ದೃಢೀಕರಿಸಿ',
    'mr-IN': 'शेत प्रोफाइलची पुष्टी करा',
    'ml-IN': 'ഫാം പ്രൊഫൈൽ സ്ഥിരീകരിക്കുക',
    'pa-IN': 'ਖੇਤ ਪ੍ਰੋਫਾਈਲ ਦੀ ਪੁਸ਼ਟੀ ਕਰੋ',
  });
  String get yourFarmProfile => _t({
    'en-IN': 'Your Farm Profile',
    'te-IN': 'మీ పొలం ప్రొఫైల్',
    'ta-IN': 'உங்கள் பண்ணை சுயவிவரம்',
    'hi-IN': 'आपका खेत प्रोफ़ाइल',
    'kn-IN': 'ನಿಮ್ಮ ಕೃಷಿ ಪ್ರೊಫೈಲ್',
    'mr-IN': 'तुमचे शेत प्रोफाइल',
    'ml-IN': 'നിങ്ങളുടെ ഫാം പ്രൊഫൈൽ',
    'pa-IN': 'ਤੁਹਾਡਾ ਖੇਤ ਪ੍ਰੋਫਾਈਲ',
  });
  String get confirmProfileReviewDesc => _t({
    'en-IN': 'Please review your self-reported farm details before submitting for official registration.',
    'te-IN': 'అధికారిక నమోదుకు సమర్పించే ముందు మీ పొలం వివరాలను ఒకసారి సరిచూసుకోండి.',
    'ta-IN': 'அதிகாரப்பூர்வ பதிவுக்கு முன் உங்கள் பண்ணை விவரங்களை சரிபார்க்கவும்.',
    'hi-IN': 'आधिकारिक पंजीकरण के लिए सबमिट करने से पहले अपने खेत के विवरण की समीक्षा करें।',
    'kn-IN': 'ಅಧಿಕೃತ ನೋಂದಣಿಗೆ ಸಲ್ಲಿಸುವ ಮೊದಲು ನಿಮ್ಮ ಕೃಷಿ ವಿವರಗಳನ್ನು ಪರಿಶೀಲಿಸಿ.',
    'mr-IN': 'अधिकृत नोंदणीसाठी सबमिट करण्यापूर्वी आपल्या शेताच्या तपशीलांची खात्री करा.',
    'ml-IN': 'ഔദ്യോഗിക രജിസ്ട്രേഷനായി സമർപ്പിക്കുന്നതിന് മുമ്പ് വിവരങ്ങൾ പരിശോധിക്കുക.',
    'pa-IN': 'ਅਧਿਕਾਰਤ ਰਜਿਸਟ੍ਰੇਸ਼ਨ ਲਈ ਜਮ੍ਹਾਂ ਕਰਨ ਤੋਂ ਪਹਿਲਾਂ ਆਪਣੇ ਵੇਰਵਿਆਂ ਦੀ ਸਮੀਖਿਆ ਕਰੋ।',
  });
  String get saveMyFarm => _t({
    'en-IN': 'Save My Farm',
    'te-IN': 'నా పొలాన్ని నమోదు చేయండి',
    'ta-IN': 'எனது பண்ணையைச் சேமிக்கவும்',
    'hi-IN': 'मेरा खेत सहेजें',
    'kn-IN': 'ನನ್ನ ಕೃಷಿ ಉಳಿಸಿ',
    'mr-IN': 'माझे शेत सेव्ह करा',
    'ml-IN': 'എൻ്റെ ഫാം സേവ് ചെയ്യുക',
    'pa-IN': 'ਮੇਰਾ ਖੇਤ ਸੰਭਾਲੋ',
  });
  String get labelCrop => _t({
    'en-IN': 'Crop',
    'te-IN': 'పంట',
    'ta-IN': 'பயிர்',
    'hi-IN': 'फसल',
    'kn-IN': 'ಬೆಳೆ',
    'mr-IN': 'पीक',
    'ml-IN': 'വിള',
    'pa-IN': 'ਫਸਲ',
  });
  String get labelLandArea => _t({
    'en-IN': 'Land Area',
    'te-IN': 'భూమి విస్తీర్ణం',
    'ta-IN': 'நிலப்பரப்பு',
    'hi-IN': 'भूमि क्षेत्र',
    'kn-IN': 'ಭೂಮಿ ವಿಸ್ತೀರ್ಣ',
    'mr-IN': 'जमीन क्षेत्र',
    'ml-IN': 'ഭൂമി വിസ്തൃതി',
    'pa-IN': 'ਜ਼ਮੀਨ ਦਾ ਰਕਬਾ',
  });
  String get labelGrowthStage => _t({
    'en-IN': 'Growth Stage',
    'te-IN': 'పెరుగుదల దశ',
    'ta-IN': 'வளர்ச்சி நிலை',
    'hi-IN': 'विकास चरण',
    'kn-IN': 'ಬೆಳವಣಿಗೆಯ ಹಂತ',
    'mr-IN': 'वाढीचा टप्पा',
    'ml-IN': 'വളർച്ചാ ഘട്ടം',
    'pa-IN': 'ਵਿਕਾਸ ਪੜਾਅ',
  });

  // Navigation / Buttons
  String get back => _t({
    'en-IN': 'Back',
    'te-IN': 'వెనుకకు',
    'ta-IN': 'பின்செல்',
    'hi-IN': 'पीछे',
    'kn-IN': 'ಹಿಂದೆ',
    'mr-IN': 'मागे',
    'ml-IN': 'പിന്നോട്ട്',
    'pa-IN': 'ਪਿੱਛੇ',
  });
  String get nextStep => _t({
    'en-IN': 'Next Step',
    'te-IN': 'తదుపరి దశ',
    'ta-IN': 'அடுத்த படி',
    'hi-IN': 'अगला कदम',
    'kn-IN': 'ಮುಂದಿನ ಹಂತ',
    'mr-IN': 'पुढची पायरी',
    'ml-IN': 'അടുത്ത ഘട്ടം',
    'pa-IN': 'ਅਗਲਾ ਕਦਮ',
  });
  String get reviewProfile => _t({
    'en-IN': 'Review Profile',
    'te-IN': 'ప్రొఫైల్ పరిశీలన',
    'ta-IN': 'சுயவிவர ஆய்வு',
    'hi-IN': 'प्रोफ़ाइल की समीक्षा करें',
    'kn-IN': 'ಪ್ರೊಫೈಲ್ ಪರಿಶೀಲಿಸಿ',
    'mr-IN': 'प्रोफाइल तपासा',
    'ml-IN': 'പ്രൊഫൈൽ പരിശോധിക്കുക',
    'pa-IN': 'ਪ੍ਰੋਫਾਈਲ ਦੀ ਸਮੀਖਿਆ ਕਰੋ',
  });
  String get continueText => _t({
    'en-IN': 'Continue',
    'te-IN': 'కొనసాగించండి',
    'ta-IN': 'தொடரவும்',
    'hi-IN': 'आगे बढ़ें',
    'kn-IN': 'ಮುಂದುವರಿಯಿರಿ',
    'mr-IN': 'पुढे जा',
    'ml-IN': 'തുടരുക',
    'pa-IN': 'ਜਾਰੀ ਰੱਖੋ',
  });
  String get retry => _t({
    'en-IN': 'Retry',
    'te-IN': 'మళ్ళీ ప్రయత్నించండి',
    'ta-IN': 'மீண்டும் முயற்சி செய்க',
    'hi-IN': 'पुनः प्रयास करें',
    'kn-IN': 'ಮತ್ತೆ ಪ್ರಯತ್ನಿಸಿ',
    'mr-IN': 'पुन्हा प्रयत्न करा',
    'ml-IN': 'വീണ്ടും ശ്രമിക്കുക',
    'pa-IN': 'ਦੁਬਾਰਾ ਕੋਸ਼ਿਸ਼ ਕਰੋ',
  });
  String get changeLanguage => _t({
    'en-IN': 'Change Language',
    'te-IN': 'భాషను మార్చండి',
    'ta-IN': 'மொழியை மாற்றவும்',
    'hi-IN': 'भाषा बदलें',
    'kn-IN': 'ಭಾಷೆ ಬದಲಾಯಿಸಿ',
    'mr-IN': 'भाषा बदला',
    'ml-IN': 'ഭാഷ മാറ്റുക',
    'pa-IN': 'ਭਾਸ਼ਾ ਬਦਲੋ',
  });

  // Farm Dashboard / Home
  String get dailyCompanion => _t({
    'en-IN': 'Daily Companion',
    'te-IN': 'దైనందిన సహచరి',
    'ta-IN': 'தினசரி துணை',
    'hi-IN': 'दैनिक साथी',
    'kn-IN': 'ದೈನಂದಿನ ಒಡನಾಡಿ',
    'mr-IN': 'दैनिक साथी',
    'ml-IN': 'പ്രതിദിന സഹായി',
    'pa-IN': 'ਰੋਜ਼ਾਨਾ ਸਾਥੀ',
  });
  String get myFarm => _t({
    'en-IN': 'My Farm',
    'te-IN': 'నా పొలం',
    'ta-IN': 'எனது பண்ணை',
    'hi-IN': 'मेरा खेत',
    'kn-IN': 'ನನ್ನ ಕೃಷಿ',
    'mr-IN': 'माझे शेत',
    'ml-IN': 'എൻ്റെ കൃഷിയിടം',
    'pa-IN': 'ਮੇਰਾ ਖੇਤ',
  });
  String get whatWouldYouLikeToDo => _t({
    'en-IN': 'What would you like to do?',
    'te-IN': 'మీరు ఏమి చేయాలనుకుంటున్నారు?',
    'ta-IN': 'நீங்கள் என்ன செய்ய விரும்புகிறீர்கள்?',
    'hi-IN': 'आप क्या करना चाहते हैं?',
    'kn-IN': 'ನೀವು ಏನು ಮಾಡಲು ಬಯಸುತ್ತೀರಿ?',
    'mr-IN': 'तुम्हाला काय करायचे आहे?',
    'ml-IN': 'നിങ്ങൾ എന്താണ് ചെയ്യാൻ ആഗ്രഹിക്കുന്നത്?',
    'pa-IN': 'ਤੁਸੀਂ ਕੀ ਕਰਨਾ ਚਾਹੁੰਦੇ ਹੋ?',
  });
  String get askBhoomi => _t({
    'en-IN': 'Ask BHOOMI',
    'te-IN': 'భూమిని అడగండి',
    'ta-IN': 'பூமியிடம் கேளுங்கள்',
    'hi-IN': 'भूमि से पूछें',
    'kn-IN': 'ಭೂಮಿಯನ್ನು ಕೇಳಿ',
    'mr-IN': 'भूमीला विचारा',
    'ml-IN': 'ഭൂമിയോട് ചോദിക്കുക',
    'pa-IN': 'ਭੂਮੀ ਨੂੰ ਪੁੱਛੋ',
  });
  String get voiceAssistant => _t({
    'en-IN': 'Voice Assistant',
    'te-IN': 'వాయిస్ అసిస్టెంట్',
    'ta-IN': 'குரல் உதவியாளர்',
    'hi-IN': 'वॉयस असिस्टेंट',
    'kn-IN': 'ಧ್ವನಿ ಸಹಾಯಕ',
    'mr-IN': 'व्हॉइस असिस्टंट',
    'ml-IN': 'വോയ്‌സ് അസിസ്റ്റന്റ്',
    'pa-IN': 'ਆਵਾਜ਼ ਸਹਾਇਕ',
  });
  String get showProblem => _t({
    'en-IN': 'Show Problem',
    'te-IN': 'సమస్యను చూపించండి',
    'ta-IN': 'சிக்கலைக் காட்டுங்கள்',
    'hi-IN': 'समस्या दिखाएं',
    'kn-IN': 'ಸಮಸ್ಯೆ ತೋರಿಸಿ',
    'mr-IN': 'समस्या दाखवा',
    'ml-IN': 'പ്രശ്നം കാണിക്കുക',
    'pa-IN': 'ਸਮੱਸਿਆ ਦਿਖਾਓ',
  });
  String get uploadCropPhoto => _t({
    'en-IN': 'Upload Crop Photo',
    'te-IN': 'పంట ఫోటో తీయండి',
    'ta-IN': 'பயிர் புகைப்படம் பதிவேற்றவும்',
    'hi-IN': 'फसल की फोटो अपलोड करें',
    'kn-IN': 'ಬೆಳೆಯ ಫೋಟೋ ಅಪ್‌ಲೋಡ್ ಮಾಡಿ',
    'mr-IN': 'पिकाचा फोटो अपलोड करा',
    'ml-IN': 'വിള ഫോട്ടോ എടുക്കുക',
    'pa-IN': 'ਫਸਲ ਦੀ ਫੋਟੋ ਅੱਪਲੋਡ ਕਰੋ',
  });
  String get govSupport => _t({
    'en-IN': 'Government Support',
    'te-IN': 'ప్రభుత్వ పథకాలు',
    'ta-IN': 'அரசு உதவி',
    'hi-IN': 'सरकारी सहायता',
    'kn-IN': 'ಸರ್ಕಾರಿ ನೆರವು',
    'mr-IN': 'शासकीय मदत',
    'ml-IN': 'സർക്കാർ സഹായം',
    'pa-IN': 'ਸਰਕਾਰੀ ਸਹਾਇਤਾ',
  });
  String get schemesAndSubsidies => _t({
    'en-IN': 'Schemes & Subsidies',
    'te-IN': 'పథకాలు & సబ్సిడీలు',
    'ta-IN': 'திட்டங்கள் & மானியங்கள்',
    'hi-IN': 'योजनाएं और सब्सिडी',
    'kn-IN': 'ಯೋಜನೆಗಳು ಮತ್ತು ಸಬ್ಸಿಡಿ',
    'mr-IN': 'योजना आणि सबसिडी',
    'ml-IN': 'പദ്ധതികളും സബ്‌സിഡികളും',
    'pa-IN': 'ਸਕੀਮਾਂ ਅਤੇ ਸਬਸਿਡੀ',
  });
  String get requiresVerifiedLand => _t({
    'en-IN': 'Requires Verified Land',
    'te-IN': 'భూమి ధృవీకరణ అవసరం',
    'ta-IN': 'சரிபார்க்கப்பட்ட நிலம் தேவை',
    'hi-IN': 'सत्यापित भूमि आवश्यक',
    'kn-IN': 'ಪರಿಶೀಲಿಸಿದ ಭೂಮಿ ಅಗತ್ಯವಿದೆ',
    'mr-IN': 'पडताळणी झालेली जमीन आवश्यक',
    'ml-IN': 'സ്ഥിരീകരിച്ച ഭൂമി ആവശ്യമാണ്',
    'pa-IN': 'ਪ੍ਰਮਾਣਿਤ ਜ਼ਮੀਨ ਦੀ ਲੋੜ ਹੈ',
  });
  String get myFarmJourney => _t({
    'en-IN': 'My Farm Journey',
    'te-IN': 'నా వ్యవసాయ ప్రయాణం',
    'ta-IN': 'எனது பண்ணைப் பயணம்',
    'hi-IN': 'मेरी कृषि यात्रा',
    'kn-IN': 'ನನ್ನ ಕೃಷಿ ಪಯಣ',
    'mr-IN': 'माझा शेती प्रवास',
    'ml-IN': 'എൻ്റെ കൃഷി യാത്ര',
    'pa-IN': 'ਮੇਰੀ ਖੇਤੀ ਯਾਤਰਾ',
  });
  String get activityTimeline => _t({
    'en-IN': 'Activity Timeline',
    'te-IN': 'కార్యకలాపాల కాలక్రమం',
    'ta-IN': 'செயல்பாட்டு காலவரிசை',
    'hi-IN': 'गतिविधि समयरेखा',
    'kn-IN': 'ಚಟುವಟಿಕೆ ಕಾಲಮಾನ',
    'mr-IN': 'क्रियाकलाप टाइमलाइन',
    'ml-IN': 'പ്രവർത്തന സമയക്രമം',
    'pa-IN': 'ਗਤੀਵਿਧੀ ਟਾਈਮਲਾਈਨ',
  });
  String get todaysFarmBrief => _t({
    'en-IN': "Today's Farm Brief",
    'te-IN': 'నేటి వ్యవసాయ సమాచారం',
    'ta-IN': 'இன்றைய பண்ணைச் சுருக்கம்',
    'hi-IN': 'आज का खेत सारांश',
    'kn-IN': 'ಇಂದಿನ ಕೃಷಿ ಮಾಹಿತಿ',
    'mr-IN': 'आजचा शेती अहवाल',
    'ml-IN': 'ഇന്നത്തെ കൃഷി വിവരണം',
    'pa-IN': 'ਅੱਜ ਦਾ ਖੇਤੀ ਸਾਰ',
  });
  String get latestUpdates => _t({
    'en-IN': 'Latest Updates',
    'te-IN': 'తాజా సమాచారం',
    'ta-IN': 'சமீபத்திய அறிவிப்புகள்',
    'hi-IN': 'नवीनतम अपडेट',
    'kn-IN': 'ಇತ್ತೀಚಿನ ಅಪ್‌ಡೇಟ್‌ಗಳು',
    'mr-IN': 'ताज्या घडामोडी',
    'ml-IN': 'പുതിയ വിവരങ്ങൾ',
    'pa-IN': 'ਤਾਜ਼ਾ ਅਪਡੇਟਾਂ',
  });
  String get viewFullBrief => _t({
    'en-IN': 'View Full Brief',
    'te-IN': 'పూర్తి సమాచారాన్ని చూడండి',
    'ta-IN': 'முழு விவரங்களைக் காண்க',
    'hi-IN': 'पूरा सारांश देखें',
    'kn-IN': 'ಪೂರ್ಣ ಮಾಹಿತಿ ನೋಡಿ',
    'mr-IN': 'पूर्ण माहिती पहा',
    'ml-IN': 'പൂർണ്ണ വിവരണം കാണുക',
    'pa-IN': 'ਪੂਰਾ ਸਾਰ ਦੇਖੋ',
  });
  String get viewAllUpdates => _t({
    'en-IN': 'View All Updates',
    'te-IN': 'అన్ని సమాచారాలను చూడండి',
    'ta-IN': 'அனைத்து அறிவிப்புகளையும் காண்க',
    'hi-IN': 'सभी अपडेट देखें',
    'kn-IN': 'ಎಲ್ಲಾ ಅಪ್‌ಡೇಟ್‌ಗಳನ್ನು ನೋಡಿ',
    'mr-IN': 'सर्व अपडेट्स पहा',
    'ml-IN': 'എല്ലാ അപ്‌ഡേറ്റുകളും കാണുക',
    'pa-IN': 'ਸਾਰੇ ਅਪਡੇਟ ਦੇਖੋ',
  });
  String get primaryCropLabel => _t({
    'en-IN': 'Primary Crop',
    'te-IN': 'ప్రధాన పంట',
    'ta-IN': 'முக்கிய பயிர்',
    'hi-IN': 'मुख्य फसल',
    'kn-IN': 'ಮುಖ್ಯ ಬೆಳೆ',
    'mr-IN': 'मुख्य पीक',
    'ml-IN': 'പ്രധാന വിള',
    'pa-IN': 'ਮੁੱਖ ਫਸਲ',
  });

  // Land Verification Status
  String landStatusText(String status) {
    switch (status.toLowerCase()) {
      case 'verified':
        return _t({
          'en-IN': 'Verified Land',
          'te-IN': 'ధృవీకరించబడిన భూమి',
          'ta-IN': 'சரிபார்க்கப்பட்ட நிலம்',
          'hi-IN': 'सत्यापित भूमि',
          'kn-IN': 'ಪರಿಶೀಲಿಸಿದ ಭೂಮಿ',
          'mr-IN': 'पडताळणी झालेली जमीन',
          'ml-IN': 'സ്ഥിരീകരിച്ച ഭൂമി',
          'pa-IN': 'ਪ੍ਰਮਾਣਿਤ ਜ਼ਮੀਨ',
        });
      case 'action_required':
        return _t({
          'en-IN': 'Action Required',
          'te-IN': 'చర్య అవసరం',
          'ta-IN': 'நடவடிக்கை தேவை',
          'hi-IN': 'कार्रवाई आवश्यक',
          'kn-IN': 'ಕ್ರಮ ಅಗತ್ಯವಿದೆ',
          'mr-IN': 'कृती आवश्यक',
          'ml-IN': 'നടപടി വേണം',
          'pa-IN': 'ਕਾਰਵਾਈ ਦੀ ਲੋੜ',
        });
      default:
        return _t({
          'en-IN': 'Verification Pending',
          'te-IN': 'ధృవీకరణ పెండింగ్‌లో ఉంది',
          'ta-IN': 'சரிபார்ப்பு நிலுவையில் உள்ளது',
          'hi-IN': 'सत्यापन लंबित',
          'kn-IN': 'ಪರಿಶೀಲನೆ ಬಾಕಿ ಇದೆ',
          'mr-IN': 'पडताळणी प्रलंबित',
          'ml-IN': 'പരിശോധന ബാക്കി',
          'pa-IN': 'ਪੁਸ਼ਟੀ ਬਾਕੀ ਹੈ',
        });
    }
  }

  // Quick helper to fetch translation based on languageCode
  String _t(Map<String, String> localizedMap) {
    return localizedMap[languageCode] ??
        localizedMap['en-IN'] ??
        localizedMap.values.first;
  }
}

/// Global provider for Bhoomi strings dynamically bound to selectedLanguageProvider
final bhoomiStringsProvider = Provider<BhoomiStrings>((ref) {
  final langCode = ref.watch(selectedLanguageProvider);
  return BhoomiStrings(langCode);
});
