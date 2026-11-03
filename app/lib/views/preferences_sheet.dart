import 'package:flutter/cupertino.dart';
import 'package:go_router/go_router.dart';
import 'package:provider/provider.dart';

import '../app/theme.dart';
import '../viewmodels/pantry_view_model.dart';
import '../viewmodels/recipe_view_model.dart';
import 'widgets.dart';

void showPreferencesSheet(BuildContext context) {
  showCupertinoSheet(context: context, scrollableBuilder: (_, c) => _PreferencesSheet(controller: c));
}

class _PreferencesSheet extends StatefulWidget {
  const _PreferencesSheet({required this.controller});
  final ScrollController controller;
  @override
  State<_PreferencesSheet> createState() => _PreferencesSheetState();
}

class _PreferencesSheetState extends State<_PreferencesSheet> {
  static const _allergyOptions = ['Gluten', 'Süt', 'Yumurta', 'Fındık'];
  late var prefs = context.read<RecipeViewModel>().prefs;

  Widget _seg<T extends Object>(Map<T, String> options, T value, ValueChanged<T> onChanged) => Padding(
        padding: const EdgeInsets.symmetric(horizontal: 16),
        child: CupertinoSlidingSegmentedControl<T>(
          groupValue: value,
          children: {for (final e in options.entries) e.key: Text(e.value, style: body(context, size: 16))},
          onValueChanged: (v) => v == null ? null : onChanged(v),
        ),
      );

  void _suggest() {
    final recipes = context.read<RecipeViewModel>()..setPrefs(prefs);
    recipes.suggest(context.read<PantryViewModel>().items);
    final router = GoRouter.of(context);
    Navigator.pop(context);
    router.push('/cook/results');
  }

  @override
  Widget build(BuildContext context) {
    return CupertinoPageScaffold(
      child: NotebookPaper(
        child: SafeArea(
          child: ListView(controller: widget.controller, padding: const EdgeInsets.only(bottom: 30), children: [
            Padding(
              padding: const EdgeInsets.fromLTRB(8, 8, 16, 0),
              child: Row(children: [
                CircleButton(icon: CupertinoIcons.xmark, label: 'Kapat', onPressed: () => Navigator.pop(context)),
                const SizedBox(width: 10),
                Expanded(child: Text('Tercihler', style: script(context, size: 28))),
                SizedBox(width: 130, child: InkButton(label: 'Tarif Öner', onPressed: _suggest)),
              ]),
            ),
            const SectionHeader('Süre', doodleKey: 'cay', angle: 0),
            _seg({15: '15 dk', 30: '30 dk', 60: '1 saat'}, prefs.minutes,
                (v) => setState(() => prefs = prefs.copyWith(minutes: v))),
            const SectionHeader('Kişi sayısı', doodleKey: 'kasik'),
            _seg({1: '1', 2: '2', 4: '4', 6: '6'}, prefs.servings,
                (v) => setState(() => prefs = prefs.copyWith(servings: v))),
            const SectionHeader('Eksik malzeme', doodleKey: 'sarimsak'),
            _seg({0: 'Olmasın', 1: 'En fazla 1', -1: 'Fark etmez'}, prefs.maxMissing ?? -1,
                (v) => setState(() => prefs = prefs.copyWith(maxMissing: () => v < 0 ? null : v))),
            const SectionHeader('Alerjiler', doodleKey: 'dereotu'),
            SketchList(children: [
              for (final a in _allergyOptions)
                Padding(
                  padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 5),
                  child: Row(children: [
                    Expanded(child: Text(a, style: body(context))),
                    CupertinoSwitch(
                      value: prefs.allergies.contains(a),
                      activeTrackColor: AppColors.accent.resolveFrom(context),
                      onChanged: (on) => setState(() {
                        final list = [...prefs.allergies];
                        on ? list.add(a) : list.remove(a);
                        prefs = prefs.copyWith(allergies: list);
                      }),
                    ),
                  ]),
                ),
            ]),
            Padding(
              padding: const EdgeInsets.fromLTRB(32, 10, 32, 0),
              child: Text(
                'Önce bozulacak malzemeler kullanılır. Tarifler internetsiz katalogdan gelir; '
                'alerjenleri yine de kontrol et.',
                style: meta(context, size: 14),
              ),
            ),
          ]),
        ),
      ),
    );
  }
}
