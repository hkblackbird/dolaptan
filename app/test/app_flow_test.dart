import 'package:dolaptan/app/dependencies.dart';
import 'package:dolaptan/data/fake_repositories.dart';
import 'package:dolaptan/data/local_recipe_service.dart';
import 'package:dolaptan/main.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter_test/flutter_test.dart';

Dependencies fakes() {
  final store = FakeHouseStore();
  return Dependencies(
    auth: FakeAuthService(),
    pantry: FakePantryRepository(store),
    list: FakeShoppingListRepository(store),
    recipes: LocalRecipeService(),
    saved: FakeSavedRecipeRepository(),
    prefs: FakePreferencesRepository(),
  );
}

void main() {
  testWidgets('Hesapsız dene -> Dolap -> Tarif önerisi -> detay -> kaydet -> Tarifler -> Liste', (t) async {
    t.view.physicalSize = const Size(390 * 3, 844 * 3);
    t.view.devicePixelRatio = 3;
    addTearDown(t.view.reset);

    await t.pumpWidget(DolaptanRoot(deps: fakes()));
    await t.pumpAndSettle();
    await t.tap(find.text('Hesapsız Dene'));
    await t.pumpAndSettle();
    expect(find.text('Yakında bozulacak'), findsOneWidget);
    expect(find.text('Yoğurt'), findsOneWidget);

    await t.tap(find.text('Ne Pişirsem?'));
    await t.pumpAndSettle();
    await t.tap(find.text('Tarif Öner'));
    await t.pumpAndSettle();
    expect(find.text('Menemen'), findsOneWidget);

    await t.tap(find.text('Menemen'));
    await t.pumpAndSettle();
    expect(find.text('Pişirdim'), findsOneWidget);
    await t.tap(find.bySemanticsLabel('Kaydet'));
    await t.pumpAndSettle();
    await t.tap(find.bySemanticsLabel('Geri').first);
    await t.pumpAndSettle();
    await t.tap(find.bySemanticsLabel('Geri').first);
    await t.pumpAndSettle();

    await t.tap(find.text('Tarifler'));
    await t.pumpAndSettle();
    expect(find.text('Kayıtlı'), findsOneWidget);
    expect(find.text('Menemen'), findsOneWidget);

    await t.tap(find.text('Liste'));
    await t.pumpAndSettle();
    expect(find.text('Tereyağı'), findsOneWidget);
  });
}
