import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'language_provider.dart';

export 'language_provider.dart';

/// Global provider for AppTranslations bound to selectedLanguageProvider
final appTranslationsProvider = Provider<AppTranslations>((ref) {
  final langCode = ref.watch(selectedLanguageProvider);
  return AppTranslations(langCode);
});

/// Global alias for BhoomiStrings
final bhoomiStringsProvider = appTranslationsProvider;

class AppTranslations {
  final String langCode;

  const AppTranslations(this.langCode);

  static const Map<String, Map<String, String>> _localizedValues = {
    'ta-IN': {
      'acres': 'ஏக்கர்',
      'active_problem_load': 'செயலில் உள்ள பாதிப்பு அளவு',
      'activity_timeline': 'செயல்பாட்டு காலவரிசை',
      'analyzing_health': 'பண்ணை ஆரோக்கியத்தை பகுப்பாய்வு செய்கிறது...',
      'analyzing_image': 'பயிரின் புகைப்படத்தை ஆய்வு செய்கிறது...',
      'app_title': 'பூமி',
      'apply_scheme': 'விண்ணப்பிக்கவும்',
      'ask_bhoomi': 'பூமியிடம் கேளுங்கள்',
      'back': 'பின்னே செல்',
      'banana': 'வாழை',
      'banana_sub': 'நேந்திரன், ரோபஸ்டா வகைகள்',
      'bhoomi_advisory': 'பூமி வேளாண் ஆலோசனை',
      'biological_control': 'இயற்கை உயிரியல் கட்டுப்பாடு',
      'chemical_control': 'இரசாயன கட்டுப்பாடு',
      'choose_language': 'உங்கள் மொழியைத் தேர்ந்தெடுக்கவும்',
      'confidence_score': 'துல்லியத்தன்மை',
      'confirm_desc': 'உங்கள் பண்ணை விவரங்களை உறுதிப்படுத்தவும்',
      'confirm_farm_title': 'பண்ணை விவரங்கள்',
      'continue': 'தொடரவும்',
      'cotton': 'பருத்தி',
      'cotton_sub': 'நீண்ட இழை பருத்தி',
      'crop_advisory_desc': 'பயிர் பாதுகாப்பு மற்றும் வளர்ச்சி வழிகாட்டி',
      'crop_diagnosis_title': 'பயிர் நோய் கண்டறிதல்',
      'crop_label': 'பயிர்',
      'crop_stage_prog': 'பயிர் வளர்ச்சி முன்னேற்றம்',
      'daily_companion': 'தினசரி வழிகாட்டி',
      'diagnose_get_advice': 'பரிசோதித்து ஆலோசனை பெறுக',
      'diagnosis_id': 'நோய் கண்டறிதல் எண்',
      'district': 'மாவட்டம்',
      'documents_required': 'தேவைப்படும் ஆவணங்கள்',
      'eligibility_criteria': 'தகுதி வரம்புகள்',
      'eligible_schemes': 'தகுதியான திட்டங்கள்',
      'env_suitability': 'சுற்றுச்சூழல் பொருத்தம்',
      'farm_health_score': 'பண்ணை ஆரோக்கிய மதிப்பெண்',
      'farm_health_title': 'பண்ணை ஆரோக்கியம் & நோய் கண்டறிதல்',
      'farm_id': 'பண்ணை எண்',
      'farm_journey_desc': 'உங்கள் பயிர் சாகுபடி பயணம்',
      'field_weather': 'வயல் வானிலை',
      'flowering': 'பூக்கும் பருவம்',
      'flowering_sub': 'பூக்கள் தோன்றும் பருவம்',
      'get_expert_help': 'நிபுணர் உதவி பெறுக',
      'get_started': 'தொடங்கவும்',
      'govt_support': 'அரசு நலத்திட்டங்கள்',
      'govt_support_desc': 'மானியங்கள் மற்றும் நிதி உதவி',
      'govt_support_finder': 'திட்டங்கள் கண்டறிதல்',
      'grain_filling': 'மணி பிடிக்கும் பருவம்',
      'grain_filling_sub': 'மணிகள் பால் பிடித்து முதிரும் நிலை',
      'growth_stage_label': 'வளர்ச்சி நிலை',
      'harvest_ready': 'அறுவடைக்கு தயார்',
      'harvest_ready_sub': 'முழு முதிர்ச்சி அடைந்த நிலை',
      'health_history': 'ஆரோக்கிய வரலாறு',
      'health_unrated': 'மதிப்பிடப்படவில்லை',
      'health_unrated_desc': 'மதிப்பீடு செய்ய கூடுதல் தரவு தேவை',
      'humidity': 'ஈரப்பதம்',
      'kuruvai_paddy': 'குறுவை நெல்',
      'kuruvai_paddy_sub': 'குறுகிய கால நெல் ரகம்',
      'land_area_label': 'நிலப்பரப்பு',
      'land_boundary_title': 'நில எல்லை & வரைபடம்',
      'land_details_title': 'நில விவரங்கள்',
      'land_status_title': 'நில சரிபார்ப்பு நிலை',
      'land_verification_required': 'நில சரிபார்ப்பு தேவை',
      'last_computed': 'கடைசியாக கணக்கிடப்பட்டது',
      'latest_update': 'சமீபத்திய அறிவிப்பு',
      'loading_journey': 'பண்ணை பயணத்தை ஏற்றுகிறது...',
      'maize': 'மக்காச்சோளம்',
      'maize_sub': 'வீரிய மக்காச்சோளம்',
      'maturity': 'முதிர்ச்சி நிலை',
      'maturity_sub': 'பயிர் முதிர்ச்சி அடையும் நிலை',
      'monitoring_recency': 'கண்காணிப்பு அண்மை நிலை',
      'my_farm': 'என் பண்ணை',
      'my_farm_journey': 'என் பண்ணை பயணம்',
      'no_timeline_events': 'இதுவரை செயல்பாடுகள் எதுவும் பதிவாகவில்லை.',
      'no_updates': 'தற்போது புதிய அறிவிப்புகள் இல்லை',
      'or_type_below': 'அல்லது கீழே தட்டச்சு செய்யவும்',
      'overall_farm_health': 'ஒட்டுமொத்த பண்ணை ஆரோக்கியம்',
      'ownership_status': 'உரிமை நிலை',
      'patta_number': 'பட்டா எண்',
      'possible_issue_identified': 'சாத்தியமான பாதிப்பு கண்டறியப்பட்டது',
      'preventive_measures': 'தடுப்பு முறைகள்',
      'primary_crop': 'முக்கிய பயிர்',
      'provide_details': 'விவரங்களை வழங்கவும்',
      'quick_selection': 'விரைவுத் தேர்வுகள்',
      'rain': 'மழை',
      'recommended_actions': 'பரிந்துரைக்கப்பட்ட நடவடிக்கைகள்',
      'recommended_schemes': 'பரிந்துரைக்கப்பட்ட திட்டங்கள்',
      'recompute_health': 'ஆரோக்கியத்தை மீண்டும் கணக்கிடு',
      'refresh_status': 'நிலையை புதுப்பிக்கவும்',
      'refresh_timeline': 'காலவரிசையை புதுப்பி',
      'requires_verified_land': 'சரிபார்க்கப்பட்ட நிலம் தேவை',
      'resource_adequacy': 'வள போதுமான நிலை',
      'retry': 'மீண்டும் முயற்சிக்கவும்',
      'samba_paddy': 'சம்பா நெல்',
      'samba_paddy_sub': 'நீண்ட கால சம்பா பயிர்',
      'save_my_farm': 'பண்ணையைச் சேமிக்கவும்',
      'scheme_details': 'திட்ட விவரங்கள்',
      'schemes_subsidies': 'திட்டங்கள் & மானியங்கள்',
      'scientific_remedy': 'அறிவியல் தீர்வு',
      'score_breakdown': 'விளக்கக்கூடிய மதிப்பெண் விவரம்',
      'score_breakdown_desc': '6 முக்கிய வேளாண் அளவுகோல்களின் அடிப்படையில் கணக்கிடப்பட்டது.',
      'select_farm_area': 'நிலப்பரப்பைத் தேர்ந்தெடுக்கவும்',
      'select_stage': 'வளர்ச்சி நிலையைத் தேர்ந்தெடுக்கவும்',
      'show_problem': 'படத்தை காட்டவும்',
      'step_area_sub': 'உங்கள் பண்ணை அளவைத் தேர்ந்தெடுக்கவும்',
      'step_area_title': 'உங்கள் நிலப்பரப்பு எவ்வளவு?',
      'step_crop_sub': 'பட்டியலிலிருந்து பயிரைத் தேர்ந்தெடுக்கவும்',
      'step_crop_title': 'நீங்கள் என்ன பயிரிடுகிறீர்கள்?',
      'step_stage_sub': 'தற்போதைய பயிர் வளர்ச்சியைத் தேர்ந்தெடுக்கவும்',
      'step_stage_title': 'பயிர் வளர்ச்சி நிலை என்ன?',
      'subsidy_amount': 'மானியத் தொகை',
      'sugarcane': 'கரும்பு',
      'sugarcane_sub': 'பன்னிரண்டு மாத பணப்பயிர்',
      'survey_number': 'சர்வே எண்',
      'symptoms_observed': 'கண்டறியப்பட்ட அறிகுறிகள்',
      'taluk': 'வட்டம்',
      'tap_to_speak_area': 'நிலப்பரப்பைச் சொல்ல தட்டவும்',
      'tap_to_speak_crop': 'உங்கள் பயிரைப் பேச தட்டவும்',
      'tap_to_speak_stage': 'வளர்ச்சி நிலையைச் சொல்ல தட்டவும்',
      'target_beneficiaries': 'பயனாளிகள்',
      'tell_about_farm': 'உங்கள் பண்ணையைப் பற்றி கூறுங்கள்',
      'timeline_header': 'பண்ணை செயல்பாட்டு பயணம்',
      'timeline_header_desc': 'அனைத்து பண்ணை நடவடிக்கைகள், சோதனைகள் மற்றும் ஒப்புதல்களின் காலவரிசை.',
      'timeline_title': 'என் பண்ணை பயணம்',
      'todays_farm_brief': 'இன்றைய பண்ணை வழிகாட்டி',
      'total_area': 'மொத்த பரப்பளவு',
      'track_progress': 'முன்னேற்றத்தைக் கண்காணிக்கவும்',
      'treatment_response': 'சிகிச்சை பலன்',
      'type_problem_hint': 'எ.கா. இலைகள் மஞ்சள் நிறமாக மாறுகின்றன...',
      'unable_load_health': 'ஆரோக்கிய தரவை ஏற்றுவதில் சிக்கல்',
      'unable_load_timeline': 'காலவரிசையை ஏற்றுவதில் சிக்கல்',
      'upload_crop_photo': 'பயிர் புகைப்படத்தைப் பதிவேற்றவும்',
      'vegetative': 'பயிர் வளர்ச்சி நிலை',
      'vegetative_sub': 'இலை மற்றும் தண்டு வளர்ச்சி நிலை',
      'verify_land_desc': 'அரசு மானியங்களுக்கு நிலத்தை சரிபார்க்கவும்',
      'verify_land_now': 'நிலத்தை இப்போது சரிபார்க்கவும்',
      'view_advice': 'ஆலோசனையைக் காண்க',
      'view_all': 'அனைத்தையும் காண்க',
      'view_details': 'விவரங்களைக் காண்க',
      'view_health_journey': 'ஆரோக்கிய காலவரிசையைக் காண்க',
      'view_scheme_details': 'திட்ட விவரங்களைக் காண்க',
      'village': 'கிராமம்',
      'voice_assistant': 'குரல் வழிகாட்டி',
      'what_problem_seeing': 'என்ன பிரச்சனையை எதிர்கொள்கிறீர்கள்?',
      'what_would_you_like_to_do': 'நீங்கள் என்ன செய்ய விரும்புகிறீர்கள்?',
      'your_farm_profile': 'உங்கள் பண்ணை விவரக்குறிப்பு',
    },
    'hi-IN': {
      'acres': 'एकड़',
      'active_problem_load': 'सक्रिय समस्या भार',
      'activity_timeline': 'गतिविधि समयरेखा',
      'analyzing_health': 'खेत स्वास्थ्य का विश्लेषण किया जा रहा है...',
      'analyzing_image': 'फसल की तस्वीर का विश्लेषण...',
      'app_title': 'भूमि',
      'apply_scheme': 'आवेदन करें',
      'ask_bhoomi': 'भूमि से पूछें',
      'back': 'पीछे जाएं',
      'banana': 'केला',
      'banana_sub': 'ग्रैंड नैन, रोबस्टा किस्में',
      'bhoomi_advisory': 'भूमि कृषि सलाह',
      'biological_control': 'जैविक नियंत्रण',
      'chemical_control': 'रासायनिक नियंत्रण',
      'choose_language': 'अपनी भाषा चुनें',
      'confidence_score': 'सटीकता स्कोर',
      'confirm_desc': 'अपने खेत के विवरण की पुष्टि करें',
      'confirm_farm_title': 'खेत का विवरण',
      'continue': 'जारी रखें',
      'cotton': 'कपास',
      'cotton_sub': 'लंबे रेशे वाली कपास',
      'crop_advisory_desc': 'फसल सुरक्षा और विकास मार्गदर्शिका',
      'crop_diagnosis_title': 'फसल रोग निदान',
      'crop_label': 'फसल',
      'crop_stage_prog': 'फसल वृद्धि प्रगति',
      'daily_companion': 'दैनिक साथी',
      'diagnose_get_advice': 'जांचें और सलाह प्राप्त करें',
      'diagnosis_id': 'निदान आईडी',
      'district': 'जिला',
      'documents_required': 'आवश्यक दस्तावेज',
      'eligibility_criteria': 'पात्रता मानदंड',
      'eligible_schemes': 'पात्र योजनाएं',
      'env_suitability': 'पर्यावरणीय उपयुक्तता',
      'farm_health_score': 'खेत स्वास्थ्य स्कोर',
      'farm_health_title': 'खेत स्वास्थ्य और निदान',
      'farm_id': 'खेत आईडी',
      'farm_journey_desc': 'आपकी खेती का सफ़र',
      'field_weather': 'खेत का मौसम',
      'flowering': 'फूल आने की अवस्था',
      'flowering_sub': 'फूल खिलने का समय',
      'get_expert_help': 'विशेषज्ञ सहायता प्राप्त करें',
      'get_started': 'शुरू करें',
      'govt_support': 'सरकारी योजनाएं',
      'govt_support_desc': 'सब्सिडी और वित्तीय सहायता',
      'govt_support_finder': 'योजना खोजक',
      'grain_filling': 'दाने भरने की अवस्था',
      'grain_filling_sub': 'दानों में दूध भरने का समय',
      'growth_stage_label': 'वृद्धि अवस्था',
      'harvest_ready': 'कटाई के लिए तैयार',
      'harvest_ready_sub': 'फसल पूरी तरह पक चुकी है',
      'health_history': 'स्वास्थ्य इतिहास',
      'health_unrated': 'अमूल्यांकित',
      'health_unrated_desc': 'मूल्यांकन के लिए अधिक डेटा की आवश्यकता है',
      'humidity': 'आर्द्रता',
      'kuruvai_paddy': 'कुरुवई धान',
      'kuruvai_paddy_sub': 'कम अवधि की धान किस्म',
      'land_area_label': 'भूमि क्षेत्र',
      'land_boundary_title': 'भूमि सीमा और मानचित्र',
      'land_details_title': 'भूमि विवरण',
      'land_status_title': 'भूमि सत्यापन स्थिति',
      'land_verification_required': 'भूमि सत्यापन आवश्यक है',
      'last_computed': 'अंतिम गणना',
      'latest_update': 'नवीनतम अपडेट',
      'loading_journey': 'सफ़र लोड हो रहा है...',
      'maize': 'मक्का',
      'maize_sub': 'संकर मक्का',
      'maturity': 'परिपक्वता अवस्था',
      'maturity_sub': 'फसल पकने की अवस्था',
      'monitoring_recency': 'हालिया निगरानी',
      'my_farm': 'मेरा खेत',
      'my_farm_journey': 'मेरा खेत सफ़र',
      'no_timeline_events': 'अभी तक कोई गतिविधि दर्ज नहीं की गई है।',
      'no_updates': 'वर्तमान में कोई नया अपडेट नहीं',
      'or_type_below': 'या नीचे टाइप करें',
      'overall_farm_health': 'समग्र खेत स्वास्थ्य',
      'ownership_status': 'स्वामित्व स्थिति',
      'patta_number': 'पट्टा संख्या',
      'possible_issue_identified': 'संभावित समस्या की पहचान की गई',
      'preventive_measures': 'निवारक उपाय',
      'primary_crop': 'मुख्य फसल',
      'provide_details': 'विवरण प्रदान करें',
      'quick_selection': 'त्वरित चयन विकल्प',
      'rain': 'वर्षा',
      'recommended_actions': 'अनुशंसित कार्रवाई',
      'recommended_schemes': 'अनुशंसित योजनाएं',
      'recompute_health': 'स्वास्थ्य पुनः गणना करें',
      'refresh_status': 'स्थिति ताज़ा करें',
      'refresh_timeline': 'समयरेखा ताज़ा करें',
      'requires_verified_land': 'सत्यापित भूमि आवश्यक',
      'resource_adequacy': 'संसाधन पर्याप्तता',
      'retry': 'पुनः प्रयास करें',
      'samba_paddy': 'सांभा धान (चावल)',
      'samba_paddy_sub': 'लंबी अवधि की सांभा फसल',
      'save_my_farm': 'मेरा खेत सहेजें',
      'scheme_details': 'योजना विवरण',
      'schemes_subsidies': 'योजनाएं और सब्सिडी',
      'scientific_remedy': 'वैज्ञानिक उपचार',
      'score_breakdown': 'विस्तृत स्कोर विवरण',
      'score_breakdown_desc': '6 प्रमुख कृषि आयामों के आधार पर गणना की गई।',
      'select_farm_area': 'खेत का क्षेत्रफल चुनें',
      'select_stage': 'वृद्धि अवस्था चुनें',
      'show_problem': 'तस्वीर दिखाएं',
      'step_area_sub': 'अपने खेत का आकार चुनें',
      'step_area_title': 'आपकी भूमि का क्षेत्रफल कितना है?',
      'step_crop_sub': 'सूची से अपनी फसल चुनें',
      'step_crop_title': 'आप क्या उगा रहे हैं?',
      'step_stage_sub': 'फसल की वर्तमान अवस्था चुनें',
      'step_stage_title': 'फसल की वृद्धि अवस्था क्या है?',
      'subsidy_amount': 'सब्सिडी राशि',
      'sugarcane': 'गन्ना',
      'sugarcane_sub': 'बारह महीने की नकदी फसल',
      'survey_number': 'खसरा / सर्वेक्षण संख्या',
      'symptoms_observed': 'देखे गए लक्षण',
      'taluk': 'तहसील',
      'tap_to_speak_area': 'क्षेत्रफल बोलने के लिए टैप करें',
      'tap_to_speak_crop': 'अपनी फसल बोलने के लिए टैप करें',
      'tap_to_speak_stage': 'अवस्था बोलने के लिए टैप करें',
      'target_beneficiaries': 'लक्षित लाभार्थी',
      'tell_about_farm': 'अपने खेत के बारे में बताएं',
      'timeline_header': 'खेत गतिविधि सफ़र',
      'timeline_header_desc': 'सभी खेत गतिविधियों, परीक्षणों और अनुमोदनों की सत्यापित समयरेखा।',
      'timeline_title': 'मेरा खेत सफ़र',
      'todays_farm_brief': 'आज की कृषि सलाह',
      'total_area': 'कुल क्षेत्रफल',
      'track_progress': 'प्रगति ट्रैक करें',
      'treatment_response': 'उपचार प्रतिक्रिया',
      'type_problem_hint': 'उदा. धान के पत्ते पीले पड़ रहे हैं...',
      'unable_load_health': 'स्वास्थ्य डेटा लोड करने में असमर्थ',
      'unable_load_timeline': 'समयरेखा लोड करने में असमर्थ',
      'upload_crop_photo': 'फसल की फोटो अपलोड करें',
      'vegetative': 'वानस्पतिक वृद्धि',
      'vegetative_sub': 'पत्ते और तने का विकास',
      'verify_land_desc': 'सरकारी लाभों के लिए भूमि सत्यापित करें',
      'verify_land_now': 'अभी भूमि सत्यापित करें',
      'view_advice': 'सलाह देखें',
      'view_all': 'सभी देखें',
      'view_details': 'विवरण देखें',
      'view_health_journey': 'स्वास्थ्य समयरेखा देखें',
      'view_scheme_details': 'योजना विवरण देखें',
      'village': 'गांव',
      'voice_assistant': 'वॉयस असिस्टेंट',
      'what_problem_seeing': 'आप क्या समस्या देख रहे हैं?',
      'what_would_you_like_to_do': 'आप क्या करना चाहेंगे?',
      'your_farm_profile': 'आपकी खेत प्रोफ़ाइल',
    },
    'en-IN': {
      'acres': 'Acres',
      'active_problem_load': 'Active Problem Load',
      'activity_timeline': 'Activity Timeline',
      'analyzing_health': 'Analyzing farm health snapshot...',
      'analyzing_image': 'Analyzing crop photograph...',
      'app_title': 'BHOOMI',
      'apply_scheme': 'Apply Scheme',
      'ask_bhoomi': 'Ask BHOOMI',
      'back': 'Back',
      'banana': 'Banana',
      'banana_sub': 'Grand Naine, Robusta varieties',
      'bhoomi_advisory': 'BHOOMI Farm Advisory',
      'biological_control': 'Biological Control',
      'chemical_control': 'Chemical Control',
      'choose_language': 'Choose Your Language',
      'confidence_score': 'Confidence Score',
      'confirm_desc': 'Review and confirm your farm details',
      'confirm_farm_title': 'Confirm Farm Details',
      'continue': 'Continue',
      'cotton': 'Cotton',
      'cotton_sub': 'Long staple varieties',
      'crop_advisory_desc': 'Crop protection & growth guide',
      'crop_diagnosis_title': 'Crop Disease Diagnosis',
      'crop_label': 'Crop',
      'crop_stage_prog': 'Crop Stage Progression',
      'daily_companion': 'Daily Companion',
      'diagnose_get_advice': 'Diagnose & Get Advice',
      'diagnosis_id': 'Diagnosis ID',
      'district': 'District',
      'documents_required': 'Documents Required',
      'eligibility_criteria': 'Eligibility Criteria',
      'eligible_schemes': 'Eligible Schemes',
      'env_suitability': 'Environmental Suitability',
      'farm_health_score': 'Farm Health Score',
      'farm_health_title': 'Farm Health & Diagnosis',
      'farm_id': 'Farm ID',
      'farm_journey_desc': 'Your farm activity timeline',
      'field_weather': 'Field Weather',
      'flowering': 'Flowering Stage',
      'flowering_sub': 'Panicle initiation & flowering',
      'get_expert_help': 'Get Expert Help',
      'get_started': 'Get Started',
      'govt_support': 'Government Support',
      'govt_support_desc': 'Subsidies & financial support',
      'govt_support_finder': 'Govt Support Finder',
      'grain_filling': 'Grain Filling Stage',
      'grain_filling_sub': 'Milky to dough grain formation',
      'growth_stage_label': 'Growth Stage',
      'harvest_ready': 'Harvest Ready',
      'harvest_ready_sub': 'Fully mature & ready for harvest',
      'health_history': 'Health History',
      'health_unrated': 'Unrated',
      'health_unrated_desc': 'Needs more observation data',
      'humidity': 'Humidity',
      'kuruvai_paddy': 'Kuruvai Paddy',
      'kuruvai_paddy_sub': 'Short duration paddy crop',
      'land_area_label': 'Land Area',
      'land_boundary_title': 'Land Boundary & Map',
      'land_details_title': 'Land Details',
      'land_status_title': 'Land Verification Status',
      'land_verification_required': 'Land verification required',
      'last_computed': 'Last computed',
      'latest_update': 'Latest Update',
      'loading_journey': 'Loading farm journey...',
      'maize': 'Maize (Corn)',
      'maize_sub': 'High-yield hybrid corn',
      'maturity': 'Maturity Stage',
      'maturity_sub': 'Golden grain maturity',
      'monitoring_recency': 'Monitoring Recency',
      'my_farm': 'My Farm',
      'my_farm_journey': 'My Farm Journey',
      'no_timeline_events': 'No timeline events recorded yet.',
      'no_updates': 'No new updates right now',
      'or_type_below': 'Or type below',
      'overall_farm_health': 'Overall Farm Health',
      'ownership_status': 'Ownership Status',
      'patta_number': 'Patta Number',
      'possible_issue_identified': 'Possible Issue Identified',
      'preventive_measures': 'Preventive Measures',
      'primary_crop': 'Primary Crop',
      'provide_details': 'Provide Details',
      'quick_selection': 'Quick Selection Options',
      'rain': 'Rain',
      'recommended_actions': 'Recommended Actions',
      'recommended_schemes': 'Recommended Schemes',
      'recompute_health': 'Recompute Health',
      'refresh_status': 'Refresh Status',
      'refresh_timeline': 'Refresh Timeline',
      'requires_verified_land': 'Requires Verified Land',
      'resource_adequacy': 'Resource Adequacy',
      'retry': 'Retry',
      'samba_paddy': 'Samba Paddy',
      'samba_paddy_sub': 'Medium to long duration rice',
      'save_my_farm': 'Save My Farm',
      'scheme_details': 'Scheme Details',
      'schemes_subsidies': 'Schemes & Subsidies',
      'scientific_remedy': 'Scientific Remedy',
      'score_breakdown': 'Explainable Score Breakdown',
      'score_breakdown_desc': 'Composite health calculated across 6 key agronomic dimensions.',
      'select_farm_area': 'Select Farm Area',
      'select_stage': 'Select Growth Stage',
      'show_problem': 'Show Image',
      'step_area_sub': 'Select your cultivated land area',
      'step_area_title': 'What is your farm size?',
      'step_crop_sub': 'Speak clearly or select from list below',
      'step_crop_title': 'What are you growing?',
      'step_stage_sub': 'Select the current development stage',
      'step_stage_title': 'What is the current growth stage?',
      'subsidy_amount': 'Subsidy Amount',
      'sugarcane': 'Sugarcane',
      'sugarcane_sub': 'Annual commercial cash crop',
      'survey_number': 'Survey Number',
      'symptoms_observed': 'Symptoms Observed',
      'taluk': 'Taluk',
      'tap_to_speak_area': 'Tap to speak your farm size',
      'tap_to_speak_crop': 'Tap to speak your crop',
      'tap_to_speak_stage': 'Tap to speak current stage',
      'target_beneficiaries': 'Target Beneficiaries',
      'tell_about_farm': 'Let\'s Get to Know Your Farm',
      'timeline_header': 'Farm Activity Journey',
      'timeline_header_desc': 'Verified chronological timeline of all farm actions, diagnostics, and approvals.',
      'timeline_title': 'My Farm Journey',
      'todays_farm_brief': 'Today\'s Guidance',
      'total_area': 'Total Area',
      'track_progress': 'Track Progress',
      'treatment_response': 'Treatment Response',
      'type_problem_hint': 'e.g. Paddy leaves turning yellow with brown spots...',
      'unable_load_health': 'Unable to Load Health Data',
      'unable_load_timeline': 'Unable to Load Timeline',
      'upload_crop_photo': 'Upload Crop Photo',
      'vegetative': 'Vegetative Stage',
      'vegetative_sub': 'Tillering & vegetative shoot growth',
      'verify_land_desc': 'Verify your land for govt schemes',
      'verify_land_now': 'Verify Land Now',
      'view_advice': 'View Advice',
      'view_all': 'View All',
      'view_details': 'View Details',
      'view_health_journey': 'View Health Journey Timeline',
      'view_scheme_details': 'View Scheme Details',
      'village': 'Village',
      'voice_assistant': 'Voice Assistant',
      'what_problem_seeing': 'What problem are you seeing?',
      'what_would_you_like_to_do': 'What would you like to do?',
      'your_farm_profile': 'Your Farm Profile',
    },
    'te-IN': {
      'acres': 'ఎకరాలు',
      'active_problem_load': 'Active Problem Load',
      'activity_timeline': 'Activity Timeline',
      'analyzing_health': 'Analyzing farm health snapshot...',
      'analyzing_image': 'Analyzing crop photograph...',
      'app_title': 'భూమి',
      'apply_scheme': 'Apply Scheme',
      'ask_bhoomi': 'భూమిని అడగండి',
      'back': 'వెనుకకు',
      'banana': 'Banana',
      'banana_sub': 'Grand Naine, Robusta varieties',
      'bhoomi_advisory': 'BHOOMI Farm Advisory',
      'biological_control': 'Biological Control',
      'chemical_control': 'Chemical Control',
      'choose_language': 'మీ భాషను ఎంచుకోండి',
      'confidence_score': 'Confidence Score',
      'confirm_desc': 'Review and confirm your farm details',
      'confirm_farm_title': 'Confirm Farm Details',
      'continue': 'కొనసాగించండి',
      'cotton': 'Cotton',
      'cotton_sub': 'Long staple varieties',
      'crop_advisory_desc': 'Crop protection & growth guide',
      'crop_diagnosis_title': 'Crop Disease Diagnosis',
      'crop_label': 'Crop',
      'crop_stage_prog': 'Crop Stage Progression',
      'daily_companion': 'Daily Companion',
      'diagnose_get_advice': 'Diagnose & Get Advice',
      'diagnosis_id': 'Diagnosis ID',
      'district': 'District',
      'documents_required': 'Documents Required',
      'eligibility_criteria': 'Eligibility Criteria',
      'eligible_schemes': 'Eligible Schemes',
      'env_suitability': 'Environmental Suitability',
      'farm_health_score': 'Farm Health Score',
      'farm_health_title': 'వ్యవసాయ ఆరోగ్యం & రోగ నిర్ధారణ',
      'farm_id': 'Farm ID',
      'farm_journey_desc': 'Your farm activity timeline',
      'field_weather': 'Field Weather',
      'flowering': 'పూత దశ',
      'flowering_sub': 'Panicle initiation & flowering',
      'get_expert_help': 'Get Expert Help',
      'get_started': 'ప్రారంభించండి',
      'govt_support': 'ప్రభుత్వ పథకాలు',
      'govt_support_desc': 'Subsidies & financial support',
      'govt_support_finder': 'Govt Support Finder',
      'grain_filling': 'గింజ పాలుపోసుకునే దశ',
      'grain_filling_sub': 'Milky to dough grain formation',
      'growth_stage_label': 'Growth Stage',
      'harvest_ready': 'కోతకు సిద్ధం',
      'harvest_ready_sub': 'Fully mature & ready for harvest',
      'health_history': 'Health History',
      'health_unrated': 'Unrated',
      'health_unrated_desc': 'Needs more observation data',
      'humidity': 'Humidity',
      'kuruvai_paddy': 'Kuruvai Paddy',
      'kuruvai_paddy_sub': 'Short duration paddy crop',
      'land_area_label': 'Land Area',
      'land_boundary_title': 'Land Boundary & Map',
      'land_details_title': 'Land Details',
      'land_status_title': 'Land Verification Status',
      'land_verification_required': 'Land verification required',
      'last_computed': 'Last computed',
      'latest_update': 'Latest Update',
      'loading_journey': 'Loading farm journey...',
      'maize': 'Maize (Corn)',
      'maize_sub': 'High-yield hybrid corn',
      'maturity': 'పక్వత దశ',
      'maturity_sub': 'Golden grain maturity',
      'monitoring_recency': 'Monitoring Recency',
      'my_farm': 'నా వ్యవసాయం',
      'my_farm_journey': 'నా వ్యవసాయ ప్రయాణం',
      'no_timeline_events': 'No timeline events recorded yet.',
      'no_updates': 'No new updates right now',
      'or_type_below': 'Or type below',
      'overall_farm_health': 'మొత్తం వ్యవసాయ ఆరోగ్యం',
      'ownership_status': 'Ownership Status',
      'patta_number': 'Patta Number',
      'possible_issue_identified': 'Possible Issue Identified',
      'preventive_measures': 'Preventive Measures',
      'primary_crop': 'Primary Crop',
      'provide_details': 'Provide Details',
      'quick_selection': 'శీఘ్ర ఎంపికలు',
      'rain': 'Rain',
      'recommended_actions': 'Recommended Actions',
      'recommended_schemes': 'Recommended Schemes',
      'recompute_health': 'Recompute Health',
      'refresh_status': 'Refresh Status',
      'refresh_timeline': 'Refresh Timeline',
      'requires_verified_land': 'Requires Verified Land',
      'resource_adequacy': 'Resource Adequacy',
      'retry': 'Retry',
      'samba_paddy': 'సాంబా వరి',
      'samba_paddy_sub': 'Medium to long duration rice',
      'save_my_farm': 'Save My Farm',
      'scheme_details': 'Scheme Details',
      'schemes_subsidies': 'Schemes & Subsidies',
      'scientific_remedy': 'Scientific Remedy',
      'score_breakdown': 'వివరణాత్మక స్కోరు విచ్ఛిన్నం',
      'score_breakdown_desc': 'Composite health calculated across 6 key agronomic dimensions.',
      'select_farm_area': 'Select Farm Area',
      'select_stage': 'Select Growth Stage',
      'show_problem': 'Show Image',
      'step_area_sub': 'Select your cultivated land area',
      'step_area_title': 'What is your farm size?',
      'step_crop_sub': 'Speak clearly or select from list below',
      'step_crop_title': 'What are you growing?',
      'step_stage_sub': 'Select the current development stage',
      'step_stage_title': 'What is the current growth stage?',
      'subsidy_amount': 'Subsidy Amount',
      'sugarcane': 'చెరకు',
      'sugarcane_sub': 'Annual commercial cash crop',
      'survey_number': 'Survey Number',
      'symptoms_observed': 'Symptoms Observed',
      'taluk': 'Taluk',
      'tap_to_speak_area': 'Tap to speak your farm size',
      'tap_to_speak_crop': 'Tap to speak your crop',
      'tap_to_speak_stage': 'Tap to speak current stage',
      'target_beneficiaries': 'Target Beneficiaries',
      'tell_about_farm': 'మీ వ్యవసాయం గురించి చెప్పండి',
      'timeline_header': 'Farm Activity Journey',
      'timeline_header_desc': 'Verified chronological timeline of all farm actions, diagnostics, and approvals.',
      'timeline_title': 'నా వ్యవసాయ ప్రయాణం',
      'todays_farm_brief': 'నేటి మార్గదర్శి',
      'total_area': 'Total Area',
      'track_progress': 'Track Progress',
      'treatment_response': 'Treatment Response',
      'type_problem_hint': 'e.g. Paddy leaves turning yellow with brown spots...',
      'unable_load_health': 'Unable to Load Health Data',
      'unable_load_timeline': 'Unable to Load Timeline',
      'upload_crop_photo': 'Upload Crop Photo',
      'vegetative': 'శాకీయ దశ',
      'vegetative_sub': 'Tillering & vegetative shoot growth',
      'verify_land_desc': 'Verify your land for govt schemes',
      'verify_land_now': 'Verify Land Now',
      'view_advice': 'View Advice',
      'view_all': 'View All',
      'view_details': 'View Details',
      'view_health_journey': 'View Health Journey Timeline',
      'view_scheme_details': 'View Scheme Details',
      'village': 'Village',
      'voice_assistant': 'Voice Assistant',
      'what_problem_seeing': 'What problem are you seeing?',
      'what_would_you_like_to_do': 'What would you like to do?',
      'your_farm_profile': 'Your Farm Profile',
    },
    'kn-IN': {
      'acres': 'ಎಕರೆ',
      'active_problem_load': 'Active Problem Load',
      'activity_timeline': 'Activity Timeline',
      'analyzing_health': 'Analyzing farm health snapshot...',
      'analyzing_image': 'Analyzing crop photograph...',
      'app_title': 'ಭೂಮಿ',
      'apply_scheme': 'Apply Scheme',
      'ask_bhoomi': 'ಭೂಮಿಯನ್ನು ಕೇಳಿ',
      'back': 'ಹಿಂದೆ',
      'banana': 'Banana',
      'banana_sub': 'Grand Naine, Robusta varieties',
      'bhoomi_advisory': 'BHOOMI Farm Advisory',
      'biological_control': 'Biological Control',
      'chemical_control': 'Chemical Control',
      'choose_language': 'ನಿಮ್ಮ ಭಾಷೆಯನ್ನು ಆಯ್ಕೆಮಾಡಿ',
      'confidence_score': 'Confidence Score',
      'confirm_desc': 'Review and confirm your farm details',
      'confirm_farm_title': 'Confirm Farm Details',
      'continue': 'ಮುಂದುವರಿಯಿರಿ',
      'cotton': 'Cotton',
      'cotton_sub': 'Long staple varieties',
      'crop_advisory_desc': 'Crop protection & growth guide',
      'crop_diagnosis_title': 'Crop Disease Diagnosis',
      'crop_label': 'Crop',
      'crop_stage_prog': 'Crop Stage Progression',
      'daily_companion': 'Daily Companion',
      'diagnose_get_advice': 'Diagnose & Get Advice',
      'diagnosis_id': 'Diagnosis ID',
      'district': 'District',
      'documents_required': 'Documents Required',
      'eligibility_criteria': 'Eligibility Criteria',
      'eligible_schemes': 'Eligible Schemes',
      'env_suitability': 'Environmental Suitability',
      'farm_health_score': 'Farm Health Score',
      'farm_health_title': 'ಕೃಷಿ ಆರೋಗ್ಯ & ರೋಗನಿರ್ಣಯ',
      'farm_id': 'Farm ID',
      'farm_journey_desc': 'Your farm activity timeline',
      'field_weather': 'Field Weather',
      'flowering': 'ಹೂಬಿಡುವ ಹಂತ',
      'flowering_sub': 'Panicle initiation & flowering',
      'get_expert_help': 'Get Expert Help',
      'get_started': 'ಪ್ರಾರಂಭಿಸಿ',
      'govt_support': 'ಸರ್ಕಾರಿ ಯೋಜನೆಗಳು',
      'govt_support_desc': 'Subsidies & financial support',
      'govt_support_finder': 'Govt Support Finder',
      'grain_filling': 'ಕಾಳು ಕಟ್ಟುವ ಹಂತ',
      'grain_filling_sub': 'Milky to dough grain formation',
      'growth_stage_label': 'Growth Stage',
      'harvest_ready': 'ಕೊಯ್ಲಿಗೆ ಸಿದ್ಧ',
      'harvest_ready_sub': 'Fully mature & ready for harvest',
      'health_history': 'Health History',
      'health_unrated': 'Unrated',
      'health_unrated_desc': 'Needs more observation data',
      'humidity': 'Humidity',
      'kuruvai_paddy': 'Kuruvai Paddy',
      'kuruvai_paddy_sub': 'Short duration paddy crop',
      'land_area_label': 'Land Area',
      'land_boundary_title': 'Land Boundary & Map',
      'land_details_title': 'Land Details',
      'land_status_title': 'Land Verification Status',
      'land_verification_required': 'Land verification required',
      'last_computed': 'Last computed',
      'latest_update': 'Latest Update',
      'loading_journey': 'Loading farm journey...',
      'maize': 'Maize (Corn)',
      'maize_sub': 'High-yield hybrid corn',
      'maturity': 'ಪಕ್ವತೆ ಹಂತ',
      'maturity_sub': 'Golden grain maturity',
      'monitoring_recency': 'Monitoring Recency',
      'my_farm': 'ನನ್ನ ಹೊಲ',
      'my_farm_journey': 'ನನ್ನ ಕೃಷಿ ಪಯಣ',
      'no_timeline_events': 'No timeline events recorded yet.',
      'no_updates': 'No new updates right now',
      'or_type_below': 'Or type below',
      'overall_farm_health': 'ಒಟ್ಟಾರೆ ಕೃಷಿ ಆರೋಗ್ಯ',
      'ownership_status': 'Ownership Status',
      'patta_number': 'Patta Number',
      'possible_issue_identified': 'Possible Issue Identified',
      'preventive_measures': 'Preventive Measures',
      'primary_crop': 'Primary Crop',
      'provide_details': 'Provide Details',
      'quick_selection': 'ತ್ವರಿತ ಆಯ್ಕೆಗಳು',
      'rain': 'Rain',
      'recommended_actions': 'Recommended Actions',
      'recommended_schemes': 'Recommended Schemes',
      'recompute_health': 'Recompute Health',
      'refresh_status': 'Refresh Status',
      'refresh_timeline': 'Refresh Timeline',
      'requires_verified_land': 'Requires Verified Land',
      'resource_adequacy': 'Resource Adequacy',
      'retry': 'Retry',
      'samba_paddy': 'ಸಾಂಬಾ ಭತ್ತ',
      'samba_paddy_sub': 'Medium to long duration rice',
      'save_my_farm': 'Save My Farm',
      'scheme_details': 'Scheme Details',
      'schemes_subsidies': 'Schemes & Subsidies',
      'scientific_remedy': 'Scientific Remedy',
      'score_breakdown': 'ವಿವರಣಾತ್ಮಕ ಅಂಕಗಳ ವಿವರಣೆ',
      'score_breakdown_desc': 'Composite health calculated across 6 key agronomic dimensions.',
      'select_farm_area': 'Select Farm Area',
      'select_stage': 'Select Growth Stage',
      'show_problem': 'Show Image',
      'step_area_sub': 'Select your cultivated land area',
      'step_area_title': 'What is your farm size?',
      'step_crop_sub': 'Speak clearly or select from list below',
      'step_crop_title': 'What are you growing?',
      'step_stage_sub': 'Select the current development stage',
      'step_stage_title': 'What is the current growth stage?',
      'subsidy_amount': 'Subsidy Amount',
      'sugarcane': 'ಕಬ್ಬು',
      'sugarcane_sub': 'Annual commercial cash crop',
      'survey_number': 'Survey Number',
      'symptoms_observed': 'Symptoms Observed',
      'taluk': 'Taluk',
      'tap_to_speak_area': 'Tap to speak your farm size',
      'tap_to_speak_crop': 'Tap to speak your crop',
      'tap_to_speak_stage': 'Tap to speak current stage',
      'target_beneficiaries': 'Target Beneficiaries',
      'tell_about_farm': 'ನಿಮ್ಮ ಕೃಷಿ ಬಗ್ಗೆ ತಿಳಿಸಿ',
      'timeline_header': 'Farm Activity Journey',
      'timeline_header_desc': 'Verified chronological timeline of all farm actions, diagnostics, and approvals.',
      'timeline_title': 'ನನ್ನ ಕೃಷಿ ಪಯಣ',
      'todays_farm_brief': 'ಇಂದಿನ ಮಾರ್ಗದರ್ಶಿ',
      'total_area': 'Total Area',
      'track_progress': 'Track Progress',
      'treatment_response': 'Treatment Response',
      'type_problem_hint': 'e.g. Paddy leaves turning yellow with brown spots...',
      'unable_load_health': 'Unable to Load Health Data',
      'unable_load_timeline': 'Unable to Load Timeline',
      'upload_crop_photo': 'Upload Crop Photo',
      'vegetative': 'ಸಸ್ಯಕ ಹಂತ',
      'vegetative_sub': 'Tillering & vegetative shoot growth',
      'verify_land_desc': 'Verify your land for govt schemes',
      'verify_land_now': 'Verify Land Now',
      'view_advice': 'View Advice',
      'view_all': 'View All',
      'view_details': 'View Details',
      'view_health_journey': 'View Health Journey Timeline',
      'view_scheme_details': 'View Scheme Details',
      'village': 'Village',
      'voice_assistant': 'Voice Assistant',
      'what_problem_seeing': 'What problem are you seeing?',
      'what_would_you_like_to_do': 'What would you like to do?',
      'your_farm_profile': 'Your Farm Profile',
    },
    'mr-IN': {
      'acres': 'एकर',
      'active_problem_load': 'Active Problem Load',
      'activity_timeline': 'Activity Timeline',
      'analyzing_health': 'Analyzing farm health snapshot...',
      'analyzing_image': 'Analyzing crop photograph...',
      'app_title': 'भूमी',
      'apply_scheme': 'Apply Scheme',
      'ask_bhoomi': 'भूमीला विचारा',
      'back': 'मागे जा',
      'banana': 'Banana',
      'banana_sub': 'Grand Naine, Robusta varieties',
      'bhoomi_advisory': 'BHOOMI Farm Advisory',
      'biological_control': 'Biological Control',
      'chemical_control': 'Chemical Control',
      'choose_language': 'तुमची भाषा निवडा',
      'confidence_score': 'Confidence Score',
      'confirm_desc': 'Review and confirm your farm details',
      'confirm_farm_title': 'Confirm Farm Details',
      'continue': 'पुढे सुरू ठेवा',
      'cotton': 'Cotton',
      'cotton_sub': 'Long staple varieties',
      'crop_advisory_desc': 'Crop protection & growth guide',
      'crop_diagnosis_title': 'Crop Disease Diagnosis',
      'crop_label': 'Crop',
      'crop_stage_prog': 'Crop Stage Progression',
      'daily_companion': 'Daily Companion',
      'diagnose_get_advice': 'Diagnose & Get Advice',
      'diagnosis_id': 'Diagnosis ID',
      'district': 'District',
      'documents_required': 'Documents Required',
      'eligibility_criteria': 'Eligibility Criteria',
      'eligible_schemes': 'Eligible Schemes',
      'env_suitability': 'Environmental Suitability',
      'farm_health_score': 'Farm Health Score',
      'farm_health_title': 'शेत आरोग्य आणि निदान',
      'farm_id': 'Farm ID',
      'farm_journey_desc': 'Your farm activity timeline',
      'field_weather': 'Field Weather',
      'flowering': 'फुलोरा अवस्था',
      'flowering_sub': 'Panicle initiation & flowering',
      'get_expert_help': 'Get Expert Help',
      'get_started': 'सुरू करा',
      'govt_support': 'सरकारी योजना',
      'govt_support_desc': 'Subsidies & financial support',
      'govt_support_finder': 'Govt Support Finder',
      'grain_filling': 'दाणे भरण्याची अवस्था',
      'grain_filling_sub': 'Milky to dough grain formation',
      'growth_stage_label': 'Growth Stage',
      'harvest_ready': 'कापणीसाठी तयार',
      'harvest_ready_sub': 'Fully mature & ready for harvest',
      'health_history': 'Health History',
      'health_unrated': 'Unrated',
      'health_unrated_desc': 'Needs more observation data',
      'humidity': 'Humidity',
      'kuruvai_paddy': 'Kuruvai Paddy',
      'kuruvai_paddy_sub': 'Short duration paddy crop',
      'land_area_label': 'Land Area',
      'land_boundary_title': 'Land Boundary & Map',
      'land_details_title': 'Land Details',
      'land_status_title': 'Land Verification Status',
      'land_verification_required': 'Land verification required',
      'last_computed': 'Last computed',
      'latest_update': 'Latest Update',
      'loading_journey': 'Loading farm journey...',
      'maize': 'Maize (Corn)',
      'maize_sub': 'High-yield hybrid corn',
      'maturity': 'परिपक्वता अवस्था',
      'maturity_sub': 'Golden grain maturity',
      'monitoring_recency': 'Monitoring Recency',
      'my_farm': 'माझे शेत',
      'my_farm_journey': 'माझा शेती प्रवास',
      'no_timeline_events': 'No timeline events recorded yet.',
      'no_updates': 'No new updates right now',
      'or_type_below': 'Or type below',
      'overall_farm_health': 'एकूण शेत आरोग्य',
      'ownership_status': 'Ownership Status',
      'patta_number': 'Patta Number',
      'possible_issue_identified': 'Possible Issue Identified',
      'preventive_measures': 'Preventive Measures',
      'primary_crop': 'Primary Crop',
      'provide_details': 'Provide Details',
      'quick_selection': 'द्रुत निवड पर्याय',
      'rain': 'Rain',
      'recommended_actions': 'Recommended Actions',
      'recommended_schemes': 'Recommended Schemes',
      'recompute_health': 'Recompute Health',
      'refresh_status': 'Refresh Status',
      'refresh_timeline': 'Refresh Timeline',
      'requires_verified_land': 'Requires Verified Land',
      'resource_adequacy': 'Resource Adequacy',
      'retry': 'Retry',
      'samba_paddy': 'सांभा भात (तांदूळ)',
      'samba_paddy_sub': 'Medium to long duration rice',
      'save_my_farm': 'Save My Farm',
      'scheme_details': 'Scheme Details',
      'schemes_subsidies': 'Schemes & Subsidies',
      'scientific_remedy': 'Scientific Remedy',
      'score_breakdown': 'तपशीलवार स्कोअर विश्लेषण',
      'score_breakdown_desc': 'Composite health calculated across 6 key agronomic dimensions.',
      'select_farm_area': 'Select Farm Area',
      'select_stage': 'Select Growth Stage',
      'show_problem': 'Show Image',
      'step_area_sub': 'Select your cultivated land area',
      'step_area_title': 'What is your farm size?',
      'step_crop_sub': 'Speak clearly or select from list below',
      'step_crop_title': 'What are you growing?',
      'step_stage_sub': 'Select the current development stage',
      'step_stage_title': 'What is the current growth stage?',
      'subsidy_amount': 'Subsidy Amount',
      'sugarcane': 'ऊस',
      'sugarcane_sub': 'Annual commercial cash crop',
      'survey_number': 'Survey Number',
      'symptoms_observed': 'Symptoms Observed',
      'taluk': 'Taluk',
      'tap_to_speak_area': 'Tap to speak your farm size',
      'tap_to_speak_crop': 'Tap to speak your crop',
      'tap_to_speak_stage': 'Tap to speak current stage',
      'target_beneficiaries': 'Target Beneficiaries',
      'tell_about_farm': 'तुमच्या शेताबद्दल सांगा',
      'timeline_header': 'Farm Activity Journey',
      'timeline_header_desc': 'Verified chronological timeline of all farm actions, diagnostics, and approvals.',
      'timeline_title': 'माझा शेती प्रवास',
      'todays_farm_brief': 'आजचे मार्गदर्शन',
      'total_area': 'Total Area',
      'track_progress': 'Track Progress',
      'treatment_response': 'Treatment Response',
      'type_problem_hint': 'e.g. Paddy leaves turning yellow with brown spots...',
      'unable_load_health': 'Unable to Load Health Data',
      'unable_load_timeline': 'Unable to Load Timeline',
      'upload_crop_photo': 'Upload Crop Photo',
      'vegetative': 'शाकीय वाढीची अवस्था',
      'vegetative_sub': 'Tillering & vegetative shoot growth',
      'verify_land_desc': 'Verify your land for govt schemes',
      'verify_land_now': 'Verify Land Now',
      'view_advice': 'View Advice',
      'view_all': 'View All',
      'view_details': 'View Details',
      'view_health_journey': 'View Health Journey Timeline',
      'view_scheme_details': 'View Scheme Details',
      'village': 'Village',
      'voice_assistant': 'Voice Assistant',
      'what_problem_seeing': 'What problem are you seeing?',
      'what_would_you_like_to_do': 'What would you like to do?',
      'your_farm_profile': 'Your Farm Profile',
    },
    'ml-IN': {
      'acres': 'ഏക്കർ',
      'active_problem_load': 'Active Problem Load',
      'activity_timeline': 'Activity Timeline',
      'analyzing_health': 'Analyzing farm health snapshot...',
      'analyzing_image': 'Analyzing crop photograph...',
      'app_title': 'ഭൂമി',
      'apply_scheme': 'Apply Scheme',
      'ask_bhoomi': 'ഭൂമിയോട് ചോദിക്കുക',
      'back': 'പിന്നോട്ട്',
      'banana': 'Banana',
      'banana_sub': 'Grand Naine, Robusta varieties',
      'bhoomi_advisory': 'BHOOMI Farm Advisory',
      'biological_control': 'Biological Control',
      'chemical_control': 'Chemical Control',
      'choose_language': 'നിങ്ങളുടെ ഭാഷ തിരഞ്ഞെടുക്കുക',
      'confidence_score': 'Confidence Score',
      'confirm_desc': 'Review and confirm your farm details',
      'confirm_farm_title': 'Confirm Farm Details',
      'continue': 'തുടരുക',
      'cotton': 'Cotton',
      'cotton_sub': 'Long staple varieties',
      'crop_advisory_desc': 'Crop protection & growth guide',
      'crop_diagnosis_title': 'Crop Disease Diagnosis',
      'crop_label': 'Crop',
      'crop_stage_prog': 'Crop Stage Progression',
      'daily_companion': 'Daily Companion',
      'diagnose_get_advice': 'Diagnose & Get Advice',
      'diagnosis_id': 'Diagnosis ID',
      'district': 'District',
      'documents_required': 'Documents Required',
      'eligibility_criteria': 'Eligibility Criteria',
      'eligible_schemes': 'Eligible Schemes',
      'env_suitability': 'Environmental Suitability',
      'farm_health_score': 'Farm Health Score',
      'farm_health_title': 'കൃഷി ആരോഗ്യവും രോഗനിർണയവും',
      'farm_id': 'Farm ID',
      'farm_journey_desc': 'Your farm activity timeline',
      'field_weather': 'Field Weather',
      'flowering': 'പൂവിടൽ ഘട്ടം',
      'flowering_sub': 'Panicle initiation & flowering',
      'get_expert_help': 'Get Expert Help',
      'get_started': 'ആരംഭിക്കുക',
      'govt_support': 'സർക്കാർ പദ്ധതികൾ',
      'govt_support_desc': 'Subsidies & financial support',
      'govt_support_finder': 'Govt Support Finder',
      'grain_filling': 'മണി നിറയുന്ന ഘട്ടം',
      'grain_filling_sub': 'Milky to dough grain formation',
      'growth_stage_label': 'Growth Stage',
      'harvest_ready': 'വിളവെടുപ്പിന് തയ്യാർ',
      'harvest_ready_sub': 'Fully mature & ready for harvest',
      'health_history': 'Health History',
      'health_unrated': 'Unrated',
      'health_unrated_desc': 'Needs more observation data',
      'humidity': 'Humidity',
      'kuruvai_paddy': 'Kuruvai Paddy',
      'kuruvai_paddy_sub': 'Short duration paddy crop',
      'land_area_label': 'Land Area',
      'land_boundary_title': 'Land Boundary & Map',
      'land_details_title': 'Land Details',
      'land_status_title': 'Land Verification Status',
      'land_verification_required': 'Land verification required',
      'last_computed': 'Last computed',
      'latest_update': 'Latest Update',
      'loading_journey': 'Loading farm journey...',
      'maize': 'Maize (Corn)',
      'maize_sub': 'High-yield hybrid corn',
      'maturity': 'വിളവെത്തൽ ഘട്ടം',
      'maturity_sub': 'Golden grain maturity',
      'monitoring_recency': 'Monitoring Recency',
      'my_farm': 'എന്റെ കൃഷി',
      'my_farm_journey': 'എന്റെ കൃഷി യാത്ര',
      'no_timeline_events': 'No timeline events recorded yet.',
      'no_updates': 'No new updates right now',
      'or_type_below': 'Or type below',
      'overall_farm_health': 'ആകെ കൃഷി ആരോഗ്യം',
      'ownership_status': 'Ownership Status',
      'patta_number': 'Patta Number',
      'possible_issue_identified': 'Possible Issue Identified',
      'preventive_measures': 'Preventive Measures',
      'primary_crop': 'Primary Crop',
      'provide_details': 'Provide Details',
      'quick_selection': 'പെട്ടെന്നുള്ള തിരഞ്ഞെടുപ്പുകൾ',
      'rain': 'Rain',
      'recommended_actions': 'Recommended Actions',
      'recommended_schemes': 'Recommended Schemes',
      'recompute_health': 'Recompute Health',
      'refresh_status': 'Refresh Status',
      'refresh_timeline': 'Refresh Timeline',
      'requires_verified_land': 'Requires Verified Land',
      'resource_adequacy': 'Resource Adequacy',
      'retry': 'Retry',
      'samba_paddy': 'സാംബാ നെല്ല്',
      'samba_paddy_sub': 'Medium to long duration rice',
      'save_my_farm': 'Save My Farm',
      'scheme_details': 'Scheme Details',
      'schemes_subsidies': 'Schemes & Subsidies',
      'scientific_remedy': 'Scientific Remedy',
      'score_breakdown': 'വിശദമായ സ്കോർ വിശകലനം',
      'score_breakdown_desc': 'Composite health calculated across 6 key agronomic dimensions.',
      'select_farm_area': 'Select Farm Area',
      'select_stage': 'Select Growth Stage',
      'show_problem': 'Show Image',
      'step_area_sub': 'Select your cultivated land area',
      'step_area_title': 'What is your farm size?',
      'step_crop_sub': 'Speak clearly or select from list below',
      'step_crop_title': 'What are you growing?',
      'step_stage_sub': 'Select the current development stage',
      'step_stage_title': 'What is the current growth stage?',
      'subsidy_amount': 'Subsidy Amount',
      'sugarcane': 'കരിമ്പ്',
      'sugarcane_sub': 'Annual commercial cash crop',
      'survey_number': 'Survey Number',
      'symptoms_observed': 'Symptoms Observed',
      'taluk': 'Taluk',
      'tap_to_speak_area': 'Tap to speak your farm size',
      'tap_to_speak_crop': 'Tap to speak your crop',
      'tap_to_speak_stage': 'Tap to speak current stage',
      'target_beneficiaries': 'Target Beneficiaries',
      'tell_about_farm': 'നിങ്ങളുടെ കൃഷിയെക്കുറിച്ച് പറയുക',
      'timeline_header': 'Farm Activity Journey',
      'timeline_header_desc': 'Verified chronological timeline of all farm actions, diagnostics, and approvals.',
      'timeline_title': 'എന്റെ കൃഷി യാത്ര',
      'todays_farm_brief': 'ഇന്നത്തെ കൃഷി ഉപദേശം',
      'total_area': 'Total Area',
      'track_progress': 'Track Progress',
      'treatment_response': 'Treatment Response',
      'type_problem_hint': 'e.g. Paddy leaves turning yellow with brown spots...',
      'unable_load_health': 'Unable to Load Health Data',
      'unable_load_timeline': 'Unable to Load Timeline',
      'upload_crop_photo': 'Upload Crop Photo',
      'vegetative': 'കായിക വളർച്ച ഘട്ടം',
      'vegetative_sub': 'Tillering & vegetative shoot growth',
      'verify_land_desc': 'Verify your land for govt schemes',
      'verify_land_now': 'Verify Land Now',
      'view_advice': 'View Advice',
      'view_all': 'View All',
      'view_details': 'View Details',
      'view_health_journey': 'View Health Journey Timeline',
      'view_scheme_details': 'View Scheme Details',
      'village': 'Village',
      'voice_assistant': 'Voice Assistant',
      'what_problem_seeing': 'What problem are you seeing?',
      'what_would_you_like_to_do': 'What would you like to do?',
      'your_farm_profile': 'Your Farm Profile',
    },
    'pa-IN': {
      'acres': 'ਏਕੜ',
      'active_problem_load': 'Active Problem Load',
      'activity_timeline': 'Activity Timeline',
      'analyzing_health': 'Analyzing farm health snapshot...',
      'analyzing_image': 'Analyzing crop photograph...',
      'app_title': 'ਭੂਮੀ',
      'apply_scheme': 'Apply Scheme',
      'ask_bhoomi': 'ਭੂਮੀ ਨੂੰ ਪੁੱਛੋ',
      'back': 'ਪਿੱਛੇ',
      'banana': 'Banana',
      'banana_sub': 'Grand Naine, Robusta varieties',
      'bhoomi_advisory': 'BHOOMI Farm Advisory',
      'biological_control': 'Biological Control',
      'chemical_control': 'Chemical Control',
      'choose_language': 'ਆਪਣੀ ਭਾਸ਼ਾ ਚੁਣੋ',
      'confidence_score': 'Confidence Score',
      'confirm_desc': 'Review and confirm your farm details',
      'confirm_farm_title': 'Confirm Farm Details',
      'continue': 'ਜਾਰੀ ਰੱਖੋ',
      'cotton': 'Cotton',
      'cotton_sub': 'Long staple varieties',
      'crop_advisory_desc': 'Crop protection & growth guide',
      'crop_diagnosis_title': 'Crop Disease Diagnosis',
      'crop_label': 'Crop',
      'crop_stage_prog': 'Crop Stage Progression',
      'daily_companion': 'Daily Companion',
      'diagnose_get_advice': 'Diagnose & Get Advice',
      'diagnosis_id': 'Diagnosis ID',
      'district': 'District',
      'documents_required': 'Documents Required',
      'eligibility_criteria': 'Eligibility Criteria',
      'eligible_schemes': 'Eligible Schemes',
      'env_suitability': 'Environmental Suitability',
      'farm_health_score': 'Farm Health Score',
      'farm_health_title': 'ਖੇਤ ਦੀ ਸਿਹਤ ਅਤੇ ਜਾਂਚ',
      'farm_id': 'Farm ID',
      'farm_journey_desc': 'Your farm activity timeline',
      'field_weather': 'Field Weather',
      'flowering': 'ਫੁੱਲ ਪੈਣ ਦਾ ਸਮਾਂ',
      'flowering_sub': 'Panicle initiation & flowering',
      'get_expert_help': 'Get Expert Help',
      'get_started': 'ਸ਼ੁਰੂ ਕਰੋ',
      'govt_support': 'ਸਰਕਾਰੀ ਸਕੀਮਾਂ',
      'govt_support_desc': 'Subsidies & financial support',
      'govt_support_finder': 'Govt Support Finder',
      'grain_filling': 'ਦਾਣਾ ਭਰਨ ਦਾ ਸਮਾਂ',
      'grain_filling_sub': 'Milky to dough grain formation',
      'growth_stage_label': 'Growth Stage',
      'harvest_ready': 'ਵਾਢੀ ਲਈ ਤਿਆਰ',
      'harvest_ready_sub': 'Fully mature & ready for harvest',
      'health_history': 'Health History',
      'health_unrated': 'Unrated',
      'health_unrated_desc': 'Needs more observation data',
      'humidity': 'Humidity',
      'kuruvai_paddy': 'Kuruvai Paddy',
      'kuruvai_paddy_sub': 'Short duration paddy crop',
      'land_area_label': 'Land Area',
      'land_boundary_title': 'Land Boundary & Map',
      'land_details_title': 'Land Details',
      'land_status_title': 'Land Verification Status',
      'land_verification_required': 'Land verification required',
      'last_computed': 'Last computed',
      'latest_update': 'Latest Update',
      'loading_journey': 'Loading farm journey...',
      'maize': 'Maize (Corn)',
      'maize_sub': 'High-yield hybrid corn',
      'maturity': 'ਪੱਕਣ ਦਾ ਸਮਾਂ',
      'maturity_sub': 'Golden grain maturity',
      'monitoring_recency': 'Monitoring Recency',
      'my_farm': 'ਮੇਰਾ ਖੇਤ',
      'my_farm_journey': 'ਮੇਰਾ ਖੇਤੀ ਸਫ਼ਰ',
      'no_timeline_events': 'No timeline events recorded yet.',
      'no_updates': 'No new updates right now',
      'or_type_below': 'Or type below',
      'overall_farm_health': 'ਕੁੱਲ ਖੇਤ ਸਿਹਤ',
      'ownership_status': 'Ownership Status',
      'patta_number': 'Patta Number',
      'possible_issue_identified': 'Possible Issue Identified',
      'preventive_measures': 'Preventive Measures',
      'primary_crop': 'Primary Crop',
      'provide_details': 'Provide Details',
      'quick_selection': 'ਤੇਜ਼ ਚੋਣ ਵਿਕਲਪ',
      'rain': 'Rain',
      'recommended_actions': 'Recommended Actions',
      'recommended_schemes': 'Recommended Schemes',
      'recompute_health': 'Recompute Health',
      'refresh_status': 'Refresh Status',
      'refresh_timeline': 'Refresh Timeline',
      'requires_verified_land': 'Requires Verified Land',
      'resource_adequacy': 'Resource Adequacy',
      'retry': 'Retry',
      'samba_paddy': 'ਸਾਂਭਾ ਝੋਨਾ (ਚੌਲ)',
      'samba_paddy_sub': 'Medium to long duration rice',
      'save_my_farm': 'Save My Farm',
      'scheme_details': 'Scheme Details',
      'schemes_subsidies': 'Schemes & Subsidies',
      'scientific_remedy': 'Scientific Remedy',
      'score_breakdown': 'ਵਿਸਤ੍ਰਿਤ ਸਕੋਰ ਵੇਰਵਾ',
      'score_breakdown_desc': 'Composite health calculated across 6 key agronomic dimensions.',
      'select_farm_area': 'Select Farm Area',
      'select_stage': 'Select Growth Stage',
      'show_problem': 'Show Image',
      'step_area_sub': 'Select your cultivated land area',
      'step_area_title': 'What is your farm size?',
      'step_crop_sub': 'Speak clearly or select from list below',
      'step_crop_title': 'What are you growing?',
      'step_stage_sub': 'Select the current development stage',
      'step_stage_title': 'What is the current growth stage?',
      'subsidy_amount': 'Subsidy Amount',
      'sugarcane': 'ਗੰਨਾ',
      'sugarcane_sub': 'Annual commercial cash crop',
      'survey_number': 'Survey Number',
      'symptoms_observed': 'Symptoms Observed',
      'taluk': 'Taluk',
      'tap_to_speak_area': 'Tap to speak your farm size',
      'tap_to_speak_crop': 'Tap to speak your crop',
      'tap_to_speak_stage': 'Tap to speak current stage',
      'target_beneficiaries': 'Target Beneficiaries',
      'tell_about_farm': 'ਆਪਣੇ ਖੇਤ ਬਾਰੇ ਦੱਸੋ',
      'timeline_header': 'Farm Activity Journey',
      'timeline_header_desc': 'Verified chronological timeline of all farm actions, diagnostics, and approvals.',
      'timeline_title': 'ਮੇਰਾ ਖੇਤੀ ਸਫ਼ਰ',
      'todays_farm_brief': 'ਅੱਜ ਦੀ ਸਲਾਹ',
      'total_area': 'Total Area',
      'track_progress': 'Track Progress',
      'treatment_response': 'Treatment Response',
      'type_problem_hint': 'e.g. Paddy leaves turning yellow with brown spots...',
      'unable_load_health': 'Unable to Load Health Data',
      'unable_load_timeline': 'Unable to Load Timeline',
      'upload_crop_photo': 'Upload Crop Photo',
      'vegetative': 'ਬਨਸਪਤੀ ਵਾਧਾ',
      'vegetative_sub': 'Tillering & vegetative shoot growth',
      'verify_land_desc': 'Verify your land for govt schemes',
      'verify_land_now': 'Verify Land Now',
      'view_advice': 'View Advice',
      'view_all': 'View All',
      'view_details': 'View Details',
      'view_health_journey': 'View Health Journey Timeline',
      'view_scheme_details': 'View Scheme Details',
      'village': 'Village',
      'voice_assistant': 'Voice Assistant',
      'what_problem_seeing': 'What problem are you seeing?',
      'what_would_you_like_to_do': 'What would you like to do?',
      'your_farm_profile': 'Your Farm Profile',
    },
  };

