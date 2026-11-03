import 'dart:math' as math;

import 'package:flutter/cupertino.dart';
import 'package:go_router/go_router.dart';

import '../app/theme.dart';

/// Tarif defteri görünümünün yapı taşları.

// Elle çizilmiş kutu -------------------------------------------------------------------------

Path wobbleRect(Rect r, double radius, int seed) {
  final rng = math.Random(seed);
  double j() => (rng.nextDouble() - 0.5) * 1.8;
  final rr = math.min(radius, math.min(r.width, r.height) / 2);
  final x = r.left, y = r.top, w = r.width, h = r.height;
  return Path()
    ..moveTo(x + rr, y + j())
    ..lineTo(x + w / 2, y + j())
    ..lineTo(x + w - rr, y + j())
    ..quadraticBezierTo(x + w + j(), y + j(), x + w + j(), y + rr)
    ..lineTo(x + w + j(), y + h / 2)
    ..lineTo(x + w + j(), y + h - rr)
    ..quadraticBezierTo(x + w + j(), y + h + j(), x + w - rr, y + h + j())
    ..lineTo(x + w / 2, y + h + j())
    ..lineTo(x + rr, y + h + j())
    ..quadraticBezierTo(x + j(), y + h + j(), x + j(), y + h - rr)
    ..lineTo(x + j(), y + h / 2)
    ..lineTo(x + j(), y + rr)
    ..quadraticBezierTo(x + j(), y + j(), x + rr, y + j())
    ..close();
}

class _SketchPainter extends CustomPainter {
  _SketchPainter(this.fill, this.ink, this.radius, this.seed);
  final Color fill, ink;
  final double radius;
  final int seed;

  @override
  void paint(Canvas canvas, Size size) {
    final path = wobbleRect(Offset.zero & size, radius, seed);
    canvas.drawPath(path, Paint()..color = fill);
    canvas.drawPath(
        path,
        Paint()
          ..color = ink.withValues(alpha: 0.55)
          ..style = PaintingStyle.stroke
          ..strokeWidth = 1.2
          ..strokeJoin = StrokeJoin.round);
  }

  @override
  bool shouldRepaint(_SketchPainter old) => old.fill != fill || old.ink != ink || old.seed != seed;
}

/// Mürekkep kenarlı, hafif titrek kutu.
class SketchBox extends StatelessWidget {
  const SketchBox({super.key, required this.child, this.color, this.radius = 20, this.padding, this.seed = 1});
  final Widget child;
  final Color? color;
  final double radius;
  final EdgeInsetsGeometry? padding;
  final int seed;

  @override
  Widget build(BuildContext context) => CustomPaint(
        painter: _SketchPainter(color ?? AppColors.surface.resolveFrom(context), AppColors.ink.resolveFrom(context),
            radius, seed),
        child: Padding(padding: padding ?? EdgeInsets.zero, child: child),
      );
}

/// Inset grouped liste, satırlar arasında ince çizgi.
class SketchList extends StatelessWidget {
  const SketchList({super.key, required this.children, this.seed = 3, this.indent = 16});
  final List<Widget> children;
  final int seed;
  final double indent;

  @override
  Widget build(BuildContext context) {
    final sep = AppColors.sep.resolveFrom(context);
    return Padding(
      padding: const EdgeInsets.symmetric(horizontal: 16),
      child: SketchBox(
        seed: seed,
        child: Column(children: [
          for (var i = 0; i < children.length; i++) ...[
            if (i > 0) Container(height: 0.6, margin: EdgeInsets.only(left: indent), color: sep),
            children[i],
          ]
        ]),
      ),
    );
  }
}

// Sayfa ------------------------------------------------------------------------------------

class _RulesPainter extends CustomPainter {
  _RulesPainter(this.color, this.top);
  final Color color;
  final double top;
  @override
  void paint(Canvas canvas, Size size) {
    final p = Paint()..color = color;
    for (var y = top; y < size.height; y += 28) {
      canvas.drawRect(Rect.fromLTWH(0, y, size.width, 1), p);
    }
  }

