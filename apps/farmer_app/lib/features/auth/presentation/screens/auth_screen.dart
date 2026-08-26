import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../../../app/theme/app_colors.dart';
import '../../../../app/theme/app_spacing.dart';
import '../../../../app/theme/app_typography.dart';
import '../../../../core/widgets/bhoomi_card.dart';
import '../../../../core/widgets/bhoomi_primary_button.dart';
import '../../../../core/widgets/bhoomi_secondary_button.dart';
import '../providers/auth_providers.dart';
import '../../data/auth_repository.dart';
import '../../data/models/auth_models.dart';

class AuthScreen extends ConsumerStatefulWidget {
  const AuthScreen({super.key});

  @override
  ConsumerState<AuthScreen> createState() => _AuthScreenState();
}

class _AuthScreenState extends ConsumerState<AuthScreen> {
  final _phoneController = TextEditingController(text: '+919876543210');
  final _otpController = TextEditingController();
  final _nameController = TextEditingController(text: 'Bhoomi Farmer');
  bool _otpSent = false;
  String? _debugOtp;
  String? _infoMessage;

  @override
  void dispose() {
    _phoneController.dispose();
    _otpController.dispose();
    _nameController.dispose();
    super.dispose();
  }

  Future<void> _requestOtp() async {
    final phone = _phoneController.text.trim();
    if (phone.isEmpty) return;

    setState(() {
      _infoMessage = null;
    });

    try {
      final repo = ref.read(authRepositoryProvider);
      final res = await repo.requestOtp(phone);
      setState(() {
        _otpSent = true;
        _debugOtp = res.debugOtp;
        _infoMessage = res.message;
      });
    } catch (e) {
      setState(() {
        _infoMessage = 'Error sending OTP: ${e.toString()}';
      });
    }
  }

  Future<void> _verifyOtp() async {
    final phone = _phoneController.text.trim();
    final otp = _otpController.text.trim();
    if (phone.isEmpty || otp.isEmpty) return;

    setState(() {
      _infoMessage = null;
    });

    try {
      await ref.read(authStateProvider.notifier).verifyOtp(
            OtpVerifyRequest(
              phoneNumber: phone,
              otp: otp,
              fullName: _nameController.text.trim(),
              preferredLanguage: 'ta',
            ),
          );

      if (mounted) {
        // Success -> Go to onboarding
        context.go('/onboarding');
      }
    } catch (e) {
      setState(() {
        _infoMessage = 'Invalid OTP: ${e.toString()}';
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    final authState = ref.watch(authStateProvider);

    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        title: const Text('Farmer Sign In', style: TextStyle(fontWeight: FontWeight.w800)),
        scrolledUnderElevation: 0,
      ),
      body: SafeArea(
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(AppSpacing.lg),
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              const SizedBox(height: AppSpacing.md),
              BhoomiCard(
                padding: const EdgeInsets.all(AppSpacing.xl),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Text(
                      _otpSent ? 'Enter 6-Digit OTP' : 'Verification Required',
                      style: AppTypography.headlineMedium.copyWith(color: AppColors.primaryDeepGreen),
                    ),
                    const SizedBox(height: AppSpacing.sm),
                    Text(
                      _otpSent
                          ? 'Please enter the OTP sent to your registered phone number.'
                          : 'Sign in or register to set up your Bhoomi farm companion.',
                      style: const TextStyle(fontSize: 13.0, color: AppColors.textSecondary),
                    ),
                    const Divider(color: AppColors.divider, height: AppSpacing.xl),
                    if (!_otpSent) ...[
                      // Name field (Optional)
                      Text('Full Name', style: AppTypography.labelMedium.copyWith(color: AppColors.textMuted)),
                      const SizedBox(height: AppSpacing.xs),
                      TextField(
                        controller: _nameController,
                        decoration: InputDecoration(
                          hintText: 'e.g. Muthu Kumar',
                          filled: true,
                          fillColor: AppColors.background,
                          border: OutlineInputBorder(
                            borderRadius: BorderRadius.circular(AppSpacing.radiusMd),
                            borderSide: const BorderSide(color: AppColors.border),
                          ),
                        ),
                      ),
                      const SizedBox(height: AppSpacing.md),
                      // Phone Number
                      Text('Phone Number', style: AppTypography.labelMedium.copyWith(color: AppColors.textMuted)),
                      const SizedBox(height: AppSpacing.xs),
                      TextField(
                        controller: _phoneController,
                        keyboardType: TextInputType.phone,
                        decoration: InputDecoration(
                          hintText: '+919876543210',
                          filled: true,
                          fillColor: AppColors.background,
                          border: OutlineInputBorder(
                            borderRadius: BorderRadius.circular(AppSpacing.radiusMd),
                            borderSide: const BorderSide(color: AppColors.border),
                          ),
                        ),
                      ),
                    ] else ...[
                      // OTP Input
                      Text('Verification Code (OTP)', style: AppTypography.labelMedium.copyWith(color: AppColors.textMuted)),
                      const SizedBox(height: AppSpacing.xs),
                      TextField(
                        controller: _otpController,
                        keyboardType: TextInputType.number,
                        maxLength: 6,
                        decoration: InputDecoration(
                          hintText: '123456',
                          filled: true,
                          fillColor: AppColors.background,
                          border: OutlineInputBorder(
                            borderRadius: BorderRadius.circular(AppSpacing.radiusMd),
                            borderSide: const BorderSide(color: AppColors.border),
                          ),
                        ),
                      ),
                    ],
                    if (_infoMessage != null) ...[
                      const SizedBox(height: AppSpacing.md),
                      Text(
                        _infoMessage!,
                        style: const TextStyle(fontSize: 12.5, color: Color(0xFFC62828), fontWeight: FontWeight.w600),
                      ),
                    ],
                    if (_debugOtp != null) ...[
                      const SizedBox(height: AppSpacing.xs),
                      Container(
                        padding: const EdgeInsets.all(AppSpacing.xs),
                        decoration: BoxDecoration(
                          color: AppColors.lightGreen,
                          borderRadius: BorderRadius.circular(AppSpacing.radiusSm),
                        ),
                        child: Text(
                          'Debug OTP: $_debugOtp',
                          style: const TextStyle(fontSize: 12.0, fontWeight: FontWeight.w700, color: AppColors.primaryGreen),
                        ),
                      ),
                    ],
                  ],
                ),
              ),
              const SizedBox(height: AppSpacing.xl),
              if (!_otpSent)
                BhoomiPrimaryButton(
                  text: 'Send Verification OTP',
                  icon: Icons.sms_rounded,
                  onPressed: _requestOtp,
                )
              else
                Column(
                  crossAxisAlignment: CrossAxisAlignment.stretch,
                  children: [
                    BhoomiPrimaryButton(
                      text: 'Verify & Proceed',
                      isLoading: authState.isLoading,
                      icon: Icons.check_circle_outline_rounded,
                      onPressed: _verifyOtp,
                    ),
                    const SizedBox(height: AppSpacing.sm),
                    BhoomiSecondaryButton(
                      text: 'Back',
                      icon: Icons.arrow_back_rounded,
                      onPressed: () {
                        setState(() {
                          _otpSent = false;
                          _debugOtp = null;
                        });
                      },
                    ),
                  ],
                ),
            ],
          ),
        ),
      ),
    );
  }
}