  /// Returns translated string by key with english fallback
  String text(String key) {
    final langDict = _localizedValues[langCode] ?? _localizedValues['en-IN']!;
    if (langDict.containsKey(key)) {
      return langDict[key]!;
    }
    final enDict = _localizedValues['en-IN']!;
    return enDict[key] ?? key;
  }

  /// Alias for text(key)
  String get(String key) => text(key);
  String operator [](String key) => text(key);

  /// Helper translation methods
  String translateCrop(String cropId) {
    switch (cropId.toLowerCase()) {
      case 'samba_paddy':
        return text('samba_paddy');
      case 'kuruvai_paddy':
        return text('kuruvai_paddy');
      case 'sugarcane':
        return text('sugarcane');
      case 'cotton':
        return text('cotton');
      case 'banana':
        return text('banana');
      case 'maize':
        return text('maize');
      default:
        return cropId;
    }
  }

  String translateStage(String stageId) {
    switch (stageId.toLowerCase()) {
      case 'vegetative':
        return text('vegetative');
      case 'flowering':
        return text('flowering');
      case 'grain_filling':
        return text('grain_filling');
      case 'maturity':
        return text('maturity');
      case 'harvest_ready':
        return text('harvest_ready');
      default:
        return stageId;
    }
  }

  String translateHealthBand(String band) {
    switch (band.toLowerCase()) {
      case 'good':
      case 'excellent':
        return langCode.startsWith('ta') ? 'நல்ல ஆரோக்கியம்' : langCode.startsWith('hi') ? 'अच्छा स्वास्थ्य' : 'Good Health';
      case 'moderate':
      case 'fair':
        return langCode.startsWith('ta') ? 'மிதமான ஆரோக்கியம்' : langCode.startsWith('hi') ? 'मध्यम स्वास्थ्य' : 'Moderate Health';
      case 'poor':
      case 'critical':
        return langCode.startsWith('ta') ? 'கவனம் தேவை' : langCode.startsWith('hi') ? 'ध्यान आवश्यक' : 'Needs Attention';
      case 'unrated':
      default:
        return text('health_unrated');
    }
  }

