import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../../../app/theme/app_colors.dart';
import '../../../../app/theme/app_spacing.dart';
import '../../../../app/theme/app_typography.dart';
import '../../../../core/api/api_exception.dart';
import '../../../../core/widgets/bhoomi_loading_view.dart';
import '../../../../core/widgets/bhoomi_primary_button.dart';
import '../../application/schemes_controller.dart';
import '../widgets/scheme_card.dart';

class SchemesScreen extends ConsumerWidget {
  final String farmId;

  const SchemesScreen({
    super.key,
    required this.farmId,
  });

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final schemesAsync = ref.watch(schemesListProvider(farmId));

    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        title: const Text('Government Support'),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh_rounded),
            tooltip: 'Refresh Schemes',
            onPressed: () {
              ref.invalidate(schemesListProvider(farmId));
            },
          ),
        ],
      ),
      body: SafeArea(
        child: schemesAsync.when(
          loading: () => const BhoomiLoadingView(message: 'Matching government support for your farm...'),
          error: (error, _) {
            final isLandNotVerified = (error is ApiException && (error.code == 'LAND_NOT_VERIFIED' || error.statusCode == 409)) ||
                error.toString().contains('LAND_NOT_VERIFIED') ||
                error.toString().contains('409') ||
                error.toString().toLowerCase().contains('land not verified');

            if (isLandNotVerified) {
              return Center(
                child: Padding(
                  padding: const EdgeInsets.all(AppSpacing.xl),
                  child: Column(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      Container(
                        padding: const EdgeInsets.all(AppSpacing.lg),
                        decoration: BoxDecoration(
                          color: const Color(0xFFD97706).withValues(alpha: 0.12),
                          shape: BoxShape.circle,
                        ),
                        child: const Icon(
                          Icons.verified_user_outlined,
                          size: 48.0,
                          color: Color(0xFFD97706),
                        ),
                      ),
                      const SizedBox(height: AppSpacing.lg),
                      const Text(
                        'Land Verification Required',
                        style: AppTypography.headlineMedium,
                        textAlign: TextAlign.center,
                      ),
                      const SizedBox(height: AppSpacing.sm),
                      const Text(
                        'Verify your farm land details to unlock personalized government schemes and subsidies.',
                        textAlign: TextAlign.center,
                        style: TextStyle(color: AppColors.textMuted, fontSize: 14.0),
                      ),
                      const SizedBox(height: AppSpacing.xl),
                      BhoomiPrimaryButton(
                        text: 'Verify Land Now',
                        icon: Icons.map_rounded,
                        onPressed: () => context.push('/land/$farmId/boundary'),
                      ),
                      const SizedBox(height: AppSpacing.md),
                      TextButton.icon(
                        onPressed: () => ref.invalidate(schemesListProvider(farmId)),
                        icon: const Icon(Icons.refresh_rounded, size: 18.0),
                        label: const Text('Refresh Status'),
                      ),
                    ],
                  ),
                ),
              );
            }

            return Center(
              child: Padding(
                padding: const EdgeInsets.all(AppSpacing.xl),
                child: Column(
                  mainAxisSize: MainAxisSize.min,
                  children: [
                    const Icon(Icons.error_outline_rounded, size: 48.0, color: Color(0xFFC62828)),
                    const SizedBox(height: AppSpacing.md),
                    const Text('Unable to Load Schemes', style: AppTypography.headlineMedium),
                    const SizedBox(height: AppSpacing.sm),
                    Text(error.toString(), textAlign: TextAlign.center, style: const TextStyle(color: AppColors.textMuted)),
                    const SizedBox(height: AppSpacing.lg),
                    BhoomiPrimaryButton(
                      text: 'Retry',
                      onPressed: () => ref.invalidate(schemesListProvider(farmId)),
                    ),
                  ],
                ),
              ),
            );
          },
          data: (schemes) => SingleChildScrollView(
            padding: const EdgeInsets.all(AppSpacing.lg),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                // Header Banner
                Container(
                  padding: const EdgeInsets.all(AppSpacing.lg),
                  decoration: BoxDecoration(
                    gradient: const LinearGradient(
                      colors: [AppColors.primaryGreen, Color(0xFF1B5E20)],
                      begin: Alignment.topLeft,
                      end: Alignment.bottomRight,
                    ),
                    borderRadius: BorderRadius.circular(AppSpacing.radiusLg),
                  ),
                  child: Row(
                    children: [
                      Container(
                        padding: const EdgeInsets.all(AppSpacing.md),
                        decoration: BoxDecoration(
                          color: Colors.white.withValues(alpha: 0.2),
                          shape: BoxShape.circle,
                        ),
                        child: const Icon(Icons.account_balance_rounded, color: Colors.white, size: 28.0),
                      ),
                      const SizedBox(width: AppSpacing.md),
                      const Expanded(
                        child: Column(
                          crossAxisAlignment: CrossAxisAlignment.start,
                          children: [
                            Text(
                              'Government Support Finder',
                              style: TextStyle(color: Colors.white, fontSize: 18.0, fontWeight: FontWeight.w800),
                            ),
                            SizedBox(height: 2.0),
                            Text(
                              'Central & State schemes relevant to your crop, land area, and district.',
                              style: TextStyle(color: Colors.white70, fontSize: 12.0),
                            ),
                          ],
                        ),
                      ),
                    ],
                  ),
                ),

                const SizedBox(height: AppSpacing.lg),

                ...schemes.map((scheme) {
                  return Padding(
                    padding: const EdgeInsets.only(bottom: AppSpacing.md),
                    child: SchemeCard(
                      scheme: scheme,
                      onTap: () {
                        if (scheme.isMoreInfoNeeded) {
                          context.push('/schemes/$farmId/${scheme.schemeId}/info');
                        } else {
                          context.push('/schemes/detail/${scheme.schemeId}');
                        }
                      },
                    ),
                  );
                }),

                const SizedBox(height: AppSpacing.xl),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
