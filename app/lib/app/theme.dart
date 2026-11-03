import 'package:flutter/cupertino.dart';

import '../data/shelf_life.dart';

/// Tarif defteri teması: krem kağıt, mürekkep kahvesi, el yazısı.
/// Renkler Figma mockup'larıyla aynı (tools/build_screens.py, LIGHT / DARK).
class AppColors {
  static const bg = CupertinoDynamicColor.withBrightness(color: Color(0xFFF7EBDD), darkColor: Color(0xFF1B1511));
  static const surface = CupertinoDynamicColor.withBrightness(color: Color(0xFFFFFAF3), darkColor: Color(0xFF2A211B));
  static const text = CupertinoDynamicColor.withBrightness(color: Color(0xFF2B1D14), darkColor: Color(0xFFF7EBDD));
  static const text2 = CupertinoDynamicColor.withBrightness(color: Color(0xFF6B5646), darkColor: Color(0xFFC8B6A3));
  static const ink = CupertinoDynamicColor.withBrightness(color: Color(0xFF2B1D14), darkColor: Color(0xFFF7EBDD));
  static const sep = CupertinoDynamicColor.withBrightness(color: Color(0xFFE8D7C2), darkColor: Color(0xFF3E332A));
  static const rule = CupertinoDynamicColor.withBrightness(color: Color(0xFFEADBC6), darkColor: Color(0xFF251D17));
  static const accent = CupertinoDynamicColor.withBrightness(color: Color(0xFFB3401E), darkColor: Color(0xFFFF8A65));
  static const onAccent = CupertinoDynamicColor.withBrightness(color: Color(0xFFFFFFFF), darkColor: Color(0xFF1B1511));
  static const herb = CupertinoDynamicColor.withBrightness(color: Color(0xFF3B6E35), darkColor: Color(0xFF9CCB8C));
  static const red = CupertinoDynamicColor.withBrightness(color: Color(0xFFB3261A), darkColor: Color(0xFFFF6F61));
  static const fill = CupertinoDynamicColor.withBrightness(color: Color(0xFFEFDFCB), darkColor: Color(0xFF3A2F27));
  static const tagRed = CupertinoDynamicColor.withBrightness(color: Color(0xFFFAE4DB), darkColor: Color(0xFF4A271D));
  static const tagGreen = CupertinoDynamicColor.withBrightness(color: Color(0xFFE0ECD6), darkColor: Color(0xFF263821));
  static const tagYellow = CupertinoDynamicColor.withBrightness(color: Color(0xFFF7E6B5), darkColor: Color(0xFF40341A));
  static const tagTextY = CupertinoDynamicColor.withBrightness(color: Color(0xFF7A5200), darkColor: Color(0xFFEBC66A));
  static const tape = CupertinoDynamicColor.withBrightness(color: Color(0xBFE9C46A), darkColor: Color(0xBF8C6A2B));
}

class Fonts {
  static const hand = 'PatrickHand'; // gövde metni
  static const script = 'Caveat'; // başlık ve vurgu
}

TextStyle body(BuildContext c, {double size = 18.5, Color? color}) =>
    TextStyle(fontFamily: Fonts.hand, fontSize: size, color: color ?? AppColors.text.resolveFrom(c), height: 1.15);

TextStyle meta(BuildContext c, {double size = 14.5}) => body(c, size: size, color: AppColors.text2.resolveFrom(c));

TextStyle script(BuildContext c, {double size = 22, Color? color}) => TextStyle(
    fontFamily: Fonts.script,
    fontWeight: FontWeight.w700,
    fontSize: size,
    color: color ?? AppColors.text.resolveFrom(c),
    height: 1.05);

final appTheme = CupertinoThemeData(
  primaryColor: AppColors.accent,
  scaffoldBackgroundColor: AppColors.bg,
  barBackgroundColor: AppColors.bg,
  textTheme: const CupertinoTextThemeData(
    textStyle: TextStyle(fontFamily: Fonts.hand, fontSize: 18.5, color: AppColors.text),
    tabLabelTextStyle: TextStyle(fontFamily: Fonts.script, fontWeight: FontWeight.w700, fontSize: 14),
    navTitleTextStyle:
        TextStyle(fontFamily: Fonts.script, fontWeight: FontWeight.w700, fontSize: 22, color: AppColors.text),
    actionTextStyle: TextStyle(fontFamily: Fonts.hand, fontSize: 18.5, color: AppColors.accent),
  ),
);

String expiryLabel(int? days) {
  if (days == null) return '';
  if (days < 0) return 'Geçti';
  if (days == 0) return 'Bugün';
  if (days == 1) return 'Yarın';
  return '$days gün';
}

const _months = ['Oca', 'Şub', 'Mar', 'Nis', 'May', 'Haz', 'Tem', 'Ağu', 'Eyl', 'Eki', 'Kas', 'Ara'];
String shortDate(DateTime d) => '${d.day} ${_months[d.month - 1]}';

/// Çizim dosyaları -------------------------------------------------------------------------
const _ingredientArt = {
  'yoğurt': 'yogurt', 'domates': 'domates', 'yumurta': 'yumurta', 'patates': 'patates', 'soğan': 'sogan',
  'peynir': 'peynir', 'beyaz peynir': 'peynir', 'maydanoz': 'maydanoz', 'biber': 'biber',
  'tereyağı': 'tereyagi', 'salatalık': 'salatalik', 'ekmek': 'ekmek', 'süt': 'sut',
};

/// Malzeme çizimi; yoksa null (yerine baş harfli bir daire çizilir).
String? ingredientArt(String name) {
  final k = _ingredientArt[norm(name)];
  if (k == null) return null;
  return k == 'peynir' ? 'assets/img/malzeme/peynir.jpg' : 'assets/img/malzeme/$k.png';
}

String doodle(String key) => 'assets/img/sus/$key.png';
String cover(String key) => 'assets/img/kapak/$key.png';
String scene(String key) => 'assets/img/sahne/$key.jpg';

/// Tarif çizimleri: kare küçük resim ve büyük kapak.
String dishSquare(String? base) => base == null ? scene('tencere') : '$base-kare.jpg';
String dishHero(String? base) {
  if (base == null) return scene('tencere');
  return base.endsWith('omlet') ? '$base-16x9.jpg' : '$base-buyuk.jpg';
}