  String translateLandStatus(String status) {
    switch (status.toLowerCase()) {
      case 'verified':
        return langCode.startsWith('ta') ? 'சரிபார்க்கப்பட்ட நிலம்' : langCode.startsWith('hi') ? 'सत्यापित भूमि' : 'Verified Land';
      case 'pending':
        return langCode.startsWith('ta') ? 'சரிபார்ப்பு நிலுவையில்' : langCode.startsWith('hi') ? 'सत्यापन लंबित' : 'Pending Verification';
      case 'unverified':
      default:
        return langCode.startsWith('ta') ? 'சரிபார்க்கப்படாத நிலம்' : langCode.startsWith('hi') ? 'असत्यापित भूमि' : 'Unverified Land';
    }
  }

  String translateSubIndex(String name) {
    switch (name.toLowerCase()) {
      case 'environmental suitability':
      case 'environmentalsuitability':
        return text('env_suitability');
      case 'resource adequacy':
      case 'resourceadequacy':
        return text('resource_adequacy');
      case 'crop stage progression':
      case 'cropstageprogression':
        return text('crop_stage_prog');
      case 'active problem load':
      case 'activeproblemload':
        return text('active_problem_load');
      case 'monitoring recency':
      case 'monitoringrecency':
        return text('monitoring_recency');
      case 'treatment response':
      case 'treatmentresponse':
        return text('treatment_response');
      default:
        return name;
    }
  }

