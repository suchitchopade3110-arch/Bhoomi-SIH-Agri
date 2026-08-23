import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../../../app/theme/app_colors.dart';
import '../../../../app/theme/app_spacing.dart';
import '../../../../app/theme/app_typography.dart';
import '../../../../core/widgets/bhoomi_loading_view.dart';
import '../../../../core/widgets/bhoomi_primary_button.dart';
import '../../application/health_provider.dart';
import '../widgets/health_breakdown_card.dart';
import '../widgets/health_score_card.dart';

class FarmHealthScreen extends ConsumerWidget {
  final String farmId;

  const FarmHealthScreen({
    super.key,
    required this.farmId,
  });

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final healthAsync = ref.watch(farmHealthProvider(farmId));

    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        title: const Text('Farm Health & Diagnosis'),
        actions: [
          IconButton(
            icon: const Icon(Icons.history_rounded),
            tooltip: 'Health History',
            onPressed: () {
              context.push('/health/$farmId/history');
            },
          ),
          IconButton(
            icon: const Icon(Icons.refresh_rounded),
            tooltip: 'Recompute Health',
            onPressed: () {
              ref.invalidate(farmHealthProvider(farmId));
            },
          ),
        ],
      ),
      body: SafeArea(
        child: healthAsync.when(
          loading: () => const BhoomiLoadingView(message: 'Analyzing farm health snapshot...'),
          error: (error, _) => Center(
            child: Padding(
              padding: const EdgeInsets.all(AppSpacing.xl),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  const Icon(Icons.error_outline, size: 48.0, color: Color(0xFFC62828)),
                  const SizedBox(height: AppSpacing.md),
                  const Text('Unable to Load Health Data', style: AppTypography.headlineMedium),
                  const SizedBox(height: AppSpacing.sm),
                  Text(error.toString(), textAlign: TextAlign.center, style: const TextStyle(color: AppColors.textMuted)),
                  const SizedBox(height: AppSpacing.lg),
                  BhoomiPrimaryButton(
                    text: 'Retry',
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
                  text: 'View Health Journey Timeline',
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
    );
  }
}
