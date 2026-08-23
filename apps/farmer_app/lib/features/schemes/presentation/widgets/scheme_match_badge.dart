import 'package:flutter/material.dart';
import '../../../../app/theme/app_colors.dart';
import '../../../../app/theme/app_spacing.dart';

class SchemeMatchBadge extends StatelessWidget {
  final String matchStatus;

  const SchemeMatchBadge({
    super.key,
    required this.matchStatus,
  });

  @override
  Widget build(BuildContext context) {
    Color color;
    String label;

    switch (matchStatus.toLowerCase()) {
      case 'likely_relevant':
        color = AppColors.primaryGreen;
        label = 'Likely Relevant';
        break;
      case 'more_info_needed':
        color = const Color(0xFFD97706);
        label = 'More Info Needed';
        break;
      case 'available':
      default:
        color = const Color(0xFF0284C7);
        label = 'Available Support';
        break;
    }

    return Container(
      padding: const EdgeInsets.symmetric(horizontal: AppSpacing.sm + 2, vertical: 3.0),
      decoration: BoxDecoration(
        color: color.withValues(alpha: 0.12),
        borderRadius: BorderRadius.circular(AppSpacing.radiusFull),
        border: Border.all(color: color.withValues(alpha: 0.3)),
      ),
      child: Text(
        label,
        style: TextStyle(
          color: color,
          fontSize: 11.0,
          fontWeight: FontWeight.w800,
        ),
      ),
    );
  }
}
