/// Kullanıcı tarih yazmasın diye ürün türüne göre tahmini raf ömrü (gün).
/// Rakip uygulamalarda en çok şikayet edilen şey her tarihi elle girmekti.
const _days = {
  'yoğurt': 7, 'domates': 5, 'yumurta': 21, 'patates': 30, 'soğan': 30, 'peynir': 14,
  'beyaz peynir': 14, 'kaşar peyniri': 21, 'maydanoz': 5, 'biber': 7, 'tereyağı': 30,
  'salatalık': 7, 'ekmek': 3, 'süt': 5, 'sarımsak': 30, 'limon': 14, 'havuç': 21,
  'ıspanak': 4, 'taze fasulye': 5, 'kırmızı mercimek': 180, 'un': 180, 'yufka': 5,
};

String norm(String s) => s.trim().replaceAll('I', 'ı').replaceAll('İ', 'i').toLowerCase();

DateTime estimateExpiry(String name, {DateTime? from}) {
  final d = _days[norm(name)] ?? 7;
  final f = from ?? DateTime.now();
  return DateTime(f.year, f.month, f.day).add(Duration(days: d));
}
