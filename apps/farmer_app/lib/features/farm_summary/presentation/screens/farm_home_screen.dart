import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../../../app/theme/app_colors.dart';
import '../../../../app/theme/app_spacing.dart';
import '../../../../app/theme/app_typography.dart';
import '../../../../core/connectivity/connectivity_service.dart';
import '../../../../core/localization/bhoomi_localizations.dart';
import '../../../../core/upload/pending_uploads_banner.dart';
import '../../../../core/widgets/bhoomi_loading_view.dart';
import '../../../../core/widgets/bhoomi_primary_button.dart';
import '../../../../core/widgets/degraded_network_banner.dart';
import '../../../daily_brief/application/daily_brief_controller.dart';
import '../../../home/presentation/widgets/daily_brief_preview.dart';
import '../../../home/presentation/widgets/latest_update_preview.dart';
import '../../../home/presentation/widgets/quick_action_grid.dart';
import '../../../land/presentation/widgets/land_status_badge.dart';
import '../../../onboarding/data/farm_api_service.dart';
import '../../../onboarding/data/models/farm_update_models.dart';
import '../../../schemes/application/schemes_controller.dart';
import '../../../updates/application/updates_controller.dart';
import '../../application/farm_summary_provider.dart';
import '../../data/models/farm_summary.dart';
import '../widgets/farm_identity_card.dart';
import '../../../auth/presentation/providers/auth_providers.dart';

class FarmHomeScreen extends ConsumerWidget {
  final String farmId;

  const FarmHomeScreen({
    super.key,
    required this.farmId,
  });

