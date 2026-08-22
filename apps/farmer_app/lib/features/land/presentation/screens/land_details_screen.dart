import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../../../app/theme/app_colors.dart';
import '../../../../app/theme/app_spacing.dart';
import '../../../../app/theme/app_typography.dart';
import '../../../../core/widgets/bhoomi_card.dart';
import '../../../../core/widgets/bhoomi_primary_button.dart';
import '../../application/land_controller.dart';

class LandDetailsScreen extends ConsumerStatefulWidget {
  final String farmId;

  const LandDetailsScreen({
    super.key,
    required this.farmId,
  });

  @override
  ConsumerState<LandDetailsScreen> createState() => _LandDetailsScreenState();
}

class _LandDetailsScreenState extends ConsumerState<LandDetailsScreen> {
  late TextEditingController _surveyController;
  late TextEditingController _areaController;

  @override
  void initState() {
    super.initState();
    final state = ref.read(landControllerProvider);
    _surveyController = TextEditingController(text: state.surveyNo.isEmpty ? '142/3B' : state.surveyNo);
    _areaController = TextEditingController(text: state.areaAcres.toString());
  }

  @override
  void dispose() {
    _surveyController.dispose();
    _areaController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    final controller = ref.read(landControllerProvider.notifier);

    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        title: const Text('My Land Registration'),
      ),
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(AppSpacing.lg),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              // Header Card
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
                      child: const Icon(Icons.terrain_rounded, color: Colors.white, size: 28.0),
                    ),
                    const SizedBox(width: AppSpacing.md),
                    const Expanded(
                      child: Column(
                        crossAxisAlignment: CrossAxisAlignment.start,
                        children: [
                          Text(
                            'Official Land Record',
                            style: TextStyle(
                              color: Colors.white,
                              fontSize: 18.0,
                              fontWeight: FontWeight.w800,
                            ),
                          ),
                          SizedBox(height: 2.0),
                          Text(
                            'Submit Survey No. and boundary coordinates for Taluk verification.',
                            style: TextStyle(color: Colors.white70, fontSize: 12.0),
                          ),
                        ],
                      ),
                    ),
                  ],
                ),
              ),

              const SizedBox(height: AppSpacing.lg),

              // Inputs Card
              BhoomiCard(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text('Survey & Patta Information', style: AppTypography.titleLarge),
                    const SizedBox(height: AppSpacing.md),

                    // Survey Number Input
                    Text('Survey Number', style: AppTypography.labelMedium.copyWith(color: AppColors.textMuted)),
                    const SizedBox(height: AppSpacing.xs),
                    TextField(
                      controller: _surveyController,
                      onChanged: controller.setSurveyNo,
                      decoration: InputDecoration(
                        hintText: 'e.g. 142/3B or 88/1A',
                        prefixIcon: const Icon(Icons.tag_rounded, color: AppColors.primaryGreen),
                        filled: true,
                        fillColor: AppColors.background,
                        border: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(AppSpacing.radiusMd),
                          borderSide: const BorderSide(color: AppColors.border),
                        ),
                        focusedBorder: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(AppSpacing.radiusMd),
                          borderSide: const BorderSide(color: AppColors.primaryGreen, width: 2.0),
                        ),
                      ),
                    ),

                    const SizedBox(height: AppSpacing.lg),

                    // Area Input
                    Text('Self-Reported Area (Acres)', style: AppTypography.labelMedium.copyWith(color: AppColors.textMuted)),
                    const SizedBox(height: AppSpacing.xs),
                    TextField(
                      controller: _areaController,
                      keyboardType: const TextInputType.numberWithOptions(decimal: true),
                      onChanged: (val) {
                        final parsed = double.tryParse(val);
                        if (parsed != null && parsed > 0) {
                          controller.setAreaAcres(parsed);
                        }
                      },
                      decoration: InputDecoration(
                        hintText: '2.0',
                        prefixIcon: const Icon(Icons.square_foot_rounded, color: AppColors.primaryGreen),
                        suffixText: 'Acres',
                        filled: true,
                        fillColor: AppColors.background,
                        border: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(AppSpacing.radiusMd),
                          borderSide: const BorderSide(color: AppColors.border),
                        ),
                        focusedBorder: OutlineInputBorder(
                          borderRadius: BorderRadius.circular(AppSpacing.radiusMd),
                          borderSide: const BorderSide(color: AppColors.primaryGreen, width: 2.0),
                        ),
                      ),
                    ),
                  ],
                ),
              ),

              const SizedBox(height: AppSpacing.xl),

              // Action CTA
              BhoomiPrimaryButton(
                text: 'Review Boundary Map',
                icon: Icons.map_rounded,
                onPressed: () {
                  controller.setSurveyNo(_surveyController.text.trim());
                  context.push('/land/${widget.farmId}/boundary');
                },
              ),
            ],
          ),
        ),
      ),
    );
  }
}
