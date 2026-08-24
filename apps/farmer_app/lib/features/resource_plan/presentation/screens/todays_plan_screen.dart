import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../../app/theme/app_colors.dart';
import '../../../../app/theme/app_spacing.dart';
import '../../../../app/theme/app_typography.dart';
import '../../../../core/widgets/bhoomi_card.dart';
import '../../../../core/widgets/bhoomi_loading_view.dart';
import '../../../../core/widgets/bhoomi_primary_button.dart';
import '../../application/resource_plan_controller.dart';
import '../widgets/irrigation_card.dart';
import '../widgets/seed_requirement_card.dart';

class TodaysPlanScreen extends ConsumerWidget {
  final String farmId;

  const TodaysPlanScreen({
    super.key,
    required this.farmId,
  });

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final planAsync = ref.watch(latestResourcePlanProvider(farmId));

    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        title: const Text("Today's Farm Plan", style: TextStyle(fontWeight: FontWeight.w800)),
        scrolledUnderElevation: 0,
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh_rounded),
            tooltip: 'Refresh Plan',
            onPressed: () {
              ref.invalidate(latestResourcePlanProvider(farmId));
            },
          ),
        ],
      ),
      body: SafeArea(
        child: planAsync.when(
          loading: () => const BhoomiLoadingView(message: "Generating today's farm plan...", showSprout: true),
          error: (error, _) => Center(
            child: Padding(
              padding: const EdgeInsets.all(AppSpacing.xl),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  const Icon(Icons.error_outline, size: 48.0, color: Color(0xFFC62828)),
                  const SizedBox(height: AppSpacing.md),
                  const Text('Unable to Load Resource Plan', style: AppTypography.headlineMedium),
                  const SizedBox(height: AppSpacing.sm),
                  Text(error.toString(), style: const TextStyle(color: AppColors.textMuted), textAlign: TextAlign.center),
                  const SizedBox(height: AppSpacing.lg),
                  BhoomiPrimaryButton(
                    text: 'Retry',
                    onPressed: () => ref.invalidate(latestResourcePlanProvider(farmId)),
                  ),
                ],
              ),
            ),
          ),
          data: (plan) => SingleChildScrollView(
            padding: const EdgeInsets.all(AppSpacing.lg),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                // Header Context Card
                Container(
                  padding: const EdgeInsets.all(AppSpacing.lg),
                  decoration: BoxDecoration(
                    gradient: const LinearGradient(
                      colors: [AppColors.primaryDeepGreen, Color(0xFF165428)],
                      begin: Alignment.topLeft,
                      end: Alignment.bottomRight,
                    ),
                    borderRadius: BorderRadius.circular(AppSpacing.radiusXl),
                    boxShadow: const [
                      BoxShadow(
                        color: AppColors.cardShadowHover,
                        blurRadius: 16.0,
                        offset: Offset(0, 6),
                      ),
                    ],
                  ),
                  child: Row(
                    children: [
                      Container(
                        padding: const EdgeInsets.all(AppSpacing.md),
                        decoration: BoxDecoration(
                          color: Colors.white.withValues(alpha: 0.15),
                          shape: BoxShape.circle,
                        ),
                        child: const Icon(Icons.wb_twilight_rounded, color: AppColors.accentGold, size: 28.0),
                      ),
                      const SizedBox(width: AppSpacing.md),
                      const Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              "Daily Farming Guidance",
                              style: TextStyle(
                                color: Colors.white,
                                fontSize: 18.0,
                                fontWeight: FontWeight.w800,
                              ),
                            ),
                            SizedBox(height: 2.0),
                            Text(
                              'Optimized daily water, market price, and resource schedules.',
                              style: TextStyle(color: Colors.white70, fontSize: 12.0),
                            ),
                          ],
                        ),
                      ),
                    ],
                  ),
                ),

                const SizedBox(height: AppSpacing.lg),

                // 1. Weather Forecast 3-Day Layout
                BhoomiCard(
                  padding: const EdgeInsets.all(AppSpacing.lg),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      const Row(
                        children: [
                          Icon(Icons.cloud_queue_rounded, color: AppColors.primaryGreen, size: 20.0),
                          SizedBox(width: AppSpacing.sm),
                          Text(
                            '3-Day Weather Outlook',
                            style: TextStyle(fontSize: 16.0, fontWeight: FontWeight.w800, color: AppColors.textPrimary),
                          ),
                        ],
                      ),
                      const SizedBox(height: AppSpacing.md),
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          _buildDayForecast('Today', '28°C', Icons.wb_sunny_rounded, AppColors.accentGold),
                          _buildDayForecast('Tomorrow', '30°C', Icons.wb_sunny_rounded, AppColors.accentGold),
                          _buildDayForecast('Day After', '29°C', Icons.cloud_rounded, const Color(0xFF60A5FA)),
                        ],
                      ),
                    ],
                  ),
                ),

                const SizedBox(height: AppSpacing.lg),

                // 2. Market Price Card
                BhoomiCard(
                  padding: const EdgeInsets.all(AppSpacing.lg),
                  child: Row(
                    mainAxisAlignment: MainAxisAlignment.spaceBetween,
                    children: [
                      const Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Row(
                            children: [
                              Icon(Icons.trending_up_rounded, color: AppColors.primaryGreen, size: 18.0),
                              SizedBox(width: AppSpacing.xs),
                              Text(
                                'Mandi Market Price (Paddy)',
                                style: TextStyle(fontSize: 12.5, fontWeight: FontWeight.w600, color: AppColors.textMuted),
                              ),
                            ],
                          ),
                          SizedBox(height: 4.0),
                          Text(
                            '₹2,150 / Quintal',
                            style: TextStyle(fontSize: 22.0, fontWeight: FontWeight.w900, color: AppColors.textPrimary),
                          ),
                        ],
                      ),
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: 10.0, vertical: 4.0),
                        decoration: BoxDecoration(
                          color: AppColors.lightGreen,
                          borderRadius: BorderRadius.circular(AppSpacing.radiusFull),
                        ),
                        child: const Row(
                          children: [
                            Icon(Icons.arrow_upward_rounded, size: 14.0, color: AppColors.primaryGreen),
                            SizedBox(width: 2.0),
                            Text(
                              '2.4%',
                              style: TextStyle(fontSize: 12.0, fontWeight: FontWeight.w800, color: AppColors.primaryGreen),
                            ),
                          ],
                        ),
                      ),
                    ],
                  ),
                ),

                const SizedBox(height: AppSpacing.lg),

                // 3. Irrigation Card
                IrrigationCard(plan: plan),

                const SizedBox(height: AppSpacing.lg),

                // 4. Seed Requirement Card
                SeedRequirementCard(plan: plan),

                const SizedBox(height: AppSpacing.xl),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildDayForecast(String day, String temp, IconData icon, Color iconColor) {
    return Expanded(
      child: Container(
        margin: const EdgeInsets.symmetric(horizontal: 4.0),
        padding: const EdgeInsets.symmetric(vertical: AppSpacing.md, horizontal: AppSpacing.sm),
        decoration: BoxDecoration(
          color: AppColors.background,
          borderRadius: BorderRadius.circular(AppSpacing.radiusMd),
          border: Border.all(color: AppColors.border),
        ),
        child: Column(
          children: [
            Text(day, style: const TextStyle(fontSize: 11.5, fontWeight: FontWeight.w600, color: AppColors.textMuted)),
            const SizedBox(height: 6.0),
            Icon(icon, size: 24.0, color: iconColor),
            const SizedBox(height: 6.0),
            Text(temp, style: const TextStyle(fontSize: 15.0, fontWeight: FontWeight.w800, color: AppColors.textPrimary)),
          ],
        ),
      ),
    );
  }
}
