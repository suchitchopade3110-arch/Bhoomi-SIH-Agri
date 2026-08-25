import 'package:flutter/widgets.dart';

class AppBranding {
  static const String logoPath = 'assets/images/bhoomi_logo.png';
  static const String emblemPath = 'assets/images/bhoomi_emblem.png';
  static const String iconPath = 'assets/icons/app_icon.png';
  static const String heroPath = 'assets/illustrations/farmer_hero.jpg';

  static Widget emblem({double? height, double? width, BoxFit fit = BoxFit.contain}) {
    return Image.asset(
      emblemPath,
      height: height,
      width: width,
      fit: fit,
      errorBuilder: (_, __, ___) => Image.asset(
        logoPath,
        height: height,
        width: width,
        fit: fit,
      ),
    );
  }

  static Widget emblemImage({double? height, double? width, BoxFit fit = BoxFit.contain}) {
    return emblem(height: height, width: width, fit: fit);
  }

  static Widget logo({double? height, double? width, BoxFit fit = BoxFit.contain}) {
    return Image.asset(
      logoPath,
      height: height,
      width: width,
      fit: fit,
      errorBuilder: (_, __, ___) => Image.asset(
        emblemPath,
        height: height,
        width: width,
        fit: fit,
      ),
    );
  }

  static Widget logoImage({double? height, double? width, BoxFit fit = BoxFit.contain}) {
    return logo(height: height, width: width, fit: fit);
  }

  static Widget appIcon({double? height, double? width, BoxFit fit = BoxFit.contain}) {
    return Image.asset(
      iconPath,
      height: height,
      width: width,
      fit: fit,
      errorBuilder: (_, __, ___) => Image.asset(
        emblemPath,
        height: height,
        width: width,
        fit: fit,
      ),
    );
  }

  static Widget heroIllustration({double? height, double? width, BoxFit fit = BoxFit.cover}) {
    return Image.asset(
      heroPath,
      height: height,
      width: width,
      fit: fit,
    );
  }
}
