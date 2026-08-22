import 'package:flutter/material.dart';
import '../../../../app/theme/app_colors.dart';
import '../../../../app/theme/app_spacing.dart';
import '../../../../app/theme/app_typography.dart';
import '../../../../core/widgets/bhoomi_card.dart';
import '../../data/models/timeline_event.dart';

class JourneyTimelineWidget extends StatelessWidget {
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
  Widget build(BuildContext context) {
    if (events.isEmpty) {
      return const BhoomiCard(
        child: Center(
          child: Text('No timeline events recorded yet.', style: TextStyle(color: AppColors.textMuted)),
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
                    color: color.withValues(alpha: 0.12),
                    shape: BoxShape.circle,
                    border: Border.all(color: color, width: 2.0),
                  ),
                  child: Icon(_getEventIcon(event.eventType), color: color, size: 16.0),
                ),
                if (!isLast)
                  Container(
                    width: 2.0,
                    height: 52.0,
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
                          Text(
                            event.title,
                            style: AppTypography.titleMedium.copyWith(fontWeight: FontWeight.w700),
                          ),
                          Text(
                            event.timestamp.length >= 10 ? event.timestamp.substring(0, 10) : event.timestamp,
                            style: const TextStyle(fontSize: 10.0, color: AppColors.textMuted),
                          ),
                        ],
                      ),
                      const SizedBox(height: 4.0),
                      Text(
                        event.summary,
                        style: AppTypography.bodyMedium.copyWith(fontSize: 12.0, color: AppColors.textSecondary),
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
