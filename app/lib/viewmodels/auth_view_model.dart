import 'dart:async';

import 'package:flutter/foundation.dart';

import '../data/repositories.dart';
import '../models/models.dart';

class AuthViewModel extends ChangeNotifier {
  AuthViewModel(this._auth) {
    _sub = _auth.userChanges.listen((u) {
      user = u;
      notifyListeners();
    });
  }
  final AuthService _auth;
  late final StreamSubscription _sub;

  AppUser? user;
  bool loading = false;
  String? error;

  bool get signedIn => user != null;

  Future<void> signIn(String email, String password) async {
    loading = true;
    error = null;
    notifyListeners();
    try {
      await _auth.signIn(email.trim(), password);
    } catch (e) {
      error = e.toString().replaceFirst('Exception: ', '');
    } finally {
      loading = false;
      notifyListeners();
    }
  }

  Future<void> signInAsGuest() => _auth.signInAsGuest();

  Future<void> signOut() => _auth.signOut();

  @override
  void dispose() {
    _sub.cancel();
    super.dispose();
  }
}
