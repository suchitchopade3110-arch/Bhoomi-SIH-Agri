import 'package:flutter/material.dart';
import '../../../../app/theme/app_colors.dart';
import '../../../../app/theme/app_spacing.dart';
import '../../../../app/theme/app_typography.dart';
import '../../../../core/widgets/bhoomi_card.dart';

class SymptomsChecklistWidget extends StatefulWidget {
  final List<String> symptoms;

  const SymptomsChecklistWidget({
    super.key,
    required this.symptoms,
  });

  @override
  State<SymptomsChecklistWidget> createState() => _SymptomsChecklistWidgetState();
}

class _SymptomsChecklistWidgetState extends State<SymptomsChecklistWidget> {
  final Set<int> _checkedIndices = {};

  @override
  Widget build(BuildContext context) {
    if (widget.symptoms.isEmpty) return const SizedBox.shrink();

    return BhoomiCard(
      padding: const EdgeInsets.all(AppSpacing.lg),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Row(
            children: [
              Icon(Icons.fact_check_outlined, size: 20.0, color: AppColors.primaryGreen),
              SizedBox(width: AppSpacing.sm),
              Text('What to Check in Your Field', style: AppTypography.titleLarge),
            ],
          ),
          const SizedBox(height: AppSpacing.xs),
          Text(
            'Tap symptoms that match what you observe on your plants:',
            style: AppTypography.bodyMedium.copyWith(fontSize: 12.0, color: AppColors.textMuted),
          ),
          const Divider(color: AppColors.divider, height: AppSpacing.lg),

          ...widget.symptoms.asMap().entries.map((entry) {
            final idx = entry.key;
            final symptom = entry.value;
            final isChecked = _checkedIndices.contains(idx);

            return InkWell(
              onTap: () {
                setState(() {
                  if (isChecked) {
                    _checkedIndices.remove(idx);
                  } else {
                    _checkedIndices.add(idx);
                  }
                });
              },
              borderRadius: BorderRadius.circular(AppSpacing.radiusSm),
              child: Padding(
                padding: const EdgeInsets.symmetric(vertical: AppSpacing.sm),
                child: Row(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Icon(
                      isChecked ? Icons.check_box_rounded : Icons.check_box_outline_blank_rounded,
                      size: 20.0,
                      color: isChecked ? AppColors.primaryGreen : AppColors.textMuted,
                    ),
                    const SizedBox(width: AppSpacing.sm),
                    Expanded(
                      child: Text(
                        symptom,
                        style: AppTypography.bodyMedium.copyWith(
                          color: isChecked ? AppColors.textPrimary : AppColors.textSecondary,
                          fontWeight: isChecked ? FontWeight.w600 : FontWeight.w400,
                        ),
                      ),
                    ),
                  ],
                ),
              ),
            );
          }),
        ],
      ),
    );
  }
}
