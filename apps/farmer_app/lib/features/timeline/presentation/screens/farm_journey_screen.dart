import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../../app/theme/app_colors.dart';
import '../../../../app/theme/app_spacing.dart';
import '../../../../app/theme/app_typography.dart';
import '../../../../core/localization/bhoomi_localizations.dart';
import '../../../../core/widgets/bhoomi_loading_view.dart';
import '../../../../core/widgets/bhoomi_primary_button.dart';
import '../../application/timeline_provider.dart';
import '../widgets/journey_timeline.dart';
import '../../../../shared/widgets/bhoomi_bottom_navigation.dart';

class FarmJourneyScreen extends ConsumerWidget {
  final String farmId;

  const FarmJourneyScreen({
    super.key,
    required this.farmId,
  });

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final timelineAsync = ref.watch(farmTimelineProvider(farmId));
    final strings = ref.watch(bhoomiStringsProvider);

    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        title: Text(strings.text('timeline_title')),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh_rounded),
            tooltip: strings.text('refresh_timeline'),
            onPressed: () {
              ref.invalidate(farmTimelineProvider(farmId));
            },
          ),
        ],
      ),
      body: SafeArea(
        child: timelineAsync.when(
          loading: () => BhoomiLoadingView(message: strings.text('loading_journey')),
          error: (error, _) => Center(
            child: Padding(
              padding: const EdgeInsets.all(AppSpacing.xl),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  const Icon(Icons.error_outline_rounded, size: 48.0, color: Color(0xFFC62828)),
                  const SizedBox(height: AppSpacing.md),
                  Text(strings.text('unable_load_timeline'), style: AppTypography.headlineMedium),
                  const SizedBox(height: AppSpacing.sm),
                  Text(error.toString(), textAlign: TextAlign.center, style: const TextStyle(color: AppColors.textMuted)),
                  const SizedBox(height: AppSpacing.lg),
                  BhoomiPrimaryButton(
                    text: strings.retry,
                    onPressed: () => ref.invalidate(farmTimelineProvider(farmId)),
                  ),
                ],
              ),
            ),
          ),
          data: (timeline) => SingleChildScrollView(
            padding: const EdgeInsets.all(AppSpacing.lg),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                // Header Banner (Redesigned without gradients)
                Container(
                  padding: const EdgeInsets.all(AppSpacing.lg),
                  decoration: BoxDecoration(
                    color: AppColors.surface,
                    borderRadius: BorderRadius.circular(AppSpacing.radiusLg),
                    border: Border.all(color: AppColors.border),
                    boxShadow: const [
                      BoxShadow(
                        color: AppColors.cardShadow,
                        blurRadius: 10.0,
                        offset: Offset(0, 4),
                      ),
                    ],
                  ),
                  child: Row(
                    children: [
                      Container(
                        padding: const EdgeInsets.all(AppSpacing.md),
                        decoration: const BoxDecoration(
                          color: AppColors.lightGreen,
                          shape: BoxShape.circle,
                        ),
                        child: const Icon(Icons.history_edu_rounded, color: AppColors.primaryGreen, size: 28.0),
                      ),
                      const SizedBox(width: AppSpacing.md),
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              strings.text('timeline_header'),
                              style: const TextStyle(color: AppColors.textPrimary, fontSize: 18.0, fontWeight: FontWeight.w800),
                            ),
                            const SizedBox(height: 2.0),
                            Text(
                              strings.text('timeline_header_desc'),
                              style: const TextStyle(color: AppColors.textSecondary, fontSize: 12.0),
                            ),
                          ],
                        ),
                      ),
                    ],
                  ),
                ),

                const SizedBox(height: AppSpacing.lg),

                // Journey Timeline
                JourneyTimelineWidget(events: timeline.events),

                const SizedBox(height: AppSpacing.xl),
              ],
            ),
          ),
        ),
      ),
      bottomNavigationBar: BhoomiBottomNavigation(farmId: farmId, currentIndex: 2),
    );
  }
}
