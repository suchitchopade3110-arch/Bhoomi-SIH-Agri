import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';
import '../../../../app/theme/app_colors.dart';
import '../../../../app/theme/app_spacing.dart';
import '../../../../app/theme/app_typography.dart';
import '../../../../core/widgets/bhoomi_card.dart';
import '../../../../core/widgets/bhoomi_primary_button.dart';
import '../../data/auth_repository.dart';
import '../../data/models/auth_models.dart';

class RegisterScreen extends ConsumerStatefulWidget {
  const RegisterScreen({super.key});

  @override
  ConsumerState<RegisterScreen> createState() => _RegisterScreenState();
}

class _RegisterScreenState extends ConsumerState<RegisterScreen> {
  final _formKey = GlobalKey<FormState>();
  final _nameController = TextEditingController();
  final _phoneController = TextEditingController(text: '+91');
  final _passwordController = TextEditingController();
  final _confirmPasswordController = TextEditingController();

  String _selectedLanguage = 'ta';
  bool _obscurePassword = true;
  bool _obscureConfirmPassword = true;
  bool _isLoading = false;
  String? _errorMessage;

  @override
  void dispose() {
    _nameController.dispose();
    _phoneController.dispose();
    _passwordController.dispose();
    _confirmPasswordController.dispose();
    super.dispose();
  }

