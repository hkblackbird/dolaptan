// Ekran görüntüleri: flutter test --update-goldens test/screens_golden_test.dart
// Gerçek fontları ve çizimleri yükleyip her ana ekranı test/goldens/ altına çizer.
import 'package:dolaptan/main.dart';
import 'package:flutter/cupertino.dart';
import 'package:flutter/services.dart';
import 'package:flutter_test/flutter_test.dart';

import 'app_flow_test.dart' show fakes;

Future<void> _fonts() async {
  for (final (family, file) in [('PatrickHand', 'PatrickHand-Regular'), ('Caveat', 'Caveat-Bold')]) {
    final loader = FontLoader(family)..addFont(rootBundle.load('assets/fonts/$file.ttf'));
    await loader.load();
  }
  final icons = FontLoader('packages/cupertino_icons/CupertinoIcons')
    ..addFont(rootBundle.load('packages/cupertino_icons/assets/CupertinoIcons.ttf'));
  await icons.load();
}

Future<void> _settle(WidgetTester t) async {
  await t.pumpAndSettle();
  await t.runAsync(() async {
    for (final e in find.byType(Image).evaluate()) {
      await precacheImage((e.widget as Image).image, e);
    }
  });
  await t.pumpAndSettle();
}

Future<void> _shot(WidgetTester t, String name) async {
  await _settle(t);
  await expectLater(find.byType(DolaptanRoot), matchesGoldenFile('goldens/$name.png'));
}

void main() {
  testWidgets('ekranlar', (t) async {
    await _fonts();
    t.view.physicalSize = const Size(390 * 2, 844 * 2);
    t.view.devicePixelRatio = 2;
    addTearDown(t.view.reset);

    await t.pumpWidget(DolaptanRoot(deps: fakes()));
    await _shot(t, '01-giris');
    await t.tap(find.text('Hesapsız Dene'));
    await _shot(t, '02-dolap');
    await t.tap(find.text('Ne Pişirsem?'));
    await _shot(t, '05-tercihler');
    await t.tap(find.text('Tarif Öner'));
    await _shot(t, '06-oneriler');
    await t.tap(find.text('Menemen').first);
    await _shot(t, '07-tarif');
    await t.tap(find.bySemanticsLabel('Kaydet'));
    await t.pumpAndSettle();
    await t.tap(find.byIcon(CupertinoIcons.timer).first);
    await _shot(t, '07b-zamanlayici');
    await t.tapAt(const Offset(195, 60));
    await t.pumpAndSettle();
    await t.tap(find.bySemanticsLabel('Geri').first);
    await t.pumpAndSettle();
    await t.tap(find.bySemanticsLabel('Geri').first);
    await t.pumpAndSettle();
    await t.tap(find.text('Malzeme Ekle'));
    await t.pumpAndSettle();
    await t.tap(find.text('Süt').first);
    await t.tap(find.text('Ekmek').first);
    await _shot(t, '04-yeni-malzemeler');
    await t.tap(find.bySemanticsLabel('Geri').first);
    await t.pumpAndSettle();
    await t.tap(find.text('Tarifler'));
    await _shot(t, '08-tarifler');
    await t.tap(find.text('Liste'));
    await _shot(t, '09-liste');
  });
}
