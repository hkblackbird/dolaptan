import 'package:flutter/cupertino.dart';
import 'package:go_router/go_router.dart';

import '../app/theme.dart';
import 'widgets.dart';

/// Yüzen, elle çizilmiş sekme çubuğu: Dolap, Tarifler, Liste.
class HomeShell extends StatelessWidget {
  const HomeShell({super.key, required this.shell});
  final StatefulNavigationShell shell;

  static const _tabs = [
    (CupertinoIcons.cube_box, 'Dolap'),
    (CupertinoIcons.book, 'Tarifler'),
    (CupertinoIcons.list_bullet, 'Liste'),
  ];

  @override
  Widget build(BuildContext context) {
    return CupertinoPageScaffold(
      child: Stack(children: [
        // Sayfalar alttaki boşluğu sekme çubuğunun üstünden başlatsın diye.
        Positioned.fill(
          child: MediaQuery(
            data: MediaQuery.of(context).copyWith(
              padding: MediaQuery.of(context).padding.copyWith(bottom: MediaQuery.of(context).padding.bottom + 78),
            ),
            child: shell,
          ),
        ),
        Positioned(
          left: 21,
          right: 21,
          bottom: 0,
          child: SafeArea(
            top: false,
            minimum: const EdgeInsets.only(bottom: 10),
            child: SizedBox(
              height: 62,
              child: SketchBox(
                radius: 31,
                seed: 11,
                padding: const EdgeInsets.all(4),
                child: Row(children: [
                  for (var i = 0; i < _tabs.length; i++)
                    Expanded(child: _Tab(icon: _tabs[i].$1, label: _tabs[i].$2, on: i == shell.currentIndex, onTap: () {
                      shell.goBranch(i, initialLocation: i == shell.currentIndex);
                    })),
                ]),
              ),
            ),
          ),
        ),
      ]),
    );
  }
}

class _Tab extends StatelessWidget {
  const _Tab({required this.icon, required this.label, required this.on, required this.onTap});
  final IconData icon;
  final String label;
  final bool on;
  final VoidCallback onTap;

  @override
  Widget build(BuildContext context) {
    final color = on ? AppColors.accent.resolveFrom(context) : AppColors.text.resolveFrom(context);
    final content = Column(mainAxisAlignment: MainAxisAlignment.center, children: [
      Icon(icon, color: color, size: 22),
      Text(label, style: on ? script(context, size: 15, color: color) : body(context, size: 12, color: color)),
    ]);
    return Semantics(
      selected: on,
      button: true,
      label: label,
      child: GestureDetector(
        behavior: HitTestBehavior.opaque,
        onTap: onTap,
        child: on
            ? SketchBox(color: AppColors.bg.resolveFrom(context), radius: 27, seed: label.hashCode, child: content)
            : content,
      ),
    );
  }
}