  @override
  bool shouldRepaint(_RulesPainter old) => old.color != color;
}

/// Çizgili defter kağıdı.
class NotebookPaper extends StatelessWidget {
  const NotebookPaper({super.key, required this.child});
  final Widget child;
  @override
  Widget build(BuildContext context) => Container(
        color: AppColors.bg.resolveFrom(context),
        child: CustomPaint(painter: _RulesPainter(AppColors.rule.resolveFrom(context), 196), child: child),
      );
}

/// Büyük el yazısı başlıklı sayfa: geri / eylem düğmeleri, alt başlık ve kapak çizimi.
class NotebookPage extends StatelessWidget {
  const NotebookPage({
    super.key,
    required this.title,
    this.subtitle,
    this.actions = const [],
    this.back = false,
    this.leading,
    this.coverArt,
    required this.slivers,
    this.bottom,
  });
  final String title;
  final String? subtitle;
  final List<Widget> actions;
  final bool back;
  final Widget? leading;
  final String? coverArt;
  final List<Widget> slivers;
  final Widget? bottom;

  @override
  Widget build(BuildContext context) {
    return CupertinoPageScaffold(
      child: NotebookPaper(
        child: Stack(children: [
          CustomScrollView(slivers: [
            SliverSafeArea(
              bottom: false,
              sliver: SliverToBoxAdapter(
                child: SizedBox(
                  height: 140,
                  child: Stack(children: [
                    if (coverArt != null)
                      Positioned(right: 14, top: 44, child: Image.asset(coverArt!, width: 96, height: 96)),
                    Positioned(
                      left: 16,
                      right: 16,
                      top: 6,
                      child: Row(children: [
                        if (back) CircleButton(icon: CupertinoIcons.back, label: 'Geri', onPressed: () => context.pop()),
                        ?leading,
                        const Spacer(),
                        ...actions,
                      ]),
                    ),
                    Positioned(
                      left: 16,
                      right: coverArt != null ? 120 : 16,
                      top: 56,
                      child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                        Text(title, style: script(context, size: 44), maxLines: 1, overflow: TextOverflow.ellipsis),
                        if (subtitle != null) Text(subtitle!, style: meta(context, size: 17)),
                      ]),
                    ),
                  ]),
                ),
              ),
            ),
            ...slivers,
            const SliverToBoxAdapter(child: SizedBox(height: 130)),
          ]),
          if (bottom != null)
            Positioned(left: 16, right: 16, bottom: 8, child: SafeArea(top: false, child: bottom!)),
        ]),
      ),
    );
  }
}

/// El yazısı bölüm başlığı, altında fırça çizgisi, yanında küçük bir çizim.
class SectionHeader extends StatelessWidget {
  const SectionHeader(this.text, {super.key, this.color, this.doodleKey, this.angle = -12});
  final String text;
  final Color? color;
  final String? doodleKey;
  final double angle;

  @override
  Widget build(BuildContext context) {
    final c = color ?? AppColors.accent.resolveFrom(context);
    return Padding(
      padding: const EdgeInsets.fromLTRB(20, 18, 16, 6),
      child: Row(crossAxisAlignment: CrossAxisAlignment.end, children: [
        Flexible(
          child: CustomPaint(
            foregroundPainter: _BrushPainter(c),
            child: Padding(
                padding: const EdgeInsets.only(bottom: 4),
                child: Text(text, style: script(context, size: 26, color: c), maxLines: 1, overflow: TextOverflow.ellipsis)),
          ),
        ),
        if (doodleKey != null)
          Padding(
            padding: const EdgeInsets.only(left: 6),
            child: Transform.rotate(
                angle: angle * math.pi / 180, child: Image.asset(doodle(doodleKey!), width: 36, height: 36)),
          ),
      ]),
    );
  }
}

