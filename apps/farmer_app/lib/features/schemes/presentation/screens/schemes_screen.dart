import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../../../app/theme/app_colors.dart';
import '../../../../app/theme/app_spacing.dart';
import '../../../../app/theme/app_typography.dart';
import '../../../../core/api/api_exception.dart';
import '../../../../core/localization/bhoomi_localizations.dart';
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
    final schemesAsync = ref.watch(farmScopedSchemesProvider(farmId));
    final strings = ref.watch(bhoomiStringsProvider);

    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        title: Text(strings.text('govt_support')),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh_rounded),
            tooltip: strings.text('refresh_status'),
            onPressed: () {
              ref.invalidate(farmScopedSchemesProvider(farmId));
            },
          ),
        ],
      ),
      body: SafeArea(
        child: schemesAsync.when(
          loading: () => BhoomiLoadingView(message: strings.text('analyzing_health')),
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
                        child: const Icon(Icons.lock_outline_rounded, size: 48.0, color: Color(0xFFD97706)),
                      ),
                      const SizedBox(height: AppSpacing.lg),
                      Text(strings.text('land_verification_required'), style: AppTypography.headlineMedium, textAlign: TextAlign.center),
                      const SizedBox(height: AppSpacing.sm),
                      Text(
                        strings.text('verify_land_desc'),
                        textAlign: TextAlign.center,
                        style: const TextStyle(color: AppColors.textMuted, fontSize: 13.5),
                      ),
                      const SizedBox(height: AppSpacing.xl),
                      BhoomiPrimaryButton(
                        text: strings.text('verify_land_now'),
                        icon: Icons.verified_user_rounded,
                        onPressed: () => context.push('/land/$farmId/status'),
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
                    Text(strings.text('unable_load_timeline'), style: AppTypography.headlineMedium),
                    const SizedBox(height: AppSpacing.sm),
                    Text(error.toString(), textAlign: TextAlign.center, style: const TextStyle(color: AppColors.textMuted)),
                    const SizedBox(height: AppSpacing.lg),
                    BhoomiPrimaryButton(
                      text: strings.retry,
                      onPressed: () => ref.invalidate(farmScopedSchemesProvider(farmId)),
                    ),
                  ],
                ),
              ),
            );
          },
          data: (schemes) {
            if (schemes.isEmpty) {
              return Center(
                child: Padding(
                  padding: const EdgeInsets.all(AppSpacing.xl),
                  child: Column(
                    mainAxisSize: MainAxisSize.min,
                    children: [
                      const Icon(Icons.account_balance_rounded, size: 48.0, color: AppColors.textMuted),
                      const SizedBox(height: AppSpacing.md),
                      Text(strings.text('no_updates'), style: AppTypography.headlineMedium),
                      const SizedBox(height: AppSpacing.sm),
                      const Text(
                        'No government schemes currently match your specific crop and location.',
                        textAlign: TextAlign.center,
                        style: TextStyle(color: AppColors.textMuted),
                      ),
                    ],
                  ),
                ),
              );
            }

            return SingleChildScrollView(
              padding: const EdgeInsets.all(AppSpacing.lg),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  Container(
                    padding: const EdgeInsets.all(AppSpacing.lg),
                    decoration: BoxDecoration(
                      color: AppColors.surface,
                      borderRadius: BorderRadius.circular(AppSpacing.radiusLg),
                      border: Border.all(color: AppColors.border),
                      boxShadow: const [
                        BoxShadow(
                          color: AppColors.cardShadow,
                          blurRadius: 10.0,
                          offset: Offset(0, 4),
                        ),
                      ],
                    ),
                    child: Row(
                      children: [
                        Container(
                          padding: const EdgeInsets.all(AppSpacing.md),
                          decoration: BoxDecoration(
                            color: const Color(0xFF0284C7).withValues(alpha: 0.12),
                            shape: BoxShape.circle,
                          ),
                          child: const Icon(Icons.account_balance_rounded, color: Color(0xFF0284C7), size: 28.0),
                        ),
                        const SizedBox(width: AppSpacing.md),
                        Expanded(
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(
                                strings.text('eligible_schemes'),
                                style: const TextStyle(color: AppColors.textPrimary, fontSize: 18.0, fontWeight: FontWeight.w800),
                              ),
                              const SizedBox(height: 2.0),
                              Text(
                                strings.text('govt_support_desc'),
                                style: const TextStyle(color: AppColors.textSecondary, fontSize: 12.0),
                              ),
                            ],
                          ),
                        ),
                      ],
                    ),
                  ),

                  const SizedBox(height: AppSpacing.lg),

                  ...schemes.map((scheme) => Padding(
                        padding: const EdgeInsets.only(bottom: AppSpacing.md),
                        child: SchemeCard(
                          scheme: scheme,
                          onTap: () {
                            context.push('/schemes/$farmId/details', extra: scheme);
                          },
                        ),
                      )),

                  const SizedBox(height: AppSpacing.xl),
                ],
              ),
            );
          },
        ),
      ),
    );
  }
}
