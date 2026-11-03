import 'dart:typed_data';

import 'package:flutter/cupertino.dart';
import 'package:go_router/go_router.dart';
import 'package:image_picker/image_picker.dart';
import 'package:provider/provider.dart';

import '../app/theme.dart';
import '../viewmodels/scan_view_model.dart';
import 'widgets.dart';

/// Dolabın fotoğrafı: kamera ya da galeri. İnceleme sırasında fotoğrafın
/// üstünde bir tarama çizgisi gidip gelir (Figma'daki 03b / 03c animasyonu).
class ScanScreen extends StatefulWidget {
  const ScanScreen({super.key});
  @override
  State<ScanScreen> createState() => _ScanScreenState();
}

class _ScanScreenState extends State<ScanScreen> with SingleTickerProviderStateMixin {
  late final _line = AnimationController(vsync: this, duration: const Duration(milliseconds: 1400));
  Uint8List? _photo;
  String? _note;

  @override
  void dispose() {
    _line.dispose();
    super.dispose();
  }

  Future<void> _pick(ImageSource source) async {
    final vm = context.read<ScanViewModel>();
    try {
      final file = await ImagePicker().pickImage(source: source, maxWidth: 1600, imageQuality: 80);
      if (file == null) return;
      final bytes = await file.readAsBytes();
      setState(() {
        _photo = bytes;
        _note = null;
      });
      _line.repeat(reverse: true);
      final ok = await vm.analyze(bytes);
      _line.stop();
      if (ok && mounted) context.pushReplacement('/scan/review');
    } catch (_) {
      // Simülatörde kamera yoktur; galeriyi öner.
      setState(() => _note = source == ImageSource.camera
          ? 'Kamera açılamadı. Galeriden bir fotoğraf seçebilirsin.'
          : 'Fotoğraf açılamadı.');
    }
  }

  @override
  Widget build(BuildContext context) {
    final vm = context.watch<ScanViewModel>();
    const white = CupertinoColors.white;
    return CupertinoPageScaffold(
      backgroundColor: CupertinoColors.black,
      child: SafeArea(
        child: Column(children: [
          Padding(
            padding: const EdgeInsets.fromLTRB(8, 6, 16, 0),
            child: Row(children: [
              CircleButton(icon: CupertinoIcons.xmark, label: 'Kapat', onPressed: () => context.pop()),
              const Spacer(),
              Text('Dolabı tara', style: script(context, size: 24, color: white)),
              const Spacer(),
              const SizedBox(width: 52),
            ]),
          ),
          Expanded(
            child: Container(
              margin: const EdgeInsets.all(16),
              clipBehavior: Clip.antiAlias,
              decoration: BoxDecoration(color: const Color(0xFF1C1C1E), borderRadius: BorderRadius.circular(20)),
              child: Stack(fit: StackFit.expand, children: [
                if (_photo != null)
                  Image.memory(_photo!, fit: BoxFit.cover)
                else
                  Center(
                    child: Column(mainAxisSize: MainAxisSize.min, children: [
                      Image.asset(cover('raf'), width: 150),
                      const SizedBox(height: 12),
                      Text('Rafları kadraja al', style: body(context, color: CupertinoColors.systemGrey)),
                    ]),
                  ),
                if (vm.analyzing)
                  AnimatedBuilder(
                    animation: _line,
                    builder: (_, _) => Align(
                      alignment: Alignment(0, _line.value * 2 - 1),
                      child: Container(height: 3, color: AppColors.tape.resolveFrom(context)),
                    ),
                  ),
              ]),
            ),
          ),
          if (vm.analyzing)
            Column(children: [
              const CupertinoActivityIndicator(color: white),
              const SizedBox(height: 8),
              Text('Malzemeler aranıyor…', style: script(context, size: 22, color: white)),
            ])
          else ...[
            if (_note != null || vm.error != null)
              Padding(
                padding: const EdgeInsets.symmetric(horizontal: 24),
                child: Text(_note ?? vm.error!, textAlign: TextAlign.center, style: body(context, size: 16, color: white)),
              ),
            Padding(
              padding: const EdgeInsets.symmetric(vertical: 18, horizontal: 40),
              child: Row(children: [
                Semantics(
                  label: 'Galeriden seç',
                  button: true,
                  child: CupertinoButton(
                    padding: EdgeInsets.zero,
                    onPressed: () => _pick(ImageSource.gallery),
                    child: const Icon(CupertinoIcons.photo_on_rectangle, color: white, size: 30),
                  ),
                ),
                const Spacer(),
                Semantics(
                  label: 'Fotoğraf çek',
                  button: true,
                  child: GestureDetector(
                    onTap: () => _pick(ImageSource.camera),
                    child: Container(
                      width: 74,
                      height: 74,
                      padding: const EdgeInsets.all(5),
                      decoration: BoxDecoration(shape: BoxShape.circle, border: Border.all(color: white, width: 4)),
                      child: const DecoratedBox(decoration: BoxDecoration(color: white, shape: BoxShape.circle)),
                    ),
                  ),
                ),
                const Spacer(),
                const SizedBox(width: 30),
              ]),
            ),
          ],
        ]),
      ),
    );
  }
}
