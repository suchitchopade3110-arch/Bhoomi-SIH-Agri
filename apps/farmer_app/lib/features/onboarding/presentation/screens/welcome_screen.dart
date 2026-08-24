import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import '../../../../app/theme/app_colors.dart';
import '../../../../app/theme/app_spacing.dart';
import '../../../../app/theme/app_typography.dart';
import '../../../../core/widgets/bhoomi_primary_button.dart';

class WelcomeScreen extends StatelessWidget {
  const WelcomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.background,
      body: SafeArea(
        child: LayoutBuilder(
          builder: (context, constraints) {
            return SingleChildScrollView(
              padding: const EdgeInsets.symmetric(horizontal: AppSpacing.lg),
              child: ConstrainedBox(
                constraints: BoxConstraints(
                  minHeight: constraints.maxHeight,
                ),
                child: IntrinsicHeight(
                  child: Column(
                    children: [
                      const Spacer(flex: 2),

                      // BHOOMI Logo & Emblem Area
                      Container(
                        width: 120.0,
                        height: 120.0,
                        decoration: BoxDecoration(
                          color: Colors.white,
                          shape: BoxShape.circle,
                          border: Border.all(
                            color: AppColors.primaryGreen.withValues(alpha: 0.2),
                            width: 2.0,
                          ),
                          boxShadow: const [
                            BoxShadow(
                              color: AppColors.cardShadow,
                              blurRadius: 20.0,
                              offset: Offset(0, 8),
                            ),
                          ],
                        ),
                        child: Center(
                          child: ClipOval(
                            child: Image.asset(
                              'assets/images/bhoomi.png',
                              width: 96.0,
                              height: 96.0,
                              fit: BoxFit.contain,
                              errorBuilder: (_, __, ___) => Container(
                                width: 90.0,
                                height: 90.0,
                                decoration: const BoxDecoration(
                                  color: AppColors.primaryGreen,
                                  shape: BoxShape.circle,
                                ),
                                child: const Icon(
                                  Icons.eco_rounded,
                                  size: 52.0,
                                  color: Colors.white,
                                ),
                              ),
                            ),
                          ),
                        ),
                      ),

                      const SizedBox(height: AppSpacing.xl),

                      // Brand Title
                      const Text(
                        'BHOOMI',
                        style: AppTypography.displayLarge,
                        textAlign: TextAlign.center,
                      ),

                      const SizedBox(height: AppSpacing.sm),

                      // Subtitle
                      Text(
                        'AI-Powered Farmer Companion',
                        style: AppTypography.titleLarge.copyWith(
                          color: AppColors.primaryGreen,
                          fontWeight: FontWeight.w600,
                        ),
                        textAlign: TextAlign.center,
                      ),

                      const SizedBox(height: AppSpacing.md),

                      // Value proposition description
                      Padding(
                        padding: const EdgeInsets.symmetric(horizontal: AppSpacing.md),
                        child: Text(
                          'Your trusted digital farming partner for land verification, crop health, and intelligent farm assistance.',
                          style: AppTypography.bodyLarge.copyWith(
                            color: AppColors.textSecondary,
                          ),
                          textAlign: TextAlign.center,
                        ),
                      ),

                      const Spacer(flex: 3),

                      // Primary CTA
                      BhoomiPrimaryButton(
                        text: 'Get Started',
                        icon: Icons.arrow_forward_rounded,
                        onPressed: () {
                          context.push('/language-select');
                        },
                      ),

                      const SizedBox(height: AppSpacing.lg),

                      // Trust indicator
                      Row(
                        mainAxisAlignment: MainAxisAlignment.center,
                        children: [
                          const Icon(
                            Icons.verified_user_outlined,
                            size: 16.0,
                            color: AppColors.textMuted,
                          ),
                          const SizedBox(width: AppSpacing.xs),
                          Text(
                            'Smart India Hackathon SIH25076',
                            style: AppTypography.labelMedium.copyWith(
                              color: AppColors.textMuted,
                            ),
                          ),
                        ],
                      ),

                      const SizedBox(height: AppSpacing.md),
                    ],
                  ),
                ),
              ),
            );
          },
        ),
      ),
    );
  }
}
