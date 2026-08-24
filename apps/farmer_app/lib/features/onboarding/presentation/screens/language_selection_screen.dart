import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../../../app/theme/app_colors.dart';
import '../../../../app/theme/app_spacing.dart';
import '../../../../app/theme/app_typography.dart';
import '../../../../core/localization/bhoomi_localizations.dart';
import '../../../../core/localization/language_provider.dart';
import '../../../../core/widgets/bhoomi_primary_button.dart';

class LanguageSelectionScreen extends ConsumerWidget {
  const LanguageSelectionScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final selectedLangCode = ref.watch(selectedLanguageProvider);
    final strings = ref.watch(bhoomiStringsProvider);
    final activeOption = kSupportedLanguages.firstWhere(
      (l) => l.code == selectedLangCode,
      orElse: () => kSupportedLanguages.first,
    );

    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        backgroundColor: Colors.transparent,
        elevation: 0,
        leading: IconButton(
          icon: const Icon(Icons.arrow_back_rounded, color: AppColors.textPrimary),
          onPressed: () => context.pop(),
        ),
      ),
      body: SafeArea(
        child: Column(
          children: [
            Expanded(
              child: SingleChildScrollView(
                padding: const EdgeInsets.symmetric(horizontal: AppSpacing.lg),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.stretch,
                  children: [
                    // Top emblem & Header
                    Center(
                      child: Container(
                        width: 64.0,
                        height: 64.0,
                        decoration: BoxDecoration(
                          color: AppColors.primaryGreen.withValues(alpha: 0.12),
                          shape: BoxShape.circle,
                          border: Border.all(
                            color: AppColors.primaryGreen.withValues(alpha: 0.25),
                            width: 1.5,
                          ),
                        ),
                        child: const Center(
                          child: Icon(
                            Icons.translate_rounded,
                            color: AppColors.primaryGreen,
                            size: 32.0,
                          ),
                        ),
                      ),
                    ),
                    const SizedBox(height: AppSpacing.md),

                    Text(
                      strings.chooseLanguageTitle,
                      style: AppTypography.headlineLarge,
                      textAlign: TextAlign.center,
                    ),
                    const SizedBox(height: 4.0),
                    Text(
                      activeOption.greeting,
                      style: AppTypography.titleMedium.copyWith(
                        color: AppColors.primaryGreen,
                        fontWeight: FontWeight.w700,
                      ),
                      textAlign: TextAlign.center,
                    ),
                    const SizedBox(height: AppSpacing.sm),
                    Text(
                      strings.chooseLanguageDesc,
                      style: AppTypography.bodyMedium.copyWith(
                        color: AppColors.textSecondary,
                      ),
                      textAlign: TextAlign.center,
                    ),
                    const SizedBox(height: AppSpacing.lg),

                    // Grid / List of Language Options
                    ...kSupportedLanguages.map((lang) {
                      final isSelected = lang.code == selectedLangCode;
                      return Padding(
                        padding: const EdgeInsets.only(bottom: AppSpacing.sm),
                        child: InkWell(
                          onTap: () {
                            ref.read(selectedLanguageProvider.notifier).state = lang.code;
                          },
                          borderRadius: BorderRadius.circular(AppSpacing.radiusMd),
                          child: AnimatedContainer(
                            duration: const Duration(milliseconds: 200),
                            padding: const EdgeInsets.all(AppSpacing.md),
                            decoration: BoxDecoration(
                              color: isSelected
                                  ? AppColors.primaryGreen.withValues(alpha: 0.08)
                                  : AppColors.surface,
                              borderRadius: BorderRadius.circular(AppSpacing.radiusMd),
                              border: Border.all(
                                color: isSelected ? AppColors.primaryGreen : AppColors.border,
                                width: isSelected ? 2.0 : 1.0,
                              ),
                              boxShadow: isSelected
                                  ? [
                                      BoxShadow(
                                        color: AppColors.primaryGreen.withValues(alpha: 0.12),
                                        blurRadius: 8.0,
                                        offset: const Offset(0, 2),
                                      ),
                                    ]
                                  : [],
                            ),
                            child: Row(
                              children: [
                                // Language Badge / Symbol
                                Container(
                                  width: 44.0,
                                  height: 44.0,
                                  decoration: BoxDecoration(
                                    color: isSelected
                                        ? AppColors.primaryGreen
                                        : AppColors.background,
                                    shape: BoxShape.circle,
                                  ),
                                  child: Center(
                                    child: Text(
                                      lang.nativeName.characters.first,
                                      style: TextStyle(
                                        color: isSelected ? Colors.white : AppColors.primaryGreen,
                                        fontSize: 20.0,
                                        fontWeight: FontWeight.w800,
                                      ),
                                    ),
                                  ),
                                ),
                                const SizedBox(width: AppSpacing.md),

                                // Language details
                                Expanded(
                                  child: Column(
                                    crossAxisAlignment: CrossAxisAlignment.start,
                                    children: [
                                      Wrap(
                                        crossAxisAlignment: WrapCrossAlignment.center,
                                        children: [
                                          Text(
                                            lang.nativeName,
                                            style: AppTypography.titleLarge.copyWith(
                                              fontWeight: isSelected ? FontWeight.w800 : FontWeight.w700,
                                              color: isSelected
                                                  ? AppColors.primaryGreen
                                                  : AppColors.textPrimary,
                                            ),
                                          ),
                                          const SizedBox(width: AppSpacing.xs),
                                          Text(
                                            '(${lang.englishName})',
                                            style: AppTypography.bodyMedium.copyWith(
                                              color: AppColors.textMuted,
                                            ),
                                          ),
                                        ],
                                      ),
                                      const SizedBox(height: 2.0),
                                      Text(
                                        'Greeting: "${lang.greeting}"',
                                        style: AppTypography.labelMedium.copyWith(
                                          color: isSelected
                                              ? AppColors.primaryGreen.withValues(alpha: 0.8)
                                              : AppColors.textSecondary,
                                        ),
                                      ),
                                    ],
                                  ),
                                ),

                                // Selection Indicator
                                if (isSelected)
                                  const Icon(
                                    Icons.check_circle_rounded,
                                    color: AppColors.primaryGreen,
                                    size: 24.0,
                                  )
                                else
                                  Icon(
                                    Icons.radio_button_unchecked_rounded,
                                    color: AppColors.textMuted.withValues(alpha: 0.5),
                                    size: 24.0,
                                  ),
                              ],
                            ),
                          ),
                        ),
                      );
                    }),

                    const SizedBox(height: AppSpacing.lg),
                  ],
                ),
              ),
            ),

            // Bottom CTA Bar
            Container(
              padding: const EdgeInsets.all(AppSpacing.lg),
              decoration: const BoxDecoration(
                color: AppColors.surface,
                border: Border(
                  top: BorderSide(color: AppColors.border, width: 1.0),
                ),
              ),
              child: BhoomiPrimaryButton(
                text: activeOption.buttonLabel,
                icon: Icons.arrow_forward_rounded,
                onPressed: () {
                  context.push('/onboarding');
                },
              ),
            ),
          ],
        ),
      ),
    );
  }
}
