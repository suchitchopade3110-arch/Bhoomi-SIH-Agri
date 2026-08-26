import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../../../app/theme/app_colors.dart';
import '../../../../app/theme/app_spacing.dart';
import '../../../../app/theme/app_typography.dart';
import '../../../../core/widgets/bhoomi_card.dart';
import '../../../../core/widgets/bhoomi_primary_button.dart';
import '../providers/auth_providers.dart';

class LoginScreen extends ConsumerStatefulWidget {
  const LoginScreen({super.key});

  @override
  ConsumerState<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends ConsumerState<LoginScreen> {
  final _formKey = GlobalKey<FormState>();
  final _phoneController = TextEditingController(text: '+919876543210');
  final _passwordController = TextEditingController(text: 'Password123!');
  bool _obscurePassword = true;
  String? _errorMessage;

  @override
  void dispose() {
    _phoneController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  Future<void> _handleLogin() async {
    if (!_formKey.currentState!.validate()) return;

    setState(() {
      _errorMessage = null;
    });

    final phone = _phoneController.text.trim();
    final password = _passwordController.text.trim();

    try {
      await ref.read(authStateProvider.notifier).login(phone, password);
      if (mounted) {
        context.go('/home/f_1');
      }
    } catch (e) {
      setState(() {
        _errorMessage = e.toString().replaceAll('Exception: ', '');
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
          child: Form(
            key: _formKey,
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
                        'Welcome Back',
                        style: AppTypography.headlineMedium.copyWith(color: AppColors.primaryDeepGreen),
                      ),
                      const SizedBox(height: AppSpacing.xs),
                      const Text(
                        'Sign in to access your Bhoomi farm dashboard, advisory, and health records.',
                        style: TextStyle(fontSize: 13.0, color: AppColors.textSecondary),
                      ),
                      const Divider(color: AppColors.divider, height: AppSpacing.xl),

                      // Phone Number Input
                      Text('Phone Number', style: AppTypography.labelMedium.copyWith(color: AppColors.textMuted)),
                      const SizedBox(height: AppSpacing.xs),
                      TextFormField(
                        controller: _phoneController,
                        keyboardType: TextInputType.phone,
                        decoration: InputDecoration(
                          hintText: '+919876543210',
                          prefixIcon: const Icon(Icons.phone_outlined, color: AppColors.primaryGreen),
                          filled: true,
                          fillColor: AppColors.background,
                          border: OutlineInputBorder(
                            borderRadius: BorderRadius.circular(AppSpacing.radiusMd),
                            borderSide: const BorderSide(color: AppColors.border),
                          ),
                        ),
                        validator: (value) {
                          if (value == null || value.trim().isEmpty) {
                            return 'Please enter your phone number';
                          }
                          return null;
                        },
                      ),
                      const SizedBox(height: AppSpacing.md),

                      // Password Input
                      Text('Password', style: AppTypography.labelMedium.copyWith(color: AppColors.textMuted)),
                      const SizedBox(height: AppSpacing.xs),
                      TextFormField(
                        controller: _passwordController,
                        obscureText: _obscurePassword,
                        decoration: InputDecoration(
                          hintText: '••••••••',
                          prefixIcon: const Icon(Icons.lock_outline_rounded, color: AppColors.primaryGreen),
                          suffixIcon: IconButton(
                            icon: Icon(
                              _obscurePassword ? Icons.visibility_outlined : Icons.visibility_off_outlined,
                              color: AppColors.textMuted,
                            ),
                            onPressed: () {
                              setState(() {
                                _obscurePassword = !_obscurePassword;
                              });
                            },
                          ),
                          filled: true,
                          fillColor: AppColors.background,
                          border: OutlineInputBorder(
                            borderRadius: BorderRadius.circular(AppSpacing.radiusMd),
                            borderSide: const BorderSide(color: AppColors.border),
                          ),
                        ),
                        validator: (value) {
                          if (value == null || value.trim().isEmpty) {
                            return 'Please enter your password';
                          }
                          return null;
                        },
                      ),

                      if (_errorMessage != null) ...[
                        const SizedBox(height: AppSpacing.md),
                        Container(
                          padding: const EdgeInsets.all(AppSpacing.md),
                          decoration: BoxDecoration(
                            color: const Color(0xFFFFEBEE),
                            borderRadius: BorderRadius.circular(AppSpacing.radiusMd),
                            border: Border.all(color: const Color(0xFFEF9A9A)),
                          ),
                          child: Row(
                            children: [
                              const Icon(Icons.error_outline_rounded, color: Color(0xFFC62828), size: 20.0),
                              const SizedBox(width: AppSpacing.sm),
                              Expanded(
                                child: Text(
                                  _errorMessage!,
                                  style: const TextStyle(fontSize: 12.5, color: Color(0xFFC62828), fontWeight: FontWeight.w600),
                                ),
                              ),
                            ],
                          ),
                        ),
                      ],
                    ],
                  ),
                ),

                const SizedBox(height: AppSpacing.xl),

                // Submit Login Button
                BhoomiPrimaryButton(
                  text: 'Sign In',
                  isLoading: authState.isLoading,
                  icon: Icons.login_rounded,
                  onPressed: _handleLogin,
                ),

                const SizedBox(height: AppSpacing.lg),

                // Alternate OTP Login Option
                OutlinedButton.icon(
                  onPressed: () => context.push('/otp-request'),
                  icon: const Icon(Icons.sms_outlined, size: 18.0),
                  label: const Text('Sign In via SMS OTP'),
                  style: OutlinedButton.styleFrom(
                    foregroundColor: AppColors.primaryGreen,
                    side: const BorderSide(color: AppColors.primaryGreen),
                    padding: const EdgeInsets.symmetric(vertical: AppSpacing.md),
                    shape: RoundedRectangleBorder(borderRadius: BorderRadius.circular(AppSpacing.radiusMd)),
                  ),
                ),

                const SizedBox(height: AppSpacing.md),

                // Register Link
                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    const Text("Don't have an account? ", style: TextStyle(color: AppColors.textMuted, fontSize: 13.0)),
                    TextButton(
                      onPressed: () => context.push('/register'),
                      child: const Text(
                        'Register Now',
                        style: TextStyle(color: AppColors.primaryGreen, fontWeight: FontWeight.w800, fontSize: 13.0),
                      ),
                    ),
                  ],
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
