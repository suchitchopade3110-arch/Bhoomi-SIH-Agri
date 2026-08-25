class ApiConstants {
  static const String baseApiUrl = String.fromEnvironment(
    'API_BASE_URL',
    defaultValue: 'http://localhost:8000',
  );

  static const bool enableMockFallback = bool.fromEnvironment(
    'ENABLE_MOCK_FALLBACK',
    defaultValue: true,
  );

  static const String apiVersion = '/api/v1';

  // Auth Endpoints
  static const String authLogin = '$apiVersion/auth/login';
  static const String authRegister = '$apiVersion/auth/register';

  // Farm Endpoints (Phase 1)
  static const String farms = '$apiVersion/farms';
  static String farmDetail(String id) => '$apiVersion/farms/$id';
  static String farmSummary(String id) => '$apiVersion/farms/$id/summary';

  // Asset Presigned Upload (Phase 2 & 3)
  static const String assetsPresign = '$apiVersion/assets/presigned-url';
  static String assetDetail(String assetId) => '$apiVersion/assets/$assetId';

  // Voice Endpoints (Phase 2 & 3)
  static const String voiceTranscribe = '$apiVersion/voice/transcribe';
  static const String voiceSynthesize = '$apiVersion/voice/synthesize';
  static const String voiceQuery = '$apiVersion/voice/query';

  // Land Endpoints (Phase 2)
  // NOTE: automated cadastral lookup was deliberately cut from scope (see
  // services/api/app/api/v1/land.py's module docstring — SIH26131 feature
  // checklist §10.1/§13.2/§13.3: HITL survey-number submission only, no
  // auto-lookup). Verification is always via `landVerify` + officer review.
  static const String landVerify = '$apiVersion/land/verify';
  static String farmLand(String farmId) => '$apiVersion/land/$farmId';
  static String landRecord(String landId) => '$apiVersion/land/$landId';

  // Resource Planner Endpoints (Phase 2)
  static String resourcePlan(String farmId) => '$apiVersion/resource-plan/$farmId';
  static String latestResourcePlan(String farmId) => '$apiVersion/resource-plan/$farmId';

  // Weather Endpoints (Phase 2)
  static const String weatherCurrent = '$apiVersion/weather/current';
  static const String weatherForecast = '$apiVersion/weather/forecast';
  static const String weatherEt0 = '$apiVersion/weather/et0';
  static String farmWeather(String farmId) => '$apiVersion/farms/$farmId/summary';

  // Health Endpoints (Phase 2 & Contract §4) — backend exposes these under
  // "risk" (see services/api/app/api/v1/health.py); path kept in sync with
  // the live contract, not the "health" naming used in this constant's name.
  static String farmHealth(String farmId) => '$apiVersion/farms/$farmId/risk';
  static String farmHealthHistory(String farmId) => '$apiVersion/farms/$farmId/risk/history';
  static String farmHealthRecompute(String farmId) => '$apiVersion/farms/$farmId/risk/recompute';

  // Diagnosis & Advisory Endpoints (Phase 3 & Contract §5)
  static String farmDiagnose(String farmId) => '$apiVersion/farms/$farmId/diagnose';
  static const String advisoryQuery = '$apiVersion/advisory/query';


  // Timeline / Farm Journey Endpoints (Phase 3)
  static String farmTimeline(String farmId) => '$apiVersion/timeline/$farmId';
  static const String timelineEvents = '$apiVersion/timeline/events';

  // Follow-up Endpoints (Phase 3)
  static const String followupCheckin = '$apiVersion/followup/checkin';
  static String farmFollowups(String farmId) => '$apiVersion/followup/checkin';

  // Expert Escalation Endpoints (Phase 3)
  static const String escalationCreate = '$apiVersion/escalation/create';
  static String escalationRecord(String caseId) => '$apiVersion/escalation/$caseId';
  static String farmEscalations(String farmId) => '$apiVersion/escalation/create';

  // KVK Agronomist Endpoints (Phase 3)
  static const String kvkCases = '$apiVersion/agronomist/queue';
  static String kvkCaseDetail(String caseId) => '$apiVersion/agronomist/case/$caseId';
  static const String kvkResolveCase = '$apiVersion/agronomist/resolve';

  // Officer Endpoints (HITL Land Boundary Verification)
  static const String officerQueue = '$apiVersion/officer/queue';
  static String officerReviewDetail(String parcelId) => '$apiVersion/officer/review/$parcelId';
  static const String officerAction = '$apiVersion/officer/action';

  // Government Scheme Endpoints (Phase 4)
  static const String schemesMatch = '$apiVersion/schemes/match';
  static String farmSchemes(String farmId) => '$apiVersion/schemes/match';
  static String schemeDetail(String schemeId) => '$apiVersion/schemes/$schemeId';
  static String schemeRequirements(String farmId, String schemeId) => '$apiVersion/schemes/$schemeId';

  // Today's Farm Brief Endpoints (Phase 4)
  static String dailyBrief(String farmId) => '$apiVersion/farms/$farmId/summary';

  // Proactive Farm Updates Endpoints (Phase 4)
  static String farmUpdates(String farmId) => '$apiVersion/timeline/$farmId';

  // Request Timeouts
  static const Duration connectTimeout = Duration(seconds: 4);
  static const Duration receiveTimeout = Duration(seconds: 4);
  static const Duration sendTimeout = Duration(seconds: 4);

  // Headers
  static const String authorizationHeader = 'Authorization';
  static const String contentTypeHeader = 'Content-Type';
  static const String applicationJson = 'application/json';
}
