import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../../app/theme/app_colors.dart';
import '../../../../app/theme/app_spacing.dart';
import '../../../../app/theme/app_typography.dart';
import '../../../../core/localization/bhoomi_localizations.dart';
import '../../../../core/widgets/bhoomi_card.dart';
import '../../../../core/widgets/bhoomi_loading_view.dart';
import '../../../../core/widgets/bhoomi_primary_button.dart';
import '../../application/schemes_controller.dart';

class SchemeDetailScreen extends ConsumerWidget {
  final String schemeId;

  const SchemeDetailScreen({
    super.key,
    required this.schemeId,
  });

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final detailAsync = ref.watch(schemeDetailProvider(schemeId));
    final strings = ref.watch(bhoomiStringsProvider);

    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        title: Text(strings.text('govt_support')),
      ),
      body: SafeArea(
        child: detailAsync.when(
          loading: () => BhoomiLoadingView(message: strings.text('analyzing_health')),
          error: (error, _) => Center(
            child: Padding(
              padding: const EdgeInsets.all(AppSpacing.xl),
              child: Column(
                mainAxisSize: MainAxisSize.min,
                children: [
                  const Icon(Icons.error_outline_rounded, size: 48.0, color: Color(0xFFC62828)),
                  const SizedBox(height: AppSpacing.md),
                  Text(strings.text('govt_support'), style: AppTypography.headlineMedium),
                  const SizedBox(height: AppSpacing.sm),
                  Text(error.toString(), textAlign: TextAlign.center, style: const TextStyle(color: AppColors.textMuted)),
                  const SizedBox(height: AppSpacing.lg),
                  BhoomiPrimaryButton(
                    text: strings.retry,
                    onPressed: () => ref.invalidate(schemeDetailProvider(schemeId)),
                  ),
                ],
              ),
            ),
          ),
          data: (scheme) => SingleChildScrollView(
            padding: const EdgeInsets.all(AppSpacing.lg),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                // Header Card
                BhoomiCard(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Container(
                        padding: const EdgeInsets.symmetric(horizontal: AppSpacing.sm, vertical: 2.0),
                        decoration: BoxDecoration(
                          color: AppColors.primaryGreen.withValues(alpha: 0.12),
                          borderRadius: BorderRadius.circular(AppSpacing.radiusFull),
                        ),
                        child: Text(
                          scheme.department,
                          style: const TextStyle(fontSize: 10.0, fontWeight: FontWeight.w700, color: AppColors.primaryGreen),
                        ),
                      ),
                      const SizedBox(height: AppSpacing.sm),
                      Text(scheme.title, style: AppTypography.headlineLarge),
                      const SizedBox(height: AppSpacing.sm),
                      Text(scheme.description, style: AppTypography.bodyMedium.copyWith(color: AppColors.textSecondary)),
                    ],
                  ),
                ),

                const SizedBox(height: AppSpacing.lg),

                // Benefits Card
                if (scheme.benefits.isNotEmpty) ...[
                  BhoomiCard(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Row(
                          children: [
                            Icon(Icons.card_giftcard_rounded, color: Color(0xFFD97706), size: 20.0),
                            SizedBox(width: AppSpacing.sm),
                            Text('Scheme Benefits & Subsidies', style: AppTypography.titleLarge),
                          ],
                        ),
                        const Divider(color: AppColors.divider, height: AppSpacing.lg),
                        ...scheme.benefits.map((b) => Padding(
                              padding: const EdgeInsets.only(bottom: AppSpacing.sm),
                              child: Row(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  const Icon(Icons.check_circle, size: 16.0, color: AppColors.primaryGreen),
                                  const SizedBox(width: AppSpacing.sm),
                                  Expanded(child: Text(b, style: AppTypography.bodyMedium)),
                                ],
                              ),
                            )),
                      ],
                    ),
                  ),
                  const SizedBox(height: AppSpacing.lg),
                ],

                // Required Documents Card
                if (scheme.requiredDocuments.isNotEmpty) ...[
                  BhoomiCard(
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        const Row(
                          children: [
                            Icon(Icons.folder_shared_outlined, color: AppColors.primaryGreen, size: 20.0),
                            SizedBox(width: AppSpacing.sm),
                            Text('Required Documents', style: AppTypography.titleLarge),
                          ],
                        ),
                        const Divider(color: AppColors.divider, height: AppSpacing.lg),
                        ...scheme.requiredDocuments.map((doc) => Padding(
                              padding: const EdgeInsets.only(bottom: AppSpacing.xs),
                              child: Row(
                                crossAxisAlignment: CrossAxisAlignment.start,
                                children: [
                                  const Icon(Icons.description_outlined, size: 16.0, color: AppColors.textMuted),
                                  const SizedBox(width: AppSpacing.sm),
                                  Expanded(child: Text(doc, style: AppTypography.bodyMedium)),
                                ],
                              ),
                            )),
                      ],
                    ),
                  ),
                  const SizedBox(height: AppSpacing.lg),
                ],

                // Official Action / Portal CTA if returned by API
                if (scheme.officialUrl != null) ...[
                  BhoomiPrimaryButton(
                    text: 'Open Official Government Portal',
                    icon: Icons.open_in_new_rounded,
                    onPressed: () {
                      ScaffoldMessenger.of(context).showSnackBar(
                        SnackBar(content: Text('Official Portal: ${scheme.officialUrl}')),
                      );
                    },
                  ),
                ],

                const SizedBox(height: AppSpacing.xl),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
