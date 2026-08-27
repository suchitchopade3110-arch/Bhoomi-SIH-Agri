import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../../../app/theme/app_colors.dart';
import '../../../../app/theme/app_spacing.dart';
import '../../../../core/localization/bhoomi_localizations.dart';
import '../../../../core/widgets/bhoomi_card.dart';
import '../../../daily_brief/application/daily_brief_controller.dart';

class DailyBriefPreview extends ConsumerWidget {
  final String farmId;

  const DailyBriefPreview({
    super.key,
    required this.farmId,
  });

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final briefAsync = ref.watch(dailyBriefProvider(farmId));
    final strings = ref.watch(bhoomiStringsProvider);

    return briefAsync.when(
      loading: () => const SizedBox.shrink(),
      error: (e, _) => const SizedBox.shrink(),
      data: (brief) => BhoomiCard(
        padding: const EdgeInsets.all(AppSpacing.lg),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              mainAxisAlignment: MainAxisAlignment.spaceBetween,
              children: [
                Expanded(
                  child: Row(
                    children: [
                      const Icon(Icons.wb_sunny_rounded, color: AppColors.warmAccent, size: 20.0),
                      const SizedBox(width: AppSpacing.xs),
                      Flexible(
                        child: Text(
                          strings.todaysFarmBrief,
                          maxLines: 1,
                          overflow: TextOverflow.ellipsis,
                          style: const TextStyle(fontSize: 15.0, fontWeight: FontWeight.w800, color: AppColors.textPrimary),
                        ),
                      ),
                    ],
                  ),
                ),
                TextButton(
                  onPressed: () => context.push('/brief/$farmId'),
                  child: Row(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      Text(strings.viewFullBrief, style: const TextStyle(fontSize: 12.0, fontWeight: FontWeight.w700, color: AppColors.primaryGreen)),
                      const SizedBox(width: 2.0),
                      const Icon(Icons.arrow_forward_rounded, size: 14.0, color: AppColors.primaryGreen),
                    ],
                  ),
                ),
              ],
            ),
            const SizedBox(height: AppSpacing.xs),
            Text(
              strings.translateBriefSummary(brief.advisorySummary),
              style: const TextStyle(fontSize: 13.0, color: AppColors.textSecondary, height: 1.35),
            ),
            if (brief.importantAction != null) ...[
              const SizedBox(height: AppSpacing.sm),
              Container(
                padding: const EdgeInsets.all(AppSpacing.sm),
                decoration: BoxDecoration(
                  color: AppColors.background,
                  borderRadius: BorderRadius.circular(AppSpacing.radiusSm),
                ),
                child: Row(
                  children: [
                    const Icon(Icons.priority_high_rounded, size: 14.0, color: Color(0xFFD97706)),
                    const SizedBox(width: AppSpacing.xs),
                    Expanded(
                      child: Text(
                        strings.translateBriefAction(brief.importantAction),
                        style: const TextStyle(fontSize: 11.0, fontWeight: FontWeight.w700, color: AppColors.textPrimary),
                        maxLines: 1,
                        overflow: TextOverflow.ellipsis,
                      ),
                    ),
                  ],
                ),
              ),
            ],
          ],
        ),
      ),
    );
  }
}
