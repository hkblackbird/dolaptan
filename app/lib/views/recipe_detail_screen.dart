import 'dart:async';

import 'package:flutter/cupertino.dart';
import 'package:flutter/services.dart';
import 'package:go_router/go_router.dart';
import 'package:provider/provider.dart';

import '../app/theme.dart';
import '../data/shelf_life.dart';
import '../models/models.dart';
import '../viewmodels/pantry_view_model.dart';
import '../viewmodels/recipe_view_model.dart';
import '../viewmodels/shopping_list_view_model.dart';
import 'widgets.dart';

/// "Peyniri ekle, 5 dk pişir." gibi adımlardaki süre (dakika).
int? stepMinutes(String step) {
  final m = RegExp(r'(\d+)\s*dk').firstMatch(step);
  return m == null ? null : int.parse(m.group(1)!);
}

class RecipeDetailScreen extends StatelessWidget {
  const RecipeDetailScreen({super.key, required this.id});
  final String id;

  Future<void> _cooked(BuildContext context, Recipe r) async {
    final ok = await showCupertinoDialog<bool>(
      context: context,
      builder: (d) => CupertinoAlertDialog(
        title: Column(children: [
          Image.asset(scene('tencere'), width: 84),
          const SizedBox(height: 6),
          Text('Afiyet olsun!', style: script(d, size: 26)),
        ]),
        content: const Text('Kullanılan malzemeler dolapta "Azaldı" olur. Bitenler alışveriş listesine eklenir.'),
        actions: [
          CupertinoDialogAction(child: const Text('Vazgeç'), onPressed: () => Navigator.pop(d, false)),
          CupertinoDialogAction(isDefaultAction: true, child: const Text('Pişirdim'), onPressed: () => Navigator.pop(d, true)),
        ],
      ),
    );
    if (ok == true && context.mounted) {
      await context.read<PantryViewModel>().markCooked(r);
      if (context.mounted) context.go('/pantry');
    }
  }

  @override
  Widget build(BuildContext context) {
    final vm = context.watch<RecipeViewModel>();
    final pantry = context.watch<PantryViewModel>();
    final r = vm.byId(id);
    if (r == null) {
      return CupertinoPageScaffold(
        child: NotebookPaper(child: Center(child: Text('Tarif bulunamadı', style: script(context, size: 26)))),
      );
    }
    final have = {for (final p in pantry.items) if (p.state != ItemState.out) norm(p.name)};
    final missing = r.usedIngredients.where((i) => !have.contains(norm(i))).toList();
    final saved = vm.isSaved(r.id);
    final stepColors = [
      (AppColors.tagRed, AppColors.accent),
      (AppColors.tagYellow, AppColors.tagTextY),
      (AppColors.tagGreen, AppColors.herb),
    ];

    return CupertinoPageScaffold(
      child: NotebookPaper(
        child: Stack(children: [
          CustomScrollView(slivers: [
            SliverToBoxAdapter(
              child: Hero(
                tag: 'photo-${r.id}',
                child: AspectRatio(aspectRatio: 16 / 9, child: Image.asset(dishHero(r.photoPath), fit: BoxFit.cover)),
              ),
            ),
            SliverToBoxAdapter(
              child: Padding(
                padding: const EdgeInsets.fromLTRB(16, 14, 16, 0),
                child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                  Text(r.title, style: script(context, size: 42)),
                  Text('${r.minutes} dk · ${r.servings} kişilik', style: meta(context, size: 17)),
                ]),
              ),
            ),
            const SliverToBoxAdapter(child: SectionHeader('Malzemeler', doodleKey: 'maydanoz')),
            SliverToBoxAdapter(
              child: SketchList(indent: 56, children: [
                for (final ing in r.usedIngredients)
                  Padding(
                    padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 7),
                    child: Row(children: [
                      Thumb(ing, size: 30),
                      const SizedBox(width: 12),
                      Expanded(child: Text(ing, style: body(context))),
                      Tag(missing.contains(ing) ? 'Eksik' : 'Dolapta', tone: missing.contains(ing) ? 'red' : 'green'),
                    ]),
                  ),
                if (missing.isNotEmpty)
                  GestureDetector(
                    behavior: HitTestBehavior.opaque,
                    onTap: () {
                      context.read<ShoppingListViewModel>().addMissing(missing);
                      toast(context, 'Eksikler listeye eklendi');
                    },
                    child: Padding(
                      padding: const EdgeInsets.all(13),
                      child: Row(children: [
                        Icon(CupertinoIcons.cart_badge_plus, color: AppColors.accent.resolveFrom(context)),
                        const SizedBox(width: 10),
                        Text('Eksikleri Listeye Ekle', style: body(context, color: AppColors.accent.resolveFrom(context))),
                      ]),
                    ),
                  ),
              ]),
            ),
            SliverToBoxAdapter(
                child: SectionHeader('Yapılışı',
                    color: AppColors.herb.resolveFrom(context), doodleKey: 'cirpici', angle: 24)),
            SliverToBoxAdapter(
              child: SketchList(seed: 9, indent: 56, children: [
                for (var i = 0; i < r.steps.length; i++)
                  Padding(
                    padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 9),
                    child: Row(children: [
                      SizedBox(
                        width: 28,
                        height: 28,
                        child: SketchBox(
                          radius: 14,
                          seed: i,
                          color: stepColors[i % 3].$1.resolveFrom(context),
                          child: Center(
                              child: Text('${i + 1}',
                                  style: script(context, size: 20, color: stepColors[i % 3].$2.resolveFrom(context)))),
                        ),
                      ),
                      const SizedBox(width: 12),
                      Expanded(child: Text(r.steps[i], style: body(context))),
                      if (stepMinutes(r.steps[i]) case final m?)
                        Semantics(
                          button: true,
                          label: '$m dakikalık zamanlayıcı',
                          child: GestureDetector(
                            onTap: () => showTimer(context, m, r.steps[i]),
                            child: Padding(padding: const EdgeInsets.only(left: 8), child: Tag('$m dk', tone: 'yellow', icon: CupertinoIcons.timer)),
                          ),
                        ),
                    ]),
                  ),
              ]),
            ),
            const SliverToBoxAdapter(child: SizedBox(height: 120)),
          ]),
          SafeArea(
            child: Padding(
              padding: const EdgeInsets.symmetric(horizontal: 8),
              child: Row(children: [
                CircleButton(icon: CupertinoIcons.back, label: 'Geri', onPressed: () => context.pop()),
                const Spacer(),
                CircleButton(
                  icon: saved ? CupertinoIcons.bookmark_fill : CupertinoIcons.bookmark,
                  label: saved ? 'Kayıttan çıkar' : 'Kaydet',
                  onPressed: () => vm.toggleSave(r),
                ),
              ]),
            ),
          ),
          Positioned(
            left: 16,
            right: 16,
            bottom: 8,
            child: SafeArea(top: false, child: InkButton(label: 'Pişirdim', onPressed: () => _cooked(context, r))),
          ),
        ]),
      ),
    );
  }
}

