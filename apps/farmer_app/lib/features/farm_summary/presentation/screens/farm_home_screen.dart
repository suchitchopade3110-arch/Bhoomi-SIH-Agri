import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../../../app/theme/app_colors.dart';
import '../../../../app/theme/app_spacing.dart';
import '../../../../app/theme/app_typography.dart';
import '../../../../core/connectivity/connectivity_service.dart';
import '../../../../core/widgets/bhoomi_loading_view.dart';
import '../../../../core/widgets/bhoomi_primary_button.dart';
import '../../../../core/widgets/degraded_network_banner.dart';
import '../../../daily_brief/application/daily_brief_controller.dart';
import '../../../home/presentation/widgets/daily_brief_preview.dart';
import '../../../home/presentation/widgets/latest_update_preview.dart';
import '../../../home/presentation/widgets/quick_action_grid.dart';
import '../../../land/presentation/widgets/land_status_badge.dart';
import '../../../schemes/application/schemes_controller.dart';
import '../../../updates/application/updates_controller.dart';
import '../../application/farm_summary_provider.dart';
import '../widgets/farm_identity_card.dart';

class FarmHomeScreen extends ConsumerWidget {
  final String farmId;

  const FarmHomeScreen({
    super.key,
    required this.farmId,
  });

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final summaryAsync = ref.watch(farmSummaryProvider(farmId));
    final networkState = ref.watch(networkStateProvider);

    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        title: const Text('BHOOMI'),
        centerTitle: false,
        actions: [
          IconButton(
            icon: const Icon(Icons.notifications_outlined),
            tooltip: 'Farm Updates',
            onPressed: () {
              context.push('/updates/$farmId');
            },
          ),
          IconButton(
            icon: const Icon(Icons.refresh_rounded),
            tooltip: 'Refresh Farm Data',
            onPressed: () {
              ref.invalidate(farmSummaryProvider(farmId));
              ref.invalidate(dailyBriefProvider(farmId));
              ref.invalidate(schemesListProvider(farmId));
              ref.invalidate(farmUpdatesProvider(farmId));
            },
          ),
        ],
      ),
      body: SafeArea(
        child: Column(
          children: [
            // Degraded Network Mode Banner
            DegradedNetworkBanner(networkState: networkState),

            Expanded(
              child: summaryAsync.when(
                loading: () => const BhoomiLoadingView(message: 'Loading your farm companion...'),
                error: (error, _) => _buildErrorView(context, ref, error),
                data: (summary) => RefreshIndicator(
                  color: AppColors.primaryGreen,
                  onRefresh: () async {
                    ref.invalidate(farmSummaryProvider(farmId));
                    ref.invalidate(dailyBriefProvider(farmId));
                    ref.invalidate(schemesListProvider(farmId));
                    ref.invalidate(farmUpdatesProvider(farmId));
                  },
                  child: SingleChildScrollView(
                    physics: const AlwaysScrollableScrollPhysics(),
                    padding: const EdgeInsets.symmetric(
                      horizontal: AppSpacing.lg,
                      vertical: AppSpacing.md,
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.stretch,
                      children: [
                        // Header Greeting & Farm Identity
                        _buildHeader(summary.farm.crop, summary.farm.landStatus),

                        const SizedBox(height: AppSpacing.lg),

                        // Farm Identity Card
                        FarmIdentityCard(farm: summary.farm),

                        const SizedBox(height: AppSpacing.lg),

                        // Section 1: TODAY'S FARM BRIEF (Proactive advice preview)
                        DailyBriefPreview(farmId: farmId),

                        const SizedBox(height: AppSpacing.lg),

                        // Section 2: WHAT WOULD YOU LIKE TO DO? (Quick Action Grid)
                        QuickActionGrid(
                          farmId: farmId,
                          isLandVerified: summary.farm.landStatus == 'verified',
                        ),

                        const SizedBox(height: AppSpacing.lg),

                        // Section 3: LATEST UPDATES (Proactive alerts preview)
                        LatestUpdatePreview(farmId: farmId),

                        const SizedBox(height: AppSpacing.xxl),
                      ],
                    ),
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildHeader(String crop, String landStatus) {
    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: [
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text('Daily Companion', style: AppTypography.bodyMedium.copyWith(color: AppColors.textMuted)),
              const Text('My Farm', style: AppTypography.displayMedium),
            ],
          ),
        ),
        const SizedBox(width: AppSpacing.sm),
        LandStatusBadge(status: landStatus),
      ],
    );
  }

  Widget _buildErrorView(BuildContext context, WidgetRef ref, Object error) {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(AppSpacing.xl),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Icon(Icons.error_outline_rounded, size: 48.0, color: Color(0xFFC62828)),
            const SizedBox(height: AppSpacing.md),
            const Text('Unable to Load Farm Dashboard', style: AppTypography.headlineMedium),
            const SizedBox(height: AppSpacing.sm),
            Text(error.toString(), textAlign: TextAlign.center, style: const TextStyle(color: AppColors.textMuted)),
            const SizedBox(height: AppSpacing.lg),
            BhoomiPrimaryButton(
              text: 'Retry',
              onPressed: () => ref.invalidate(farmSummaryProvider(farmId)),
            ),
          ],
        ),
      ),
    );
  }
}
