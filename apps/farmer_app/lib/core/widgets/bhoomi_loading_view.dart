import 'package:flutter/material.dart';
import '../../app/theme/app_colors.dart';
import '../../app/theme/app_spacing.dart';

class BhoomiLoadingView extends StatelessWidget {
  final String? message;
  final bool showSprout;

  const BhoomiLoadingView({
    super.key,
    this.message,
    this.showSprout = false,
  });

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(AppSpacing.xl),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            if (showSprout) ...[
              Container(
                width: 64.0,
                height: 64.0,
                decoration: BoxDecoration(
                  color: AppColors.lightGreen,
                  shape: BoxShape.circle,
                  border: Border.all(color: AppColors.primaryGreen.withValues(alpha: 0.3)),
                ),
                child: const Center(
                  child: Text('🌱', style: TextStyle(fontSize: 32.0)),
                ),
              ),
              const SizedBox(height: AppSpacing.md),
            ] else ...[
              const SizedBox(
                width: 44.0,
                height: 44.0,
                child: CircularProgressIndicator(
                  strokeWidth: 3.5,
                  valueColor: AlwaysStoppedAnimation<Color>(AppColors.primaryGreen),
                ),
              ),
              const SizedBox(height: AppSpacing.lg),
            ],
            if (message != null)
              Text(
                message!,
                textAlign: TextAlign.center,
                style: const TextStyle(
                  fontSize: 14.0,
                  color: AppColors.textSecondary,
                  fontWeight: FontWeight.w600,
                ),
              ),
          ],
        ),
      ),
    );
  }
}
