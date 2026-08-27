import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../app/theme/app_colors.dart';
import '../../app/theme/app_spacing.dart';
import '../../core/localization/bhoomi_localizations.dart';

class BhoomiBottomNavigation extends ConsumerWidget {
  final String farmId;
  final int currentIndex;

  const BhoomiBottomNavigation({
    super.key,
    required this.farmId,
    required this.currentIndex,
  });

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final strings = ref.watch(bhoomiStringsProvider);

    return Container(
      decoration: BoxDecoration(
        color: AppColors.surface,
        border: const Border(
          top: BorderSide(color: AppColors.border, width: 1.0),
        ),
        boxShadow: [
          BoxShadow(
            color: Colors.black.withValues(alpha: 0.04),
            blurRadius: 16.0,
            offset: const Offset(0, -4),
          ),
        ],
      ),
      child: SafeArea(
        top: false,
        child: Padding(
          padding: const EdgeInsets.symmetric(vertical: 8.0, horizontal: 12.0),
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceAround,
            children: [
              _buildNavItem(
                context,
                index: 0,
                icon: Icons.home_rounded,
                activeIcon: Icons.home_filled,
                label: strings.navHome,
                route: '/home/$farmId',
              ),
              _buildNavItem(
                context,
                index: 1,
                icon: Icons.mic_none_rounded,
                activeIcon: Icons.mic_rounded,
                label: strings.navCompanion,
                route: '/ask/$farmId',
              ),
              _buildNavItem(
                context,
                index: 2,
                icon: Icons.timeline_rounded,
                activeIcon: Icons.timeline_rounded,
                label: strings.navJourney,
                route: '/timeline/$farmId',
              ),
              _buildNavItem(
                context,
                index: 3,
                icon: Icons.favorite_border_rounded,
                activeIcon: Icons.favorite_rounded,
                label: strings.navProfile,
                route: '/health/$farmId',
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildNavItem(
    BuildContext context, {
    required int index,
    required IconData icon,
    required IconData activeIcon,
    required String label,
    required String route,
  }) {
    final isSelected = currentIndex == index;

    return Expanded(
      child: InkWell(
        onTap: () {
          if (!isSelected) {
            context.go(route);
          }
        },
        borderRadius: BorderRadius.circular(AppSpacing.radiusMd),
        child: Padding(
          padding: const EdgeInsets.symmetric(vertical: 6.0),
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Icon(
                isSelected ? activeIcon : icon,
                color: isSelected ? AppColors.primaryGreen : AppColors.textMuted,
                size: 24.0,
              ),
              const SizedBox(height: 3.0),
              Text(
                label,
                style: TextStyle(
                  fontSize: 11.5,
                  fontWeight: isSelected ? FontWeight.w800 : FontWeight.w600,
                  color: isSelected ? AppColors.primaryGreen : AppColors.textMuted,
                  letterSpacing: -0.1,
                ),
              ),
              const SizedBox(height: 2.0),
              // Subtle indicator bar
              AnimatedContainer(
                duration: const Duration(milliseconds: 200),
                height: 3.0,
                width: isSelected ? 16.0 : 0.0,
                decoration: BoxDecoration(
                  color: AppColors.primaryGreen,
                  borderRadius: BorderRadius.circular(1.5),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
