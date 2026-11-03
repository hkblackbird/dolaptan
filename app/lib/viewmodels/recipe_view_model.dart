import 'dart:async';

import 'package:flutter/foundation.dart';

import '../data/repositories.dart';
import '../models/models.dart';

class RecipeViewModel extends ChangeNotifier {
  RecipeViewModel(this._ai, this._saved, this._prefs) : prefs = _prefs.load() {
    _sub = _saved.watchAll().listen((r) {
      saved = r;
      notifyListeners();
    });
  }
  final RecipeAiService _ai;
  final SavedRecipeRepository _saved;
  final PreferencesRepository _prefs;
  late final StreamSubscription _sub;

  Preferences prefs;
  List<Recipe> suggestions = [];
  List<Recipe> saved = [];
  bool loading = false;
  String? error;
  String query = '';

  /// Tercihler bir sonraki açılışta hatırlanır.
  void setPrefs(Preferences p) {
    prefs = p;
    _prefs.save(p);
    notifyListeners();
  }

  /// Bozulmaya yakın malzemeler önce gelir; katalog süre, alerji ve eksik sınırına uyar.
  Future<void> suggest(List<PantryItem> pantry) async {
    loading = true;
    error = null;
    suggestions = [];
    notifyListeners();
    try {
      final sorted = [...pantry]..sort((a, b) => (a.daysLeft ?? 999).compareTo(b.daysLeft ?? 999));
      suggestions = await _ai.suggestRecipes(sorted, prefs);
    } catch (_) {
      error = 'Tarifler alınamadı.';
    } finally {
      loading = false;
      notifyListeners();
    }
  }

  void search(String q) {
    query = q;
    notifyListeners();
  }

  List<Recipe> get filteredSaved => query.trim().isEmpty
      ? saved
      : saved.where((r) => r.title.toLowerCase().contains(query.trim().toLowerCase())).toList();

  Recipe? byId(String id) {
    for (final r in [...suggestions, ...saved]) {
      if (r.id == id) return r;
    }
    return null;
  }

  bool isSaved(String id) => saved.any((r) => r.id == id);

  Future<void> toggleSave(Recipe r) => isSaved(r.id) ? _saved.delete(r.id) : _saved.save(r);

  @override
  void dispose() {
    _sub.cancel();
    super.dispose();
  }
}
