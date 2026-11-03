import 'package:flutter/cupertino.dart';
import 'package:flutter/services.dart';
import 'package:provider/provider.dart';

import '../app/theme.dart';
import '../models/models.dart';
import '../viewmodels/shopping_list_view_model.dart';
import 'widgets.dart';

class ShoppingListScreen extends StatefulWidget {
  const ShoppingListScreen({super.key});
  @override
  State<ShoppingListScreen> createState() => _ShoppingListScreenState();
}

class _ShoppingListScreenState extends State<ShoppingListScreen> {
  final _add = TextEditingController();
  final _ticked = <String>{};

  @override
  void dispose() {
    _add.dispose();
    super.dispose();
  }

  void _submit() {
    context.read<ShoppingListViewModel>().add(_add.text);
    _add.clear();
  }

  /// Önce tik atılır, kısa bir an sonra ürün dolaba geçer.
  Future<void> _bought(ListItem item) async {
    setState(() => _ticked.add(item.id));
    HapticFeedback.lightImpact();
    await Future.delayed(const Duration(milliseconds: 450));
    if (!mounted) return;
    await context.read<ShoppingListViewModel>().markBought(item);
    _ticked.remove(item.id);
  }

  @override
  Widget build(BuildContext context) {
    final vm = context.watch<ShoppingListViewModel>();
    return NotebookPage(
      title: 'Alışveriş Listesi',
      subtitle: 'Ev listesi',
      actions: [
        CircleButton(
          icon: CupertinoIcons.square_arrow_up,
          label: 'Listeyi kopyala',
          onPressed: () {
            Clipboard.setData(ClipboardData(text: vm.asText()));
            toast(context, 'Liste kopyalandı');
          },
        ),
      ],
      slivers: [
        SliverToBoxAdapter(
          child: Padding(
            padding: const EdgeInsets.fromLTRB(16, 4, 16, 0),
            child: SketchBox(
              seed: 41,
              child: CupertinoTextField(
                controller: _add,
                placeholder: 'Ekle: süt, ekmek…',
                decoration: null,
                style: body(context),
                placeholderStyle: meta(context, size: 18),
                padding: const EdgeInsets.symmetric(horizontal: 14, vertical: 12),
                textInputAction: TextInputAction.done,
                onSubmitted: (_) => _submit(),
                suffix: CupertinoButton(
                  padding: const EdgeInsets.only(right: 8),
                  onPressed: _submit,
                  child: Icon(CupertinoIcons.add_circled_solid, color: AppColors.accent.resolveFrom(context)),
                ),
              ),
            ),
          ),
        ),
        if (vm.items.isEmpty)
          const EmptyState(
            sceneKey: 'sepet',
            title: 'Liste boş',
            message: 'Pişirdikçe biten malzemeler buraya kendiliğinden düşer.',
            doodles: ('limon', 'sarimsak'),
          )
        else ...[
          const SliverToBoxAdapter(child: SectionHeader('Alınacaklar', doodleKey: 'limon')),
          SliverToBoxAdapter(
            child: SketchList(indent: 56, children: [
              for (final item in vm.items) _ListRow(item: item, ticked: _ticked.contains(item.id), onTap: () => _bought(item)),
            ]),
          ),
          SliverToBoxAdapter(
            child: Padding(
              padding: const EdgeInsets.fromLTRB(32, 10, 32, 0),
              child: Text('Aldığın ürüne dokun, dolaba "Var" olarak geçer.', style: meta(context, size: 14)),
            ),
          ),
        ],
      ],
    );
  }
}

class _ListRow extends StatelessWidget {
  const _ListRow({required this.item, required this.ticked, required this.onTap});
  final ListItem item;
  final bool ticked;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    final accent = AppColors.accent.resolveFrom(context);
    return Semantics(
      button: true,
      label: '${item.name}, alındı olarak işaretle',
      child: GestureDetector(
        behavior: HitTestBehavior.opaque,
        onTap: ticked ? null : onTap,
        child: Padding(
          padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 9),
          child: Row(children: [
            AnimatedContainer(
              duration: const Duration(milliseconds: 200),
              width: 26,
              height: 26,
              decoration: BoxDecoration(
                shape: BoxShape.circle,
                color: ticked ? accent : null,
                border: Border.all(color: ticked ? accent : AppColors.text2.resolveFrom(context), width: 1.6),
              ),
              child: ticked ? const Icon(CupertinoIcons.check_mark, size: 16, color: CupertinoColors.white) : null,
            ),
            const SizedBox(width: 18),
            Expanded(
              child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                Text(item.name,
                    style: body(context).copyWith(
                        decoration: ticked ? TextDecoration.lineThrough : null,
                        color: ticked ? AppColors.text2.resolveFrom(context) : null)),
                Text(ticked ? 'Dolaba ekleniyor…' : (item.addedBy == 'me' ? 'Sen ekledin' : '${item.addedByName} ekledi'),
                    style: meta(context, size: 14)),
              ]),
            ),
            Thumb(item.name, size: 40),
          ]),
        ),
      ),
    );
  }
}
