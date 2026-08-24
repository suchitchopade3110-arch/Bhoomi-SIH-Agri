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
  String get welcomeSubtitle => 'AI-Powered\nFarmer Companion';
  String get welcomeTagline => 'Your Farm.\nOur Intelligence.';
  String get welcomeDesc =>
      'Your trusted digital farming partner for land verification, crop health, and intelligent farm assistance.';
  String get getStarted => 'Get Started';
  String get joinNow => 'Join Now';
  String get hackathonBadge => 'Smart India Hackathon SIH25076';

  // Navigation
  String get navHome => _t({
    'en-IN': 'Home',
    'te-IN': 'హోమ్',
    'ta-IN': 'முகப்பு',
    'hi-IN': 'होम',
    'kn-IN': 'ಮುಖಪುಟ',
    'mr-IN': 'मुख्यपृष्ठ',
    'ml-IN': 'ഹോം',
    'pa-IN': 'ਮੁੱਖ ਪੰਨਾ',
  });
  String get navCompanion => _t({
    'en-IN': 'Companion',
    'te-IN': 'మిత్రుడు',
    'ta-IN': 'தோழன்',
    'hi-IN': 'साथी',
    'kn-IN': 'ಒಡನಾಡಿ',
    'mr-IN': 'मित्र',
    'ml-IN': 'സഹായി',
    'pa-IN': 'ਸਾਥੀ',
  });
  String get navJourney => _t({
    'en-IN': 'Journey',
    'te-IN': 'ప్రయాణం',
    'ta-IN': 'பயணம்',
    'hi-IN': 'सफ़र',
    'kn-IN': 'ಪ್ರಯಾಣ',
    'mr-IN': 'प्रवास',
    'ml-IN': 'യാത്ര',
    'pa-IN': 'ਸਫ਼ਰ',
  });
  String get navProfile => _t({
    'en-IN': 'Profile',
    'te-IN': 'ప్రొఫైల్',
    'ta-IN': 'சுயவிவரம்',
    'hi-IN': 'प्रोफ़ाइल',
    'kn-IN': 'ಪ್ರೊಫೈಲ್',
    'mr-IN': 'प्रोफाइल',
    'ml-IN': 'പ്രൊഫൈൽ',
    'pa-IN': 'ਪ੍ਰੋਫਾਈਲ',
  });

  // Voice & Interaction
  String get letsGetToKnow => _t({
    'en-IN': "Let's get to know your farm",
    'te-IN': 'మీ పొలం గురించి తెలుసుకుందాం',
    'ta-IN': 'உங்கள் பண்ணையைப் பற்றி அறிவோம்',
    'hi-IN': 'आइए आपके खेत को जानें',
    'kn-IN': 'ನಿಮ್ಮ ಕೃಷಿ ಬಗ್ಗೆ ತಿಳಿಯೋಣ',
    'mr-IN': 'तुमच्या शेतीबद्दल जाणून घेऊया',
    'ml-IN': 'നിങ്ങളുടെ കൃഷിയിടത്തെ അറിയാം',
    'pa-IN': 'ਆਓ ਤੁਹਾਡੇ ਖੇਤ ਬਾਰੇ ਜਾਣੀਏ',
  });
  String get youCanSpeak => _t({
    'en-IN': 'You can speak in your language',
    'te-IN': 'మీరు మీ భాషలోనే మాట్లాడవచ్చు',
    'ta-IN': 'நீங்கள் உங்கள் மொழியிலேயே பேசலாம்',
    'hi-IN': 'आप अपनी भाषा में बोल सकते हैं',
    'kn-IN': 'ನೀವು ನಿಮ್ಮ ಭಾಷೆಯಲ್ಲಿ ಮಾತನಾಡಬಹುದು',
    'mr-IN': 'तुम्ही तुमच्या भाषेत बोलू शकता',
    'ml-IN': 'നിങ്ങൾക്ക് സ്വന്തം ഭാഷയിൽ സംസാരിക്കാം',
    'pa-IN': 'ਤੁਸੀਂ ਆਪਣੀ ਭਾਸ਼ਾ ਵਿੱਚ ਬੋਲ ਸਕਦੇ ਹੋ',
  });
  String get tapAndSpeak => _t({
    'en-IN': 'Tap and speak',
    'te-IN': 'తాకి మాట్లాడండి',
    'ta-IN': 'தட்டி பேசவும்',
    'hi-IN': 'टैप करें और बोलें',
    'kn-IN': 'ಟ್ಯಾಪ್ ಮಾಡಿ ಮಾತನಾಡಿ',
    'mr-IN': 'टॅप करा आणि बोला',
    'ml-IN': 'ടാപ്പ് ചെയ്ത് സംസാരിക്കുക',
    'pa-IN': 'ਟੈਪ ਕਰੋ ਅਤੇ ਬੋਲੋ',
  });
  String get tapAndAsk => _t({
    'en-IN': 'Tap and ask',
    'te-IN': 'తాకి అడగండి',
    'ta-IN': 'தட்டி கேட்கவும்',
    'hi-IN': 'टैप करें और पूछें',
    'kn-IN': 'ಟ್ಯಾಪ್ ಮಾಡಿ ಕೇಳಿ',
    'mr-IN': 'टॅप करा आणि विचारा',
    'ml-IN': 'ടാപ്പ് ചെയ്ത് ചോദിക്കുക',
    'pa-IN': 'ਟੈਪ ਕਰੋ ਅਤੇ ਪੁੱਛੋ',
  });
  String get showToBhoomi => _t({
    'en-IN': 'Show to BHOOMI',
    'te-IN': 'భూమికి చూపించండి',
    'ta-IN': 'பூமியிடம் காட்டுங்கள்',
    'hi-IN': 'भूमि को दिखाएं',
    'kn-IN': 'ಭೂಮಿಗೆ ತೋರಿಸಿ',
    'mr-IN': 'भूमीला दाखवा',
    'ml-IN': 'ഭൂമിയെ കാണിക്കുക',
    'pa-IN': 'ਭੂਮੀ ਨੂੰ ਦਿਖਾਓ',
  });
  String get uploadOrTake => _t({
    'en-IN': 'Upload or take a photo',
    'te-IN': 'ఫోటో తీయండి లేదా అప్‌లోడ్ చేయండి',
    'ta-IN': 'புகைப்படம் எடுக்கவும் அல்லது பதிவேற்றவும்',
    'hi-IN': 'फोटो लें या अपलोड करें',
    'kn-IN': 'ಫೋಟೋ ತೆಗೆಯಿರಿ ಅಥವಾ ಅಪ್‌ಲೋಡ್ ಮಾಡಿ',
    'mr-IN': 'फोटो काढा किंवा अपलोड करा',
    'ml-IN': 'ഫോട്ടോ എടുക്കുക അല്ലെങ്കിൽ അപ്‌ലോഡ് ചെയ്യുക',
    'pa-IN': 'ਫੋਟੋ ਖਿੱਚੋ ਜਾਂ ਅੱਪਲੋਡ ਕਰੋ',
  });
  String get aiWillIdentify => _t({
    'en-IN': 'AI will identify the issue and guide you.',
    'te-IN': 'AI సమస్యను గుర్తించి మీకు మార్గనిర్దేశం చేస్తుంది.',
    'ta-IN': 'AI சிக்கலைக் கண்டறிந்து உங்களுக்கு வழிகாட்டும்.',
    'hi-IN': 'AI समस्या की पहचान करेगा और आपका मार्गदर्शन करेगा।',
    'kn-IN': 'AI ಸಮಸ್ಯೆಯನ್ನು ಗುರುತಿಸಿ ನಿಮಗೆ ಮಾರ್ಗದರ್ಶನ ನೀಡುತ್ತದೆ.',
    'mr-IN': 'AI समस्येची ओळख पटवून तुम्हाला मार्गदर्शन करेल.',
    'ml-IN': 'AI പ്രശ്നം കണ്ടെത്തി നിങ്ങൾക്ക് വഴികാട്ടും.',
    'pa-IN': 'AI ਸਮੱਸਿਆ ਦੀ ਪਛਾਣ ਕਰੇਗਾ ਅਤੇ ਤੁਹਾਡੀ ਅਗਵਾਈ ਕਰੇਗਾ।',
  });
  String get notEnoughDataYet => _t({
    'en-IN': 'Not enough data yet',
    'te-IN': 'ఇంకా తగినంత సమాచారం లేదు',
    'ta-IN': 'இன்னும் போதிய தரவு இல்லை',
    'hi-IN': 'अभी पर्याप्त डेटा नहीं है',
    'kn-IN': 'ಇನ್ನೂ ಸಾಕಷ್ಟು ಡೇಟಾ ಇಲ್ಲ',
    'mr-IN': 'अद्याप पुरेसा डेटा नाही',
    'ml-IN': 'ഇതുവരെ ആവശ്യത്തിന് വിവരങ്ങൾ ഇല്ല',
    'pa-IN': 'ਅਜੇ ਲੋੜੀਂਦਾ ਡਾਟਾ ਨਹੀਂ ਹੈ',
  });
  String get overallFarmHealth => _t({
    'en-IN': 'Overall Farm Health',
    'te-IN': 'మొత్తం పొలం ఆరోగ్యం',
    'ta-IN': 'ஒட்டுமொத்த பண்ணை ஆரோக்கியம்',
    'hi-IN': 'समग्र खेत स्वास्थ्य',
    'kn-IN': 'ಒಟ್ಟಾರೆ ಕೃಷಿ ಆರೋಗ್ಯ',
    'mr-IN': 'एकूण शेतीचे आरोग्य',
    'ml-IN': 'മൊത്തത്തിലുള്ള കൃഷിയിട ആരോഗ്യം',
    'pa-IN': 'ਸਮੁੱਚੀ ਖੇਤ ਦੀ ਸਿਹਤ',
  });

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

  // Phase 2: AI Processing & Intelligence Workflow
  String get processingYourQuery => _t({
    'en-IN': 'Processing Your Query',
    'te-IN': 'మీ అభ్యర్థన ప్రాసెస్ చేయబడుతోంది',
    'ta-IN': 'உங்கள் கேள்வி செயல்படுத்தப்படுகிறது',
    'hi-IN': 'आपके प्रश्न पर काम हो रहा है',
    'kn-IN': 'ನಿಮ್ಮ ಪ್ರಶ್ನೆಯನ್ನು ಪ್ರಕ್ರಿಯೆಗೊಳಿಸಲಾಗುತ್ತಿದೆ',
    'mr-IN': 'तुमच्या प्रश्नावर प्रक्रिया सुरू आहे',
    'ml-IN': 'നിങ്ങളുടെ ചോദ്യം പ്രോസസ്സ് ചെയ്യുന്നു',
    'pa-IN': 'ਤੁਹਾਡੇ ਸਵਾਲ ਦੀ ਪ੍ਰਕਿਰਿਆ ਹੋ ਰਹੀ ਹੈ',
  });
  String get analyzingYourFarm => _t({
    'en-IN': 'Analyzing your farm...',
    'te-IN': 'మీ పొలాన్ని విశ్లేషిస్తోంది...',
    'ta-IN': 'உங்கள் பண்ணை பகுப்பாய்வு செய்யப்படுகிறது...',
    'hi-IN': 'आपके खेत का विश्लेषण हो रहा है...',
    'kn-IN': 'ನಿಮ್ಮ ಕೃಷಿಯನ್ನು ವಿಶ್ಲೇಷಿಸಲಾಗುತ್ತಿದೆ...',
    'mr-IN': 'तुमच्या शेतीचे विश्लेषण केले जात आहे...',
    'ml-IN': 'നിങ്ങളുടെ കൃഷിയിടം വിശകലനം ചെയ്യുന്നു...',
    'pa-IN': 'ਤੁਹਾਡੇ ਖੇਤ ਦਾ ਵਿਸ਼ਲੇਸ਼ਣ ਕੀਤਾ ਜਾ ਰਿਹਾ ਹੈ...',
  });
  String get stepUnderstandingIssue => _t({
    'en-IN': 'Understanding your issue',
    'te-IN': 'మీ సమస్యను అర్థం చేసుకోవడం',
    'ta-IN': 'உங்கள் சிக்கலை புரிந்துகொள்வது',
    'hi-IN': 'आपकी समस्या को समझना',
    'kn-IN': 'ನಿಮ್ಮ ಸಮಸ್ಯೆಯನ್ನು ಅರ್ಥಮಾಡಿಕೊಳ್ಳುವುದು',
    'mr-IN': 'तुमची समस्या समजून घेणे',
    'ml-IN': 'നിങ്ങളുടെ പ്രശ്നം മനസ്സിലാക്കുന്നു',
    'pa-IN': 'ਤੁਹਾਡੀ ਸਮੱਸਿਆ ਨੂੰ ਸਮਝਣਾ',
  });
  String get stepSearchingKnowledge => _t({
    'en-IN': 'Searching agricultural knowledge',
    'te-IN': 'వ్యవసాయ జ్ఞానాన్ని శోధించడం',
    'ta-IN': 'விவசாய அறிவை தேடுகிறது',
    'hi-IN': 'कृषि ज्ञान खोजना',
    'kn-IN': 'ಕೃಷಿ ಜ್ಞಾನವನ್ನು ಹುಡುಕಲಾಗುತ್ತಿದೆ',
    'mr-IN': 'कृषी ज्ञान शोधणे',
    'ml-IN': 'കാർഷിക അറിവുകൾ തിരയുന്നു',
    'pa-IN': 'ਖੇਤੀਬਾੜੀ ਗਿਆਨ ਦੀ ਖੋਜ ਕਰਨਾ',
  });
  String get stepCheckingIndicators => _t({
    'en-IN': 'Checking farm indicators',
    'te-IN': 'పొలం సూచికలను తనిఖీ చేస్తోంది',
    'ta-IN': 'பண்ணை குறிகாட்டிகளை சரிபார்க்கிறது',
    'hi-IN': 'खेत के संकेतकों की जांच',
    'kn-IN': 'ಕೃಷಿ ಸೂಚಕಗಳನ್ನು ಪರಿಶೀಲಿಸಲಾಗುತ್ತಿದೆ',
    'mr-IN': 'शेतीचे निर्देशक तपासत आहे',
    'ml-IN': 'കൃഷിയിട സൂചകങ്ങൾ പരിശോധിക്കുന്നു',
    'pa-IN': 'ਖੇਤ ਦੇ ਸੂਚਕਾਂ ਦੀ ਜਾਂਚ ਕਰਨਾ',
  });
  String get ourIntelligenceWorking => _t({
    'en-IN': 'Our Intelligence Working',
    'te-IN': 'మా AI మేధస్సు పనిచేస్తోంది',
    'ta-IN': 'எங்கள் நுண்ணறிவு செயல்படுகிறது',
    'hi-IN': 'हमारी बुद्धिमत्ता काम कर रही है',
    'kn-IN': 'ನಮ್ಮ ಇಂಟೆಲಿಜೆನ್ಸ್ ಕಾರ್ಯನಿರ್ವಹಿಸುತ್ತಿದೆ',
    'mr-IN': 'आमची बुद्धिमत्ता कार्यरत आहे',
    'ml-IN': 'ഞങ്ങളുടെ ഇന്റലിജൻസ് പ്രവർത്തിക്കുന്നു',
    'pa-IN': 'ਸਾਡੀ ਬੁੱਧੀ ਕੰਮ ਕਰ ਰਹੀ ਹੈ',
  });
  String get ragAdvisoryTitle => _t({
    'en-IN': 'RAG Advisory',
    'te-IN': 'RAG సలహా',
    'ta-IN': 'RAG ஆலோசனை',
    'hi-IN': 'RAG सलाह',
    'kn-IN': 'RAG ಸಲಹೆ',
    'mr-IN': 'RAG सल्ला',
    'ml-IN': 'RAG ഉപദേശം',
    'pa-IN': 'RAG ਸਲਾਹ',
  });
  String get ragAdvisoryDesc => _t({
    'en-IN': 'Finding relevant agricultural knowledge',
    'te-IN': 'సంబంధిత వ్యవసాయ జ్ఞానాన్ని కనుగొంటోంది',
    'ta-IN': 'பொருத்தமான விவசாய அறிவை கண்டறிதல்',
    'hi-IN': 'संबद्ध कृषि ज्ञान प्राप्त करना',
    'kn-IN': 'ಸಂಬಂಧಿತ ಕೃಷಿ ಜ್ಞಾನವನ್ನು ಕಂಡುಹಿಡಿಯುವುದು',
    'mr-IN': 'संबंधित कृषी ज्ञान शोधणे',
    'ml-IN': 'പ്രസക്തമായ കാർഷിക അറിവ് കണ്ടെത്തുന്നു',
    'pa-IN': 'ਢੁਕਵਾਂ ਖੇਤੀਬਾੜੀ ਗਿਆਨ ਲੱਭਣਾ',
  });
  String get faoPlannerTitle => _t({
    'en-IN': 'FAO-56 Planner',
    'te-IN': 'FAO-56 ప్రణాళిక',
    'ta-IN': 'FAO-56 திட்டமிடுபவர்',
    'hi-IN': 'FAO-56 योजनाकार',
    'kn-IN': 'FAO-56 ಯೋಜಕ',
    'mr-IN': 'FAO-56 प्लॅनर',
    'ml-IN': 'FAO-56 പ്ലാനർ',
    'pa-IN': 'FAO-56 ਯੋਜਨਾਕਾਰ',
  });
  String get faoPlannerDesc => _t({
    'en-IN': 'Checking irrigation requirements',
    'te-IN': 'నీటిపారుదల అవసరాలను తనిఖీ చేస్తోంది',
    'ta-IN': 'நீர்ப்பாசன தேவைகளை சரிபார்க்கிறது',
    'hi-IN': 'सिंचाई आवश्यकताओं की जांच',
    'kn-IN': 'ನೀರಾವರಿ ಅಗತ್ಯಗಳನ್ನು ಪರಿಶೀಲಿಸಲಾಗುತ್ತಿದೆ',
    'mr-IN': 'सिंचनाची गरज तपासणे',
    'ml-IN': 'നനയ്ക്കൽ ആവശ്യകതകൾ പരിശോധിക്കുന്നു',
    'pa-IN': 'ਸਿੰਚਾਈ ਦੀਆਂ ਲੋੜਾਂ ਦੀ ਜਾਂਚ ਕਰਨਾ',
  });
  String get healthIndicatorTitle => _t({
    'en-IN': 'Health Indicator',
    'te-IN': 'ఆరోగ్య సూచిక',
    'ta-IN': 'ஆரோக்கிய குறிகாட்டி',
    'hi-IN': 'स्वास्थ्य संकेतक',
    'kn-IN': 'ಆರೋಗ್ಯ ಸೂಚಕ',
    'mr-IN': 'आरोग्य निर्देशक',
    'ml-IN': 'ആരോഗ്യ സൂചകം',
    'pa-IN': 'ਸਿਹਤ ਸੂਚਕ',
  });
  String get healthIndicatorDesc => _t({
    'en-IN': 'Analyzing farm conditions',
    'te-IN': 'పొలం పరిస్థితులను విశ్లేషిస్తోంది',
    'ta-IN': 'பண்ணை நிலைமைகளை பகுப்பாய்வு செய்கிறது',
    'hi-IN': 'खेत की स्थितियों का विश्लेषण',
    'kn-IN': 'ಕೃಷಿ ಪರಿಸ್ಥಿತಿಗಳನ್ನು ವಿಶ್ಲೇಷಿಸಲಾಗುತ್ತಿದೆ',
    'mr-IN': 'शेतातील परिस्थितीचे विश्लेषण',
    'ml-IN': 'കൃഷിയിട സാഹചര്യങ്ങൾ വിശകലനം ചെയ്യുന്നു',
    'pa-IN': 'ਖੇਤ ਦੀਆਂ ਸਥਿਤੀਆਂ ਦਾ ਵਿਸ਼ਲੇਸ਼ਣ',
  });

  // Action Plan & Resources
  String get actionPlanTitle => _t({
    'en-IN': '5-Point Action Plan',
    'te-IN': '5-అంశాల కార్యాచరణ ప్రణాళిక',
    'ta-IN': '5-புள்ளி செயல் திட்டம்',
    'hi-IN': '5-सूत्रीय कार्य योजना',
    'kn-IN': '5-ಅಂಶಗಳ ಕ್ರಿಯಾ ಯೋಜನೆ',
    'mr-IN': '5-मुद्द्यांची कृती योजना',
    'ml-IN': '5-ഘട്ട കർമ്മപദ്ധതി',
    'pa-IN': '5-ਨੁਕਾਤੀ ਕਾਰਜ ਯੋਜਨਾ',
  });
  String get saveAdvice => _t({
    'en-IN': 'Save Advice',
    'te-IN': 'సలహాను భద్రపరచండి',
    'ta-IN': 'ஆலோசனையை சேமிக்கவும்',
    'hi-IN': 'सलाह सहेजें',
    'kn-IN': 'ಸಲಹೆ ಉಳಿಸಿ',
    'mr-IN': 'सल्ला जतन करा',
    'ml-IN': 'ഉപദേശം സേവ് ചെയ്യുക',
    'pa-IN': 'ਸਲਾਹ ਸੰਭਾਲੋ',
  });
  String get shareAdvice => _t({
    'en-IN': 'Share',
    'te-IN': 'భాగస్వామ్యం చేయండి',
    'ta-IN': 'பகிரவும்',
    'hi-IN': 'शेयर करें',
    'kn-IN': 'ಹಂಚಿಕೊಳ್ಳಿ',
    'mr-IN': 'शेअर करा',
    'ml-IN': 'പങ്കുവെക്കുക',
    'pa-IN': 'ਸਾਂਝਾ ਕਰੋ',
  });
  String get articles => _t({
    'en-IN': 'Articles',
    'te-IN': 'వ్యాసాలు',
    'ta-IN': 'கட்டுரைகள்',
    'hi-IN': 'लेख',
    'kn-IN': 'ಲೇಖನಗಳು',
    'mr-IN': 'लेख',
    'ml-IN': 'ലേഖനങ്ങൾ',
    'pa-IN': 'ਲੇਖ',
  });
  String get videos => _t({
    'en-IN': 'Videos',
    'te-IN': 'వీడియోలు',
    'ta-IN': 'காணொளிகள்',
    'hi-IN': 'वीडियो',
    'kn-IN': 'ವೀಡಿಯೊಗಳು',
    'mr-IN': 'व्हिडिओ',
    'ml-IN': 'വീഡിയോകൾ',
    'pa-IN': 'ਵੀਡੀਓ',
  });
  String get documents => _t({
    'en-IN': 'Documents',
    'te-IN': 'పత్రాలు',
    'ta-IN': 'ஆவணங்கள்',
    'hi-IN': 'दस्तावेज़',
    'kn-IN': 'ದಾಖಲೆಗಳು',
    'mr-IN': 'दस्तऐवज',
    'ml-IN': 'രേഖകൾ',
    'pa-IN': 'ਦਸਤਾਵੇਜ਼',
  });

  // Follow-up
  String get howIsItNow => _t({
    'en-IN': 'How is it now?',
    'te-IN': 'ఇప్పుడు ఎలా ఉంది?',
    'ta-IN': 'இப்போது எப்படி உள்ளது?',
    'hi-IN': 'अब कैसी स्थिति है?',
    'kn-IN': 'ಈಗ ಹೇಗಿದೆ?',
    'mr-IN': 'आता कसे आहे?',
    'ml-IN': 'ഇപ്പോൾ എങ്ങനെയുണ്ട്?',
    'pa-IN': 'ਹੁਣ ਕਿਵੇਂ ਹੈ?',
  });
  String get problemImprovedQuestion => _t({
    'en-IN': 'Has the problem improved after following the advice?',
    'te-IN': 'సలహాను పాటించిన తర్వాత సమస్య తగ్గిందా?',
    'ta-IN': 'ஆலோசனையைப் பின்பற்றிய பிறகு சிக்கல் மேம்பட்டுள்ளதா?',
    'hi-IN': 'क्या सलाह मानने के बाद समस्या में सुधार हुआ है?',
    'kn-IN': 'ಸಲಹೆ ಪಾಲಿಸಿದ ನಂತರ ಸಮಸ್ಯೆಯಲ್ಲಿ ಸುಧಾರಣೆಯಾಗಿದೆಯೇ?',
    'mr-IN': 'सल्ला पाळल्यानंतर समस्येत सुधारणा झाली आहे का?',
    'ml-IN': 'ഉപദേശം സ്വീകരിച്ച ശേഷം പ്രശ്നം കുറഞ്ഞോ?',
    'pa-IN': 'ਕੀ ਸਲਾਹ ਮੰਨਣ ਤੋਂ ਬਾਅਦ ਸਮੱਸਿਆ ਵਿੱਚ ਸੁਧਾਰ ਹੋਇਆ ਹੈ?',
  });
  String get outcomeImproved => _t({
    'en-IN': 'Improved',
    'te-IN': 'మెరుగుపడింది',
    'ta-IN': 'மேம்பட்டுள்ளது',
    'hi-IN': 'सुधार हुआ',
    'kn-IN': 'ಸುಧಾರಿಸಿದೆ',
    'mr-IN': 'सुधारणा झाली',
    'ml-IN': 'മെച്ചപ്പെട്ടു',
    'pa-IN': 'ਸੁਧਾਰ ਹੋਇਆ',
  });
  String get outcomeNoChange => _t({
    'en-IN': 'No Change',
    'te-IN': 'మార్పు లేదు',
    'ta-IN': 'மாற்றமில்லை',
    'hi-IN': 'कोई बदलाव नहीं',
    'kn-IN': 'ಯಾವ ಬದಲಾವಣೆಯೂ ಇಲ್ಲ',
    'mr-IN': 'काही बदल नाही',
    'ml-IN': 'മാറ്റമില്ല',
    'pa-IN': 'ਕੋਈ ਬਦਲਾਅ ਨਹੀਂ',
  });
  String get outcomeGotWorse => _t({
    'en-IN': 'Got Worse',
    'te-IN': 'మరింత తీవ్రమైంది',
    'ta-IN': 'மோசமாகிவிட்டது',
    'hi-IN': 'स्थिति बिगड़ी',
    'kn-IN': 'ಉಲ್ಬಣಗೊಂಡಿದೆ',
    'mr-IN': 'अधिक वाईट झाले',
    'ml-IN': 'കൂടുതൽ വഷളായി',
    'pa-IN': 'ਹੋਰ ਖਰਾਬ ਹੋਇਆ',
  });
  String get skipForNow => _t({
    'en-IN': 'Skip for Now',
    'te-IN': 'ఇప్పటికి దాటవేయండి',
    'ta-IN': 'இப்போதைக்கு தவிர்க்கவும்',
    'hi-IN': 'अभी छोड़ें',
    'kn-IN': 'ಈಗಿಗೆ ಬಿಟ್ಟುಬಿಡಿ',
    'mr-IN': 'आत्तासाठी वगळा',
    'ml-IN': 'ഇപ്പൊഴത്തേക്ക് ഒഴിവാക്കുക',
    'pa-IN': 'ਹੁਣ ਲਈ ਛੱਡੋ',
  });
  String get uploadNewPhoto => _t({
    'en-IN': 'Upload new photo',
    'te-IN': 'కొత్త ఫోటో అప్‌లోడ్ చేయండి',
    'ta-IN': 'புதிய புகைப்படத்தை பதிவேற்றவும்',
    'hi-IN': 'नई फोटो अपलोड करें',
    'kn-IN': 'ಹೊಸ ಫೋಟೋ ಅಪ್‌ಲೋಡ್ ಮಾಡಿ',
    'mr-IN': 'नवीन फोटो अपलोड करा',
    'ml-IN': 'പുതിയ ഫോട്ടോ അപ്‌ലോഡ് ചെയ്യുക',
    'pa-IN': 'ਨਵੀਂ ਫੋਟੋ ਅੱਪਲੋਡ ਕਰੋ',
  });
  String get addNote => _t({
    'en-IN': 'Add Note',
    'te-IN': 'గమనిక జోడించండి',
    'ta-IN': 'குறிப்பைச் சேர்க்கவும்',
    'hi-IN': 'टिप्पणी जोड़ें',
    'kn-IN': 'ಟಿಪ್ಪಣಿ ಸೇರಿಸಿ',
    'mr-IN': 'नोंद जोडा',
    'ml-IN': 'കുറിപ്പ് ചേർക്കുക',
    'pa-IN': 'ਨੋਟ ਸ਼ਾਮਲ ਕਰੋ',
  });
  String get submitUpdate => _t({
    'en-IN': 'Submit Update',
    'te-IN': 'తాజా వివరాలను సమర్పించండి',
    'ta-IN': 'புதுப்பிப்பை சமர்ப்பிக்கவும்',
    'hi-IN': 'अपडेट सबमिट करें',
    'kn-IN': 'ಅಪ್‌ಡೇಟ್ ಸಲ್ಲಿಸಿ',
    'mr-IN': 'अपडेट सबमिट करा',
    'ml-IN': 'അപ്‌ഡേറ്റ് സമർപ്പിക്കുക',
    'pa-IN': 'ਅਪਡੇਟ ਸਬਮਿਟ ਕਰੋ',
  });
  String get trackingProgress => _t({
    'en-IN': 'Tracking Progress',
    'te-IN': 'పురోగతిని ట్రాక్ చేస్తోంది',
    'ta-IN': 'முன்னேற்றத்தை கண்காணிக்கிறது',
    'hi-IN': 'प्रगति ट्रैक करना',
    'kn-IN': 'ಪ್ರಗತಿಯನ್ನು ಟ್ರ್ಯಾಕ್ ಮಾಡಲಾಗುತ್ತಿದೆ',
    'mr-IN': 'प्रगती ट्रॅक करत आहे',
    'ml-IN': 'പുരോഗതി നിരീക്ഷിക്കുന്നു',
    'pa-IN': 'ਪ੍ਰਗਤੀ ਨੂੰ ਟਰੈਕ ਕਰਨਾ',
  });

  // Escalation & Expert Case Summary
  String get escalatingToExpert => _t({
    'en-IN': 'Escalating to Expert',
    'te-IN': 'నిపుణుడికి బదిలీ చేస్తోంది',
    'ta-IN': 'நிபுணரிடம் ஒப்படைக்கப்படுகிறது',
    'hi-IN': 'विशेषज्ञ को भेजा जा रहा है',
    'kn-IN': 'ತಜ್ಞರಿಗೆ ಕಳುಹಿಸಲಾಗುತ್ತಿದೆ',
    'mr-IN': 'तज्ज्ञांकडे हस्तांतरित करत आहे',
    'ml-IN': 'വിദഗ്ദ്ധനിലേക്ക് കൈമാറുന്നു',
    'pa-IN': 'ਮਾਹਿਰ ਨੂੰ ਭੇਜਿਆ ਜਾ ਰਿਹਾ ਹੈ',
  });
  String get expertWillReview => _t({
    'en-IN': 'Our agricultural expert will review your case.',
    'te-IN': 'మా వ్యవసాయ నిపుణుడు మీ కేసును సమీక్షిస్తారు.',
    'ta-IN': 'எங்கள் விவசாய நிபுணர் உங்கள் வழக்கை மதிப்பாய்வு செய்வார்.',
    'hi-IN': 'हमारे कृषि विशेषज्ञ आपके मामले की समीक्षा करेंगे।',
    'kn-IN': 'ನಮ್ಮ ಕೃಷಿ ತಜ್ಞರು ನಿಮ್ಮ ಪ್ರಕರಣವನ್ನು ಪರಿಶೀಲಿಸುತ್ತಾರೆ.',
    'mr-IN': 'आमचे कृषी तज्ज्ञ तुमच्या प्रकरणाचा आढावा घेतील.',
    'ml-IN': 'ഞങ്ങളുടെ കാർഷിക വിദഗ്ദ്ധൻ നിങ്ങളുടെ കേസ് പരിശോധിക്കും.',
    'pa-IN': 'ਸਾਡੇ ਖੇਤੀਬਾੜੀ ਮਾਹਿਰ ਤੁਹਾਡੇ ਕੇਸ ਦੀ ਸਮੀਖਿਆ ਕਰਨਗੇ।',
  });
  String get caseTransferred => _t({
    'en-IN': 'Case transferred',
    'te-IN': 'కేసు బదిలీ చేయబడింది',
    'ta-IN': 'வழக்கு மாற்றப்பட்டது',
    'hi-IN': 'मामला स्थानांतरित हुआ',
    'kn-IN': 'ಪ್ರಕರಣ ವರ್ಗಾಯಿಸಲಾಗಿದೆ',
    'mr-IN': 'प्रकरण हस्तांतरित झाले',
    'ml-IN': 'കേസ് കൈമാറി',
    'pa-IN': 'ਕੇਸ ਤਬਦੀਲ ਕੀਤਾ ਗਿਆ',
  });
  String get expertNotified => _t({
    'en-IN': 'Expert notified',
    'te-IN': 'నిపుణుడికి తెలియజేయబడింది',
    'ta-IN': 'நிபுணருக்கு தெரிவிக்கப்பட்டது',
    'hi-IN': 'विशेषज्ञ को सूचित किया गया',
    'kn-IN': 'ತಜ್ಞರಿಗೆ ತಿಳಿಸಲಾಗಿದೆ',
    'mr-IN': 'तज्ज्ञांना सूचित केले',
    'ml-IN': 'വിദഗ്ദ്ധനെ അറിയിച്ചു',
    'pa-IN': 'ਮਾਹਿਰ ਨੂੰ ਸੂਚਿਤ ਕੀਤਾ ਗਿਆ',
  });
  String get reviewInProgress => _t({
    'en-IN': 'Review in progress',
    'te-IN': 'సమీక్ష జరుగుతోంది',
    'ta-IN': 'மதிப்பாய்வு நடக்கிறது',
    'hi-IN': 'समीक्षा प्रगति पर है',
    'kn-IN': 'ಪರಿಶೀಲನೆ ಪ್ರಗತಿಯಲ್ಲಿದೆ',
    'mr-IN': 'पुनरावलोकन प्रगतीपथावर आहे',
    'ml-IN': 'പരിശോധന പുരോഗമിക്കുന്നു',
    'pa-IN': 'ਸਮੀਖਿਆ ਜਾਰੀ ਹੈ',
  });
  String get expertCaseSummary => _t({
    'en-IN': 'Expert Case Summary',
    'te-IN': 'నిపుణుల కేసు సారాంశం',
    'ta-IN': 'நிபுணர் வழக்கு சுருக்கம்',
    'hi-IN': 'विशेषज्ञ मामला सारांश',
    'kn-IN': 'ತಜ್ಞರ ಪ್ರಕರಣದ ಸಾರಾಂಶ',
    'mr-IN': 'तज्ज्ञ प्रकरण सारांश',
    'ml-IN': 'വിദഗ്ദ്ധ കേസ് സംഗ്രഹം',
    'pa-IN': 'ਮਾਹਿਰ ਕੇਸ ਸੰਖੇਪ',
  });
  String get viewFullCase => _t({
    'en-IN': 'View Full Case',
    'te-IN': 'పూర్తి కేసును చూడండి',
    'ta-IN': 'முழு வழக்கையும் பார்க்கவும்',
    'hi-IN': 'पूरा मामला देखें',
    'kn-IN': 'ಸಂಪೂರ್ಣ ಪ್ರಕರಣವನ್ನು ವೀಕ್ಷಿಸಿ',
    'mr-IN': 'पूर्ण प्रकरण पहा',
    'ml-IN': 'പൂർണ്ണ കേസ് കാണുക',
    'pa-IN': 'ਪੂਰਾ ਕੇਸ ਦੇਖੋ',
  });

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
