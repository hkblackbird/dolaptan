import 'dart:typed_data';

import '../models/models.dart';
import 'recipe_catalog.dart';
import 'repositories.dart';
import 'shelf_life.dart';

/// [RecipeAiService] sözleşmesini yapay zeka olmadan, katalogla yerine getirir.
/// Gerçek AI servisi hazır olunca main.dart'ta yalnızca bu sınıf değişir.
class LocalRecipeService implements RecipeAiService {
  int _round = 0;

  /// Fotoğraftan tanıma için henüz model yok: örnek bir sonuç döner
  /// ve emin olunmayan ürünü işaretler. Tarihler tahminidir.
  @override
  Future<List<ScannedItem>> detectItems(Uint8List photo) async {
    await Future.delayed(const Duration(milliseconds: 1500));
    return [
      for (final (name, unsure) in [('Süt', false), ('Salatalık', false), ('Tereyağı', true)])
        ScannedItem(name: name, isUncertain: unsure, expiresOn: estimateExpiry(name), estimated: true),
    ];
  }

  @override
  Future<List<Recipe>> suggestRecipes(List<PantryItem> pantry, Preferences prefs) async {
    await Future.delayed(const Duration(milliseconds: 600));
    final have = {for (final p in pantry) if (p.state != ItemState.out) norm(p.name): p};
    final expiring = {for (final p in pantry) if (p.isExpiringSoon) norm(p.name)};
    final allergies = prefs.allergies.map(norm).toSet();

    final scored = <(double, Recipe)>[];
    for (final c in catalog) {
      if (c.minutes > prefs.minutes) continue;
      if (c.allergens.any((a) => allergies.contains(norm(a)))) continue;
      final used = <String>[], missing = <String>[], usesExpiring = <String>[];
      for (final ing in c.ingredients) {
        final k = norm(ing);
        if (have.containsKey(k)) {
          used.add(ing);
          if (expiring.contains(k)) usesExpiring.add(ing);
        } else if (!staples.contains(k)) {
          missing.add(ing);
        }
      }
      if (used.isEmpty) continue;
      if (prefs.maxMissing != null && missing.length > prefs.maxMissing!) continue;
      final score = usesExpiring.length * 3 + used.length - missing.length * 2.0;
      scored.add((
        score,
        Recipe(
          id: c.id,
          title: c.title,
          minutes: c.minutes,
          servings: prefs.servings,
          usedIngredients: c.ingredients,
          usesExpiring: usesExpiring,
          missingIngredients: missing,
          steps: c.steps,
          photoPath: c.image,
        )
      ));
    }
    scored.sort((a, b) => b.$1.compareTo(a.$1));
    final all = scored.map((e) => e.$2).toList();
    if (all.length <= 3) return all;
    // "Başka tarifler öner": her turda listenin bir sonraki üçlüsü.
    final start = (_round++ * 3) % all.length;
    return [for (var i = 0; i < 3; i++) all[(start + i) % all.length]];
  }
}