  String translateTimelineTitle(String title) {
    final lower = title.toLowerCase();
    if (lower.contains('profile created') || lower.contains('farm profile')) {
      return langCode.startsWith('ta') ? 'பண்ணை விவரக்குறிப்பு உருவாக்கப்பட்டது' : langCode.startsWith('hi') ? 'खेत प्रोफ़ाइल बनाई गई' : 'Farm Profile Created';
    }
    if (lower.contains('boundary verified') || lower.contains('cadastral')) {
      return langCode.startsWith('ta') ? 'நில எல்லை சரிபார்க்கப்பட்டது' : langCode.startsWith('hi') ? 'भूमि सीमा सत्यापित' : 'Cadastral Boundary Verified';
    }
    if (lower.contains('blight') || lower.contains('bacterial') || lower.contains('disease') || lower.contains('advisory')) {
      return langCode.startsWith('ta') ? 'பயிர்ப் பாதுகாப்பு & நோய் ஆலோசனை' : langCode.startsWith('hi') ? 'फसल सुरक्षा एवं रोग सलाह' : title;
    }
    return title;
  }

  String translateTimelineSummary(String summary) {
    final lower = summary.toLowerCase();
    if (lower.contains('registered') && lower.contains('samba')) {
      return langCode.startsWith('ta') ? 'ஈரோடு மாவட்டத்தில் 2.0 ஏக்கர் சம்பா நெல் பதிவு செய்யப்பட்டது.' : langCode.startsWith('hi') ? 'इरोड जिले में 2.0 एकड़ सांभा धान पंजीकृत।' : summary;
    }
    if (lower.contains('fmb') || lower.contains('revenue parcel')) {
      return langCode.startsWith('ta') ? 'அரசு நில வருவாய் வரைபடம் FMB 2.0 ஏக்கருடன் ஒத்துப்போனது.' : langCode.startsWith('hi') ? 'आधिकारिक राजस्व पार्सल FMB 2.0 एकड़ से मेल खाता है।' : summary;
    }
    if (lower.contains('bio-control') || lower.contains('drainage')) {
      return langCode.startsWith('ta') ? 'உயிரியல் கட்டுப்பாட்டு சிகிச்சை மற்றும் வடிகால் வழிகாட்டுதல் வழங்கப்பட்டது.' : langCode.startsWith('hi') ? 'जैव-नियंत्रण उपचार और जल निकासी सलाह जारी की गई।' : summary;
    }
    return summary;
  }

