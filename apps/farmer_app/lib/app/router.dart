import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../features/auth/presentation/providers/auth_providers.dart';
import '../features/auth/presentation/screens/login_screen.dart';
import '../features/auth/presentation/screens/otp_request_screen.dart';
import '../features/auth/presentation/screens/otp_verify_screen.dart';
import '../features/auth/presentation/screens/register_screen.dart';
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
import '../features/onboarding/data/farm_repository.dart';
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
import '../features/voice/presentation/screens/voice_qa_screen.dart';

class RouterNotifier extends ChangeNotifier {
  final Ref _ref;

  RouterNotifier(this._ref) {
    _ref.listen(authStateProvider, (_, __) {
      notifyListeners();
    });
  }
}

final routerNotifierProvider = Provider<RouterNotifier>((ref) {
  return RouterNotifier(ref);
});

final routerProvider = Provider<GoRouter>((ref) {
  final notifier = ref.watch(routerNotifierProvider);

  return GoRouter(
    refreshListenable: notifier,
    initialLocation: '/welcome',
    redirect: (context, state) async {
      final authValue = ref.read(authStateProvider);

      // Do not redirect while initial auth token check is in progress
      if (authValue.isLoading) return null;

      final isAuthenticated = authValue.value != null &&
          (authValue.value?.accessToken.isNotEmpty ?? false);

      final isAuthRoute = state.matchedLocation == '/login' ||
          state.matchedLocation == '/register' ||
          state.matchedLocation == '/otp-request' ||
          state.matchedLocation == '/otp-verify' ||
          state.matchedLocation == '/welcome' ||
          state.matchedLocation == '/auth';

      // 1. Unauthenticated user accessing a protected route -> Redirect to Login
      if (!isAuthenticated && !isAuthRoute) {
        return '/login';
      }

      // 2. Authenticated user accessing login/register/welcome -> Redirect to Home
      if (isAuthenticated &&
          (state.matchedLocation == '/login' ||
           state.matchedLocation == '/register' ||
           state.matchedLocation == '/welcome' ||
           state.matchedLocation == '/auth')) {
        // Route to the user's actual farm, never a hardcoded placeholder id
        // that may not exist server-side — see FarmRepository.firstFarmId().
        final farmId = await ref.read(farmRepositoryProvider).firstFarmId();
        return farmId != null ? '/home/$farmId' : '/onboarding';
      }

      return null;
    },
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
        path: '/login',
        builder: (context, state) => const LoginScreen(),
      ),
      GoRoute(
        path: '/register',
        builder: (context, state) => const RegisterScreen(),
      ),
      GoRoute(
        path: '/otp-request',
        builder: (context, state) => const OtpRequestScreen(),
      ),
      GoRoute(
        path: '/otp-verify',
        builder: (context, state) {
          final phone = state.uri.queryParameters['phone'] ?? '+919876543210';
          final debugOtp = state.uri.queryParameters['debugOtp'];
          return OtpVerifyScreen(
            phoneNumber: phone,
            initialDebugOtp: debugOtp,
          );
        },
      ),
      GoRoute(
        path: '/auth',
        builder: (context, state) => const LoginScreen(),
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
        path: '/voice-qa/:farmId',
        builder: (context, state) {
          final farmId = state.pathParameters['farmId'] ?? 'f_1';
          return VoiceQaScreen(farmId: farmId);
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
});

// Backward compatibility export for appRouter
final appRouter = GoRouter(
  initialLocation: '/welcome',
  routes: [
    GoRoute(path: '/', builder: (context, state) => const LoginScreen()),
  ],
);