  Future<void> _handleRegister() async {
    if (!_formKey.currentState!.validate()) return;

    setState(() {
      _isLoading = true;
      _errorMessage = null;
    });

    final phone = _phoneController.text.trim();
    final name = _nameController.text.trim();
    final password = _passwordController.text.trim();

    try {
      final repository = ref.read(authRepositoryProvider);
      await repository.register(UserRegisterRequest(
        phoneNumber: phone,
        fullName: name,
        role: 'farmer',
        preferredLanguage: _selectedLanguage,
        password: password,
      ));

      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          const SnackBar(
            content: Text('Registration successful! Please verify OTP or Sign In.'),
            backgroundColor: AppColors.primaryGreen,
          ),
        );
        // Navigate to OTP request or Login
        context.push('/otp-request');
      }
    } catch (e) {
      setState(() {
        _errorMessage = e.toString().replaceAll('Exception: ', '');
      });
    } finally {
      if (mounted) {
        setState(() {
          _isLoading = false;
        });
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.background,
      appBar: AppBar(
        title: const Text('Farmer Registration', style: TextStyle(fontWeight: FontWeight.w800)),
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
                        'Create Bhoomi Account',
                        style: AppTypography.headlineMedium.copyWith(color: AppColors.primaryDeepGreen),
                      ),
                      const SizedBox(height: AppSpacing.xs),
                      const Text(
                        'Register your farm details to access localized advisory, satellite land verification, and expert support.',
                        style: TextStyle(fontSize: 13.0, color: AppColors.textSecondary),
                      ),
                      const Divider(color: AppColors.divider, height: AppSpacing.xl),

                      // Full Name Input
                      Text('Full Name', style: AppTypography.labelMedium.copyWith(color: AppColors.textMuted)),
                      const SizedBox(height: AppSpacing.xs),
                      TextFormField(
                        controller: _nameController,
                        decoration: InputDecoration(
                          hintText: 'e.g. Muthu Kumar',
                          prefixIcon: const Icon(Icons.person_outline_rounded, color: AppColors.primaryGreen),
                          filled: true,
                          fillColor: AppColors.background,
                          border: OutlineInputBorder(
                            borderRadius: BorderRadius.circular(AppSpacing.radiusMd),
                            borderSide: const BorderSide(color: AppColors.border),
                          ),
                        ),
                        validator: (value) {
                          if (value == null || value.trim().isEmpty) {
                            return 'Please enter your full name';
                          }
                          return null;
                        },
                      ),
                      const SizedBox(height: AppSpacing.md),

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
                          if (value == null || value.trim().length < 10) {
                            return 'Please enter a valid phone number';
                          }
                          return null;
                        },
                      ),
                      const SizedBox(height: AppSpacing.md),

                      // Preferred Language Dropdown
                      Text('Preferred Language', style: AppTypography.labelMedium.copyWith(color: AppColors.textMuted)),
                      const SizedBox(height: AppSpacing.xs),
                      DropdownButtonFormField<String>(
                        initialValue: _selectedLanguage,
                        items: const [
                          DropdownMenuItem(value: 'ta', child: Text('Tamil (தமிழ்)')),
                          DropdownMenuItem(value: 'en', child: Text('English')),
                          DropdownMenuItem(value: 'hi', child: Text('Hindi (हिन्दी)')),
                        ],
                        onChanged: (val) {
                          if (val != null) setState(() => _selectedLanguage = val);
                        },
                        decoration: InputDecoration(
                          prefixIcon: const Icon(Icons.language_rounded, color: AppColors.primaryGreen),
                          filled: true,
                          fillColor: AppColors.background,
                          border: OutlineInputBorder(
                            borderRadius: BorderRadius.circular(AppSpacing.radiusMd),
                            borderSide: const BorderSide(color: AppColors.border),
                          ),
                        ),
                      ),
                      const SizedBox(height: AppSpacing.md),

                      // Password Input
                      Text('Password', style: AppTypography.labelMedium.copyWith(color: AppColors.textMuted)),
                      const SizedBox(height: AppSpacing.xs),
                      TextFormField(
                        controller: _passwordController,
                        obscureText: _obscurePassword,
                        decoration: InputDecoration(
                          hintText: 'At least 6 characters',
                          prefixIcon: const Icon(Icons.lock_outline_rounded, color: AppColors.primaryGreen),
                          suffixIcon: IconButton(
                            icon: Icon(
                              _obscurePassword ? Icons.visibility_outlined : Icons.visibility_off_outlined,
                              color: AppColors.textMuted,
                            ),
                            onPressed: () => setState(() => _obscurePassword = !_obscurePassword),
                          ),
                          filled: true,
                          fillColor: AppColors.background,
                          border: OutlineInputBorder(
                            borderRadius: BorderRadius.circular(AppSpacing.radiusMd),
                            borderSide: const BorderSide(color: AppColors.border),
                          ),
                        ),
                        validator: (value) {
                          if (value == null || value.trim().length < 6) {
                            return 'Password must be at least 6 characters';
                          }
                          return null;
                        },
                      ),
                      const SizedBox(height: AppSpacing.md),

                      // Confirm Password Input
                      Text('Confirm Password', style: AppTypography.labelMedium.copyWith(color: AppColors.textMuted)),
                      const SizedBox(height: AppSpacing.xs),
                      TextFormField(
                        controller: _confirmPasswordController,
                        obscureText: _obscureConfirmPassword,
                        decoration: InputDecoration(
                          hintText: 'Re-enter password',
                          prefixIcon: const Icon(Icons.lock_clock_outlined, color: AppColors.primaryGreen),
                          suffixIcon: IconButton(
                            icon: Icon(
                              _obscureConfirmPassword ? Icons.visibility_outlined : Icons.visibility_off_outlined,
                              color: AppColors.textMuted,
                            ),
                            onPressed: () => setState(() => _obscureConfirmPassword = !_obscureConfirmPassword),
                          ),
                          filled: true,
                          fillColor: AppColors.background,
                          border: OutlineInputBorder(
                            borderRadius: BorderRadius.circular(AppSpacing.radiusMd),
                            borderSide: const BorderSide(color: AppColors.border),
                          ),
                        ),
                        validator: (value) {
                          if (value != _passwordController.text) {
                            return 'Passwords do not match';
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

                // Register Button
                BhoomiPrimaryButton(
                  text: 'Register Account',
                  isLoading: _isLoading,
                  icon: Icons.person_add_rounded,
                  onPressed: _handleRegister,
                ),

                const SizedBox(height: AppSpacing.md),

                // Back to Login Link
                Row(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: [
                    const Text('Already have an account? ', style: TextStyle(color: AppColors.textMuted, fontSize: 13.0)),
                    TextButton(
                      onPressed: () => context.go('/login'),
                      child: const Text(
                        'Sign In',
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
