import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../../../app/theme/app_colors.dart';
import '../../../../app/theme/app_spacing.dart';
import '../../../../app/theme/app_typography.dart';
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

    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        title: const Text('Parcel Boundary'),
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
                        Text('Survey Number', style: AppTypography.labelMedium.copyWith(color: AppColors.textMuted)),
                        Text(state.surveyNo.isEmpty ? '142/3B' : state.surveyNo, style: AppTypography.titleLarge),
                      ],
                    ),
                    const Divider(color: AppColors.divider, height: AppSpacing.lg),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Text('Self-Reported Area', style: AppTypography.labelMedium.copyWith(color: AppColors.textMuted)),
                        Text('${state.areaAcres} Acres', style: AppTypography.titleLarge),
                      ],
                    ),
                    const Divider(color: AppColors.divider, height: AppSpacing.lg),
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Text('Boundary Type', style: AppTypography.labelMedium.copyWith(color: AppColors.textMuted)),
                        const Text('Polygon (GeoJSON)', style: TextStyle(fontWeight: FontWeight.w700, color: AppColors.primaryGreen)),
                      ],
                    ),
                  ],
                ),
              ),

              const SizedBox(height: AppSpacing.md),

              // Notice
              Container(
                padding: const EdgeInsets.all(AppSpacing.md),
                decoration: BoxDecoration(
                  color: AppColors.warmAccent.withValues(alpha: 0.12),
                  borderRadius: BorderRadius.circular(AppSpacing.radiusMd),
                  border: Border.all(color: AppColors.warmAccent.withValues(alpha: 0.3)),
                ),
                child: Row(
                  children: [
                    const Icon(Icons.info_outline_rounded, color: Color(0xFFD35400), size: 20.0),
                    const SizedBox(width: AppSpacing.sm),
                    Expanded(
                      child: Text(
                        'Submitting will queue your land parcel for official verification by the Taluk agricultural officer.',
                        style: AppTypography.bodyMedium.copyWith(fontSize: 12.0, color: const Color(0xFF873600)),
                      ),
                    ),
                  ],
                ),
              ),

              const SizedBox(height: AppSpacing.xl),

              // Submit Action
              BhoomiPrimaryButton(
                text: 'Submit Land for Verification',
                isLoading: state.isSubmitting,
                icon: Icons.send_rounded,
                onPressed: () async {
                  final record = await controller.submitLand(farmId);
                  if (record != null && context.mounted) {
                    context.pushReplacement('/land/status/${record.landRecordId}');
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