  String translateSoilType(String soilType) {
    switch (soilType.toLowerCase()) {
      case 'clay_loam':
        return langCode.startsWith('ta') ? 'களிமண் படிவு' : 'Clay Loam';
      case 'alluvial':
        return langCode.startsWith('ta') ? 'வண்டல் மண்' : 'Alluvial Soil';
      case 'black_cotton':
        return langCode.startsWith('ta') ? 'கரிசல் மண்' : 'Black Soil';
      case 'red_loam':
        return langCode.startsWith('ta') ? 'செம்மண்' : 'Red Loam';
      default:
        return soilType;
    }
  }

  String translateIrrigation(String irrigation) {
    switch (irrigation.toLowerCase()) {
      case 'canal':
        return langCode.startsWith('ta') ? 'கால்வாய் பாசனம்' : 'Canal Water';
      case 'borewell':
        return langCode.startsWith('ta') ? 'ஆழ்துளை கிணறு' : 'Borewell';
      case 'drip':
        return langCode.startsWith('ta') ? 'சொட்டு நீர்' : 'Drip Irrigation';
      case 'rainfed':
        return langCode.startsWith('ta') ? 'மானாவாரி' : 'Rainfed';
      default:
        return irrigation;
    }
  }

  String translateSeason(String season) {
    switch (season.toLowerCase()) {
      case 'samba':
        return langCode.startsWith('ta') ? 'சம்பா பருவம்' : 'Samba Season';
      case 'kuruvai':
        return langCode.startsWith('ta') ? 'குறுவை பருவம்' : 'Kuruvai Season';
      case 'thaladi':
        return langCode.startsWith('ta') ? 'தாளடி பருவம்' : 'Thaladi Season';
      case 'kharif':
        return langCode.startsWith('hi') ? 'खरीफ' : 'Kharif';
      case 'rabi':
        return langCode.startsWith('hi') ? 'रबी' : 'Rabi';
      default:
        return season;
    }
  }

