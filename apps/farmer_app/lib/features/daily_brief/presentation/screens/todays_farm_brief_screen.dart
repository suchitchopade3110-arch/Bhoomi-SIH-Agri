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

class TodaysFarmBriefScreen extends ConsumerStatefulWidget {
  final String farmId;

  const TodaysFarmBriefScreen({
    super.key,
    required this.farmId,
  });

  @override
  ConsumerState<TodaysFarmBriefScreen> createState() => _TodaysFarmBriefScreenState();
}

class _TodaysFarmBriefScreenState extends ConsumerState<TodaysFarmBriefScreen> {
  final Set<int> _completedTasks = {};

  @override
  Widget build(BuildContext context) {
    final briefAsync = ref.watch(dailyBriefProvider(widget.farmId));
    final voiceState = ref.watch(voiceControllerProvider);
    final voiceController = ref.read(voiceControllerProvider.notifier);

    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        title: const Text("Today's Guidance", style: TextStyle(fontWeight: FontWeight.w800)),
        scrolledUnderElevation: 0,
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
                      : "Today's Guidance for ${brief.crop} at ${brief.growthStage}. Important action: ${brief.importantAction ?? ''}. Farm priority: ${brief.farmPriority ?? ''}.";
                  voiceController.synthesizeAndSpeak(speech);
                }
              },
            ),
            orElse: () => const SizedBox.shrink(),
          ),
          IconButton(
            icon: const Icon(Icons.refresh_rounded),
            tooltip: 'Refresh Guidance',
            onPressed: () {
              ref.invalidate(dailyBriefProvider(widget.farmId));
            },
          ),
        ],
      ),
      body: SafeArea(
        child: briefAsync.when(
          loading: () => const BhoomiLoadingView(message: 'Generating today\'s field guidance...'),
          error: (error, _) => Center(
            child: Padding(
              padding: const EdgeInsets.all(AppSpacing.xl),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  const Icon(Icons.error_outline_rounded, size: 48.0, color: Color(0xFFC62828)),
                  const SizedBox(height: AppSpacing.md),
                  const Text('Unable to Load Daily Guidance', style: AppTypography.headlineMedium),
                  const SizedBox(height: AppSpacing.sm),
                  Text(error.toString(), textAlign: TextAlign.center, style: const TextStyle(color: AppColors.textMuted)),
                  const SizedBox(height: AppSpacing.lg),
                  BhoomiPrimaryButton(
                    text: 'Retry',
                    onPressed: () => ref.invalidate(dailyBriefProvider(widget.farmId)),
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
                // Weather & Conditions Card (Location, Date, Temp, Weather, Humidity, Wind)
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
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          Row(
                            children: [
                              const Icon(Icons.location_on_rounded, color: AppColors.accentGold, size: 18.0),
                              const SizedBox(width: 4.0),
                              Text(
                                '${brief.crop} Field',
                                style: const TextStyle(color: Colors.white, fontSize: 14.0, fontWeight: FontWeight.w700),
                              ),
                            ],
                          ),
                          Container(
                            padding: const EdgeInsets.symmetric(horizontal: 10.0, vertical: 3.0),
                            decoration: BoxDecoration(
                              color: Colors.white.withValues(alpha: 0.15),
                              borderRadius: BorderRadius.circular(AppSpacing.radiusFull),
                            ),
                            child: Text(
                              brief.growthStage,
                              style: const TextStyle(color: Colors.white, fontSize: 11.0, fontWeight: FontWeight.w600),
                            ),
                          ),
                        ],
                      ),
                      const SizedBox(height: AppSpacing.md),
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(
                                brief.weatherContext?.temperatureRange ?? '28°C - 34°C',
                                style: const TextStyle(
                                  fontSize: 32.0,
                                  fontWeight: FontWeight.w900,
                                  color: Colors.white,
                                ),
                              ),
                              Text(
                                brief.weatherContext?.summary ?? 'Partly Sunny • Good Spray Window',
                                style: TextStyle(
                                  color: Colors.white.withValues(alpha: 0.9),
                                  fontSize: 13.0,
                                  fontWeight: FontWeight.w500,
                                ),
                              ),
                            ],
                          ),
                          Container(
                            padding: const EdgeInsets.all(AppSpacing.md),
                            decoration: BoxDecoration(
                              color: Colors.white.withValues(alpha: 0.15),
                              shape: BoxShape.circle,
                            ),
                            child: const Icon(Icons.wb_sunny_rounded, color: AppColors.accentGold, size: 36.0),
                          ),
                        ],
                      ),
                      const SizedBox(height: AppSpacing.md),
                      const Divider(color: Colors.white24),
                      const SizedBox(height: AppSpacing.xs),
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          _buildWeatherMetric(Icons.water_drop_outlined, 'Humidity', '68%'),
                          _buildWeatherMetric(Icons.air_rounded, 'Wind', '12 km/h'),
                          _buildWeatherMetric(Icons.umbrella_outlined, 'Rain Risk', brief.weatherContext?.rainRisk ?? 'Low'),
                        ],
                      ),
                    ],
                  ),
                ),

                const SizedBox(height: AppSpacing.lg),

                // Section: Today's Farm Tasks (Checklist)
                Row(
                  mainAxisAlignment: MainAxisAlignment.spaceBetween,
                  children: [
                    const Text(
                      "Today's Farm Tasks",
                      style: TextStyle(
                        fontSize: 18.0,
                        fontWeight: FontWeight.w800,
                        color: AppColors.textPrimary,
                      ),
                    ),
                    Text(
                      '${_completedTasks.length}/${(brief.cropWatch.length + (brief.importantAction != null ? 1 : 0) + (brief.farmPriority != null ? 1 : 0))} done',
                      style: const TextStyle(fontSize: 12.0, color: AppColors.primaryGreen, fontWeight: FontWeight.w700),
                    ),
                  ],
                ),
                const SizedBox(height: AppSpacing.md),

                // Top Priority Action as Task 0
                if (brief.importantAction != null) ...[
                  _buildTaskChecklistCard(
                    taskId: 0,
                    title: 'Priority: ${brief.importantAction!}',
                    subtitle: 'Critical action for ${brief.growthStage} stage',
                    icon: Icons.priority_high_rounded,
                    tagColor: const Color(0xFFD97706),
                  ),
                  const SizedBox(height: AppSpacing.sm),
                ],

                // Scheduled Farm Priority as Task 1
                if (brief.farmPriority != null) ...[
                  _buildTaskChecklistCard(
                    taskId: 1,
                    title: brief.farmPriority!,
                    subtitle: 'Scheduled irrigation & nutrient application',
                    icon: Icons.water_drop_rounded,
                    tagColor: const Color(0xFF0284C7),
                  ),
                  const SizedBox(height: AppSpacing.sm),
                ],

                // Crop Watch Items as subsequent tasks
                ...brief.cropWatch.asMap().entries.map((entry) {
                  final idx = entry.key + 2;
                  return Padding(
                    padding: const EdgeInsets.only(bottom: AppSpacing.sm),
                    child: _buildTaskChecklistCard(
                      taskId: idx,
                      title: entry.value,
                      subtitle: 'Field surveillance & disease scouting',
                      icon: Icons.search_rounded,
                      tagColor: AppColors.primaryGreen,
                    ),
                  );
                }),

                const SizedBox(height: AppSpacing.xl),
              ],
            ),
          ),
        ),
      ),
    );
  }

  Widget _buildWeatherMetric(IconData icon, String label, String value) {
    return Row(
      children: [
        Icon(icon, color: Colors.white70, size: 16.0),
        const SizedBox(width: 4.0),
        Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(label, style: const TextStyle(color: Colors.white60, fontSize: 10.0)),
            Text(value, style: const TextStyle(color: Colors.white, fontSize: 12.0, fontWeight: FontWeight.w700)),
          ],
        ),
      ],
    );
  }

  Widget _buildTaskChecklistCard({
    required int taskId,
    required String title,
    required String subtitle,
    required IconData icon,
    required Color tagColor,
  }) {
    final isDone = _completedTasks.contains(taskId);

    return BhoomiCard(
      padding: const EdgeInsets.symmetric(horizontal: AppSpacing.md, vertical: AppSpacing.md),
      child: InkWell(
        onTap: () {
          setState(() {
            if (isDone) {
              _completedTasks.remove(taskId);
            } else {
              _completedTasks.add(taskId);
            }
          });
        },
        child: Row(
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            // Checkbox
            Container(
              width: 24.0,
              height: 24.0,
              decoration: BoxDecoration(
                color: isDone ? AppColors.primaryGreen : Colors.transparent,
                shape: BoxShape.circle,
                border: Border.all(
                  color: isDone ? AppColors.primaryGreen : AppColors.border,
                  width: 2.0,
                ),
              ),
              child: isDone
                  ? const Icon(Icons.check_rounded, size: 16.0, color: Colors.white)
                  : null,
            ),
            const SizedBox(width: AppSpacing.md),

            // Content
            Expanded(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: [
                  Text(
                    title,
                    style: TextStyle(
                      fontSize: 14.0,
                      fontWeight: FontWeight.w700,
                      color: isDone ? AppColors.textMuted : AppColors.textPrimary,
                      decoration: isDone ? TextDecoration.lineThrough : null,
                    ),
                  ),
                  const SizedBox(height: 2.0),
                  Text(
                    subtitle,
                    style: const TextStyle(fontSize: 11.5, color: AppColors.textMuted),
                  ),
                ],
              ),
            ),
          ],
        ),
      ),
    );
  }
}
