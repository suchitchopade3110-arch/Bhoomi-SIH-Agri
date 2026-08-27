import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../../../app/theme/app_colors.dart';
import '../../../../app/theme/app_spacing.dart';
import '../../../../app/theme/app_typography.dart';
import '../../../../core/localization/bhoomi_localizations.dart';
import '../../../../core/widgets/bhoomi_card.dart';
import '../../../../core/widgets/bhoomi_loading_view.dart';
import '../../../../core/widgets/bhoomi_primary_button.dart';
import '../../application/updates_controller.dart';
import '../../../alerts/presentation/providers/alerts_providers.dart';
import '../../../alerts/data/alerts_repository.dart';

class FarmUpdatesScreen extends ConsumerWidget {
  final String farmId;

  const FarmUpdatesScreen({
    super.key,
    required this.farmId,
  });

  IconData _getUpdateIcon(String type) {
    switch (type.toLowerCase()) {
      case 'advisory':
        return Icons.eco_rounded;
      case 'followup_reminder':
        return Icons.alarm_rounded;
      case 'scheme_alert':
        return Icons.account_balance_rounded;
      case 'case_status':
        return Icons.support_agent_rounded;
      case 'notice':
      default:
        return Icons.notifications_active_rounded;
    }
  }

  Color _getUpdateColor(String type) {
    switch (type.toLowerCase()) {
      case 'advisory':
        return AppColors.primaryGreen;
      case 'followup_reminder':
        return const Color(0xFFD97706);
      case 'scheme_alert':
        return const Color(0xFF0284C7);
      case 'case_status':
        return const Color(0xFF9333EA);
      default:
        return AppColors.primaryGreen;
    }
  }

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final updatesAsync = ref.watch(farmUpdatesProvider(farmId));
    final strings = ref.watch(bhoomiStringsProvider);

    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        title: Text(strings.latestUpdates),
        actions: [
          IconButton(
            icon: const Icon(Icons.refresh_rounded),
            onPressed: () => ref.invalidate(farmUpdatesProvider(farmId)),
          ),
        ],
      ),
      body: SafeArea(
        child: Column(
          children: [
            _buildAlertsSection(context, ref),
            Expanded(
              child: updatesAsync.when(
                loading: () => BhoomiLoadingView(message: strings.text('analyzing_health')),
                error: (error, _) => Center(
                  child: Padding(
                    padding: const EdgeInsets.all(AppSpacing.xl),
                    child: Column(
                      mainAxisSize: MainAxisSize.min,
                      children: [
                        const Icon(Icons.error_outline_rounded, size: 48.0, color: Color(0xFFC62828)),
                        const SizedBox(height: AppSpacing.md),
                        Text(strings.latestUpdates, style: AppTypography.headlineMedium),
                        const SizedBox(height: AppSpacing.sm),
                        Text(error.toString(), textAlign: TextAlign.center, style: const TextStyle(color: AppColors.textMuted)),
                        const SizedBox(height: AppSpacing.lg),
                        BhoomiPrimaryButton(
                          text: strings.retry,
                          onPressed: () => ref.invalidate(farmUpdatesProvider(farmId)),
                        ),
                      ],
                    ),
                  ),
                ),
                data: (updates) => updates.isEmpty
                    ? Center(
                        child: Text(strings.text('no_updates'), style: const TextStyle(color: AppColors.textMuted)),
                      )
                    : ListView.builder(
                        padding: const EdgeInsets.all(AppSpacing.lg),
                        itemCount: updates.length,
                        itemBuilder: (context, index) {
                          final update = updates[index];
                          final color = _getUpdateColor(update.updateType);

                          return Padding(
                            padding: const EdgeInsets.only(bottom: AppSpacing.md),
                            child: BhoomiCard(
                              padding: const EdgeInsets.all(AppSpacing.lg),
                              child: InkWell(
                                onTap: update.actionRoute != null
                                    ? () => context.push(update.actionRoute!)
                                    : null,
                                borderRadius: BorderRadius.circular(AppSpacing.radiusMd),
                                child: Row(
                                  crossAxisAlignment: CrossAxisAlignment.start,
                                  children: [
                                    Container(
                                      padding: const EdgeInsets.all(AppSpacing.sm),
                                      decoration: BoxDecoration(
                                        color: color.withValues(alpha: 0.12),
                                        shape: BoxShape.circle,
                                      ),
                                      child: Icon(_getUpdateIcon(update.updateType), color: color, size: 20.0),
                                    ),
                                    const SizedBox(width: AppSpacing.md),
                                    Expanded(
                                      child: Column(
                                        crossAxisAlignment: CrossAxisAlignment.start,
                                        children: [
                                          Row(
                                            mainAxisAlignment: MainAxisAlignment.spaceBetween,
                                            children: [
                                              Expanded(
                                                child: Text(
                                                  update.title,
                                                  style: AppTypography.titleMedium.copyWith(fontWeight: FontWeight.w700),
                                                ),
                                              ),
                                              Text(
                                                update.timestamp.length >= 10 ? update.timestamp.substring(0, 10) : update.timestamp,
                                                style: const TextStyle(fontSize: 10.0, color: AppColors.textMuted),
                                              ),
                                            ],
                                          ),
                                          const SizedBox(height: 4.0),
                                          Text(
                                            update.description,
                                            style: AppTypography.bodyMedium.copyWith(fontSize: 12.0, color: AppColors.textSecondary),
                                          ),
                                          if (update.actionRoute != null) ...[
                                            const SizedBox(height: AppSpacing.sm),
                                            Row(
                                              mainAxisSize: MainAxisSize.min,
                                              children: [
                                                Text(
                                                  'View Details',
                                                  style: TextStyle(fontSize: 11.0, fontWeight: FontWeight.w700, color: color),
                                                ),
                                                const SizedBox(width: 2.0),
                                                Icon(Icons.arrow_forward_rounded, size: 12.0, color: color),
                                              ],
                                            ),
                                          ],
                                        ],
                                      ),
                                    ),
                                  ],
                                ),
                              ),
                            ),
                          );
                        },
                      ),
              ),
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildAlertsSection(BuildContext context, WidgetRef ref) {
    final alertsAsync = ref.watch(farmAlertsProvider(farmId));

    return alertsAsync.when(
      loading: () => const SizedBox.shrink(),
      error: (_, __) => const SizedBox.shrink(),
      data: (alerts) {
        if (alerts.activeAlerts.isEmpty) return const SizedBox.shrink();

        return Column(
          mainAxisSize: MainAxisSize.min,
          children: alerts.activeAlerts.map((alert) {
            return Container(
              margin: const EdgeInsets.fromLTRB(AppSpacing.lg, AppSpacing.lg, AppSpacing.lg, 0),
              padding: const EdgeInsets.all(AppSpacing.lg),
              decoration: BoxDecoration(
                color: const Color(0xFFFFFBEB),
                borderRadius: BorderRadius.circular(AppSpacing.radiusLg),
                border: Border.all(color: const Color(0xFFFCD34D), width: 1.5),
              ),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: [
                  Row(
                    children: [
                      const Icon(Icons.warning_amber_rounded, color: Color(0xFFD97706), size: 24.0),
                      const SizedBox(width: AppSpacing.sm),
                      Expanded(
                        child: Text(
                          'Early Warning: ${alert.pathogenName}',
                          style: const TextStyle(
                            fontSize: 14.5,
                            fontWeight: FontWeight.w800,
                            color: Color(0xFFB45309),
                          ),
                        ),
                      ),
                    ],
                  ),
                  const SizedBox(height: AppSpacing.sm),
                  Text(
                    'Trigger Reason: ${alert.triggerReason}',
                    style: const TextStyle(fontSize: 12.5, fontWeight: FontWeight.w700, color: AppColors.textPrimary),
                  ),
                  const SizedBox(height: 2.0),
                  Text(
                    'Preventative Action: ${alert.preventativeAction}',
                    style: const TextStyle(fontSize: 12.5, color: AppColors.textSecondary, height: 1.35),
                  ),
                  const Divider(color: Color(0xFFFCD34D), height: AppSpacing.lg),
                  Align(
                    alignment: Alignment.centerRight,
                    child: TextButton.icon(
                      icon: const Icon(Icons.check_circle_outline_rounded, size: 16.0),
                      label: const Text('Acknowledge & Dismiss'),
                      style: TextButton.styleFrom(
                        foregroundColor: const Color(0xFFB45309),
                        padding: const EdgeInsets.symmetric(horizontal: AppSpacing.md, vertical: AppSpacing.xs),
                      ),
                      onPressed: () async {
                        try {
                          await ref.read(alertsRepositoryProvider).acknowledgeAlert(
                            alertId: alert.alertId,
                            farmId: farmId,
                          );
                          ref.invalidate(farmAlertsProvider(farmId));
                          if (context.mounted) {
                            ScaffoldMessenger.of(context).showSnackBar(
                              const SnackBar(
                                content: Text('Alert acknowledged and dismissed.'),
                                backgroundColor: AppColors.primaryGreen,
                              ),
                            );
                          }
                        } catch (_) {}
                      },
                    ),
                  ),
                ],
              ),
            );
          }).toList(),
        );
      },
    );
  }
}