class _BrushPainter extends CustomPainter {
  _BrushPainter(this.color);
  final Color color;
  @override
  void paint(Canvas canvas, Size size) {
    final y = size.height - 1;
    final w = size.width;
    final path = Path()
      ..moveTo(0, y)
      ..quadraticBezierTo(w * 0.3, y - 3, w * 0.55, y)
      ..quadraticBezierTo(w * 0.8, y + 3, w + 6, y - 1);
    canvas.drawPath(
        path,
        Paint()
          ..color = color.withValues(alpha: 0.45)
          ..style = PaintingStyle.stroke
          ..strokeWidth = 2.4
          ..strokeCap = StrokeCap.round);
  }

  @override
  bool shouldRepaint(_BrushPainter old) => old.color != color;
}

// Düğmeler ---------------------------------------------------------------------------------

class CircleButton extends StatelessWidget {
  const CircleButton({super.key, required this.icon, required this.onPressed, required this.label});
  final IconData icon;
  final VoidCallback onPressed;
  final String label;

  @override
  Widget build(BuildContext context) => Padding(
        padding: const EdgeInsets.only(left: 8),
        child: Semantics(
          label: label,
          button: true,
          child: GestureDetector(
            onTap: onPressed,
            child: SizedBox(
              width: 44,
              height: 44,
              child: SketchBox(
                radius: 22,
                seed: icon.codePoint,
                child: Center(child: Icon(icon, size: 21, color: AppColors.text.resolveFrom(context))),
              ),
            ),
          ),
        ),
      );
}

/// Ana eylem düğmesi: terrakota, el yazısı.
class InkButton extends StatelessWidget {
  const InkButton({super.key, required this.label, required this.onPressed});
  final String label;
  final VoidCallback? onPressed;

  @override
  Widget build(BuildContext context) => Semantics(
        button: true,
        label: label,
        child: GestureDetector(
          onTap: onPressed,
          child: Opacity(
            opacity: onPressed == null ? 0.5 : 1,
            child: SizedBox(
              height: 52,
              width: double.infinity,
              child: SketchBox(
                color: AppColors.accent.resolveFrom(context),
                radius: 26,
                seed: label.hashCode,
                child: Center(
                    child: Text(label, style: script(context, size: 24, color: AppColors.onAccent.resolveFrom(context)))),
              ),
            ),
          ),
        ),
      );
}

class TextInkButton extends StatelessWidget {
  const TextInkButton({super.key, required this.label, required this.onPressed, this.bold = false});
  final String label;
  final VoidCallback? onPressed;
  final bool bold;

  @override
  Widget build(BuildContext context) => CupertinoButton(
        minimumSize: const Size(44, 44),
        onPressed: onPressed,
        child: Text(label,
            style: bold
                ? script(context, size: 22, color: AppColors.accent.resolveFrom(context))
                : body(context, color: AppColors.accent.resolveFrom(context))),
      );
}

// Küçük parçalar ---------------------------------------------------------------------------

/// Durum ve tarih etiketi: Var yeşil, Azaldı hardal, Yarın kırmızı.
class Tag extends StatelessWidget {
  const Tag(this.label, {super.key, this.tone, this.icon});
  final String label;
  final String? tone; // red | green | yellow
  final IconData? icon;

  @override
  Widget build(BuildContext context) {
    final t = tone ??
        switch (label) {
          'Var' => 'green',
          'Yarın' || 'Bugün' || 'Geçti' => 'red',
          _ => 'yellow',
        };
    final (bg, fg) = switch (t) {
      'red' => (AppColors.tagRed, AppColors.accent),
      'green' => (AppColors.tagGreen, AppColors.herb),
      _ => (AppColors.tagYellow, AppColors.tagTextY),
    };
    return SketchBox(
      color: bg.resolveFrom(context),
      radius: 13,
      seed: label.hashCode,
      padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 3),
      child: Row(mainAxisSize: MainAxisSize.min, children: [
        if (icon != null) Padding(padding: const EdgeInsets.only(right: 4), child: Icon(icon, size: 16, color: fg.resolveFrom(context))),
        Text(label, style: script(context, size: 19.5, color: fg.resolveFrom(context))),
      ]),
    );
  }
}