// Zamanlayıcı ------------------------------------------------------------------------------

void showTimer(BuildContext context, int minutes, String step) {
  showCupertinoModalPopup(context: context, builder: (_) => _TimerSheet(minutes: minutes, step: step));
}

class _TimerSheet extends StatefulWidget {
  const _TimerSheet({required this.minutes, required this.step});
  final int minutes;
  final String step;
  @override
  State<_TimerSheet> createState() => _TimerSheetState();
}

class _TimerSheetState extends State<_TimerSheet> {
  late int left = widget.minutes * 60;
  Timer? _t;

  @override
  void dispose() {
    _t?.cancel();
    super.dispose();
  }

  void _toggle() {
    if (_t != null) {
      _t!.cancel();
      setState(() => _t = null);
      return;
    }
    setState(() {
      _t = Timer.periodic(const Duration(seconds: 1), (t) {
        if (left <= 1) {
          t.cancel();
          setState(() {
            left = 0;
            _t = null;
          });
          HapticFeedback.heavyImpact();
          SystemSound.play(SystemSoundType.alert);
          toast(context, 'Süre doldu!');
          return;
        }
        setState(() => left--);
      });
    });
  }

  @override
  Widget build(BuildContext context) {
    final mm = (left ~/ 60).toString().padLeft(2, '0');
    final ss = (left % 60).toString().padLeft(2, '0');
    return SafeArea(
      top: false,
      child: Container(
        margin: const EdgeInsets.all(12),
        child: SketchBox(
          radius: 26,
          seed: 77,
          padding: const EdgeInsets.fromLTRB(20, 18, 20, 18),
          child: Column(mainAxisSize: MainAxisSize.min, children: [
            Image.asset(doodle('cay'), width: 46),
            Text(widget.step, textAlign: TextAlign.center, style: meta(context, size: 17)),
            Text('$mm:$ss', style: script(context, size: 72, color: AppColors.accent.resolveFrom(context))),
            Row(children: [
              Expanded(
                child: TextInkButton(
                  label: 'Sıfırla',
                  onPressed: () {
                    _t?.cancel();
                    setState(() {
                      _t = null;
                      left = widget.minutes * 60;
                    });
                  },
                ),
              ),
              Expanded(flex: 2, child: InkButton(label: _t == null ? 'Başlat' : 'Duraklat', onPressed: _toggle)),
            ]),
          ]),
        ),
      ),
    );
  }
}
