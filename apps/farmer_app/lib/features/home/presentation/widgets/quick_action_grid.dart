import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import '../../../../app/theme/app_colors.dart';
import '../../../../app/theme/app_spacing.dart';

class QuickActionGrid extends StatelessWidget {
  final String farmId;
  final bool isLandVerified;

  const QuickActionGrid({
    super.key,
    required this.farmId,
    this.isLandVerified = true,
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        const Text(
          'What would you like to do?',
          style: TextStyle(fontSize: 16.0, fontWeight: FontWeight.w800, color: AppColors.textPrimary),
        ),
        const SizedBox(height: AppSpacing.md),
        GridView.count(
          crossAxisCount: 2,
          shrinkWrap: true,
          physics: const NeverScrollableScrollPhysics(),
          crossAxisSpacing: AppSpacing.md,
          mainAxisSpacing: AppSpacing.md,
          childAspectRatio: 1.25,
          children: [
            _buildActionTile(
              title: 'Ask BHOOMI',
              subtitle: 'Voice Assistant',
              icon: Icons.mic_rounded,
              color: AppColors.primaryGreen,
              onTap: () => context.push('/ask/$farmId'),
            ),
            _buildActionTile(
              title: 'Show Problem',
              subtitle: 'Upload Crop Photo',
              icon: Icons.camera_alt_rounded,
              color: const Color(0xFFD97706),
              onTap: () => context.push('/ask/$farmId'),
            ),
            _buildActionTile(
              title: 'Government Support',
              subtitle: isLandVerified ? 'Schemes & Subsidies' : 'Requires Verified Land',
              icon: isLandVerified ? Icons.account_balance_rounded : Icons.lock_outline_rounded,
              color: isLandVerified ? const Color(0xFF0284C7) : const Color(0xFF64748B),
              onTap: () => context.push('/schemes/$farmId'),
            ),
            _buildActionTile(
              title: 'My Farm Journey',
              subtitle: 'Activity Timeline',
              icon: Icons.history_edu_rounded,
              color: const Color(0xFF9333EA),
              onTap: () => context.push('/timeline/$farmId'),
            ),
          ],
        ),
      ],
    );
  }

  Widget _buildActionTile({
    required String title,
    required String subtitle,
    required IconData icon,
    required Color color,
    required VoidCallback onTap,
  }) {
    return InkWell(
      onTap: onTap,
      borderRadius: BorderRadius.circular(AppSpacing.radiusLg),
      child: Container(
        padding: const EdgeInsets.all(AppSpacing.md),
        decoration: BoxDecoration(
          color: AppColors.surface,
          borderRadius: BorderRadius.circular(AppSpacing.radiusLg),
          border: Border.all(color: AppColors.border),
          boxShadow: [
            BoxShadow(
              color: Colors.black.withValues(alpha: 0.02),
              blurRadius: 4.0,
              offset: const Offset(0, 2),
            ),
          ],
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Container(
              padding: const EdgeInsets.all(AppSpacing.sm),
              decoration: BoxDecoration(
                color: color.withValues(alpha: 0.12),
                shape: BoxShape.circle,
              ),
              child: Icon(icon, color: color, size: 22.0),
            ),
            Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  title,
                  style: const TextStyle(fontSize: 13.0, fontWeight: FontWeight.w800, color: AppColors.textPrimary),
                ),
                const SizedBox(height: 2.0),
                Text(
                  subtitle,
                  style: const TextStyle(fontSize: 10.0, color: AppColors.textMuted),
                ),
              ],
            ),
          ],
        ),
      ),
    );
  }
}
