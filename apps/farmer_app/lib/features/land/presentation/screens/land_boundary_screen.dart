import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import '../../../../app/theme/app_colors.dart';
import '../../../../app/theme/app_spacing.dart';
import '../../../../app/theme/app_typography.dart';
import '../../../../core/localization/bhoomi_localizations.dart';
import '../../../../core/widgets/bhoomi_card.dart';
import '../../../../core/widgets/bhoomi_primary_button.dart';
import '../../application/land_controller.dart';
import '../widgets/boundary_map.dart';

class LandBoundaryScreen extends ConsumerWidget {
  final String farmId;

  const LandBoundaryScreen({
    super.key,
    required this.farmId,
  });

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final state = ref.watch(landControllerProvider);
    final controller = ref.read(landControllerProvider.notifier);
    final strings = ref.watch(bhoomiStringsProvider);

    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        title: Text(strings.text('land_boundary_title')),
      ),
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(AppSpacing.lg),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              // Boundary Map View
              BoundaryMapWidget(
                boundaryGeojson: state.boundaryGeojson,
                isEditable: true,
                onSketchBoundary: () {
                  ScaffoldMessenger.of(context).showSnackBar(
                    const SnackBar(
                      content: Text('Boundary vertices updated from GPS field coordinates.'),
                      duration: Duration(seconds: 2),
                    ),
                  );
                },
              ),

              const SizedBox(height: AppSpacing.lg),

              // Summary Card
              BhoomiCard(
                child: Column(
                  children: [
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Text(strings.text('survey_number'), style: AppTypography.labelMedium.copyWith(color: AppColors.textMuted)),
                        Text(state.surveyNo.isEmpty ? '142/3B' : state.surveyNo, style: AppTypography.titleLarge),
                      ],
                    ),
                    const Divider(color: AppColors.divider, height: AppSpacing.lg),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Text(strings.text('total_area'), style: AppTypography.labelMedium.copyWith(color: AppColors.textMuted)),
                        Text('${state.areaAcres.toStringAsFixed(1)} ${strings.text('acres')}', style: AppTypography.titleLarge),
                      ],
                    ),
                    const Divider(color: AppColors.divider, height: AppSpacing.lg),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Text(strings.text('ownership_status'), style: AppTypography.labelMedium.copyWith(color: AppColors.textMuted)),
                        Text(
                          strings.translateLandStatus(state.currentRecord?.status ?? 'verified'),
                          style: AppTypography.titleLarge.copyWith(color: AppColors.primaryGreen),
                        ),
                      ],
                    ),
                  ],
                ),
              ),

              const SizedBox(height: AppSpacing.lg),

              // Confirm and Submit Boundary
              BhoomiPrimaryButton(
                text: strings.save,
                isLoading: state.isSubmitting,
                icon: Icons.check_circle_rounded,
                onPressed: () async {
                  await controller.submitLand(farmId);
                  if (context.mounted) {
                    ScaffoldMessenger.of(context).showSnackBar(
                      const SnackBar(
                        content: Text('Land parcel boundary submitted for revenue verification.'),
                        backgroundColor: AppColors.primaryGreen,
                      ),
                    );
                    Navigator.of(context).pop();
                  }
                },
              ),

              const SizedBox(height: AppSpacing.xl),
            ],
          ),
        ),
      ),
    );
  }
}