  // Common getters
  String get appTitle => text('app_title');
  String get appSubtitle => langCode.startsWith('ta') ? 'விவசாயிகளுக்கான AI தோழன்' : langCode.startsWith('hi') ? 'किसानों का AI साथी' : 'AI-Powered Farmer Companion';
  String get getStarted => text('get_started');
  String get welcomeDesc => text('brand_desc');
  String get welcomeTagline => 'Your Farm.\nOur Intelligence.';
  String get chooseLanguageTitle => text('choose_language');
  String get chooseLanguageDesc => langCode.startsWith('ta') ? 'பூமி உங்கள் மொழியில் பேசி, வழிகாட்டும்.' : langCode.startsWith('hi') ? 'भूमि आपकी भाषा में बात करेगी और मार्गदर्शन करेगी।' : 'BHOOMI will speak and advise in your language.';
  String get onboardingTitle => text('your_farm_profile');
  String get letsGetToKnow => text('tell_about_farm');
  String get youCanSpeak => langCode.startsWith('ta') ? 'உங்கள் மொழியில் பேசலாம்' : langCode.startsWith('hi') ? 'आप अपनी भाषा में बोल सकते हैं' : 'You can speak in your language';
  String get cropVoicePrompt => text('tap_to_speak_crop');
  String get areaVoicePrompt => text('tap_to_speak_area');
  String get growthVoicePrompt => text('tap_to_speak_stage');
  String get quickSelectOptions => text('quick_selection');
  String get selectFarmAreaTitle => text('select_farm_area');
  String get selectGrowthStageTitle => text('select_stage');
  String get nextStep => text('continue');
  String get back => text('back');
  String get save => text('save');
  String get cancel => text('cancel');
  String get edit => text('edit');
  String get retry => text('retry');
  String get reviewProfile => text('confirm_farm_title');
  String get whatWouldYouLikeToDo => text('what_would_you_like_to_do');
  String get askBhoomi => text('ask_bhoomi');
  String get voiceAssistant => text('voice_assistant');
  String get uploadCropPhoto => text('upload_crop_photo');
  String get myFarmJourney => text('my_farm_journey');
  String get activityTimeline => text('activity_timeline');
  String get govSupport => text('govt_support');
  String get schemesAndSubsidies => text('schemes_subsidies');
  String get requiresVerifiedLand => text('requires_verified_land');
  String get cropLabel => text('crop_label');
  String get growthStageLabel => text('growth_stage_label');
  String get landAreaLabel => text('land_area_label');
  String get continueButton => text('continue');
  String get hackathonBadge => 'Smart India Hackathon SIH25076';
  String get changeLanguage => langCode.startsWith('ta') ? 'மொழி மாற்று' : langCode.startsWith('hi') ? 'भाषा बदलें' : 'Change Language';
  String get latestUpdates => text('latest_update');
  String get navHome => langCode.startsWith('ta') ? 'முகப்பு' : langCode.startsWith('hi') ? 'होम' : 'Home';
  String get navCompanion => langCode.startsWith('ta') ? 'தோழன்' : langCode.startsWith('hi') ? 'साथी' : 'Companion';
  String get navJourney => langCode.startsWith('ta') ? 'பயணம்' : langCode.startsWith('hi') ? 'सफ़र' : 'Journey';
  String get navProfile => langCode.startsWith('ta') ? 'விவரக்குறிப்பு' : langCode.startsWith('hi') ? 'प्रोफ़ाइल' : 'Profile';
  String get dailyCompanion => text('daily_companion');
  String get myFarm => text('my_farm');
  String get primaryCropLabel => text('primary_crop');
  String get todaysFarmBrief => text('todays_farm_brief');
  String get viewFullBrief => text('view_details');
  String get viewAllUpdates => text('view_all');
  String get yourFarmProfile => text('your_farm_profile');
  String get areaStepTitle => text('step_area_title');
  String get areaStepSub => text('step_area_sub');
  String get growthStepTitle => text('step_stage_title');
  String get growthStepSub => text('step_stage_sub');

