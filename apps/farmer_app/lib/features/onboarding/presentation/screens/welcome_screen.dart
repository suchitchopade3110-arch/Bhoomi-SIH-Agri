import 'package:flutter/material.dart';
import 'package:go_router/go_router.dart';
import '../../../../app/theme/app_branding.dart';
import '../../../../app/theme/app_colors.dart';
import '../../../../app/theme/app_spacing.dart';
import '../../../../app/theme/app_typography.dart';
import '../../../../core/widgets/bhoomi_primary_button.dart';

/// BHOOMI Onboarding Landing Screen
class WelcomeScreen extends StatelessWidget {
  const WelcomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final size = MediaQuery.of(context).size;

    return Scaffold(
      backgroundColor: AppColors.background,
      body: Stack(
        children: [
          // 1. HERO BACKGROUND IMAGE (Upper 62% of Screen)
          Positioned(
            top: 0,
            left: 0,
            right: 0,
            height: size.height * 0.62,
            child: Stack(
              fit: StackFit.expand,
              children: [
                AppBranding.heroIllustration(
                  fit: BoxFit.cover,
                ),
                // Subtle gradient overlay for top contrast
                Container(
                  decoration: BoxDecoration(
                    gradient: LinearGradient(
                      begin: Alignment.topCenter,
                      end: Alignment.bottomCenter,
                      colors: [
                        Colors.black.withValues(alpha: 0.30),
                        Colors.transparent,
                        Colors.black.withValues(alpha: 0.15),
                      ],
                      stops: const [0.0, 0.45, 1.0],
                    ),
                  ),
                ),
              ],
            ),
          ),

          // 2. TOP BHOOMI BRAND BADGE
          SafeArea(
            child: Align(
              alignment: Alignment.topCenter,
              child: Padding(
                padding: const EdgeInsets.only(top: AppSpacing.sm),
                child: Container(
                  constraints: BoxConstraints(maxWidth: size.width * 0.9),
                  padding: const EdgeInsets.symmetric(
                    horizontal: AppSpacing.md + 2,
                    vertical: AppSpacing.sm,
                  ),
                  decoration: BoxDecoration(
                    color: Colors.white.withValues(alpha: 0.95),
                    borderRadius: BorderRadius.circular(AppSpacing.radiusXl),
                    boxShadow: [
                      BoxShadow(
                        color: Colors.black.withValues(alpha: 0.15),
                        blurRadius: 16.0,
                        offset: const Offset(0, 4),
                      ),
                    ],
                  ),
                  child: Row(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      AppBranding.emblemImage(
                        height: 36.0,
                        width: 36.0,
                        fit: BoxFit.contain,
                      ),
                      const SizedBox(width: AppSpacing.sm),
                      const Flexible(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          mainAxisSize: MainAxisSize.min,
                          children: [
                            Text(
                              'BHOOMI',
                              maxLines: 1,
                              overflow: TextOverflow.ellipsis,
                              style: TextStyle(
                                fontSize: 17.0,
                                fontWeight: FontWeight.w900,
                                letterSpacing: 1.5,
                                color: AppColors.primaryDeepGreen,
                                height: 1.0,
                              ),
                            ),
                            SizedBox(height: 2.0),
                            Text(
                              'AI-Powered Farmer Companion',
                              maxLines: 1,
                              overflow: TextOverflow.ellipsis,
                              style: TextStyle(
                                fontSize: 10.0,
                                fontWeight: FontWeight.w700,
                                color: AppColors.secondaryGreen,
                                height: 1.0,
                              ),
                            ),
                          ],
                        ),
                      ),
                    ],
                  ),
                ),
              ),
            ),
          ),

          // 3. CURVED BOTTOM CONTENT PANEL
          Positioned(
            left: 0,
            right: 0,
            bottom: 0,
            child: ClipPath(
              clipper: const CurvedTopPanelClipper(),
              child: Container(
                color: AppColors.surface,
                padding: const EdgeInsets.fromLTRB(
                  AppSpacing.xl,
                  AppSpacing.xxl,
                  AppSpacing.xl,
                  AppSpacing.lg,
                ),
                child: SafeArea(
                  top: false,
                  child: Column(
                    mainAxisSize: MainAxisSize.min,
                    crossAxisAlignment: CrossAxisAlignment.stretch,
                    children: [
                      const SizedBox(height: 8.0),

                      // Headline
                      const Text(
                        'Your Farm. Our Intelligence.\nBetter Tomorrow.',
                        textAlign: TextAlign.center,
                        style: TextStyle(
                          fontSize: 22.0,
                          fontWeight: FontWeight.w800,
                          color: AppColors.textPrimary,
                          height: 1.3,
                          letterSpacing: -0.3,
                        ),
                      ),

                      const SizedBox(height: AppSpacing.sm),

                      // Subtitle / Tagline
                      Text(
                        'Your trusted digital farming partner for land verification, crop health, and intelligent farm assistance.',
                        textAlign: TextAlign.center,
                        style: AppTypography.bodyMedium.copyWith(
                          color: AppColors.textSecondary,
                          fontSize: 13.0,
                          height: 1.45,
                        ),
                      ),

                      const SizedBox(height: AppSpacing.lg),

                      // Primary CTA: Join Now
                      BhoomiPrimaryButton(
                        text: 'Join Now',
                        icon: Icons.arrow_forward_rounded,
                        onPressed: () {
                          context.push('/register');
                        },
                      ),

                      const SizedBox(height: AppSpacing.xs),

                      // Secondary Action: I'm Already a User
                      TextButton(
                        onPressed: () {
                          context.push('/login');
                        },
                        style: TextButton.styleFrom(
                          foregroundColor: AppColors.primaryGreen,
                          padding: const EdgeInsets.symmetric(
                            horizontal: AppSpacing.md,
                            vertical: AppSpacing.xs,
                          ),
                        ),
                        child: const Text(
                          "I'm Already a User",
                          style: TextStyle(
                            fontSize: 15.0,
                            fontWeight: FontWeight.w700,
                            color: AppColors.primaryGreen,
                          ),
                        ),
                      ),

                      const SizedBox(height: 2.0),

                      // SIH Hackathon trust badge
                      Row(
                        mainAxisAlignment: MainAxisAlignment.center,
                        mainAxisSize: MainAxisSize.min,
                        children: [
                          const Icon(
                            Icons.verified_user_rounded,
                            size: 13.0,
                            color: AppColors.textMuted,
                          ),
                          const SizedBox(width: AppSpacing.xs),
                          Flexible(
                            child: Text(
                              'Smart India Hackathon SIH25076',
                              maxLines: 1,
                              overflow: TextOverflow.ellipsis,
                              style: AppTypography.labelMedium.copyWith(
                                color: AppColors.textMuted,
                                fontSize: 11.0,
                                fontWeight: FontWeight.w500,
                              ),
                            ),
                          ),
                        ],
                      ),
                    ],
                  ),
                ),
              ),
            ),
          ),
        ],
      ),
    );
  }
}

/// Smooth upward curve clipper for the bottom content panel
class CurvedTopPanelClipper extends CustomClipper<Path> {
  const CurvedTopPanelClipper();

  @override
  Path getClip(Size size) {
    final path = Path();
    path.moveTo(0, 32.0);
    path.quadraticBezierTo(
      size.width * 0.5,
      0.0,
      size.width,
      32.0,
    );
    path.lineTo(size.width, size.height);
    path.lineTo(0, size.height);
    path.close();
    return path;
  }

  @override
  bool shouldReclip(covariant CustomClipper<Path> oldClipper) => false;
}