  void _showLanguageSwitcher(BuildContext context, WidgetRef ref) {
    showModalBottomSheet(
      context: context,
      isScrollControlled: true,
      useSafeArea: true,
      backgroundColor: AppColors.surface,
      shape: const RoundedRectangleBorder(
        borderRadius: BorderRadius.vertical(top: Radius.circular(AppSpacing.radiusLg)),
      ),
      builder: (ctx) {
        final currentCode = ref.watch(selectedLanguageProvider);
        final strings = ref.watch(bhoomiStringsProvider);
        final screenHeight = MediaQuery.of(ctx).size.height;

        return Container(
          constraints: BoxConstraints(
            maxHeight: screenHeight * 0.75,
          ),
          padding: const EdgeInsets.symmetric(horizontal: AppSpacing.lg, vertical: AppSpacing.md),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceBetween,
                children: [
                  Text(
                    strings.changeLanguage,
                    style: AppTypography.titleLarge.copyWith(fontWeight: FontWeight.w700),
                  ),
                  IconButton(
                    icon: const Icon(Icons.close_rounded),
                    onPressed: () => Navigator.pop(ctx),
                  ),
                ],
              ),
              const Divider(color: AppColors.divider),
              Flexible(
                child: ListView.builder(
                  shrinkWrap: true,
                  itemCount: kSupportedLanguages.length,
                  itemBuilder: (context, index) {
                    final lang = kSupportedLanguages[index];
                    final isSelected = lang.code == currentCode;
                    return ListTile(
                      contentPadding: const EdgeInsets.symmetric(horizontal: AppSpacing.sm, vertical: 2.0),
                      leading: CircleAvatar(
                        backgroundColor: isSelected ? AppColors.primaryGreen : AppColors.background,
                        child: Text(
                          lang.nativeName.characters.first,
                          style: TextStyle(
                            color: isSelected ? Colors.white : AppColors.primaryGreen,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ),
                      title: Text(
                        '${lang.nativeName} (${lang.englishName})',
                        style: TextStyle(
                          fontWeight: isSelected ? FontWeight.w800 : FontWeight.w600,
                          color: isSelected ? AppColors.primaryGreen : AppColors.textPrimary,
                        ),
                      ),
                      trailing: isSelected
                          ? const Icon(Icons.check_circle_rounded, color: AppColors.primaryGreen)
                          : null,
                      onTap: () {
                        ref.read(selectedLanguageProvider.notifier).state = lang.code;
                        Navigator.pop(ctx);
                      },
                    );
                  },
                ),
              ),
              const SizedBox(height: AppSpacing.sm),
            ],
          ),
        );
      },
    );
  }

  /// Flips the veteran/novice UI density toggle (checklist §1.5) and
  /// persists it on the farm profile via `PUT /farms/{id}`, so it survives
  /// across sessions and devices rather than living only as client state.
  Future<void> _toggleUiMode(BuildContext context, WidgetRef ref, FarmIdentity farm) async {
    final next = farm.uiMode == 'veteran' ? UiMode.novice : UiMode.veteran;
    try {
      await ref.read(farmApiServiceProvider).updateFarm(farmId, FarmUpdateRequest(uiMode: next));
      ref.invalidate(farmSummaryProvider(farmId));
    } catch (_) {
      if (context.mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(content: Text('Could not update display mode. Please try again.')),
        );
      }
    }
  }

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final summaryAsync = ref.watch(farmSummaryProvider(farmId));
    final networkState = ref.watch(networkStateProvider);
    final strings = ref.watch(bhoomiStringsProvider);

    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        title: Row(
          children: [
            Container(
              padding: const EdgeInsets.all(6.0),
              decoration: const BoxDecoration(
                color: AppColors.lightGreen,
                shape: BoxShape.circle,
              ),
              child: const Icon(Icons.eco_rounded, size: 20.0, color: AppColors.primaryGreen),
            ),
            const SizedBox(width: AppSpacing.sm),
            Text(
              strings.appTitle,
              style: const TextStyle(fontWeight: FontWeight.w900, color: AppColors.primaryGreen, fontSize: 20.0),
            ),
          ],
        ),
        centerTitle: false,
        scrolledUnderElevation: 0,
        actions: [
          Builder(builder: (context) {
            final farm = summaryAsync.valueOrNull?.farm;
            final isVeteran = farm?.uiMode == 'veteran';
            return IconButton(
              icon: Icon(isVeteran ? Icons.military_tech_rounded : Icons.school_rounded),
              tooltip: isVeteran ? 'Veteran mode — tap for Novice' : 'Novice mode — tap for Veteran',
              onPressed: farm == null ? null : () => _toggleUiMode(context, ref, farm),
            );
          }),
          IconButton(
            icon: const Icon(Icons.translate_rounded),
            tooltip: strings.changeLanguage,
            onPressed: () => _showLanguageSwitcher(context, ref),
          ),
          IconButton(
            icon: const Icon(Icons.notifications_outlined),
            tooltip: strings.latestUpdates,
            onPressed: () {
              context.push('/updates/$farmId');
            },
          ),
          IconButton(
            icon: const Icon(Icons.refresh_rounded),
            tooltip: 'Refresh Farm Data',
            onPressed: () {
              ref.invalidate(farmSummaryProvider(farmId));
              ref.invalidate(dailyBriefProvider(farmId));
              ref.invalidate(schemesListProvider(farmId));
              ref.invalidate(farmUpdatesProvider(farmId));
            },
          ),
        ],
      ),
      body: SafeArea(
        child: Column(
          children: [
            // Degraded Network Mode Banner
            DegradedNetworkBanner(networkState: networkState),

            // Offline upload queue (checklist §12.4) — per-item state for
            // any photo/voice note still waiting to reach the server.
            const PendingUploadsBanner(),

            Expanded(
              child: summaryAsync.when(
                loading: () => const BhoomiLoadingView(message: 'Loading your farm companion...'),
                error: (error, _) => _buildErrorView(context, ref, error, strings),
                data: (summary) => RefreshIndicator(
                  color: AppColors.primaryGreen,
                  onRefresh: () async {
                    ref.invalidate(farmSummaryProvider(farmId));
                    ref.invalidate(dailyBriefProvider(farmId));
                    ref.invalidate(schemesListProvider(farmId));
                    ref.invalidate(farmUpdatesProvider(farmId));
                  },
                  child: SingleChildScrollView(
                    physics: const AlwaysScrollableScrollPhysics(),
                    padding: const EdgeInsets.symmetric(
                      horizontal: AppSpacing.lg,
                      vertical: AppSpacing.md,
                    ),
                    child: Column(
                      crossAxisAlignment: CrossAxisAlignment.stretch,
                      children: [
                        // Header Greeting & Farm Identity
                        _buildHeader(ref, summary.farm.crop, summary.farm.landStatus, strings),

                        const SizedBox(height: AppSpacing.lg),

                        // Farm Identity Card
                        FarmIdentityCard(farm: summary.farm),

                        const SizedBox(height: AppSpacing.lg),

                        // Section 1: TODAY'S FARM BRIEF (Proactive advice preview)
                        DailyBriefPreview(farmId: farmId),

                        const SizedBox(height: AppSpacing.lg),

                        // Section 2: WHAT WOULD YOU LIKE TO DO? (Quick Action Grid)
                        QuickActionGrid(
                          farmId: farmId,
                          isLandVerified: summary.farm.landStatus == 'verified',
                        ),

                        const SizedBox(height: AppSpacing.lg),

                        // Section 3: LATEST UPDATES (Proactive alerts preview)
                        LatestUpdatePreview(farmId: farmId),

                        const SizedBox(height: AppSpacing.xxl),
                      ],
                    ),
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
      bottomNavigationBar: Container(
        decoration: const BoxDecoration(
          color: AppColors.surface,
          border: Border(top: BorderSide(color: AppColors.border, width: 1.0)),
          boxShadow: [
            BoxShadow(
              color: AppColors.cardShadow,
              blurRadius: 10.0,
              offset: Offset(0, -2),
            ),
          ],
        ),
        child: BottomNavigationBar(
          currentIndex: 0,
          elevation: 0,
          backgroundColor: Colors.transparent,
          selectedItemColor: AppColors.primaryGreen,
          unselectedItemColor: AppColors.textMuted,
          selectedLabelStyle: const TextStyle(fontWeight: FontWeight.w700, fontSize: 12.0),
          unselectedLabelStyle: const TextStyle(fontWeight: FontWeight.w500, fontSize: 11.0),
          type: BottomNavigationBarType.fixed,
          onTap: (index) {
            switch (index) {
              case 0:
                // Already on Home
                break;
              case 1:
                context.push('/ask/$farmId');
                break;
              case 2:
                context.push('/timeline/$farmId');
                break;
              case 3:
                context.push('/health/$farmId');
                break;
            }
          },
          items: [
            BottomNavigationBarItem(
              icon: const Icon(Icons.home_filled),
              label: strings.navHome,
            ),
            BottomNavigationBarItem(
              icon: const Icon(Icons.mic_rounded),
              label: strings.navCompanion,
            ),
            BottomNavigationBarItem(
              icon: const Icon(Icons.timeline_rounded),
              label: strings.navJourney,
            ),
            BottomNavigationBarItem(
              icon: const Icon(Icons.favorite_rounded),
              label: strings.navProfile,
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildHeader(WidgetRef ref, String crop, String landStatus, BhoomiStrings strings) {
    final userAsync = ref.watch(currentUserProvider);
    final greetingText = userAsync.maybeWhen(
      data: (user) => user.fullName.isNotEmpty ? 'Welcome, ${user.fullName}' : strings.dailyCompanion,
      orElse: () => strings.dailyCompanion,
    );

    return Row(
      mainAxisAlignment: MainAxisAlignment.spaceBetween,
      children: [
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                greetingText,
                style: AppTypography.bodyMedium.copyWith(
                  color: AppColors.textMuted,
                  fontWeight: FontWeight.w500,
                ),
              ),
              Text(
                strings.myFarm,
                style: const TextStyle(
                  fontSize: 26.0,
                  fontWeight: FontWeight.w900,
                  color: AppColors.textPrimary,
                  letterSpacing: -0.5,
                ),
              ),
            ],
          ),
        ),
        const SizedBox(width: AppSpacing.sm),
        LandStatusBadge(status: landStatus),
      ],
    );
  }

  Widget _buildErrorView(BuildContext context, WidgetRef ref, Object error, BhoomiStrings strings) {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(AppSpacing.xl),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            const Icon(Icons.error_outline_rounded, size: 48.0, color: Color(0xFFC62828)),
            const SizedBox(height: AppSpacing.md),
            const Text('Unable to Load Farm Dashboard', style: AppTypography.headlineMedium),
            const SizedBox(height: AppSpacing.sm),
            Text(error.toString(), textAlign: TextAlign.center, style: const TextStyle(color: AppColors.textMuted)),
            const SizedBox(height: AppSpacing.lg),
            BhoomiPrimaryButton(
              text: strings.retry,
              onPressed: () => ref.invalidate(farmSummaryProvider(farmId)),
            ),
          ],
        ),
      ),
    );
  }
}
