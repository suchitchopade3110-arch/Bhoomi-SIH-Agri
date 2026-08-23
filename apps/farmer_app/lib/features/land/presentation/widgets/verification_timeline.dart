import 'package:flutter/material.dart';
import '../../../../app/theme/app_colors.dart';
import '../../../../app/theme/app_spacing.dart';
import '../../../../app/theme/app_typography.dart';

class VerificationTimeline extends StatelessWidget {
  final String status; // 'submitted' | 'under_review' | 'pending_verification' | 'verified' | 'rejected'
  final String? submittedAt;
  final String? verifiedAt;
  final String? verifier;
  final String? rejectionReason;

  const VerificationTimeline({
    super.key,
    required this.status,
    this.submittedAt,
    this.verifiedAt,
    this.verifier,
    this.rejectionReason,
  });

  @override
  Widget build(BuildContext context) {
    final isUnderReview = status != 'submitted';
    final isVerified = status == 'verified';
    final isRejected = status == 'rejected';

    return Column(
      children: [
        _buildTimelineStep(
          title: 'Land Record Submitted',
          subtitle: submittedAt != null ? 'Timestamp: $submittedAt' : 'Self-reported survey & area recorded',
          isDone: true,
          isActive: status == 'submitted',
          icon: Icons.check_circle_rounded,
          color: AppColors.primaryGreen,
        ),
        _buildConnector(isDone: isUnderReview),
        _buildTimelineStep(
          title: 'Officer Under Review',
          subtitle: 'Taluk verification office reviewing parcel boundary',
          isDone: isVerified || isRejected,
          isActive: status == 'under_review' || status == 'pending_verification',
          icon: Icons.assignment_turned_in_rounded,
          color: (isVerified || isRejected)
              ? AppColors.primaryGreen
              : const Color(0xFFD35400),
        ),
        _buildConnector(isDone: isVerified || isRejected),
        if (isRejected) ...[
          _buildTimelineStep(
            title: 'Verification Rejected',
            subtitle: rejectionReason ?? 'Boundary discrepancy or survey mismatch',
            isDone: true,
            isActive: true,
            icon: Icons.cancel_rounded,
            color: const Color(0xFFC62828),
          ),
        ] else ...[
          _buildTimelineStep(
            title: isVerified ? 'Verified & Stamped' : 'Pending Verification',
            subtitle: isVerified
                ? 'Signed by ${verifier ?? "Officer"} on ${verifiedAt ?? "recently"}'
                : 'Awaiting final government officer signature',
            isDone: isVerified,
            isActive: isVerified,
            icon: isVerified ? Icons.verified_user_rounded : Icons.hourglass_top_rounded,
            color: isVerified ? AppColors.primaryGreen : AppColors.textMuted,
          ),
        ],
      ],
    );
  }

  Widget _buildTimelineStep({
    required String title,
    required String subtitle,
    required bool isDone,
    required bool isActive,
    required IconData icon,
    required Color color,
  }) {
    return Row(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Container(
          padding: const EdgeInsets.all(AppSpacing.sm),
          decoration: BoxDecoration(
            color: isDone ? color : color.withValues(alpha: 0.1),
            shape: BoxShape.circle,
            border: Border.all(color: color, width: 2.0),
          ),
          child: Icon(
            icon,
            size: 18.0,
            color: isDone ? Colors.white : color,
          ),
        ),
        const SizedBox(width: AppSpacing.md),
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                title,
                style: AppTypography.titleMedium.copyWith(
                  fontWeight: FontWeight.w700,
                  color: isDone ? AppColors.textPrimary : AppColors.textMuted,
                ),
              ),
              const SizedBox(height: 2.0),
              Text(
                subtitle,
                style: AppTypography.bodyMedium.copyWith(
                  fontSize: 12.0,
                  color: AppColors.textSecondary,
                ),
              ),
            ],
          ),
        ),
      ],
    );
  }

  Widget _buildConnector({required bool isDone}) {
    return Container(
      margin: const EdgeInsets.only(left: 17.0),
      height: 24.0,
      width: 2.0,
      color: isDone ? AppColors.primaryGreen : AppColors.border,
    );
  }
}
