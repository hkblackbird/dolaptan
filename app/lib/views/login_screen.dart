import 'package:flutter/cupertino.dart';
import 'package:provider/provider.dart';

import '../app/theme.dart';
import '../viewmodels/auth_view_model.dart';
import 'widgets.dart';

class LoginScreen extends StatefulWidget {
  const LoginScreen({super.key});
  @override
  State<LoginScreen> createState() => _LoginScreenState();
}

class _LoginScreenState extends State<LoginScreen> {
  final _email = TextEditingController();
  final _password = TextEditingController();

  @override
  void dispose() {
    _email.dispose();
    _password.dispose();
    super.dispose();
  }

  Widget _field(TextEditingController c, String hint, {bool secret = false, TextInputType? type}) =>
      CupertinoTextField(
        controller: c,
        placeholder: hint,
        obscureText: secret,
        keyboardType: type,
        autocorrect: false,
        decoration: null,
        style: body(context),
        placeholderStyle: meta(context, size: 18.5),
        padding: const EdgeInsets.symmetric(horizontal: 16, vertical: 13),
      );

  @override
  Widget build(BuildContext context) {
    final vm = context.watch<AuthViewModel>();
    return CupertinoPageScaffold(
      child: NotebookPaper(
        child: SafeArea(
          child: ListView(padding: const EdgeInsets.fromLTRB(0, 56, 0, 24), children: [
            Padding(
              padding: const EdgeInsets.symmetric(horizontal: 16),
              child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                Text('Giriş Yap', style: script(context, size: 44)),
                Text('Dolaptan hesabınla devam et.', style: meta(context, size: 17)),
              ]),
            ),
            const SizedBox(height: 20),
            SketchList(children: [
              _field(_email, 'E-posta', type: TextInputType.emailAddress),
              _field(_password, 'Şifre', secret: true),
            ]),
            if (vm.error != null)
              Padding(
                padding: const EdgeInsets.fromLTRB(32, 10, 32, 0),
                child: Text(vm.error!, style: body(context, size: 16, color: AppColors.red.resolveFrom(context))),
              ),
            Padding(
              padding: const EdgeInsets.fromLTRB(16, 20, 16, 4),
              child: vm.loading
                  ? const CupertinoActivityIndicator()
                  : InkButton(label: 'Giriş Yap', onPressed: () => vm.signIn(_email.text, _password.text)),
            ),
            TextInkButton(label: 'Hesap Oluştur', onPressed: () => vm.signIn(_email.text, _password.text)),
            TextInkButton(label: 'Hesapsız Dene', onPressed: vm.signInAsGuest),
            const SizedBox(height: 16),
            SizedBox(
              height: 260,
              child: Stack(alignment: Alignment.center, children: [
                Polaroid(scene('dolap-dolu'), size: 180, angle: 3),
                Positioned(left: 18, top: 10, child: Transform.rotate(angle: -0.35, child: Image.asset(doodle('maydanoz'), width: 60))),
                Positioned(right: 22, top: 0, child: Transform.rotate(angle: 0.2, child: Image.asset(doodle('limon'), width: 50))),
                Positioned(right: 18, bottom: 0, child: Transform.rotate(angle: 0.5, child: Image.asset(doodle('biber'), width: 64))),
                Positioned(left: 26, bottom: 4, child: Image.asset(doodle('cay'), width: 52)),
              ]),
            ),
          ]),
        ),
      ),
    );
  }
}