  String cropName(String cropId) => translateCrop(cropId);
  String cropSubtitle(String cropId) {
    switch (cropId.toLowerCase()) {
      case 'samba_paddy':
        return text('samba_paddy_sub');
      case 'kuruvai_paddy':
        return text('kuruvai_paddy_sub');
      case 'sugarcane':
        return text('sugarcane_sub');
      case 'cotton':
        return text('cotton_sub');
      case 'banana':
        return text('banana_sub');
      case 'maize':
        return text('maize_sub');
      default:
        return '';
    }
  }

  String stageName(String stageId) => translateStage(stageId);
  String stageSubtitle(String stageId) {
    switch (stageId.toLowerCase()) {
      case 'vegetative':
        return text('vegetative_sub');
      case 'flowering':
        return text('flowering_sub');
      case 'grain_filling':
        return text('grain_filling_sub');
      case 'maturity':
        return text('maturity_sub');
      case 'harvest_ready':
        return text('harvest_ready_sub');
      default:
        return '';
    }
  }

  String get regionStepTitle => langCode.startsWith('ta') ? 'உங்கள் மாவட்டம் எது?' : langCode.startsWith('hi') ? 'आपका जिला कौन सा है?' : 'Select Your Region';
  String get regionStepSub => langCode.startsWith('ta') ? 'வட்டார வேளாண் வானிலை' : langCode.startsWith('hi') ? 'स्थानीय कृषि मौसम' : 'Localized agro-climatic advisories';
  String get regionVoicePrompt => langCode.startsWith('ta') ? 'மாவட்டத்தை பேச தட்டவும்' : langCode.startsWith('hi') ? 'जिला बोलने के लिए टैप करें' : 'Tap to speak your region';
  String get selectRegionTitle => langCode.startsWith('ta') ? 'மாவட்டத்தைத் தேர்ந்தெடுக்கவும்' : langCode.startsWith('hi') ? 'जिला चुनें' : 'Select Region / District';

