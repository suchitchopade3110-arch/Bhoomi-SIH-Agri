import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../../../app/theme/app_colors.dart';
import '../../../../app/theme/app_spacing.dart';
import '../../../../app/theme/app_typography.dart';
import '../../../../core/localization/bhoomi_localizations.dart';
import '../../../../core/widgets/bhoomi_card.dart';
import '../../../../core/widgets/bhoomi_primary_button.dart';
import '../../../../core/widgets/bhoomi_secondary_button.dart';
import '../../application/land_controller.dart';
import '../widgets/land_status_badge.dart';
import '../widgets/verification_timeline.dart';

class LandStatusScreen extends ConsumerStatefulWidget {
  final String farmId;

  const LandStatusScreen({
    super.key,
    required this.farmId,
  });

  @override
  ConsumerState<LandStatusScreen> createState() => _LandStatusScreenState();
}

class _LandStatusScreenState extends ConsumerState<LandStatusScreen> {
  @override
  void initState() {
    super.initState();
    Future.microtask(() {
      ref.read(landControllerProvider.notifier).fetchLandRecord(widget.farmId);
    });
  }

  @override
  Widget build(BuildContext context) {
    final state = ref.watch(landControllerProvider);
    final record = state.currentRecord;
    final strings = ref.watch(bhoomiStringsProvider);

    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        title: Text(strings.text('land_status_title')),
      ),
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(AppSpacing.lg),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              // Header Card
              BhoomiCard(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      mainAxisAlignment: MainAxisAlignment.spaceBetween,
                      children: [
                        Expanded(
                          child: Column(
                            crossAxisAlignment: CrossAxisAlignment.start,
                            children: [
                              Text(
                                strings.text('survey_number'),
                                style: AppTypography.labelMedium.copyWith(color: AppColors.textMuted),
                              ),
                              Text(
                                record?.farmerStated.surveyNo ?? '142/3B',
                                style: AppTypography.headlineLarge,
                                maxLines: 1,
                                overflow: TextOverflow.ellipsis,
                              ),
                            ],
                          ),
                        ),
                        const SizedBox(width: AppSpacing.sm),
                        LandStatusBadge(status: record?.status ?? 'pending_verification'),
                      ],
                    ),
                    const SizedBox(height: AppSpacing.md),
                    Text(
                      'Land Record ID: ${record?.landRecordId ?? widget.farmId}',
                      style: AppTypography.labelMedium.copyWith(color: AppColors.textMuted, fontFamily: 'monospace'),
                    ),
                  ],
                ),
              ),

              const SizedBox(height: AppSpacing.lg),

              // Lifecycle Timeline
              BhoomiCard(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(strings.text('activity_timeline'), style: AppTypography.titleLarge),
                    const SizedBox(height: AppSpacing.lg),
                    VerificationTimeline(
                      status: record?.status ?? 'pending_verification',
                      submittedAt: record?.submittedAt,
                      verifiedAt: record?.verifiedAt,
                      rejectionReason: record?.rejectionReason,
                    ),
                  ],
                ),
              ),

              const SizedBox(height: AppSpacing.lg),

              // Actions
              BhoomiPrimaryButton(
                text: strings.text('land_boundary_title'),
                icon: Icons.map_rounded,
                onPressed: () {
                  context.push('/land/${widget.farmId}/boundary');
                },
              ),

              const SizedBox(height: AppSpacing.md),

              BhoomiSecondaryButton(
                text: strings.text('land_details_title'),
                icon: Icons.description_rounded,
                onPressed: () {
                  context.push('/land/${widget.farmId}/details');
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
