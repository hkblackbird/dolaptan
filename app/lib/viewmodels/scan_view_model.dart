import 'package:flutter/foundation.dart';

import '../data/repositories.dart';
import '../data/shelf_life.dart';
import '../models/models.dart';

/// Yeni malzemeler: fotoğraftan bulunanlar ya da elle eklenenler.
/// Tarihler ürün türüne göre tahmin edilir, kullanıcı yalnızca yanlışsa düzeltir.
class ScanViewModel extends ChangeNotifier {
  ScanViewModel(this._ai);
  final RecipeAiService _ai;

  bool analyzing = false;
  String? error;
  List<ScannedItem> detected = [];

  void startManual() {
    detected = [];
    error = null;
    notifyListeners();
  }

  Future<bool> analyze(Uint8List photo) async {
    analyzing = true;
    error = null;
    notifyListeners();
    try {
      detected = await _ai.detectItems(photo);
      return true;
    } catch (_) {
      error = 'Fotoğraf incelenemedi. Tekrar dene.';
      return false;
    } finally {
      analyzing = false;
      notifyListeners();
    }
  }

  void add(String name) {
    final n = name.trim();
    if (n.isEmpty || detected.any((d) => norm(d.name) == norm(n))) return;
    detected.add(ScannedItem(name: _capitalize(n), expiresOn: estimateExpiry(n), estimated: true));
    notifyListeners();
  }

  void removeAt(int i) {
    detected.removeAt(i);
    notifyListeners();
  }

  void rename(int i, String name) {
    detected[i]
      ..name = _capitalize(name.trim())
      ..isUncertain = false;
    notifyListeners();
  }

  void setDate(int i, DateTime d) {
    detected[i]
      ..expiresOn = d
      ..estimated = false;
    notifyListeners();
  }

  static String _capitalize(String s) =>
      s.isEmpty ? s : s[0].replaceAll('i', 'İ').replaceAll('ı', 'I').toUpperCase() + s.substring(1);
}
