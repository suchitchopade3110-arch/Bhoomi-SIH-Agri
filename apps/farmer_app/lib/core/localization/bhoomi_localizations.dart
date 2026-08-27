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
      'no_schemes_found': 'உங்கள் பயிர் மற்றும் மாவட்டத்திற்கு தற்போது புதிய திட்டங்கள் எதுவும் பொருந்தவில்லை.',
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
      'show_image': 'படத்தைக் காட்டு',
      'todays_guidance': 'இன்றைய வழிகாட்டல்',
      'weather_field_advice': 'வானிலை & வயல் ஆலோசனை',
      'farm_health': 'பண்ணை ஆரோக்கியம்',
      'score_diagnosis': 'மதிப்பெண் & நோய் கண்டறிதல்',
      'ask_bhoomi_sub': 'உங்கள் மொழியில் எந்த கேள்வியையும் கேளுங்கள்',
      'tap_to_ask_bhoomi': 'பூமியிடம் கேட்க தட்டவும்',
      'recording_tap_to_send': 'பதிவாகிறது... அனுப்ப தட்டவும்',
      'uploading_audio': 'ஆடியோ பதிவேற்றப்படுகிறது...',
      'transcribing_speech': 'பேச்சு உரையாக மாற்றப்படுகிறது...',
      'you_can_ask_about': 'நீங்கள் கேட்கக்கூடிய தலைப்புகள்:',
      'topic_crops': 'பயிர்கள்',
      'topic_diseases': 'நோய்கள்',
      'topic_pests': 'பூச்சிகள்',
      'topic_soil': 'மண்',
      'topic_weather': 'வானிலை',
      'topic_prices': 'சந்தை விலை',
      'topic_schemes': 'திட்டங்கள்',
      'show_to_bhoomi': 'பூமிக்குக் காட்டுங்கள்',
      'upload_or_take_photo': 'புகைப்படத்தை எடுக்கவும் அல்லது பதிவேற்றவும்',
      'attached': 'இணைக்கப்பட்டது',
      'no_image_selected': 'புகைப்படம் எதுவும் தேர்ந்தெடுக்கப்படவில்லை',
      'camera': 'கேமரா',
      'gallery': 'கேலரி',
      'ai_crop_assist_hint': 'AI பயிர் பிரச்சனையை கண்டறிந்து வழிகாட்டும்.',
      'additional_context_optional': 'கூடுதல் விவரங்கள் (விருப்பத்திற்குரியது)',
      'photo_required_hint': 'பயிரின் புகைப்படம் அவசியம் — மேலே படம் எடுத்து பதிவேற்றவும்.',
      'bhoomi_intelligence': 'பூமி வேளாண் நுண்ணறிவு',
      'processing_query': 'உங்கள் கேள்வியை ஆய்வு செய்கிறது...',
      'analyzing_farm': 'உங்கள் பண்ணையை ஆய்வு செய்கிறது...',
      'review_required': 'நிபுணர் ஆய்வு தேவை',
      'expert_verification_required': 'நிபுணர் சரிபார்ப்பு தேவைப்படுகிறது',
      'below_confidence_gate_desc': 'துல்லியத்தன்மை பாதுகாப்பு வரம்பை விட குறைவாக உள்ளது. பாதுகாப்பான ஆலோசனைக்காக இந்த வழக்கு வேளாண் நிபுணர் ஆய்வுக்கு அனுப்பப்படுகிறது.',
      'escalate_to_kvk': 'KVK வேளாண் நிபுணரிடம் அனுப்பவும்',
      'return_to_farm_home': 'பண்ணை முகப்பிற்குச் செல்',
      'listen_to_advisory': 'ஆலோசனையைக் கேளுங்கள்',
      'stop_audio': 'ஆடியோவை நிறுத்து',
      'listen_to_brief': 'வழிகாட்டலைக் கேளுங்கள்',
      'refresh_guidance': 'வழிகாட்டலை புதுப்பி',
      'generating_guidance': 'இன்றைய வயல் வழிகாட்டல் தயாராகிறது...',
      'todays_tasks': 'இன்றைய பண்ணை பணிகள்',
      'task_completed': 'முடிந்தது',
      'wind': 'காற்று',
      'rain_risk': 'மழை வாய்ப்பு',
      'action_plan': 'செயல் திட்டம்',
      'immediate_steps': 'பரிந்துரைக்கப்பட்ட உடனடி மேலாண்மை நடவடிக்கைகள்:',
      'why_need_expert': 'ஏன் நிபுணர் உதவி தேவைப்படுகிறது? (விருப்பத்திற்குரியது)',
      'how_is_it_now': 'இப்போது பாதிப்பு எப்படி உள்ளது?',
      'followup_question': 'ஆலோசனையைப் பின்பற்றிய பிறகு பிரச்சனை சீரடைந்துள்ளதா?',
      'improved': 'சீரடைந்துள்ளது',
      'improved_desc': 'மஞ்சள் நிறம் குறைந்து, புதிய ஆரோக்கியமான இலைகள் வளர்கின்றன',
      'no_change': 'மாற்றமில்லை',
      'no_change_desc': 'அறிகுறிகள் அதே நிலையில் தொடர்கின்றன',
      'got_worse': 'அதிகரித்துள்ளது',
      'got_worse_desc': 'பாதிப்பு மற்ற தளிர்களுக்கும் வேகமாக பரவுகிறது',
      'upload_new_photo': 'புதிய புகைப்படத்தை பதிவேற்றவும் (விருப்பத்திற்குரியது)',
      'submit_to_kvk': 'KVK வேளாண் நிபுணரிடம் சமர்ப்பிக்கவும்',
      'expert_case_summary': 'நிபுணர் வழக்கு விவரம்',
      'case_transferred': 'வழக்கு மாற்றப்பட்டது',
      'expert_notified': 'நிபுணருக்கு அறிவிக்கப்பட்டது',
      'review_in_progress': 'ஆய்வு நடைபெறுகிறது',
      'assigned_kvk': 'ஒதுக்கப்பட்ட KVK மையம்',
      'estimated_review': 'மதிப்பிடப்பட்ட ஆய்வு நேரம்',
      'farmer': 'விவசாயி',
      'location': 'இடம்',
      'case_identifier': 'வழக்கு எண்',
      'summary': 'சுருக்கம்',
      'expert_note': 'நிபுணர் குறிப்பு',
      'verified_by_land': 'நில ஆவணத்தால் சரிபார்க்கப்பட்டது',
      'action_required': 'நடவடிக்கை தேவை',
      'check_eligibility': 'தகுதியை சரிபார்க்கவும்',
      'eligible': 'தகுதியானது',
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
      'no_schemes_found': 'आपकी फसल और स्थान के लिए वर्तमान में कोई सरकारी योजनाएं उपलब्ध नहीं हैं।',
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
      'show_image': 'तस्वीर दिखाएं',
      'todays_guidance': 'आज का मार्गदर्शन',
      'weather_field_advice': 'मौसम और खेत सलाह',
      'farm_health': 'खेत स्वास्थ्य',
      'score_diagnosis': 'स्कोर और रोग निदान',
      'ask_bhoomi_sub': 'अपनी भाषा में कोई भी प्रश्न पूछें',
      'tap_to_ask_bhoomi': 'भूमि से पूछने के लिए टैप करें',
      'recording_tap_to_send': 'रिकॉर्डिंग जारी... भेजने के लिए टैप करें',
      'uploading_audio': 'ऑडियो अपलोड हो रहा है...',
      'transcribing_speech': 'आवाज को टेक्स्ट में बदला जा रहा है...',
      'you_can_ask_about': 'आप इनके बारे में पूछ सकते हैं:',
      'topic_crops': 'फसलें',
      'topic_diseases': 'रोग',
      'topic_pests': 'कीट',
      'topic_soil': 'मिट्टी',
      'topic_weather': 'मौसम',
      'topic_prices': 'मंडी भाव',
      'topic_schemes': 'योजनाएं',
      'show_to_bhoomi': 'भूमि को दिखाएं',
      'upload_or_take_photo': 'फोटो अपलोड करें या खींचें',
      'attached': 'संलग्न',
      'no_image_selected': 'कोई फोटो चयनित नहीं है',
      'camera': 'कैमरा',
      'gallery': 'गैलरी',
      'ai_crop_assist_hint': 'AI समस्या की पहचान कर आपका मार्गदर्शन करेगा।',
      'additional_context_optional': 'अतिरिक्त संदर्भ (वैकल्पिक)',
      'photo_required_hint': 'फोटो आवश्यक है — निदान के लिए ऊपर फोटो लें या चुनें।',
      'bhoomi_intelligence': 'भूमि कृषि बुद्धिमत्ता',
      'processing_query': 'आपके प्रश्न का विश्लेषण हो रहा है...',
      'analyzing_farm': 'आपके खेत का विश्लेषण हो रहा है...',
      'review_required': 'समीक्षा आवश्यक है',
      'expert_verification_required': 'विशेषज्ञ सत्यापन आवश्यक है',
      'below_confidence_gate_desc': 'निदान सटीकता सुरक्षा सीमा से कम है। सुरक्षित और सटीक मार्गदर्शन सुनिश्चित करने के लिए यह मामला विशेषज्ञ समीक्षा के लिए तैयार किया गया है।',
      'escalate_to_kvk': 'केवीके कृषि विशेषज्ञ को भेजें',
      'return_to_farm_home': 'खेत होम पर लौटें',
      'listen_to_advisory': 'सलाह सुनें',
      'stop_audio': 'ऑडियो रोकें',
      'listen_to_brief': 'सलाह सुनें',
      'refresh_guidance': 'मार्गदर्शन ताज़ा करें',
      'generating_guidance': 'आज का खेत मार्गदर्शन तैयार हो रहा है...',
      'todays_tasks': 'आज के खेत कार्य',
      'task_completed': 'पूर्ण हुआ',
      'wind': 'हवा',
      'rain_risk': 'बारिश का जोखिम',
      'action_plan': 'कार्य योजना',
      'immediate_steps': 'अनुशंसित तत्काल कृषि प्रबंधन कदम:',
      'why_need_expert': 'आपको विशेषज्ञ सहायता की आवश्यकता क्यों है? (वैकल्पिक)',
      'how_is_it_now': 'अब स्थिति कैसी है?',
      'followup_question': 'सलाह का पालन करने के बाद क्या समस्या में सुधार हुआ है?',
      'improved': 'सुधार हुआ',
      'improved_desc': 'पीलापन रुक गया है, नए स्वस्थ पत्ते निकल रहे हैं',
      'no_change': 'कोई बदलाव नहीं',
      'no_change_desc': 'लक्षण उसी स्तर पर दिखाई दे रहे हैं',
      'got_worse': 'स्थिति बिगड़ी है',
      'got_worse_desc': 'घाव बढ़ रहे हैं या आसपास के कल्लों में फैल रहे हैं',
      'upload_new_photo': 'नई फोटो अपलोड करें (वैकल्पिक)',
      'submit_to_kvk': 'केवीके कृषि विशेषज्ञ को सबमिट करें',
      'expert_case_summary': 'विशेषज्ञ केस सारांश',
      'case_transferred': 'केस स्थानांतरित',
      'expert_notified': 'विशेषज्ञ को सूचित किया गया',
      'review_in_progress': 'समीक्षा जारी है',
      'assigned_kvk': 'आवंटित केवीके केंद्र',
      'estimated_review': 'अनुमानित समीक्षा समय',
      'farmer': 'किसान',
      'location': 'स्थान',
      'case_identifier': 'केस पहचानकर्ता',
      'summary': 'सारांश',
      'expert_note': 'विशेषज्ञ नोट',
      'verified_by_land': 'भूमि रिकॉर्ड द्वारा सत्यापित',
      'action_required': 'कार्रवाई आवश्यक',
      'check_eligibility': 'पात्रता जांचें',
      'eligible': 'पात्र',
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
      'no_schemes_found': 'No government schemes currently match your specific crop and location.',
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
      'show_image': 'Show Image',
      'todays_guidance': "Today's Guidance",
      'weather_field_advice': 'Weather & field advice',
      'farm_health': 'Farm Health',
      'score_diagnosis': 'Score & diagnosis',
      'ask_bhoomi_sub': 'Tap and ask any question in your language',
      'tap_to_ask_bhoomi': 'Tap to Ask BHOOMI',
      'recording_tap_to_send': 'Recording... Tap to send',
      'uploading_audio': 'Uploading audio...',
      'transcribing_speech': 'Transcribing speech...',
      'you_can_ask_about': 'You can ask about:',
      'topic_crops': 'Crops',
      'topic_diseases': 'Diseases',
      'topic_pests': 'Pests',
      'topic_soil': 'Soil',
      'topic_weather': 'Weather',
      'topic_prices': 'Prices',
      'topic_schemes': 'Schemes',
      'show_to_bhoomi': 'Show to BHOOMI',
      'upload_or_take_photo': 'Upload or take a photo',
      'attached': 'Attached',
      'no_image_selected': 'No image selected yet',
      'camera': 'Camera',
      'gallery': 'Gallery',
      'ai_crop_assist_hint': 'AI will identify the issue and guide you.',
      'additional_context_optional': 'Additional Context (optional)',
      'photo_required_hint': 'A photo is required — take or select one above to diagnose.',
      'bhoomi_intelligence': 'BHOOMI Intelligence',
      'processing_query': 'Processing Your Query',
      'analyzing_farm': 'Analyzing your farm...',
      'review_required': 'Review Required',
      'expert_verification_required': 'Expert Verification Required',
      'below_confidence_gate_desc': 'The diagnosis confidence is below the safety threshold. To ensure safe and accurate guidance, this case has been prepared for expert review.',
      'escalate_to_kvk': 'Escalate to KVK Agronomist',
      'return_to_farm_home': 'Return to Farm Home',
      'listen_to_advisory': 'Listen to Advisory',
      'stop_audio': 'Stop Audio',
      'listen_to_brief': 'Listen to Brief',
      'refresh_guidance': 'Refresh Guidance',
      'generating_guidance': 'Generating today\'s field guidance...',
      'todays_tasks': 'Today\'s Farm Tasks',
      'task_completed': 'done',
      'wind': 'Wind',
      'rain_risk': 'Rain Risk',
      'action_plan': 'Action Plan',
      'immediate_steps': 'Recommended immediate agronomic management steps:',
      'why_need_expert': 'Why do you need expert help? (Optional)',
      'how_is_it_now': 'How is it now?',
      'followup_question': 'Has the problem improved after following the advice?',
      'improved': 'Improved',
      'improved_desc': 'Yellowing stopped, new healthy leaves emerging',
      'no_change': 'No Change',
      'no_change_desc': 'Symptoms remain visible at the same level',
      'got_worse': 'Got Worse',
      'got_worse_desc': 'Lesions expanding or spreading to adjacent tillers',
      'upload_new_photo': 'Upload new photo (Optional)',
      'submit_to_kvk': 'Submit to KVK Agronomist',
      'expert_case_summary': 'Expert Case Summary',
      'case_transferred': 'Case transferred',
      'expert_notified': 'Expert notified',
      'review_in_progress': 'Review in progress',
      'assigned_kvk': 'Assigned KVK Center',
      'estimated_review': 'Estimated Review',
      'farmer': 'Farmer',
      'location': 'Location',
      'case_identifier': 'Case Identifier',
      'summary': 'Summary',
      'expert_note': 'Expert Note',
      'verified_by_land': 'Verified by Land Record',
      'action_required': 'Action required',
      'check_eligibility': 'Check Eligibility',
      'eligible': 'Eligible',
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
      'no_schemes_found': 'మీ పంట మరియు ప్రాంతానికి ప్రస్తుతం ప్రభుత్వ పథకాలు అందుబాటులో లేవు.',
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
      'what_would_you_like_to_do': 'మీరు ఏమి చేయాలనుకుంటున్నారు?',
      'your_farm_profile': 'మీ వ్యవసాయ వివరాలు',
      'show_image': 'చిత్రాన్ని చూపించు',
      'todays_guidance': 'నేటి మార్గదర్శకత్వం',
      'weather_field_advice': 'వాతావరణ & పొలం సలహా',
      'farm_health': 'వ్యవసాయ ఆరోగ్యం',
      'score_diagnosis': 'స్కోరు & రోగ నిర్ధారణ',
      'ask_bhoomi_sub': 'మీ భాషలో ఏదైనా ప్రశ్న అడగండి',
      'tap_to_ask_bhoomi': 'భూమిని అడగడానికి నొక్కండి',
      'recording_tap_to_send': 'రికార్డింగ్ అవుతోంది... పంపడానికి నొక్కండి',
      'uploading_audio': 'ఆడియో అప్‌లోడ్ అవుతోంది...',
      'transcribing_speech': 'మాటలను వచనంగా మారుస్తోంది...',
      'you_can_ask_about': 'మీరు అడగగల అంశాలు:',
      'topic_crops': 'పంటలు',
      'topic_diseases': 'వ్యాధులు',
      'topic_pests': 'పురుగులు',
      'topic_soil': 'నేల',
      'topic_weather': 'వాతావరణం',
      'topic_prices': 'మార్కెట్ ధరలు',
      'topic_schemes': 'పథకాలు',
      'show_to_bhoomi': 'భూమికి చూపించండి',
      'upload_or_take_photo': 'ఫోటో తీయండి లేదా అప్‌లోడ్ చేయండి',
      'attached': 'జతచేయబడింది',
      'no_image_selected': 'ఫోటో ఏదీ ఎంచుకోలేదు',
      'camera': 'కెమెరా',
      'gallery': 'గ్యాలరీ',
      'ai_crop_assist_hint': 'AI సమస్యను గుర్తించి మార్గనిర్దేశం చేస్తుంది.',
      'additional_context_optional': 'అదనపు వివరాలు (ఐచ్ఛికం)',
      'photo_required_hint': 'పంట ఫోటో తప్పనిసరి — పైన ఫోటో తీయండి.',
      'bhoomi_intelligence': 'భూమి వ్యవసాయ మేధస్సు',
      'processing_query': 'మీ ప్రశ్నను విశ్లేషిస్తోంది...',
      'analyzing_farm': 'మీ పొలాన్ని విశ్లేషిస్తోంది...',
      'review_required': 'నిపుణుల సమీక్ష అవసరం',
      'expert_verification_required': 'నిపుణుల ధృవీకరణ అవసరం',
      'below_confidence_gate_desc': 'ఖచ్చితత్వ భద్రతా పరిమితి కంటే తక్కువగా ఉంది. సురక్షిత సలహా కోసం వ్యవసాయ నిపుణులకు పంపబడుతోంది.',
      'escalate_to_kvk': 'KVK వ్యవసాయ నిపుణుడికి పంపండి',
      'return_to_farm_home': 'వ్యవసాయ ముఖపు పేజీకి వెళ్లండి',
      'listen_to_advisory': 'సలహాను వినండి',
      'stop_audio': 'ఆడియో ఆపండి',
      'listen_to_brief': 'సారాంశాన్ని వినండి',
      'refresh_guidance': 'మార్గదర్శకత్వాన్ని రిఫ్రెష్ చేయండి',
      'generating_guidance': 'నేటి పొలం మార్గదర్శకత్వం సిద్ధమవుతోంది...',
      'todays_tasks': 'నేటి వ్యవసాయ పనులు',
      'task_completed': 'పూర్తయింది',
      'wind': 'గాలి',
      'rain_risk': 'వర్షం ముప్పు',
      'action_plan': 'కార్యాచరణ ప్రణాళిక',
      'immediate_steps': 'సిఫార్సు చేసిన తక్షణ చర్యలు:',
      'why_need_expert': 'నిపుణుల సహాయం ఎందుకు అవసరం? (ఐచ్ఛికం)',
      'how_is_it_now': 'ఇప్పుడు పరిస్థితి ఎలా ఉంది?',
      'followup_question': 'సలహాను పాటించిన తర్వాత సమస్య తగ్గిందా?',
      'improved': 'మెరుగుపడింది',
      'improved_desc': 'పసుపు రంగు తగ్గి, కొత్త ఆరోగ్యకరమైన ఆకులు వస్తున్నాయి',
      'no_change': 'మార్పు లేదు',
      'no_change_desc': 'లక్షణాలు అలాగే కొనసాగుతున్నాయి',
      'got_worse': 'మరింత తీవ్రమైంది',
      'got_worse_desc': 'నష్టం ఇతర మొక్కలకు వేగంగా విస్తరిస్తోంది',
      'upload_new_photo': 'కొత్త ఫోటో అప్‌లోడ్ చేయండి (ఐచ్ఛికం)',
      'submit_to_kvk': 'KVK వ్యవసాయ నిపుణుడికి సమర్పించండి',
      'expert_case_summary': 'నిపుణుల కేసు సారాంశం',
      'case_transferred': 'కేసు బదిలీ చేయబడింది',
      'expert_notified': 'నిపుణుడికి తెలియజేయబడింది',
      'review_in_progress': 'సమీక్ష జరుగుతోంది',
      'assigned_kvk': 'కేటాయించిన KVK కేంద్రం',
      'estimated_review': 'అంచనా వేసిన సమీక్ష సమయం',
      'farmer': 'రైతు',
      'location': 'ప్రాంతం',
      'case_identifier': 'కేసు సంఖ్య',
      'summary': 'సారాంశం',
      'expert_note': 'నిపుణుల గమనిక',
      'verified_by_land': 'భూ రికార్డు ద్వారా ధృవీకరించబడింది',
      'action_required': 'చర్య అవసరం',
      'check_eligibility': 'అర్హతను తనిఖీ చేయండి',
      'eligible': 'అర్హులు',
      'diagnose_get_advice': 'రోగ నిర్ధారణ చేసి సలహా పొందండి',
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
      'no_schemes_found': 'ನಿಮ್ಮ ಬೆಳೆ ಮತ್ತು ಸ್ಥಳಕ್ಕೆ ಪ್ರಸ್ತುತ ಯಾವುದೇ ಸರ್ಕಾರಿ ಯೋಜನೆಗಳು ಲಭ್ಯವಿಲ್ಲ.',
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
      'what_would_you_like_to_do': 'ನೀವು ಏನು ಮಾಡಲು ಬಯಸುತ್ತೀರಿ?',
      'your_farm_profile': 'ನಿಮ್ಮ ಕೃಷಿ ವಿವರ',
      'show_image': 'ಚಿತ್ರವನ್ನು ತೋರಿಸಿ',
      'todays_guidance': 'ಇಂದಿನ ಮಾರ್ಗದರ್ಶನ',
      'weather_field_advice': 'ಹವಾಮಾನ ಮತ್ತು ಹೊಲದ ಸಲಹೆ',
      'farm_health': 'ಕೃಷಿ ಆರೋಗ್ಯ',
      'score_diagnosis': 'ಅಂಕ ಮತ್ತು ರೋಗ ನಿರ್ಣಯ',
      'ask_bhoomi_sub': 'ನಿಮ್ಮ ಭಾಷೆಯಲ್ಲಿ ಯಾವುದೇ ಪ್ರಶ್ನೆ ಕೇಳಿ',
      'tap_to_ask_bhoomi': 'ಭೂಮಿಯನ್ನು ಕೇಳಲು ಸ್ಪರ್ಶಿಸಿ',
      'recording_tap_to_send': 'ರೆಕಾರ್ಡ್ ಆಗುತ್ತಿದೆ... ಕಳುಹಿಸಲು ಸ್ಪರ್ಶಿಸಿ',
      'uploading_audio': 'ಆಡಿಯೋ ಅಪ್‌ಲೋಡ್ ಆಗುತ್ತಿದೆ...',
      'transcribing_speech': 'ಧ್ವನಿಯನ್ನು ಪಠ್ಯಕ್ಕೆ ಪರಿವರ್ತಿಸಲಾಗುತ್ತಿದೆ...',
      'you_can_ask_about': 'ನೀವು ಕೇಳಬಹುದಾದ ವಿಷಯಗಳು:',
      'topic_crops': 'ಬೆಳೆಗಳು',
      'topic_diseases': 'ರೋಗಗಳು',
      'topic_pests': 'ಕೀಟಗಳು',
      'topic_soil': 'ಮಣ್ಣು',
      'topic_weather': 'ಹವಾಮಾನ',
      'topic_prices': 'ಮಾರುಕಟ್ಟೆ ಬೆಲೆ',
      'topic_schemes': 'ಯೋಜನೆಗಳು',
      'show_to_bhoomi': 'ಭೂಮಿಗೆ ತೋರಿಸಿ',
      'upload_or_take_photo': 'ಫೋಟೋ ತೆಗೆಯಿರಿ ಅಥವಾ ಅಪ್‌ಲೋಡ್ ಮಾಡಿ',
      'attached': 'ಲಗತ್ತಿಸಲಾಗಿದೆ',
      'no_image_selected': 'ಯಾವುದೇ ಫೋಟೋ ಆಯ್ಕೆ ಮಾಡಿಲ್ಲ',
      'camera': 'ಕ್ಯಾಮೆರಾ',
      'gallery': 'ಗ್ಯಾಲರಿ',
      'ai_crop_assist_hint': 'AI ಸಮಸ್ಯೆಯನ್ನು ಗುರುತಿಸಿ ಮಾರ್ಗದರ್ಶನ ನೀಡುತ್ತದೆ.',
      'additional_context_optional': 'ಹೆಚ್ಚುವರಿ ವಿವರಗಳು (ಐಚ್ಛಿಕ)',
      'photo_required_hint': 'ಬೆಳೆಯ ಫೋಟೋ ಕಡ್ಡಾಯವಾಗಿದೆ — ಮೇಲೆ ಫೋಟೋ ತೆಗೆಯಿರಿ.',
      'bhoomi_intelligence': 'ಭೂಮಿ ಕೃಷಿ ಬುದ್ಧಿಮತ್ತೆ',
      'processing_query': 'ನಿಮ್ಮ ಪ್ರಶ್ನೆಯನ್ನು ವಿಶ್ಲೇಷಿಸಲಾಗುತ್ತಿದೆ...',
      'analyzing_farm': 'ನಿಮ್ಮ ಜಮೀನನ್ನು ವಿಶ್ಲೇಷಿಸಲಾಗುತ್ತಿದೆ...',
      'review_required': 'ತಜ್ಞರ ಪರಿಶೀಲನೆ ಅಗತ್ಯ',
      'expert_verification_required': 'ತಜ್ಞರ ಪರಿಶೀಲನೆ ಅಗತ್ಯವಿದೆ',
      'below_confidence_gate_desc': 'ನಿಖರತೆ ಸುರಕ್ಷತಾ ಮಿತಿಗಿಂತ ಕಡಿಮೆಯಾಗಿದೆ. ಸುರಕ್ಷಿತ ಸಲಹೆಗಾಗಿ ಕೃಷಿ ತಜ್ಞರಿಗೆ ಕಳುಹಿಸಲಾಗುತ್ತಿದೆ.',
      'escalate_to_kvk': 'KVK ಕೃಷಿ ತಜ್ಞರಿಗೆ ಕಳುಹಿಸಿ',
      'return_to_farm_home': 'ಮುಖಪುಟಕ್ಕೆ ಹಿಂತಿರುಗಿ',
      'listen_to_advisory': 'ಸಲಹೆಯನ್ನು ಕೇಳಿ',
      'stop_audio': 'ಆಡಿಯೋ ನಿಲ್ಲಿಸಿ',
      'listen_to_brief': 'ಸಾರಾಂಶವನ್ನು ಕೇಳಿ',
      'refresh_guidance': 'ಮಾರ್ಗದರ್ಶನವನ್ನು ನವೀಕರಿಸಿ',
      'generating_guidance': 'ಇಂದಿನ ಮಾರ್ಗದರ್ಶನ ಸಿದ್ಧವಾಗುತ್ತಿದೆ...',
      'todays_tasks': 'ಇಂದಿನ ಕೃಷಿ ಕೆಲಸಗಳು',
      'task_completed': 'ಪೂರ್ಣಗೊಂಡಿದೆ',
      'wind': 'ಗಾಳಿ',
      'rain_risk': 'ಮಳೆಯ ಸಾಧ್ಯತೆ',
      'action_plan': 'ಕಾರ್ಯ ಯೋಜನೆ',
      'immediate_steps': 'ಶಿಫಾರಸು ಮಾಡಿದ ತುರ್ತು ಕ್ರಮಗಳು:',
      'why_need_expert': 'ತಜ್ಞರ ಸಹಾಯ ಏಕೆ ಬೇಕು? (ಐಚ್ಛಿಕ)',
      'how_is_it_now': 'ಈಗ ಪರಿಸ್ಥಿತಿ ಹೇಗಿದೆ?',
      'followup_question': 'ಸಲಹೆಯನ್ನು ಪಾಲಿಸಿದ ನಂತರ ಸಮಸ್ಯೆ ಕಡಿಮೆಯಾಗಿದೆಯೇ?',
      'improved': 'ಸುಧಾರಿಸಿದೆ',
      'improved_desc': 'ಹಳದಿ ಬಣ್ಣ ಕಡಿಮೆಯಾಗಿ, ಹೊಸ ಆರೋಗ್ಯಕರ ಎಲೆಗಳು ಬರುತ್ತಿವೆ',
      'no_change': 'ಬದಲಾವಣೆಯಿಲ್ಲ',
      'no_change_desc': 'ಲಕ್ಷಣಗಳು ಹಾಗೆಯೇ ಮುಂದುವರಿದಿವೆ',
      'got_worse': 'ಉಲ್ಬಣಗೊಂಡಿದೆ',
      'got_worse_desc': 'ಹಾನಿ ಇತರ ಸಸ್ಯಗಳಿಗೆ ವೇಗವಾಗಿ ಹರಡುತ್ತಿದೆ',
      'upload_new_photo': 'ಹೊಸ ಫೋಟೋ ಅಪ್‌ಲೋಡ್ ಮಾಡಿ (ಐಚ್ಛಿಕ)',
      'submit_to_kvk': 'KVK ಕೃಷಿ ತಜ್ಞರಿಗೆ ಸಲ್ಲಿಸಿ',
      'expert_case_summary': 'ತಜ್ಞರ ಪ್ರಕರಣದ ಸಾರಾಂಶ',
      'case_transferred': 'ಪ್ರಕರಣ ವರ್ಗಾಯಿಸಲಾಗಿದೆ',
      'expert_notified': 'ತಜ್ಞರಿಗೆ ತಿಳಿಸಲಾಗಿದೆ',
      'review_in_progress': 'ಪರಿಶೀಲನೆ ಪ್ರಗತಿಯಲ್ಲಿದೆ',
      'assigned_kvk': 'ನಿಯೋಜಿತ KVK ಕೇಂದ್ರ',
      'estimated_review': 'ಅಂದಾಜು ಪರಿಶೀಲನಾ ಸಮಯ',
      'farmer': 'ರೈತ',
      'location': 'ಸ್ಥಳ',
      'case_identifier': 'ಪ್ರಕರಣ ಸಂಖ್ಯೆ',
      'summary': 'ಸಾರಾಂಶ',
      'expert_note': 'ತಜ್ಞರ ಟಿಪ್ಪಣಿ',
      'verified_by_land': 'ಭೂ ದಾಖಲೆಯ ಮೂಲಕ ಪರಿಶೀಲಿಸಲಾಗಿದೆ',
      'action_required': 'ಕ್ರಮ ಅಗತ್ಯವಿದೆ',
      'check_eligibility': 'ಅರ್ಹತೆಯನ್ನು ಪರಿಶೀಲಿಸಿ',
      'eligible': 'ಅರ್ಹ',
      'diagnose_get_advice': 'ರೋಗ ನಿರ್ಣಯಿಸಿ ಸಲಹೆ ಪಡೆಯಿರಿ',
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
      'no_schemes_found': 'तुमच्या पिकासाठी आणि स्थानासाठी सध्या कोणत्याही शासकीय योजना उपलब्ध नाहीत.',
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
      'what_would_you_like_to_do': 'तुम्ही काय करू इच्छिता?',
      'your_farm_profile': 'तुमची शेत माहिती',
      'show_image': 'फोटो दाखवा',
      'todays_guidance': 'आजचे मार्गदर्शन',
      'weather_field_advice': 'हवामान आणि शेती सल्ला',
      'farm_health': 'शेतीचे आरोग्य',
      'score_diagnosis': 'गुण आणि रोग निदान',
      'ask_bhoomi_sub': 'तुमच्या भाषेत कोणताही प्रश्न विचारा',
      'tap_to_ask_bhoomi': 'भूमीला विचारण्यासाठी टॅप करा',
      'recording_tap_to_send': 'रेकॉर्डिंग सुरू आहे... पाठवण्यासाठी टॅप करा',
      'uploading_audio': 'ऑडिओ अपलोड होत आहे...',
      'transcribing_speech': 'आवाजाचे मजकुरात रूपांतर होत आहे...',
      'you_can_ask_about': 'तुम्ही या विषयांवर विचारू शकता:',
      'topic_crops': 'पिके',
      'topic_diseases': 'रोग',
      'topic_pests': 'कीटक',
      'topic_soil': 'माती',
      'topic_weather': 'हवामान',
      'topic_prices': 'बाजारभाव',
      'topic_schemes': 'योजना',
      'show_to_bhoomi': 'भूमीला दाखवा',
      'upload_or_take_photo': 'फोटो काढा किंवा अपलोड करा',
      'attached': 'जोडले आहे',
      'no_image_selected': 'कोणताही फोटो निवडलेला नाही',
      'camera': 'कॅमेरा',
      'gallery': 'गॅलरी',
      'ai_crop_assist_hint': 'AI समस्या ओळखून मार्गदर्शन करेल.',
      'additional_context_optional': 'अतिरिक्त माहिती (पर्यायी)',
      'photo_required_hint': 'पिकाचा फोटो आवश्यक आहे — कृपया फोटो काढा.',
      'bhoomi_intelligence': 'भूमी कृषी बुद्धिमत्ता',
      'processing_query': 'तुमच्या प्रश्नाचे विश्लेषण सुरू आहे...',
      'analyzing_farm': 'तुमच्या शेताचे विश्लेषण सुरू आहे...',
      'review_required': 'तज्ज्ञ पुनरावलोकन आवश्यक',
      'expert_verification_required': 'तज्ज्ञ पडताळणी आवश्यक आहे',
      'below_confidence_gate_desc': 'अचूकता सुरक्षा मर्यादेपेक्षा कमी आहे. सुरक्षित सल्ल्यासाठी हे कृषी तज्ज्ञांकडे पाठवले जात आहे.',
      'escalate_to_kvk': 'KVK कृषी तज्ज्ञांकडे पाठवा',
      'return_to_farm_home': 'मुख्यपृष्ठावर जा',
      'listen_to_advisory': 'सल्ला ऐका',
      'stop_audio': 'ऑडिओ थांबवा',
      'listen_to_brief': 'सारांश ऐका',
      'refresh_guidance': 'मार्गदर्शन रीफ्रेश करा',
      'generating_guidance': 'आजचे मार्गदर्शन तयार होत आहे...',
      'todays_tasks': 'आजची शेतीतील कामे',
      'task_completed': 'पूर्ण झाले',
      'wind': 'वारा',
      'rain_risk': 'पावसाची शक्यता',
      'action_plan': 'कृती योजना',
      'immediate_steps': 'तातडीने करावयाच्या शिफारसी:',
      'why_need_expert': 'तज्ज्ञांची मदत का हवी आहे? (पर्यायी)',
      'how_is_it_now': 'आता परिस्थिती कशी आहे?',
      'followup_question': 'सल्ल्याचे पालन केल्यानंतर समस्येत सुधारणा झाली का?',
      'improved': 'सुधारणा झाली',
      'improved_desc': 'पिवळेपणा कमी झाला, नवीन निरोगी पाने येत आहेत',
      'no_change': 'काही बदल नाही',
      'no_change_desc': 'लक्षणे अजूनही तशीच आहेत',
      'got_worse': 'अधिक बिघडली',
      'got_worse_desc': 'रोग इतर रोपांवर वेगाने पसरत आहे',
      'upload_new_photo': 'नवीन फोटो अपलोड करा (पर्यायी)',
      'submit_to_kvk': 'KVK कृषी तज्ज्ञांना सादर करा',
      'expert_case_summary': 'तज्ज्ञ केस सारांश',
      'case_transferred': 'केस हस्तांतरित केली',
      'expert_notified': 'तज्ज्ञांना सूचित केले',
      'review_in_progress': 'पुनरावलोकन सुरू आहे',
      'assigned_kvk': 'नियुक्त KVK केंद्र',
      'estimated_review': 'अंदाजे वेळ',
      'farmer': 'शेतकरी',
      'location': 'स्थान',
      'case_identifier': 'केस क्रमांक',
      'summary': 'सारांश',
      'expert_note': 'तज्ज्ञ नोंद',
      'verified_by_land': 'जमीन नोंदीद्वारे सत्यापित',
      'action_required': 'कृती आवश्यक',
      'check_eligibility': 'पात्रता तपासा',
      'eligible': 'पात्र',
      'diagnose_get_advice': 'निदान करा आणि सल्ला मिळवा',
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
      'no_schemes_found': 'നിങ്ങളുടെ വിളയ്ക്കും സ്ഥലത്തിനും അനുയോജ്യമായ സർക്കാർ പദ്ധതികൾ നിലവിൽ ലഭ്യമല്ല.',
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
      'what_would_you_like_to_do': 'നിങ്ങൾ എന്താണ് ചെയ്യാൻ ആഗ്രഹിക്കുന്നത്?',
      'your_farm_profile': 'നിങ്ങളുടെ കൃഷി വിവരണം',
      'show_image': 'ചിത്രം കാണിക്കുക',
      'todays_guidance': 'ഇന്നത്തെ നിർദ്ദേശങ്ങൾ',
      'weather_field_advice': 'കാലാവസ്ഥയും കൃഷി ഉപദേശവും',
      'farm_health': 'കൃഷി ആരോഗ്യം',
      'score_diagnosis': 'സ്കോറും രോഗനിർണയവും',
      'ask_bhoomi_sub': 'നിങ്ങളുടെ ഭാഷയിൽ ഏത് ചോദ്യവും ചോദിക്കാം',
      'tap_to_ask_bhoomi': 'ഭൂമിയോട് ചോദിക്കാൻ അമർത്തുക',
      'recording_tap_to_send': 'റെക്കോർഡ് ചെയ്യുന്നു... അയക്കാൻ അമർത്തുക',
      'uploading_audio': 'ഓഡിയോ അപ്‌ലോഡ് ചെയ്യുന്നു...',
      'transcribing_speech': 'ശബ്ദം ടെക്‌സ്‌റ്റാക്കി മാറ്റുന്നു...',
      'you_can_ask_about': 'നിങ്ങൾക്ക് ചോദിക്കാവുന്ന വിഷയങ്ങൾ:',
      'topic_crops': 'വിളകൾ',
      'topic_diseases': 'രോഗങ്ങൾ',
      'topic_pests': 'കീടങ്ങൾ',
      'topic_soil': 'മണ്ണ്',
      'topic_weather': 'കാലാവസ്ഥ',
      'topic_prices': 'വിപണി വില',
      'topic_schemes': 'പദ്ധതികൾ',
      'show_to_bhoomi': 'ഭൂമിയെ കാണിക്കുക',
      'upload_or_take_photo': 'ഫോട്ടോ എടുക്കുക അല്ലെങ്കിൽ അപ്‌ലോഡ് ചെയ്യുക',
      'attached': 'ചേർത്തു',
      'no_image_selected': 'ഫോട്ടോ തിരഞ്ഞെടുത്തിട്ടില്ല',
      'camera': 'ക്യാമറ',
      'gallery': 'ഗാലറി',
      'ai_crop_assist_hint': 'AI പ്രശ്നം കണ്ടെത്തി മാർഗ്ഗനിർദ്ദേശം നൽകും.',
      'additional_context_optional': 'കൂടുതൽ വിവരങ്ങൾ (നിർബന്ധമില്ല)',
      'photo_required_hint': 'വിളയുടെ ഫോട്ടോ ആവശ്യമാണ് — ദയവായി ഫോട്ടോ എടുക്കുക.',
      'bhoomi_intelligence': 'ഭൂമി കാർഷിക ഇന്റലിജൻസ്',
      'processing_query': 'നിങ്ങളുടെ ചോദ്യം പരിശോധിക്കുന്നു...',
      'analyzing_farm': 'നിങ്ങളുടെ കൃഷിയിടം പരിശോധിക്കുന്നു...',
      'review_required': 'വിദഗ്ദ്ധ പരിശോധന ആവശ്യം',
      'expert_verification_required': 'വിദഗ്ദ്ധ പരിശോധന ആവശ്യമാണ്',
      'below_confidence_gate_desc': 'കൃത്യത സുരക്ഷാ പരിധിയേക്കാൾ കുറവാണ്. കൃത്യമായ ഉപദേശത്തിനായി കൃഷി വിദഗ്ദ്ധർക്ക് അയക്കുന്നു.',
      'escalate_to_kvk': 'KVK കൃഷി വിദഗ്ദ്ധർക്ക് അയക്കുക',
      'return_to_farm_home': 'പ്രധാന പേജിലേക്ക് മടങ്ങുക',
      'listen_to_advisory': 'ഉപദേശം കേൾക്കുക',
      'stop_audio': 'ഓഡിയോ നിർത്തുക',
      'listen_to_brief': 'സംഗ്രഹം കേൾക്കുക',
      'refresh_guidance': 'നിർദ്ദേശങ്ങൾ പുതുക്കുക',
      'generating_guidance': 'ഇന്നത്തെ നിർദ്ദേശങ്ങൾ തയ്യാറാക്കുന്നു...',
      'todays_tasks': 'ഇന്നത്തെ കാർഷിക ജോലികൾ',
      'task_completed': 'പൂർത്തിയായി',
      'wind': 'കാറ്റ്',
      'rain_risk': 'മഴ സാധ്യത',
      'action_plan': 'കർമ്മ പദ്ധതി',
      'immediate_steps': 'ഉടൻ ചെയ്യേണ്ട നടപടികൾ:',
      'why_need_expert': 'എന്തുകൊണ്ട് വിദഗ്ദ്ധ സഹായം വേണം? (ഐച്ഛികം)',
      'how_is_it_now': 'ഇപ്പോൾ അവസ്ഥ എങ്ങനെയുണ്ട്?',
      'followup_question': 'ഉപദേശം സ്വീകരിച്ച ശേഷം പ്രശ്നം കുറഞ്ഞോ?',
      'improved': 'മെച്ചപ്പെട്ടു',
      'improved_desc': 'മഞ്ഞനിറം മാറി പുതിയ ആരോഗ്യമുള്ള ഇലകൾ വരുന്നു',
      'no_change': 'മാറ്റമില്ല',
      'no_change_desc': 'ലക്ഷണങ്ങൾ അതേപടി തുടരുന്നു',
      'got_worse': 'കൂടുതൽ മോശമായി',
      'got_worse_desc': 'രോഗം മറ്റ് ചെടികളിലേക്കും വേഗത്തിൽ പടരുന്നു',
      'upload_new_photo': 'പുതിയ ഫോട്ടോ അപ്‌ലോഡ് ചെയ്യുക (ഐച്ഛികം)',
      'submit_to_kvk': 'KVK കൃഷി വിദഗ്ദ്ധർക്ക് സമർപ്പിക്കുക',
      'expert_case_summary': 'വിദഗ്ദ്ധ കേസ് വിവരങ്ങൾ',
      'case_transferred': 'കേസ് കൈമാറി',
      'expert_notified': 'വിദഗ്ദ്ധനെ അറിയിച്ചു',
      'review_in_progress': 'പരിശോധന പുരോഗമിക്കുന്നു',
      'assigned_kvk': 'നിയോഗിച്ച KVK കേന്ദ്രം',
      'estimated_review': 'പ്രതീക്ഷിക്കുന്ന സമയം',
      'farmer': 'കർഷകൻ',
      'location': 'സ്ഥലം',
      'case_identifier': 'കേസ് നമ്പർ',
      'summary': 'സംഗ്രഹം',
      'expert_note': 'വിദഗ്ദ്ധ കുറിപ്പ്',
      'verified_by_land': 'ഭൂമി രേഖ പ്രകാരം പരിശോധിച്ചു',
      'action_required': 'നടപടി ആവശ്യം',
      'check_eligibility': 'അർഹത പരിശോധിക്കുക',
      'eligible': 'അർഹതയുണ്ട്',
      'diagnose_get_advice': 'രോഗനിർണയം നടത്തി ഉപദേശം നേടുക',
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
      'no_schemes_found': 'ਤੁਹਾਡੀ ਫ਼ਸਲ ਅਤੇ ਸਥਾਨ ਲਈ ਫਿਲਹਾਲ ਕੋਈ ਸਰਕਾਰੀ ਸਕੀਮਾਂ ਉਪਲਬਧ ਨਹੀਂ ਹਨ।',
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
      'what_would_you_like_to_do': 'ਤੁਸੀਂ ਕੀ ਕਰਨਾ ਚਾਹੁੰਦੇ ਹੋ?',
      'your_farm_profile': 'ਤੁਹਾਡਾ ਖੇਤ ਪ੍ਰੋਫਾਈਲ',
      'show_image': 'ਤਸਵੀਰ ਦਿਖਾਓ',
      'todays_guidance': 'ਅੱਜ ਦੀ ਸਲਾਹ',
      'weather_field_advice': 'ਮੌਸਮ ਅਤੇ ਖੇਤੀ ਸਲਾਹ',
      'farm_health': 'ਖੇਤ ਦੀ ਸਿਹਤ',
      'score_diagnosis': 'ਸਕੋਰ ਅਤੇ ਰੋਗ ਨਿਦਾਨ',
      'ask_bhoomi_sub': 'ਆਪਣੀ ਭਾਸ਼ਾ ਵਿੱਚ ਕੋਈ ਵੀ ਸਵਾਲ ਪੁੱਛੋ',
      'tap_to_ask_bhoomi': 'ਭੂਮੀ ਨੂੰ ਪੁੱਛਣ ਲਈ ਟੈਪ ਕਰੋ',
      'recording_tap_to_send': 'ਰਿਕਾਰਡਿੰਗ ਹੋ ਰਹੀ ਹੈ... ਭੇਜਣ ਲਈ ਟੈਪ ਕਰੋ',
      'uploading_audio': 'ਆਡੀਓ ਅੱਪਲੋਡ ਹੋ ਰਿਹਾ ਹੈ...',
      'transcribing_speech': 'ਬੋਲ ਨੂੰ ਲਿਖਤ ਵਿੱਚ ਬਦਲਿਆ ਜਾ ਰਿਹਾ ਹੈ...',
      'you_can_ask_about': 'ਤੁਸੀਂ ਇਹਨਾਂ ਵਿਸ਼ਿਆਂ ਬਾਰੇ ਪੁੱਛ ਸਕਦੇ ਹੋ:',
      'topic_crops': 'ਫ਼ਸਲਾਂ',
      'topic_diseases': 'ਬਿਮਾਰੀਆਂ',
      'topic_pests': 'ਕੀੜੇ',
      'topic_soil': 'ਮਿੱਟੀ',
      'topic_weather': 'ਮੌਸਮ',
      'topic_prices': 'ਮੰਡੀ ਭਾਅ',
      'topic_schemes': 'ਸਕੀਮਾਂ',
      'show_to_bhoomi': 'ਭੂਮੀ ਨੂੰ ਦਿਖਾਓ',
      'upload_or_take_photo': 'ਤਸਵੀਰ ਖਿੱਚੋ ਜਾਂ ਅੱਪਲੋਡ ਕਰੋ',
      'attached': 'ਨੱਥੀ ਕੀਤੀ ਗਈ',
      'no_image_selected': 'ਕੋਈ ਤਸਵੀਰ ਨਹੀਂ ਚੁਣੀ ਗਈ',
      'camera': 'ਕੈਮਰਾ',
      'gallery': 'ਗੈਲਰੀ',
      'ai_crop_assist_hint': 'AI ਸਮੱਸਿਆ ਦੀ ਪਛਾਣ ਕਰੇਗਾ ਅਤੇ ਮਾਰਗਦਰਸ਼ਨ ਕਰੇਗਾ।',
      'additional_context_optional': 'ਵਾਧੂ ਵੇਰਵੇ (ਵਿਕਲਪਿਕ)',
      'photo_required_hint': 'ਫ਼ਸਲ ਦੀ ਤਸਵੀਰ ਲਾਜ਼ਮੀ ਹੈ — ਕਿਰਪਾ ਕਰਕੇ ਤਸਵੀਰ ਲਵੋ।',
      'bhoomi_intelligence': 'ਭੂਮੀ ਖੇਤੀਬਾੜੀ ਇੰਟੈਲੀਜੈਂਸ',
      'processing_query': 'ਤੁਹਾਡੇ ਸਵਾਲ ਦਾ ਵਿਸ਼ਲੇਸ਼ਣ ਕੀਤਾ ਜਾ ਰਿਹਾ ਹੈ...',
      'analyzing_farm': 'ਤੁਹਾਡੇ ਖੇਤ ਦਾ ਵਿਸ਼ਲੇਸ਼ਣ ਕੀਤਾ ਜਾ ਰਿਹਾ ਹੈ...',
      'review_required': 'ਮਾਹਰ ਸਮੀਖਿਆ ਜ਼ਰੂਰੀ',
      'expert_verification_required': 'ਮਾਹਰ ਤਸਦੀਕ ਦੀ ਲੋੜ ਹੈ',
      'below_confidence_gate_desc': 'ਸਟੀਕਤਾ ਸੁਰੱਖਿਆ ਸੀਮਾ ਤੋਂ ਘੱਟ ਹੈ। ਸੁਰੱਖਿਅਤ ਸਲਾਹ ਲਈ ਖੇਤੀਬਾੜੀ ਮਾਹਰ ਨੂੰ ਭੇਜਿਆ ਜਾ ਰਿਹਾ ਹੈ।',
      'escalate_to_kvk': 'KVK ਖੇਤੀਬਾੜੀ ਮਾਹਰ ਨੂੰ ਭੇਜੋ',
      'return_to_farm_home': 'ਮੁੱਖ ਪੰਨੇ ਤੇ ਵਾਪਸ ਜਾਓ',
      'listen_to_advisory': 'ਸਲਾਹ ਸੁਣੋ',
      'stop_audio': 'ਆਡੀਓ ਰੋਕੋ',
      'listen_to_brief': 'ਸੰਖੇਪ ਸੁਣੋ',
      'refresh_guidance': 'ਸਲਾਹ ਤਾਜ਼ਾ ਕਰੋ',
      'generating_guidance': 'ਅੱਜ ਦੀ ਸਲਾਹ ਤਿਆਰ ਹੋ ਰਹੀ ਹੈ...',
      'todays_tasks': 'ਅੱਜ ਦੇ ਖੇਤ ਕਾਰਜ',
      'task_completed': 'ਮੁਕੰਮਲ',
      'wind': 'ਹਵਾ',
      'rain_risk': 'ਮੀਂਹ ਦਾ ਖ਼ਤਰਾ',
      'action_plan': 'ਕਾਰਜ ਯੋਜਨਾ',
      'immediate_steps': 'ਸਿਫ਼ਾਰਸ਼ ਕੀਤੇ ਤੁਰੰਤ ਕਦਮ:',
      'why_need_expert': 'ਮਾਹਰ ਦੀ ਮਦਦ ਕਿਉਂ ਚਾਹੀਦੀ ਹੈ? (ਵਿਕਲਪਿਕ)',
      'how_is_it_now': 'ਹੁਣ ਹਾਲਤ ਕਿਵੇਂ ਹੈ?',
      'followup_question': 'ਸਲਾਹ ਮੰਨਣ ਤੋਂ ਬਾਅਦ ਸਮੱਸਿਆ ਵਿੱਚ ਸੁਧਾਰ ਹੋਇਆ ਹੈ?',
      'improved': 'ਸੁਧਾਰ ਹੋਇਆ',
      'improved_desc': 'ਪੀਲਾਪਣ ਘਟਿਆ, ਨਵੇਂ ਸਿਹਤਮੰਦ ਪੱਤੇ ਆ ਰਹੇ ਹਨ',
      'no_change': 'ਕੋਈ ਬਦਲਾਅ ਨਹੀਂ',
      'no_change_desc': 'ਲੱਛਣ ਅਜੇ ਵੀ ਓਸੇ ਤਰ੍ਹਾਂ ਹਨ',
      'got_worse': 'ਹੋਰ ਵਿਗੜ ਗਿਆ',
      'got_worse_desc': 'ਨੁਕਸਾਨ ਹੋਰ ਬੂਟਿਆਂ ਤੱਕ ਤੇਜ਼ੀ ਨਾਲ ਫੈਲ ਰਿਹਾ ਹੈ',
      'upload_new_photo': 'ਨਵੀਂ ਤਸਵੀਰ ਅੱਪਲੋਡ ਕਰੋ (ਵਿਕਲਪਿਕ)',
      'submit_to_kvk': 'KVK ਖੇਤੀਬਾੜੀ ਮਾਹਰ ਨੂੰ ਸੌਂਪੋ',
      'expert_case_summary': 'ਮਾਹਰ ਕੇਸ ਸੰਖੇਪ',
      'case_transferred': 'ਕੇਸ ਤਬਦੀਲ ਕੀਤਾ ਗਿਆ',
      'expert_notified': 'ਮਾਹਰ ਨੂੰ ਸੂਚਿਤ ਕੀਤਾ ਗਿਆ',
      'review_in_progress': 'ਸਮੀਖਿਆ ਜਾਰੀ ਹੈ',
      'assigned_kvk': 'ਨਿਰਧਾਰਤ KVK ਕੇਂਦਰ',
      'estimated_review': 'ਅੰਦਾਜ਼ਨ ਸਮਾਂ',
      'farmer': 'ਕਿਸਾਨ',
      'location': 'ਸਥਾਨ',
      'case_identifier': 'ਕੇਸ ਨੰਬਰ',
      'summary': 'ਸੰਖੇਪ',
      'expert_note': 'ਮਾਹਰ ਨੋਟ',
      'verified_by_land': 'ਜ਼ਮੀਨ ਰਿਕਾਰਡ ਦੁਆਰਾ ਤਸਦੀਕਸ਼ੁਦਾ',
      'action_required': 'ਕਾਰਵਾਈ ਲੋੜੀਂਦੀ',
      'check_eligibility': 'ਯੋਗਤਾ ਦੀ ਜਾਂਚ ਕਰੋ',
      'eligible': 'ਯੋਗ',
      'diagnose_get_advice': 'ਰੋਗ ਪਛਾਣੋ ਅਤੇ ਸਲਾਹ ਲਵੋ',
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

  String translateHealthExplanation(String band, String? explanation) {
    if (explanation != null && explanation.isNotEmpty && !explanation.contains('Farm parameters are in healthy range') && !explanation.contains('Complete onboarding')) {
      final lower = explanation.toLowerCase();
      if (lower.contains('healthy range') || lower.contains('parameters are in healthy')) {
        return langCode.startsWith('ta')
            ? 'பண்ணை அளவுகோல்கள் ஆரோக்கியமான வரம்பில் உள்ளன.'
            : langCode.startsWith('hi')
                ? 'खेत के सभी पैरामीटर स्वस्थ सीमा में हैं।'
                : explanation;
      }
      if (lower.contains('onboarding') || lower.contains('upload farm photos')) {
        return langCode.startsWith('ta')
            ? 'தொடக்க நிலையை முடித்து, முதல் மதிப்பெண்ணைப் பெற பயிர் புகைப்படங்களைப் பதிவேற்றவும்.'
            : langCode.startsWith('hi')
                ? 'प्रारंभिक स्कोर की गणना के लिए खेत की तस्वीरें अपलोड करें।'
                : explanation;
      }
    }
    switch (band.toLowerCase()) {
      case 'good':
      case 'excellent':
        return langCode.startsWith('ta')
            ? 'பண்ணை அளவுகோல்கள் ஆரோக்கியமான வரம்பில் உள்ளன.'
            : langCode.startsWith('hi')
                ? 'खेत के सभी पैरामीटर स्वस्थ सीमा में हैं।'
                : 'Farm parameters are in healthy range.';
      case 'moderate':
      case 'fair':
        return langCode.startsWith('ta')
            ? 'சில வேளாண் காரணிகளுக்கு தொடர் கண்காணிப்பு தேவைப்படுகிறது.'
            : langCode.startsWith('hi')
                ? 'कुछ कृषि मापदंडों पर निरंतर निगरानी की आवश्यकता है।'
                : 'Some agronomic parameters require regular monitoring.';
      case 'poor':
      case 'critical':
        return langCode.startsWith('ta')
            ? 'பயிர் பாதுகாப்புக்கு உடனடி மேலாண்மை தலையீடு தேவைப்படுகிறது.'
            : langCode.startsWith('hi')
                ? 'फसल सुरक्षा के लिए तत्काल प्रबंधन हस्तक्षेप आवश्यक है।'
                : 'Immediate agronomic management required for crop recovery.';
      case 'unrated':
      default:
        return langCode.startsWith('ta')
            ? 'முதல் மதிப்பெண்ணைப் பெற பயிர் புகைப்படங்களைப் பதிவேற்றவும்.'
            : langCode.startsWith('hi')
                ? 'प्रारंभिक स्कोर की गणना के लिए खेत की तस्वीरें अपलोड करें।'
                : 'Complete onboarding and upload farm photos to compute initial score.';
    }
  }

  String translateBriefSummary(String summary) {
    final lower = summary.toLowerCase();
    if (lower.contains('moisture management') || lower.contains('field scouting') || lower.contains('favorable')) {
      return langCode.startsWith('ta')
          ? 'இன்றைய வானிலை பாசன மேலாண்மை மற்றும் வயல் ஆய்வுக்கு உகந்ததாக உள்ளது.'
          : langCode.startsWith('hi')
              ? 'आज का मौसम सिंचाई प्रबंधन और खेत निरीक्षण के लिए अनुकूल है।'
              : summary;
    }
    if (lower.contains('rain') || lower.contains('spray window')) {
      return langCode.startsWith('ta')
          ? 'வானிலை நிலவரப்படி உரம் மற்றும் பூச்சிக்கொல்லி தெளிப்புக்கு உகந்த நேரம்.'
          : langCode.startsWith('hi')
              ? 'मौसम की स्थिति उर्वरक और कीटनाशक छिड़काव के लिए उपयुक्त है।'
              : summary;
    }
    return summary;
  }

  String translateBriefAction(String? action) {
    if (action == null || action.isEmpty) return '';
    final lower = action.toLowerCase();
    if (lower.contains('irrigation') || lower.contains('2,200') || lower.contains('2200')) {
      return langCode.startsWith('ta')
          ? 'அதிகாலை வேளையில் பரிந்துரைக்கப்பட்ட 2,200 லிட்டர் பாசனத்தை வழங்கவும்.'
          : langCode.startsWith('hi')
              ? 'सुबह के समय अनुशंसित 2,200 लीटर सिंचाई लागू करें।'
              : action;
    }
    if (lower.contains('drainage') || lower.contains('standing water')) {
      return langCode.startsWith('ta')
          ? 'வயலில் தேங்கியுள்ள உபரி நீரை உடனடியாக வடிய வைக்கவும்.'
          : langCode.startsWith('hi')
              ? 'खेत में जमा अतिरिक्त पानी को तुरंत बाहर निकालें।'
              : action;
    }
    return action;
  }

  String translateWeatherSummary(String weatherSummary) {
    final lower = weatherSummary.toLowerCase();
    if (lower.contains('partly sunny') && lower.contains('spray window')) {
      return langCode.startsWith('ta')
          ? 'பகுதி வெயில் • மருந்து தெளிக்க உகந்த நேரம்'
          : langCode.startsWith('hi')
              ? 'हल्की धूप • छिड़काव के लिए अच्छा समय'
              : weatherSummary;
    }
    if (lower.contains('sunny') || lower.contains('clear')) {
      return langCode.startsWith('ta')
          ? 'வெயில் நிறைந்த வானிலை'
          : langCode.startsWith('hi')
              ? 'धूप वाला मौसम'
              : weatherSummary;
    }
    if (lower.contains('rain') || lower.contains('cloudy')) {
      return langCode.startsWith('ta')
          ? 'மேகமூட்டம் • மழை வாய்ப்பு'
          : langCode.startsWith('hi')
              ? 'बादल छाए रहेंगे • बारिश की संभावना'
              : weatherSummary;
    }
    return weatherSummary;
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
  String get showImage => text('show_image');
  String get todaysGuidance => text('todays_guidance');
  String get weatherFieldAdvice => text('weather_field_advice');
  String get farmHealth => text('farm_health');
  String get scoreDiagnosis => text('score_diagnosis');
  String get askBhoomiSub => text('ask_bhoomi_sub');
  String get tapToAskBhoomi => text('tap_to_ask_bhoomi');
  String get recordingTapToSend => text('recording_tap_to_send');
  String get uploadingAudio => text('uploading_audio');
  String get transcribingSpeech => text('transcribing_speech');
  String get youCanAskAbout => text('you_can_ask_about');
  String get topicCrops => text('topic_crops');
  String get topicDiseases => text('topic_diseases');
  String get topicPests => text('topic_pests');
  String get topicSoil => text('topic_soil');
  String get topicWeather => text('topic_weather');
  String get topicPrices => text('topic_prices');
  String get topicSchemes => text('topic_schemes');
  String get showToBhoomi => text('show_to_bhoomi');
  String get uploadOrTakePhoto => text('upload_or_take_photo');
  String get attached => text('attached');
  String get noImageSelected => text('no_image_selected');
  String get camera => text('camera');
  String get gallery => text('gallery');
  String get aiCropAssistHint => text('ai_crop_assist_hint');
  String get additionalContextOptional => text('additional_context_optional');
  String get photoRequiredHint => text('photo_required_hint');
  String get bhoomiIntelligence => text('bhoomi_intelligence');
  String get processingQuery => text('processing_query');
  String get analyzingFarm => text('analyzing_farm');
  String get reviewRequired => text('review_required');
  String get expertVerificationRequired => text('expert_verification_required');
  String get belowConfidenceGateDesc => text('below_confidence_gate_desc');
  String get escalateToKvk => text('escalate_to_kvk');
  String get returnToFarmHome => text('return_to_farm_home');
  String get listenToAdvisory => text('listen_to_advisory');
  String get stopAudio => text('stop_audio');
  String get listenToBrief => text('listen_to_brief');
  String get refreshGuidance => text('refresh_guidance');
  String get generatingGuidance => text('generating_guidance');
  String get todaysTasks => text('todays_tasks');
  String get taskCompleted => text('task_completed');
  String get wind => text('wind');
  String get rainRisk => text('rain_risk');
  String get actionPlan => text('action_plan');
  String get immediateSteps => text('immediate_steps');
  String get whyNeedExpert => text('why_need_expert');
  String get howIsItNow => text('how_is_it_now');
  String get followupQuestion => text('followup_question');
  String get improved => text('improved');
  String get improvedDesc => text('improved_desc');
  String get noChange => text('no_change');
  String get noChangeDesc => text('no_change_desc');
  String get gotWorse => text('got_worse');
  String get gotWorseDesc => text('got_worse_desc');
  String get uploadNewPhoto => text('upload_new_photo');
  String get submitToKvk => text('submit_to_kvk');
  String get expertCaseSummary => text('expert_case_summary');
  String get caseTransferred => text('case_transferred');
  String get expertNotified => text('expert_notified');
  String get reviewInProgress => text('review_in_progress');
  String get assignedKvk => text('assigned_kvk');
  String get estimatedReview => text('estimated_review');
  String get farmer => text('farmer');
  String get location => text('location');
  String get caseIdentifier => text('case_identifier');
  String get summary => text('summary');
  String get expertNote => text('expert_note');
  String get verifiedByLand => text('verified_by_land');
  String get actionRequired => text('action_required');
  String get checkEligibility => text('check_eligibility');
  String get eligible => text('eligible');
  String get possibleIssueIdentified => text('possible_issue_identified');
  String get trackProgress => text('track_progress');
  String get getExpertHelp => text('get_expert_help');

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
