import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../../app/theme/app_colors.dart';
import '../../../../app/theme/app_spacing.dart';
import '../../../../app/theme/app_typography.dart';
import '../../../../core/widgets/bhoomi_card.dart';
import '../../../../core/widgets/bhoomi_loading_view.dart';
import '../../../../core/widgets/bhoomi_primary_button.dart';
import '../../../voice/application/voice_controller.dart';
import '../../application/daily_brief_controller.dart';

class TodaysFarmBriefScreen extends ConsumerWidget {
  final String farmId;

  const TodaysFarmBriefScreen({
    super.key,
    required this.farmId,
  });

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final briefAsync = ref.watch(dailyBriefProvider(farmId));
    final voiceState = ref.watch(voiceControllerProvider);
    final voiceController = ref.read(voiceControllerProvider.notifier);

    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        title: const Text("Today's Farm Brief"),
        actions: [
          briefAsync.maybeWhen(
            data: (brief) => IconButton(
              icon: Icon(
                voiceState.isPlaying ? Icons.stop_circle_rounded : Icons.volume_up_rounded,
                color: AppColors.primaryGreen,
                size: 26.0,
              ),
              tooltip: voiceState.isPlaying ? 'Stop Audio' : 'Listen to Brief',
              onPressed: () {
                if (voiceState.isPlaying) {
                  voiceController.stopPlayback();
                } else {
                  final speech = (brief.spokenSummary != null && brief.spokenSummary!.trim().isNotEmpty)
                      ? brief.spokenSummary!
                      : "Today's Farm Brief for ${brief.crop} at ${brief.growthStage}. Important action: ${brief.importantAction ?? ''}. Farm priority: ${brief.farmPriority ?? ''}.";
                  voiceController.synthesizeAndSpeak(speech);
                }
              },
            ),
            orElse: () => const SizedBox.shrink(),
          ),
          IconButton(
            icon: const Icon(Icons.refresh_rounded),
            tooltip: 'Refresh Brief',
            onPressed: () {
              ref.invalidate(dailyBriefProvider(farmId));
            },
          ),
        ],
      ),
      body: SafeArea(
        child: briefAsync.when(
          loading: () => const BhoomiLoadingView(message: 'Generating today\'s field brief...'),
          error: (error, _) => Center(
            child: Padding(
              padding: const EdgeInsets.all(AppSpacing.xl),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  const Icon(Icons.error_outline_rounded, size: 48.0, color: Color(0xFFC62828)),
                  const SizedBox(height: AppSpacing.md),
                  const Text('Unable to Load Daily Brief', style: AppTypography.headlineMedium),
                  const SizedBox(height: AppSpacing.sm),
                  Text(error.toString(), textAlign: TextAlign.center, style: const TextStyle(color: AppColors.textMuted)),
                  const SizedBox(height: AppSpacing.lg),
                  BhoomiPrimaryButton(
                    text: 'Retry',
                    onPressed: () => ref.invalidate(dailyBriefProvider(farmId)),
                  ),
                ],
              ),
            ),
          ),
          data: (brief) => SingleChildScrollView(
            padding: const EdgeInsets.all(AppSpacing.lg),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                // Header Context Card
                Container(
                  padding: const EdgeInsets.all(AppSpacing.lg),
                  decoration: BoxDecoration(
                    gradient: const LinearGradient(
                      colors: [AppColors.primaryGreen, Color(0xFF1B5E20)],
                      begin: Alignment.topLeft,
                      end: Alignment.bottomRight,
                    ),
                    borderRadius: BorderRadius.circular(AppSpacing.radiusLg),
                  ),
                  child: Row(
                    children: [
                      Container(
                        padding: const EdgeInsets.all(AppSpacing.md),
                        decoration: BoxDecoration(
                          color: Colors.white.withValues(alpha: 0.2),
                          shape: BoxShape.circle,
                        ),
                        child: const Icon(Icons.wb_sunny_rounded, color: Colors.white, size: 28.0),
                      ),
                      const SizedBox(width: AppSpacing.md),
                      Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              "${brief.crop} • ${brief.growthStage}",
                              style: const TextStyle(color: Colors.white, fontSize: 18.0, fontWeight: FontWeight.w800),
                            ),
                            const SizedBox(height: 2.0),
                            Text(
                              brief.advisorySummary,
                              style: const TextStyle(color: Colors.white70, fontSize: 12.0),
                            ),
                          ],
                        ),
                      ),
                    ],
                  ),
                ),

                const SizedBox(height: AppSpacing.lg),

                // 1. Important Action Card
                if (brief.importantAction != null) ...[
                  BhoomiCard(
                    padding: const EdgeInsets.all(AppSpacing.lg),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Row(
                          children: [
                            Icon(Icons.priority_high_rounded, color: Color(0xFFD97706), size: 20.0),
                            SizedBox(width: AppSpacing.sm),
                            Text('Top Priority Action', style: AppTypography.titleLarge),
                          ],
                        ),
                        const Divider(color: AppColors.divider, height: AppSpacing.lg),
                        Text(
                          brief.importantAction!,
                          style: AppTypography.bodyLarge.copyWith(
                            fontWeight: FontWeight.w700,
                            color: AppColors.textPrimary,
                          ),
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(height: AppSpacing.lg),
                ],

                // 2. Farm Priority Card
                if (brief.farmPriority != null) ...[
                  BhoomiCard(
                    padding: const EdgeInsets.all(AppSpacing.lg),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Row(
                          children: [
                            Icon(Icons.water_drop_outlined, color: Color(0xFF0284C7), size: 20.0),
                            SizedBox(width: AppSpacing.sm),
                            Text('Scheduled Field Priority', style: AppTypography.titleLarge),
                          ],
                        ),
                        const Divider(color: AppColors.divider, height: AppSpacing.lg),
                        Text(
                          brief.farmPriority!,
                          style: AppTypography.bodyMedium.copyWith(color: AppColors.textSecondary),
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(height: AppSpacing.lg),
                ],

                // 3. Weather Context Card
                if (brief.weatherContext != null) ...[
                  BhoomiCard(
                    padding: const EdgeInsets.all(AppSpacing.lg),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Row(
                          children: [
                            Icon(Icons.cloud_queue_rounded, color: AppColors.primaryGreen, size: 20.0),
                            SizedBox(width: AppSpacing.sm),
                            Text('Weather & Spray Conditions', style: AppTypography.titleLarge),
                          ],
                        ),
                        const Divider(color: AppColors.divider, height: AppSpacing.lg),
                        Row(
                          mainAxisAlignment: MainAxisAlignment.spaceBetween,
                          children: [
                            Text(
                              brief.weatherContext!.summary,
                              style: AppTypography.bodyMedium.copyWith(fontWeight: FontWeight.w600),
                            ),
                            Text(
                              brief.weatherContext!.temperatureRange,
                              style: const TextStyle(fontWeight: FontWeight.w800, color: AppColors.primaryGreen),
                            ),
                          ],
                        ),
                        const SizedBox(height: 4.0),
                        Text(
                          'Rain Probability: ${brief.weatherContext!.rainRisk}',
                          style: const TextStyle(fontSize: 11.0, color: AppColors.textMuted),
                        ),
                      ],
                    ),
                  ),
                  const SizedBox(height: AppSpacing.lg),
                ],

                // 4. Crop Watch List
                if (brief.cropWatch.isNotEmpty) ...[
                  BhoomiCard(
                    padding: const EdgeInsets.all(AppSpacing.lg),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Row(
                          children: [
                            Icon(Icons.remove_red_eye_outlined, color: AppColors.primaryGreen, size: 20.0),
                            SizedBox(width: AppSpacing.sm),
                            Text('Crop Watch Items', style: AppTypography.titleLarge),
                          ],
                        ),
                        const Divider(color: AppColors.divider, height: AppSpacing.lg),
                        ...brief.cropWatch.map((item) => Padding(
                              padding: const EdgeInsets.only(bottom: AppSpacing.sm),
                              child: Row(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  const Icon(Icons.check_circle_outline_rounded, size: 16.0, color: AppColors.primaryGreen),
                                  const SizedBox(width: AppSpacing.sm),
                                  Expanded(child: Text(item, style: AppTypography.bodyMedium)),
                                ],
                              ),
                            )),
                      ],
                    ),
                  ),
                ],

                const SizedBox(height: AppSpacing.xl),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