/// Malzemenin yuvarlak boyalı çizimi; çizimi yoksa baş harfi.
class Thumb extends StatelessWidget {
  const Thumb(this.name, {super.key, this.size = 36});
  final String name;
  final double size;

  @override
  Widget build(BuildContext context) {
    final art = ingredientArt(name);
    if (art != null) {
      final img = Image.asset(art, width: size, height: size, fit: BoxFit.cover);
      return art.endsWith('.jpg') ? ClipOval(child: img) : img;
    }
    return Container(
      width: size,
      height: size,
      decoration: BoxDecoration(color: AppColors.tagYellow.resolveFrom(context), shape: BoxShape.circle),
      alignment: Alignment.center,
      child: Text(name.isEmpty ? '?' : name.characters.first.toUpperCase(),
          style: script(context, size: size * 0.55, color: AppColors.tagTextY.resolveFrom(context))),
    );
  }
}

/// Deftere bantla yapıştırılmış çizim.
class Polaroid extends StatelessWidget {
  const Polaroid(this.asset, {super.key, this.size = 104, this.angle = -3});
  final String asset;
  final double size;
  final double angle;

  @override
  Widget build(BuildContext context) => Transform.rotate(
        angle: angle * math.pi / 180,
        child: Stack(clipBehavior: Clip.none, alignment: Alignment.topCenter, children: [
          SketchBox(
            radius: 6,
            seed: asset.hashCode,
            padding: const EdgeInsets.fromLTRB(8, 8, 8, 22),
            child: ClipRRect(
                borderRadius: BorderRadius.circular(3),
                child: Image.asset(asset, width: size, height: size, fit: BoxFit.cover)),
          ),
          Positioned(
            top: -9,
            child: Transform.rotate(
              angle: -angle * 2 * math.pi / 180,
              child: Container(width: 60, height: 18, color: AppColors.tape.resolveFrom(context)),
            ),
          ),
        ]),
      );
}

/// Boş, hata ve yok durumları: polaroid, iki yanda küçük çizimler.
class EmptyState extends StatelessWidget {
  const EmptyState({
    super.key,
    required this.sceneKey,
    required this.title,
    required this.message,
    this.action,
    this.doodles = const ('maydanoz', 'biber'),
  });
  final String sceneKey;
  final String title;
  final String message;
  final Widget? action;
  final (String, String) doodles;

  @override
  Widget build(BuildContext context) => SliverToBoxAdapter(
        child: Padding(
          padding: const EdgeInsets.fromLTRB(32, 40, 32, 0),
          child: Column(children: [
            SizedBox(
              height: 170,
              child: Stack(alignment: Alignment.center, clipBehavior: Clip.none, children: [
                Polaroid(scene(sceneKey)),
                Positioned(
                    left: 8,
                    top: 10,
                    child: Transform.rotate(angle: -0.3, child: Image.asset(doodle(doodles.$1), width: 48))),
                Positioned(
                    right: 8,
                    bottom: 20,
                    child: Transform.rotate(angle: 0.28, child: Image.asset(doodle(doodles.$2), width: 48))),
              ]),
            ),
            const SizedBox(height: 14),
            Text(title, style: script(context, size: 29), textAlign: TextAlign.center),
            const SizedBox(height: 6),
            Text(message, style: meta(context, size: 18), textAlign: TextAlign.center),
            if (action != null) ...[const SizedBox(height: 8), action!],
          ]),
        ),
      );
}

/// Kısa bilgi mesajı (ör. "Liste kopyalandı").
void toast(BuildContext context, String message) {
  showCupertinoDialog(
    context: context,
    barrierDismissible: true,
    builder: (d) => CupertinoAlertDialog(
      title: Text(message, style: script(d, size: 22)),
      actions: [CupertinoDialogAction(child: const Text('Tamam'), onPressed: () => Navigator.pop(d))],
    ),
  );
}
