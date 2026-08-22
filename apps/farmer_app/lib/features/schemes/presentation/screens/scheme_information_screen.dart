import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../../../app/theme/app_colors.dart';
import '../../../../app/theme/app_spacing.dart';
import '../../../../app/theme/app_typography.dart';
import '../../../../core/widgets/bhoomi_card.dart';
import '../../../../core/widgets/bhoomi_primary_button.dart';
import '../../data/schemes_repository.dart';

class SchemeInformationScreen extends ConsumerStatefulWidget {
  final String farmId;
  final String schemeId;

  const SchemeInformationScreen({
    super.key,
    required this.farmId,
    required this.schemeId,
  });

  @override
  ConsumerState<SchemeInformationScreen> createState() => _SchemeInformationScreenState();
}

class _SchemeInformationScreenState extends ConsumerState<SchemeInformationScreen> {
  String _category = 'Small Farmer (< 2 Ha)';
  String _incomeBracket = '< ₹2.5 Lakhs / Year';
  bool _isSubmitting = false;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        title: const Text('Provide Details'),
      ),
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(AppSpacing.lg),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              BhoomiCard(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Row(
                      children: [
                        Icon(Icons.help_outline_rounded, color: Color(0xFFD97706), size: 22.0),
                        SizedBox(width: AppSpacing.sm),
                        Text('Additional Criteria Check', style: AppTypography.titleLarge),
                      ],
                    ),
                    const SizedBox(height: AppSpacing.xs),
                    Text(
                      'This government scheme requires verification of farmer category and annual income bracket.',
                      style: AppTypography.bodyMedium.copyWith(color: AppColors.textSecondary),
                    ),
                  ],
                ),
              ),

              const SizedBox(height: AppSpacing.lg),

              BhoomiCard(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text('Farmer Operational Category', style: AppTypography.titleMedium),
                    const SizedBox(height: AppSpacing.sm),
                    DropdownButtonFormField<String>(
                      initialValue: _category,
                      decoration: InputDecoration(
                        filled: true,
                        fillColor: AppColors.background,
                        border: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(AppSpacing.radiusMd),
                          borderSide: const BorderSide(color: AppColors.border),
                        ),
                      ),
                      items: const [
                        DropdownMenuItem(value: 'Marginal Farmer (< 1 Ha)', child: Text('Marginal Farmer (< 1 Ha)')),
                        DropdownMenuItem(value: 'Small Farmer (< 2 Ha)', child: Text('Small Farmer (< 2 Ha)')),
                        DropdownMenuItem(value: 'Medium Farmer (2 - 10 Ha)', child: Text('Medium Farmer (2 - 10 Ha)')),
                      ],
                      onChanged: (val) {
                        if (val != null) setState(() => _category = val);
                      },
                    ),

                    const SizedBox(height: AppSpacing.lg),

                    const Text('Annual Income Bracket', style: AppTypography.titleMedium),
                    const SizedBox(height: AppSpacing.sm),
                    DropdownButtonFormField<String>(
                      initialValue: _incomeBracket,
                      decoration: InputDecoration(
                        filled: true,
                        fillColor: AppColors.background,
                        border: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(AppSpacing.radiusMd),
                          borderSide: const BorderSide(color: AppColors.border),
                        ),
                      ),
                      items: const [
                        DropdownMenuItem(value: '< ₹1.5 Lakhs / Year', child: Text('< ₹1.5 Lakhs / Year')),
                        DropdownMenuItem(value: '< ₹2.5 Lakhs / Year', child: Text('< ₹2.5 Lakhs / Year')),
                        DropdownMenuItem(value: '₹2.5L - ₹5L / Year', child: Text('₹2.5L - ₹5L / Year')),
                      ],
                      onChanged: (val) {
                        if (val != null) setState(() => _incomeBracket = val);
                      },
                    ),
                  ],
                ),
              ),

              const SizedBox(height: AppSpacing.xl),

              BhoomiPrimaryButton(
                text: 'Submit & Verify Eligibility',
                isLoading: _isSubmitting,
                icon: Icons.check_circle_rounded,
                onPressed: () async {
                  setState(() => _isSubmitting = true);
                  try {
                    await ref.read(schemesRepositoryProvider).submitRequirements(
                          farmId: widget.farmId,
                          schemeId: widget.schemeId,
                          additionalData: {
                            'category': _category,
                            'annual_income_bracket': _incomeBracket,
                          },
                        );
                    if (context.mounted) {
                      context.pushReplacement('/schemes/detail/${widget.schemeId}');
                    }
                  } catch (e) {
                    if (context.mounted) {
                      ScaffoldMessenger.of(context).showSnackBar(
                        SnackBar(content: Text('Submission failed: $e')),
                      );
                    }
                  } finally {
                    if (mounted) setState(() => _isSubmitting = false);
                  }
                },
              ),
            ],
          ),
        ),
      ),
    );
  }
}
