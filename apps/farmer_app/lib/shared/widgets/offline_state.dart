import 'package:flutter/material.dart';
import '../../app/theme/app_colors.dart';
import '../../app/theme/app_spacing.dart';
import '../../app/theme/app_typography.dart';
import '../../core/widgets/bhoomi_primary_button.dart';

class OfflineState extends StatelessWidget {
  final VoidCallback onRetry;
  final bool hasCachedData;

  const OfflineState({
    super.key,
    required this.onRetry,
    this.hasCachedData = false,
  });

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(AppSpacing.xl),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Container(
              padding: const EdgeInsets.all(AppSpacing.lg),
              decoration: BoxDecoration(
                color: const Color(0xFFD97706).withValues(alpha: 0.08),
                shape: BoxShape.circle,
              ),
              child: const Icon(Icons.wifi_off_rounded, size: 44.0, color: Color(0xFFD97706)),
            ),
            const SizedBox(height: AppSpacing.lg),
            const Text(
              'No Internet Connection',
              textAlign: TextAlign.center,
              style: AppTypography.headlineMedium,
            ),
            const SizedBox(height: AppSpacing.xs),
            Text(
              hasCachedData
                  ? 'Showing previously loaded farm information. Connect to the internet to get real-time updates.'
                  : 'This action requires an active internet connection. Please check your network.',
              textAlign: TextAlign.center,
              style: AppTypography.bodyMedium.copyWith(color: AppColors.textSecondary),
            ),
            const SizedBox(height: AppSpacing.lg),
            BhoomiPrimaryButton(
              text: 'Check Connection & Retry',
              icon: Icons.refresh_rounded,
              onPressed: onRetry,
            ),
          ],
        ),
      ),
    );
  }
}
