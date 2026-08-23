import 'package:flutter/material.dart';
import '../../../../app/theme/app_colors.dart';
import '../../../../app/theme/app_spacing.dart';
import '../../../../app/theme/app_typography.dart';
import '../../../../core/widgets/bhoomi_card.dart';
import '../../data/models/resource_plan.dart';
import 'plan_explanation_card.dart';

class IrrigationCard extends StatefulWidget {
  final ResourcePlan plan;

  const IrrigationCard({
    super.key,
    required this.plan,
  });

  @override
  State<IrrigationCard> createState() => _IrrigationCardState();
}

class _IrrigationCardState extends State<IrrigationCard> {
  bool _showExplanation = false;

  @override
  Widget build(BuildContext context) {
    return BhoomiCard(
      padding: const EdgeInsets.all(AppSpacing.lg),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Row(
            mainAxisAlignment: MainAxisAlignment.spaceBetween,
            children: [
              Row(
                children: [
                  Container(
                    padding: const EdgeInsets.all(AppSpacing.sm),
                    decoration: const BoxDecoration(
                      color: Color(0xFFE0F2FE),
                      shape: BoxShape.circle,
                    ),
                    child: const Icon(Icons.water_drop_rounded, color: Color(0xFF0284C7), size: 20.0),
                  ),
                  const SizedBox(width: AppSpacing.sm),
                  const Text("Today's Irrigation", style: AppTypography.titleLarge),
                ],
              ),
              Container(
                padding: const EdgeInsets.symmetric(horizontal: AppSpacing.sm + 2, vertical: 2.0),
                decoration: BoxDecoration(
                  color: AppColors.primaryGreen.withValues(alpha: 0.1),
                  borderRadius: BorderRadius.circular(AppSpacing.radiusFull),
                ),
                child: Text(
                  'Recommended',
                  style: AppTypography.labelMedium.copyWith(
                    color: AppColors.primaryGreen,
                    fontWeight: FontWeight.w700,
                  ),
                ),
              ),
            ],
          ),
          const SizedBox(height: AppSpacing.lg),

          // API-supported amount and unit
          Row(
            crossAxisAlignment: CrossAxisAlignment.baseline,
            textBaseline: TextBaseline.alphabetic,
            children: [
              Text(
                '${widget.plan.irrigationAmount.toInt()}',
                style: AppTypography.displayLarge.copyWith(
                  color: const Color(0xFF0284C7),
                  fontWeight: FontWeight.w900,
                ),
              ),
              const SizedBox(width: AppSpacing.sm),
              Text(
                widget.plan.irrigationUnit,
                style: AppTypography.titleMedium.copyWith(color: AppColors.textMuted),
              ),
            ],
          ),
          const SizedBox(height: AppSpacing.xs),
          Text(
            widget.plan.irrigationAdvice,
            style: AppTypography.bodyMedium.copyWith(color: AppColors.textSecondary),
          ),

          const SizedBox(height: AppSpacing.md),

          // "Why this amount?" Action Button
          Align(
            alignment: Alignment.centerLeft,
            child: TextButton.icon(
              onPressed: () {
                setState(() {
                  _showExplanation = !_showExplanation;
                });
              },
              icon: Icon(
                _showExplanation ? Icons.keyboard_arrow_up_rounded : Icons.help_outline_rounded,
                size: 18.0,
                color: AppColors.primaryGreen,
              ),
              label: Text(
                _showExplanation ? 'Hide calculation basis' : 'Why this amount?',
                style: AppTypography.labelMedium.copyWith(
                  color: AppColors.primaryGreen,
                  fontWeight: FontWeight.w700,
                ),
              ),
              style: TextButton.styleFrom(
                padding: EdgeInsets.zero,
                tapTargetSize: MaterialTapTargetSize.shrinkWrap,
              ),
            ),
          ),

          // Inspectable Inputs when expanded
          if (_showExplanation && widget.plan.explainabilityInputs != null) ...[
            const SizedBox(height: AppSpacing.md),
            PlanExplanationCard(
              inputs: widget.plan.explainabilityInputs!,
              et0: widget.plan.et0MmPerDay,
              kc: widget.plan.cropCoefficientKc,
              waterNeed: widget.plan.cropWaterNeedMm,
            ),
          ],
        ],
      ),
    );
  }
}
