import 'package:flutter/material.dart';
import '../../../../app/theme/app_colors.dart';
import '../../../../app/theme/app_spacing.dart';
import '../../../../app/theme/app_typography.dart';

class LandStatusBadge extends StatelessWidget {
  final String status;

  const LandStatusBadge({
    super.key,
    required this.status,
  });

  @override
  Widget build(BuildContext context) {
    final isVerified = status.toLowerCase() == 'verified';
    final isRejected = status.toLowerCase() == 'rejected';

    final Color bgColor = isVerified
        ? AppColors.statusVerified.withValues(alpha: 0.12)
        : isRejected
            ? const Color(0xFFFFEBEE)
            : AppColors.warmAccent.withValues(alpha: 0.15);

    final Color textColor = isVerified
        ? AppColors.statusVerified
        : isRejected
            ? const Color(0xFFC62828)
            : const Color(0xFFD35400);

    final Color borderColor = isVerified
        ? AppColors.statusVerified.withValues(alpha: 0.3)
        : isRejected
            ? const Color(0xFFFFCDD2)
            : AppColors.warmAccent.withValues(alpha: 0.4);

    final IconData icon = isVerified
        ? Icons.verified_rounded
        : isRejected
            ? Icons.cancel_rounded
            : Icons.pending_actions_rounded;

    final String text = isVerified
        ? 'Verified Land'
        : isRejected
            ? 'Rejected'
            : 'Pending Verification';

    return Container(
      padding: const EdgeInsets.symmetric(
        horizontal: AppSpacing.sm + 2,
        vertical: AppSpacing.xs + 2,
      ),
      decoration: BoxDecoration(
        color: bgColor,
        borderRadius: BorderRadius.circular(AppSpacing.radiusFull),
        border: Border.all(color: borderColor),
      ),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Icon(icon, size: 13.0, color: textColor),
          const SizedBox(width: 4.0),
          Flexible(
            child: Text(
              text,
              maxLines: 1,
              overflow: TextOverflow.ellipsis,
              style: AppTypography.labelMedium.copyWith(
                color: textColor,
                fontWeight: FontWeight.w700,
                fontSize: 11.5,
              ),
            ),
          ),
        ],
      ),
    );
  }
}
