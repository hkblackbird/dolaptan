import 'package:flutter/cupertino.dart';
import 'package:go_router/go_router.dart';
import 'package:provider/provider.dart';

import '../app/theme.dart';
import '../viewmodels/pantry_view_model.dart';
import '../viewmodels/scan_view_model.dart';
import 'edit_item_sheet.dart';
import 'widgets.dart';

/// Yeni malzemeler: fotoğraftan gelenleri kontrol et ya da elle yaz.
/// Tarihler tahminidir; yalnızca yanlışsa düzeltilir.
class ScanReviewScreen extends StatefulWidget {
  const ScanReviewScreen({super.key});
  @override
  State<ScanReviewScreen> createState() => _ScanReviewScreenState();
}

class _ScanReviewScreenState extends State<ScanReviewScreen> {
  final _input = TextEditingController();
  static const _quick = ['Süt', 'Yumurta', 'Domates', 'Ekmek', 'Peynir', 'Yoğurt', 'Salatalık', 'Biber'];

  @override
  void dispose() {
    _input.dispose();
    super.dispose();
  }

  void _add(String name) {
    context.read<ScanViewModel>().add(name);
    _input.clear();
  }

  Future<void> _rename(ScanViewModel vm, int i) async {
    final c = TextEditingController(text: vm.detected[i].name);
    final name = await showCupertinoDialog<String>(
      context: context,
      builder: (d) => CupertinoAlertDialog(
        title: const Text('Malzeme adı'),
        content: Padding(padding: const EdgeInsets.only(top: 8), child: CupertinoTextField(controller: c, autofocus: true)),
        actions: [
          CupertinoDialogAction(child: const Text('Vazgeç'), onPressed: () => Navigator.pop(d)),
          CupertinoDialogAction(isDefaultAction: true, child: const Text('Tamam'), onPressed: () => Navigator.pop(d, c.text)),
        ],
      ),
    );
    if (name != null && name.trim().isNotEmpty) vm.rename(i, name);
  }

  void _options(ScanViewModel vm, int i) {
    final item = vm.detected[i];
    showCupertinoModalPopup(
      context: context,
      builder: (c) => CupertinoActionSheet(
        title: Text(item.name),
        actions: [
          CupertinoActionSheetAction(
              onPressed: () {
                Navigator.pop(c);
                _rename(vm, i);
              },
              child: const Text('Adını düzelt')),
          CupertinoActionSheetAction(
              onPressed: () async {
                Navigator.pop(c);
                final d = await pickDate(context, item.expiresOn ?? DateTime.now());
                if (d != null) vm.setDate(i, d);
              },
              child: const Text('Tarihi değiştir')),
          CupertinoActionSheetAction(
              isDestructiveAction: true,
              onPressed: () {
                Navigator.pop(c);
                vm.removeAt(i);
              },
              child: const Text('Sil')),
        ],
        cancelButton: CupertinoActionSheetAction(onPressed: () => Navigator.pop(c), child: const Text('Vazgeç')),
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final vm = context.watch<ScanViewModel>();
    final n = vm.detected.length;
    return NotebookPage(
      title: 'Yeni Malzemeler',
      subtitle: 'Kontrol et, tarihleri biz tahmin ettik.',
      back: true,
      bottom: n == 0
          ? null
          : InkButton(
              label: 'Dolaba Ekle ($n)',
              onPressed: () async {
                await context.read<PantryViewModel>().addAll(List.of(vm.detected));
                vm.startManual();
                if (context.mounted) context.go('/pantry');
              },
            ),
      slivers: [
        SliverToBoxAdapter(
          child: Padding(
            padding: const EdgeInsets.fromLTRB(16, 4, 16, 0),
            child: SketchBox(
              seed: 21,
              child: CupertinoTextField(
                controller: _input,
                placeholder: 'Malzeme yaz: süt, ekmek…',
                decoration: null,
                style: body(context),
                placeholderStyle: meta(context, size: 18),
                padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
                textInputAction: TextInputAction.done,
                onSubmitted: _add,
                suffix: CupertinoButton(
                  padding: const EdgeInsets.only(right: 8),
                  onPressed: () => _add(_input.text),
                  child: Icon(CupertinoIcons.add_circled_solid, color: AppColors.accent.resolveFrom(context)),
                ),
              ),
            ),
          ),
        ),
        SliverToBoxAdapter(
          child: SizedBox(
            height: 52,
            child: ListView(
              scrollDirection: Axis.horizontal,
              padding: const EdgeInsets.fromLTRB(16, 8, 16, 0),
              children: [
                for (final q in _quick)
                  Padding(
                    padding: const EdgeInsets.only(right: 8),
                    child: GestureDetector(
                      onTap: () => _add(q),
                      child: SketchBox(
                        radius: 18,
                        seed: q.hashCode,
                        padding: const EdgeInsets.fromLTRB(6, 4, 12, 4),
                        child: Row(children: [Thumb(q, size: 26), const SizedBox(width: 6), Text(q, style: body(context, size: 16))]),
                      ),
                    ),
                  ),
              ],
            ),
          ),
        ),
        if (n == 0)
          EmptyState(
            sceneKey: 'buyutec',
            title: 'Henüz malzeme yok',
            message: 'Yukarıya yaz ya da hazır olanlara dokun.',
            doodles: ('biber', 'maydanoz'),
            action: TextInkButton(label: 'Fotoğraf Çek', onPressed: () => context.pushReplacement('/scan')),
          )
        else ...[
          SliverToBoxAdapter(child: SectionHeader('$n malzeme', doodleKey: 'kasik', angle: 30)),
          SliverToBoxAdapter(
            child: SketchList(indent: 58, children: [
              for (var i = 0; i < n; i++)
                Dismissible(
                  key: ValueKey('${vm.detected[i].name}-$i'),
                  direction: DismissDirection.endToStart,
                  onDismissed: (_) => vm.removeAt(i),
                  background: Container(
                    color: AppColors.red.resolveFrom(context),
                    alignment: Alignment.centerRight,
                    padding: const EdgeInsets.only(right: 20),
                    child: Text('Sil', style: body(context, color: CupertinoColors.white)),
                  ),
                  child: GestureDetector(
                    behavior: HitTestBehavior.opaque,
                    onTap: () => _options(vm, i),
                    child: Padding(
                      padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 9),
                      child: Row(children: [
                        Thumb(vm.detected[i].name, size: 34),
                        const SizedBox(width: 12),
                        Expanded(
                          child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                            Text(vm.detected[i].name, style: body(context)),
                            if (vm.detected[i].isUncertain) Text('Emin değiliz, kontrol et', style: meta(context)),
                          ]),
                        ),
                        if (vm.detected[i].expiresOn != null)
                          Text(
                            '${vm.detected[i].estimated ? '~' : ''}${shortDate(vm.detected[i].expiresOn!)}',
                            style: meta(context, size: 17),
                          ),
                      ]),
                    ),
                  ),
                ),
            ]),
          ),
          SliverToBoxAdapter(
            child: Padding(
              padding: const EdgeInsets.fromLTRB(32, 8, 32, 0),
              child: Text('~ tahmini tarih. Satıra dokunup düzelt, sola kaydırıp sil.', style: meta(context, size: 14)),
            ),
          ),
        ],
      ],
    );
  }
}
