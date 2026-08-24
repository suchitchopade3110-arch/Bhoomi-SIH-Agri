import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../../../app/theme/app_colors.dart';
import '../../../../app/theme/app_spacing.dart';
import '../../../../app/theme/app_typography.dart';
import '../../../../core/widgets/bhoomi_card.dart';
import '../../../../core/widgets/bhoomi_primary_button.dart';
import '../../application/land_controller.dart';
import '../widgets/land_status_badge.dart';
import '../widgets/verification_timeline.dart';

class LandStatusScreen extends ConsumerStatefulWidget {
  final String landId;

  const LandStatusScreen({
    super.key,
    required this.landId,
  });

  @override
  ConsumerState<LandStatusScreen> createState() => _LandStatusScreenState();
}

class _LandStatusScreenState extends ConsumerState<LandStatusScreen> {
  @override
  void initState() {
    super.initState();
    Future.microtask(() {
      ref.read(landControllerProvider.notifier).fetchLandRecord(widget.landId);
    });
  }

  @override
  Widget build(BuildContext context) {
    final state = ref.watch(landControllerProvider);
    final record = state.currentRecord;

    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        title: const Text('Land Verification Status'),
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
                                'Survey No.',
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
                      'Land Record ID: ${record?.landRecordId ?? widget.landId}',
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
                    const Text('Verification Lifecycle', style: AppTypography.titleLarge),
                    const SizedBox(height: AppSpacing.lg),
                    VerificationTimeline(
                      status: record?.status ?? 'pending_verification',
                      submittedAt: record?.submittedAt,
                      verifiedAt: record?.verifiedAt,
                      verifier: record?.verifier,
                      rejectionReason: record?.rejectionReason,
                    ),
                  ],
                ),
              ),

              const SizedBox(height: AppSpacing.xl),

              // Back to Home
              BhoomiPrimaryButton(
                text: 'Return to Farm Home',
                icon: Icons.home_rounded,
                onPressed: () {
                  context.go('/home/${record?.farmId ?? "f_1"}');
                },
              ),
            ],
          ),
        ),
      ),
    );
  }
}
