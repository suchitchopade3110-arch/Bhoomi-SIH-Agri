import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../../../app/theme/app_colors.dart';
import '../../../../app/theme/app_spacing.dart';
import '../../../../app/theme/app_typography.dart';
import '../../../../core/localization/bhoomi_localizations.dart';
import '../../../../core/widgets/bhoomi_loading_view.dart';
import '../../../../core/widgets/bhoomi_primary_button.dart';
import '../../application/health_provider.dart';
import '../widgets/health_breakdown_card.dart';
import '../widgets/health_score_card.dart';
import '../../../../shared/widgets/bhoomi_bottom_navigation.dart';

class FarmHealthScreen extends ConsumerWidget {
  final String farmId;

  const FarmHealthScreen({
    super.key,
    required this.farmId,
  });

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final healthAsync = ref.watch(farmHealthProvider(farmId));
    final strings = ref.watch(bhoomiStringsProvider);

    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        title: Text(strings.text('farm_health_title')),
        actions: [
          IconButton(
            icon: const Icon(Icons.history_rounded),
            tooltip: strings.text('health_history'),
            onPressed: () {
              context.push('/health/$farmId/history');
            },
          ),
          IconButton(
            icon: const Icon(Icons.refresh_rounded),
            tooltip: strings.text('recompute_health'),
            onPressed: () {
              ref.invalidate(farmHealthProvider(farmId));
            },
          ),
        ],
      ),
      body: SafeArea(
        child: healthAsync.when(
          loading: () => BhoomiLoadingView(message: strings.text('analyzing_health')),
          error: (error, _) => Center(
            child: Padding(
              padding: const EdgeInsets.all(AppSpacing.xl),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  const Icon(Icons.error_outline, size: 48.0, color: Color(0xFFC62828)),
                  const SizedBox(height: AppSpacing.md),
                  Text(strings.text('unable_load_health'), style: AppTypography.headlineMedium),
                  const SizedBox(height: AppSpacing.sm),
                  Text(error.toString(), textAlign: TextAlign.center, style: const TextStyle(color: AppColors.textMuted)),
                  const SizedBox(height: AppSpacing.lg),
                  BhoomiPrimaryButton(
                    text: strings.retry,
                    onPressed: () => ref.invalidate(farmHealthProvider(farmId)),
                  ),
                ],
              ),
            ),
          ),
          data: (snapshot) => SingleChildScrollView(
            padding: const EdgeInsets.all(AppSpacing.lg),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                HealthScoreCard(snapshot: snapshot),

                if (snapshot.subIndices != null) ...[
                  const SizedBox(height: AppSpacing.lg),
                  HealthBreakdownCard(subIndices: snapshot.subIndices!),
                ],

                const SizedBox(height: AppSpacing.lg),

                // Navigate to Health Journey
                BhoomiPrimaryButton(
                  text: strings.text('view_health_journey'),
                  icon: Icons.timeline_rounded,
                  onPressed: () {
                    context.push('/health/$farmId/history');
                  },
                ),

                const SizedBox(height: AppSpacing.xl),
              ],
            ),
          ),
        ),
      ),
      bottomNavigationBar: BhoomiBottomNavigation(farmId: farmId, currentIndex: 3),
    );
  }
}
