import 'package:dolaptan/data/fake_repositories.dart';
import 'package:dolaptan/data/local_recipe_service.dart';
import 'package:dolaptan/data/shelf_life.dart';
import 'package:dolaptan/models/models.dart';
import 'package:flutter_test/flutter_test.dart';

void main() {
  test('Pişirdim: Var -> Azaldı, Azaldı -> Bitti ve listeye eklenir', () async {
    final store = FakeHouseStore();
    final pantry = FakePantryRepository(store);
    const r = Recipe(id: 'x', title: 'T', minutes: 1, servings: 1, usedIngredients: ['Yumurta', 'Patates'], steps: []);
    await pantry.markCooked('ev', r);
    expect(store.pantry.value.firstWhere((p) => p.name == 'Yumurta').state, ItemState.low);
    expect(store.pantry.value.any((p) => p.name == 'Patates'), isFalse);
    expect(store.list.value.any((l) => l.name == 'Patates'), isTrue);
  });

  test('Alındı: listeden çıkar, dolaba Var olarak girer', () async {
    final store = FakeHouseStore();
    final list = FakeShoppingListRepository(store);
    final item = store.list.value.first;
    await list.markBought('ev', item);
    expect(store.list.value.any((l) => l.id == item.id), isFalse);
    expect(store.pantry.value.firstWhere((p) => p.name == item.name).state, ItemState.have);
  });

  group('Katalog önerileri', () {
    final now = DateTime.now();
    PantryItem p(String n, {int? days}) => PantryItem(
        id: n, name: n, addedBy: 'me', updatedAt: now, expiresOn: days == null ? null : now.add(Duration(days: days)));
    final pantry = [p('Domates', days: 1), p('Yumurta'), p('Biber'), p('Soğan'), p('Yoğurt', days: 2)];

    test('önce bozulacakları kullananlar gelir', () async {
      final r = await LocalRecipeService().suggestRecipes(pantry, const Preferences(maxMissing: 0));
      expect(r.first.title, 'Menemen');
      expect(r.first.usesExpiring, contains('Domates'));
      expect(r.every((x) => x.missingIngredients.isEmpty), isTrue);
    });

    test('alerji ve süre sınırına uyar', () async {
      final r = await LocalRecipeService()
          .suggestRecipes(pantry, const Preferences(minutes: 15, allergies: ['Yumurta'], maxMissing: null));
      expect(r.any((x) => x.title == 'Menemen'), isFalse);
      expect(r.every((x) => x.minutes <= 15), isTrue);
    });
  });

  test('tahmini son kullanma tarihi', () {
    final d = estimateExpiry('Süt', from: DateTime(2026, 11, 4));
    expect(d, DateTime(2026, 11, 9));
    expect(norm('YOĞURT'), 'yoğurt');
  });
}
