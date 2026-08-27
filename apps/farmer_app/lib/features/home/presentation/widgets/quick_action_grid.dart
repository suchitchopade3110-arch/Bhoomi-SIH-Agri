import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../../../app/theme/app_colors.dart';
import '../../../../app/theme/app_spacing.dart';
import '../../../../core/localization/bhoomi_localizations.dart';

class QuickActionGrid extends ConsumerWidget {
  final String farmId;
  final bool isLandVerified;

  const QuickActionGrid({
    super.key,
    required this.farmId,
    this.isLandVerified = true,
  });

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final strings = ref.watch(bhoomiStringsProvider);

    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Row(
          mainAxisAlignment: MainAxisAlignment.spaceBetween,
          children: [
            Text(
              strings.whatWouldYouLikeToDo,
              style: const TextStyle(
                fontSize: 16.0,
                fontWeight: FontWeight.w800,
                color: AppColors.textPrimary,
              ),
            ),
          ],
        ),
        const SizedBox(height: AppSpacing.md),
        GridView.count(
          crossAxisCount: 2,
          shrinkWrap: true,
          physics: const NeverScrollableScrollPhysics(),
          crossAxisSpacing: AppSpacing.sm + 2,
          mainAxisSpacing: AppSpacing.sm + 2,
          childAspectRatio: 1.02,
          children: [
            // 1. Ask BHOOMI (Voice)
            _buildActionTile(
              title: strings.askBhoomi,
              subtitle: strings.voiceAssistant,
              icon: Icons.mic_rounded,
              color: AppColors.primaryGreen,
              onTap: () => context.push('/ask/$farmId'),
            ),

            // 2. Show Image / Photo Diagnosis
            _buildActionTile(
              title: strings.showImage,
              subtitle: strings.uploadCropPhoto,
              icon: Icons.camera_alt_rounded,
              color: const Color(0xFFE76F51),
              onTap: () => context.push('/ask/$farmId'),
            ),

            // 3. Today's Guidance
            _buildActionTile(
              title: strings.todaysGuidance,
              subtitle: strings.weatherFieldAdvice,
              icon: Icons.wb_sunny_rounded,
              color: const Color(0xFFD97706),
              onTap: () => context.push('/brief/$farmId'),
            ),

            // 4. Farm Health
            _buildActionTile(
              title: strings.farmHealth,
              subtitle: strings.scoreDiagnosis,
              icon: Icons.favorite_rounded,
              color: const Color(0xFF059669),
              onTap: () => context.push('/health/$farmId'),
            ),

            // 5. Scheme Support
            _buildActionTile(
              title: strings.govSupport,
              subtitle: isLandVerified ? strings.schemesAndSubsidies : strings.requiresVerifiedLand,
              icon: isLandVerified ? Icons.account_balance_rounded : Icons.lock_outline_rounded,
              color: isLandVerified ? const Color(0xFF0284C7) : const Color(0xFF64748B),
              onTap: () => context.push('/schemes/$farmId'),
            ),

            // 6. Farm Journey
            _buildActionTile(
              title: strings.myFarmJourney,
              subtitle: strings.activityTimeline,
              icon: Icons.timeline_rounded,
              color: const Color(0xFF7C3AED),
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
        padding: const EdgeInsets.all(AppSpacing.sm + 4),
        decoration: BoxDecoration(
          color: AppColors.surface,
          borderRadius: BorderRadius.circular(AppSpacing.radiusLg),
          border: Border.all(color: AppColors.border),
          boxShadow: const [
            BoxShadow(
              color: AppColors.cardShadow,
              blurRadius: 8.0,
              offset: Offset(0, 2),
            ),
          ],
        ),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Container(
              padding: const EdgeInsets.all(AppSpacing.xs + 2),
              decoration: BoxDecoration(
                color: color.withValues(alpha: 0.12),
                shape: BoxShape.circle,
              ),
              child: Icon(icon, color: color, size: 20.0),
            ),
            const Spacer(),
            Text(
              title,
              maxLines: 2,
              overflow: TextOverflow.ellipsis,
              style: const TextStyle(
                fontSize: 13.0,
                fontWeight: FontWeight.w800,
                color: AppColors.textPrimary,
                height: 1.2,
              ),
            ),
            const SizedBox(height: 2.0),
            Text(
              subtitle,
              maxLines: 1,
              overflow: TextOverflow.ellipsis,
              style: const TextStyle(
                fontSize: 10.0,
                color: AppColors.textMuted,
                fontWeight: FontWeight.w500,
                height: 1.15,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
