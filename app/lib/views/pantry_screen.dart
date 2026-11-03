import 'package:flutter/cupertino.dart';
import 'package:go_router/go_router.dart';
import 'package:provider/provider.dart';

import '../app/theme.dart';
import '../models/models.dart';
import '../viewmodels/auth_view_model.dart';
import '../viewmodels/pantry_view_model.dart';
import '../viewmodels/scan_view_model.dart';
import 'edit_item_sheet.dart';
import 'preferences_sheet.dart';
import 'widgets.dart';

class PantryScreen extends StatelessWidget {
  const PantryScreen({super.key});

  void _addManually(BuildContext context) {
    context.read<ScanViewModel>().startManual();
    context.push('/scan/review');
  }

  @override
  Widget build(BuildContext context) {
    final vm = context.watch<PantryViewModel>();
    final user = context.watch<AuthViewModel>().user;
    return NotebookPage(
      title: 'Dolap',
      subtitle: user?.guest == true ? 'Misafir · bu cihazda' : 'Evin dolabı',
      coverArt: cover('raf'),
      actions: [
        CircleButton(
          icon: CupertinoIcons.square_arrow_right,
          label: 'Çıkış yap',
          onPressed: () => context.read<AuthViewModel>().signOut(),
        ),
        CircleButton(icon: CupertinoIcons.camera, label: 'Fotoğrafla ekle', onPressed: () => context.push('/scan')),
      ],
      bottom: vm.items.isEmpty ? null : InkButton(label: 'Ne Pişirsem?', onPressed: () => showPreferencesSheet(context)),
      slivers: [
        if (vm.loading)
          const SliverToBoxAdapter(child: Padding(padding: EdgeInsets.all(40), child: CupertinoActivityIndicator()))
        else if (vm.items.isEmpty)
          EmptyState(
            sceneKey: 'dolap-bos',
            title: 'Dolap boş',
            message: 'Dolabın fotoğrafını çek ya da malzemeleri kendin yaz.',
            doodles: ('kasik', 'maydanoz'),
            action: Column(children: [
              TextInkButton(label: 'Fotoğraf Çek', bold: true, onPressed: () => context.push('/scan')),
              TextInkButton(label: 'Elle Ekle', onPressed: () => _addManually(context)),
            ]),
          )
        else ...[
          if (vm.expiringSoon.isNotEmpty) ...[
            const SliverToBoxAdapter(child: SectionHeader('Yakında bozulacak', doodleKey: 'biber', angle: 20)),
            SliverToBoxAdapter(child: SketchList(children: [for (final i in vm.expiringSoon) _ItemRow(i)])),
          ],
          SliverToBoxAdapter(
              child: SectionHeader('Dolapta', color: AppColors.herb.resolveFrom(context), doodleKey: 'maydanoz')),
          SliverToBoxAdapter(
            child: SketchList(seed: 5, children: [
              for (final i in vm.others) _ItemRow(i),
              _AddRow(onTap: () => _addManually(context)),
            ]),
          ),
        ],
      ],
    );
  }
}

class _ItemRow extends StatelessWidget {
  const _ItemRow(this.item);
  final PantryItem item;

  @override
  Widget build(BuildContext context) {
    final label = item.isExpiringSoon ? expiryLabel(item.daysLeft) : item.state.label;
    return GestureDetector(
      behavior: HitTestBehavior.opaque,
      onTap: () => showEditItemSheet(context, item),
      child: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 12, vertical: 8),
        child: Row(children: [
          Thumb(item.name),
          const SizedBox(width: 12),
          Expanded(child: Text(item.name, style: body(context))),
          Tag(label),
        ]),
      ),
    );
  }
}

class _AddRow extends StatelessWidget {
  const _AddRow({required this.onTap});
  final VoidCallback onTap;
  @override
  Widget build(BuildContext context) {
    final c = AppColors.accent.resolveFrom(context);
    return GestureDetector(
      behavior: HitTestBehavior.opaque,
      onTap: onTap,
      child: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
        child: Row(children: [
          Icon(CupertinoIcons.add, color: c, size: 20),
          const SizedBox(width: 10),
          Text('Malzeme Ekle', style: body(context, color: c)),
        ]),
      ),
    );
  }
}
