import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../../app/theme/app_colors.dart';
import '../../../../app/theme/app_spacing.dart';
import '../../../../app/theme/app_typography.dart';
import '../../../../core/localization/bhoomi_localizations.dart';
import '../../../../core/widgets/bhoomi_card.dart';
import '../../data/models/timeline_event.dart';

class JourneyTimelineWidget extends ConsumerWidget {
  final List<TimelineEvent> events;

  const JourneyTimelineWidget({
    super.key,
    required this.events,
  });

  IconData _getEventIcon(String type) {
    switch (type.toLowerCase()) {
      case 'diagnosis':
        return Icons.healing_rounded;
      case 'land':
        return Icons.verified_rounded;
      case 'resource_plan':
        return Icons.water_drop_rounded;
      case 'followup':
        return Icons.update_rounded;
      case 'escalation':
        return Icons.support_agent_rounded;
      case 'onboarding':
      default:
        return Icons.eco_rounded;
    }
  }

  Color _getEventColor(String type) {
    switch (type.toLowerCase()) {
      case 'diagnosis':
        return const Color(0xFFD97706);
      case 'land':
        return AppColors.primaryGreen;
      case 'resource_plan':
        return const Color(0xFF0284C7);
      case 'escalation':
        return const Color(0xFF9333EA);
      default:
        return AppColors.primaryGreen;
    }
  }

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final strings = ref.watch(bhoomiStringsProvider);

    if (events.isEmpty) {
      return BhoomiCard(
        child: Center(
          child: Padding(
            padding: const EdgeInsets.all(AppSpacing.lg),
            child: Text(strings.text('no_timeline_events'), style: const TextStyle(color: AppColors.textMuted)),
          ),
        ),
      );
    }

    return Column(
      children: events.asMap().entries.map((entry) {
        final idx = entry.key;
        final event = entry.value;
        final isLast = idx == events.length - 1;
        final color = _getEventColor(event.eventType);

        return Row(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Column(
              children: [
                Container(
                  padding: const EdgeInsets.all(AppSpacing.sm),
                  decoration: BoxDecoration(
                    color: color.withValues(alpha: 0.15),
                    shape: BoxShape.circle,
                    border: Border.all(color: color, width: 2.0),
                  ),
                  child: Icon(_getEventIcon(event.eventType), color: color, size: 16.0),
                ),
                if (!isLast)
                  Container(
                    width: 2.0,
                    height: 64.0,
                    color: AppColors.border,
                  ),
              ],
            ),
            const SizedBox(width: AppSpacing.md),
            Expanded(
              child: Padding(
                padding: const EdgeInsets.only(bottom: AppSpacing.md),
                child: BhoomiCard(
                  padding: const EdgeInsets.all(AppSpacing.md),
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Row(
                        mainAxisAlignment: MainAxisAlignment.spaceBetween,
                        children: [
                          Expanded(
                            child: Text(
                              strings.translateTimelineTitle(event.title),
                              style: const TextStyle(
                                fontSize: 14.5,
                                fontWeight: FontWeight.w800,
                                color: AppColors.textPrimary,
                              ),
                            ),
                          ),
                          Container(
                            padding: const EdgeInsets.symmetric(horizontal: 6.0, vertical: 2.0),
                            decoration: BoxDecoration(
                              color: AppColors.background,
                              borderRadius: BorderRadius.circular(AppSpacing.radiusSm),
                            ),
                            child: Text(
                              event.timestamp.length >= 10 ? event.timestamp.substring(0, 10) : event.timestamp,
                              style: const TextStyle(fontSize: 10.0, color: AppColors.textMuted, fontWeight: FontWeight.w600),
                            ),
                          ),
                        ],
                      ),
                      const SizedBox(height: 4.0),
                      Text(
                        strings.translateTimelineSummary(event.summary),
                        style: AppTypography.bodyMedium.copyWith(
                          fontSize: 12.5,
                          color: AppColors.textSecondary,
                          height: 1.3,
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ),
          ],
        );
      }).toList(),
    );
  }
}
