import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import '../features/daily_brief/presentation/screens/todays_farm_brief_screen.dart';
import '../features/diagnosis/presentation/screens/ask_bhoomi_screen.dart';
import '../features/diagnosis/presentation/screens/diagnosis_result_screen.dart';
import '../features/escalation/presentation/screens/escalation_screen.dart';
import '../features/farm_summary/presentation/screens/farm_home_screen.dart';
import '../features/followups/presentation/screens/followup_screen.dart';
import '../features/health/presentation/screens/farm_health_screen.dart';
import '../features/health/presentation/screens/health_history_screen.dart';
import '../features/land/presentation/screens/land_boundary_screen.dart';
import '../features/land/presentation/screens/land_details_screen.dart';
import '../features/land/presentation/screens/land_status_screen.dart';
import '../features/onboarding/presentation/screens/confirm_farm_screen.dart';
import '../features/onboarding/presentation/screens/language_selection_screen.dart';
import '../features/onboarding/presentation/screens/onboarding_screen.dart';
import '../features/onboarding/presentation/screens/welcome_screen.dart';
import '../features/resource_plan/presentation/screens/todays_plan_screen.dart';
import '../features/schemes/presentation/screens/scheme_detail_screen.dart';
import '../features/schemes/presentation/screens/scheme_information_screen.dart';
import '../features/schemes/presentation/screens/schemes_screen.dart';
import '../features/timeline/presentation/screens/farm_journey_screen.dart';
import '../features/updates/presentation/screens/farm_updates_screen.dart';

final appRouter = GoRouter(
  initialLocation: '/welcome',
  routes: [
    GoRoute(
      path: '/',
      redirect: (_, __) => '/welcome',
    ),
    GoRoute(
      path: '/welcome',
      builder: (context, state) => const WelcomeScreen(),
    ),
    GoRoute(
      path: '/language-select',
      builder: (context, state) => const LanguageSelectionScreen(),
    ),
    GoRoute(
      path: '/onboarding',
      builder: (context, state) => const OnboardingScreen(),
    ),
    GoRoute(
      path: '/confirm-farm',
      builder: (context, state) => const ConfirmFarmScreen(),
    ),
    GoRoute(
      path: '/home/:farmId',
      builder: (context, state) {
        final farmId = state.pathParameters['farmId'] ?? 'f_1';
        return FarmHomeScreen(farmId: farmId);
      },
    ),
    // Phase 2 Routes
    GoRoute(
      path: '/plan/:farmId',
      builder: (context, state) {
        final farmId = state.pathParameters['farmId'] ?? 'f_1';
        return TodaysPlanScreen(farmId: farmId);
      },
    ),
    GoRoute(
      path: '/health/:farmId',
      builder: (context, state) {
        final farmId = state.pathParameters['farmId'] ?? 'f_1';
        return FarmHealthScreen(farmId: farmId);
      },
    ),
    GoRoute(
      path: '/health/:farmId/history',
      builder: (context, state) {
        final farmId = state.pathParameters['farmId'] ?? 'f_1';
        return HealthHistoryScreen(farmId: farmId);
      },
    ),
    GoRoute(
      path: '/land/:farmId',
      builder: (context, state) {
        final farmId = state.pathParameters['farmId'] ?? 'f_1';
        return LandDetailsScreen(farmId: farmId);
      },
    ),
    GoRoute(
      path: '/land/:farmId/boundary',
      builder: (context, state) {
        final farmId = state.pathParameters['farmId'] ?? 'f_1';
        return LandBoundaryScreen(farmId: farmId);
      },
    ),
    GoRoute(
      path: '/land/status/:farmId',
      builder: (context, state) {
        final farmId = state.pathParameters['farmId'] ?? 'f_1';
        return LandStatusScreen(farmId: farmId);
      },
    ),
    // Phase 3 Routes
    GoRoute(
      path: '/ask/:farmId',
      builder: (context, state) {
        final farmId = state.pathParameters['farmId'] ?? 'f_1';
        return AskBhoomiScreen(farmId: farmId);
      },
    ),
    GoRoute(
      path: '/diagnosis/result/:farmId',
      builder: (context, state) {
        final farmId = state.pathParameters['farmId'] ?? 'f_1';
        return DiagnosisResultScreen(farmId: farmId);
      },
    ),
    GoRoute(
      path: '/timeline/:farmId',
      builder: (context, state) {
        final farmId = state.pathParameters['farmId'] ?? 'f_1';
        return FarmJourneyScreen(farmId: farmId);
      },
    ),
    GoRoute(
      path: '/followup/:farmId/:diagnosisId',
      builder: (context, state) {
        final farmId = state.pathParameters['farmId'] ?? 'f_1';
        final diagnosisId = state.pathParameters['diagnosisId'] ?? 'diag_101';
        return FollowupScreen(farmId: farmId, diagnosisId: diagnosisId);
      },
    ),
    GoRoute(
      path: '/escalation/:farmId/:diagnosisId',
      builder: (context, state) {
        final farmId = state.pathParameters['farmId'] ?? 'f_1';
        final diagnosisId = state.pathParameters['diagnosisId'] ?? 'diag_101';
        return EscalationScreen(farmId: farmId, diagnosisId: diagnosisId);
      },
    ),
    // Phase 4 Routes
    GoRoute(
      path: '/schemes/:farmId',
      builder: (context, state) {
        final farmId = state.pathParameters['farmId'] ?? 'f_1';
        return SchemesScreen(farmId: farmId);
      },
    ),
    GoRoute(
      path: '/schemes/detail/:schemeId',
      builder: (context, state) {
        final schemeId = state.pathParameters['schemeId'] ?? 'sch_pmkisan';
        return SchemeDetailScreen(schemeId: schemeId);
      },
    ),
    GoRoute(
      path: '/schemes/:farmId/:schemeId/info',
      builder: (context, state) {
        final farmId = state.pathParameters['farmId'] ?? 'f_1';
        final schemeId = state.pathParameters['schemeId'] ?? 'sch_pmkisan';
        return SchemeInformationScreen(farmId: farmId, schemeId: schemeId);
      },
    ),
    GoRoute(
      path: '/brief/:farmId',
      builder: (context, state) {
        final farmId = state.pathParameters['farmId'] ?? 'f_1';
        return TodaysFarmBriefScreen(farmId: farmId);
      },
    ),
    GoRoute(
      path: '/updates/:farmId',
      builder: (context, state) {
        final farmId = state.pathParameters['farmId'] ?? 'f_1';
        return FarmUpdatesScreen(farmId: farmId);
      },
    ),
  ],
  errorBuilder: (context, state) => Scaffold(
    body: Center(
      child: Text('Page not found: ${state.uri.toString()}'),
    ),
  ),
);