  String regionName(String regionId) {
    switch (regionId.toLowerCase()) {
      case 'coimbatore':
      case 'tn_coimbatore':
        return langCode.startsWith('ta') ? 'கோயம்புத்தூர்' : langCode.startsWith('hi') ? 'कोयंबटूर' : 'Coimbatore';
      case 'thanjavur':
      case 'tn_thanjavur':
        return langCode.startsWith('ta') ? 'தஞ்சாவூர்' : langCode.startsWith('hi') ? 'तंजावुर' : 'Thanjavur (Cauvery Delta)';
      case 'madurai':
      case 'tn_madurai':
        return langCode.startsWith('ta') ? 'மதுரை' : langCode.startsWith('hi') ? 'मदुरै' : 'Madurai';
      default:
        return regionId.replaceAll('_', ' ');
    }
  }

  String regionSubtitle(String regionId) {
    switch (regionId.toLowerCase()) {
      case 'coimbatore':
      case 'tn_coimbatore':
        return langCode.startsWith('ta') ? 'மேற்கு மண்டலம் - பருத்தி & மக்காச்சோளம்' : 'Western Agro-Zone';
      case 'thanjavur':
      case 'tn_thanjavur':
        return langCode.startsWith('ta') ? 'காவிரி டெல்டா - சம்பா நெல்' : 'Cauvery Delta Basin';
      case 'madurai':
      case 'tn_madurai':
        return langCode.startsWith('ta') ? 'தெற்கு மண்டலம்' : 'Southern Agro-Zone';
      default:
        return '';
    }
  }

  String formatAcres(double acres) {
    if (acres == 0.5) return '0.5 ${text('acres')}';
    if (acres == 1.0) return '1.0 ${text('acres')}';
    if (acres == 2.0) return '2.0 ${text('acres')}';
    if (acres == 2.5) return '2.5 ${text('acres')}';
    if (acres == 3.5) return '3.5 ${text('acres')}';
    if (acres == 5.0) return '5.0 ${text('acres')}';
    if (acres == 10.0) return '10.0 ${text('acres')}';
    return '$acres ${text('acres')}';
  }
}

/// Alias typedef so both BhoomiStrings and AppTranslations work interchangeably
typedef BhoomiStrings = AppTranslations;
