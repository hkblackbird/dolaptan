import 'package:flutter/cupertino.dart';
import 'package:provider/provider.dart';

import '../app/theme.dart';
import '../models/models.dart';
import '../viewmodels/pantry_view_model.dart';
import 'widgets.dart';

void showEditItemSheet(BuildContext context, PantryItem item) {
  showCupertinoSheet(context: context, scrollableBuilder: (_, c) => _EditItemSheet(item: item, controller: c));
}

Future<DateTime?> pickDate(BuildContext context, DateTime initial) async {
  var picked = initial;
  final ok = await showCupertinoModalPopup<bool>(
    context: context,
    builder: (c) => Container(
      height: 300,
      color: AppColors.surface.resolveFrom(c),
      child: SafeArea(
        top: false,
        child: Column(children: [
          Align(
            alignment: Alignment.centerRight,
            child: CupertinoButton(child: const Text('Tamam'), onPressed: () => Navigator.pop(c, true)),
          ),
          Expanded(
            child: CupertinoDatePicker(
              mode: CupertinoDatePickerMode.date,
              initialDateTime: initial,
              minimumDate: DateTime.now().subtract(const Duration(days: 30)),
              onDateTimeChanged: (d) => picked = d,
            ),
          ),
        ]),
      ),
    ),
  );
  return ok == true ? picked : null;
}

class _EditItemSheet extends StatefulWidget {
  const _EditItemSheet({required this.item, required this.controller});
  final PantryItem item;
  final ScrollController controller;
  @override
  State<_EditItemSheet> createState() => _EditItemSheetState();
}

class _EditItemSheetState extends State<_EditItemSheet> {
  late PantryItem draft = widget.item;

  @override
  Widget build(BuildContext context) {
    final vm = context.read<PantryViewModel>();
    final e = draft.expiresOn;
    return CupertinoPageScaffold(
      child: NotebookPaper(
        child: SafeArea(
          child: ListView(controller: widget.controller, children: [
            Padding(
              padding: const EdgeInsets.fromLTRB(8, 8, 16, 0),
              child: Row(children: [
                CircleButton(icon: CupertinoIcons.xmark, label: 'Kapat', onPressed: () => Navigator.pop(context)),
                const SizedBox(width: 8),
                Thumb(draft.name, size: 34),
                const SizedBox(width: 8),
                Expanded(child: Text(widget.item.name, style: script(context, size: 26))),
                SizedBox(
                  width: 110,
                  child: InkButton(
                    label: 'Kaydet',
                    onPressed: () {
                      vm.update(draft);
                      Navigator.pop(context);
                    },
                  ),
                ),
              ]),
            ),
            const SectionHeader('Durum'),
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 16),
              child: CupertinoSlidingSegmentedControl<ItemState>(
                groupValue: draft.state,
                children: {for (final s in ItemState.values) s: Text(s.label, style: body(context, size: 16))},
                onValueChanged: (s) => setState(() => draft = draft.copyWith(state: s)),
              ),
            ),
            const SectionHeader('Son kullanma', doodleKey: 'sarimsak'),
            SketchList(children: [
              GestureDetector(
                behavior: HitTestBehavior.opaque,
                onTap: () async {
                  final d = await pickDate(context, e ?? DateTime.now().add(const Duration(days: 3)));
                  if (d != null) setState(() => draft = draft.copyWith(expiresOn: d));
                },
                child: Padding(
                  padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 12),
                  child: Row(children: [
                    Expanded(child: Text('Tarih', style: body(context))),
                    Tag(e == null ? 'Ekle' : '${e.day} ${shortDate(e).split(' ').last} ${e.year}', tone: 'yellow'),
                  ]),
                ),
              ),
              Padding(
                padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 6),
                child: Row(children: [
                  Expanded(child: Text('Bir gün önce hatırlat', style: body(context))),
                  CupertinoSwitch(
                    value: draft.remind,
                    activeTrackColor: AppColors.accent.resolveFrom(context),
                    onChanged: (v) => setState(() => draft = draft.copyWith(remind: v)),
                  ),
                ]),
              ),
            ]),
            const SizedBox(height: 20),
            SketchList(children: [
              GestureDetector(
                behavior: HitTestBehavior.opaque,
                onTap: () {
                  vm.remove(widget.item.id);
                  Navigator.pop(context);
                },
                child: Padding(
                  padding: const EdgeInsets.all(14),
                  child: Text('Dolaptan Çıkar', style: body(context, color: AppColors.red.resolveFrom(context))),
                ),
              ),
            ]),
          ]),
        ),
      ),
    );
  }
}
