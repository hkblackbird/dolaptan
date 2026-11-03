import 'dart:async';

import 'package:flutter/foundation.dart';

import '../data/repositories.dart';
import '../models/models.dart';

class PantryViewModel extends ChangeNotifier {
  PantryViewModel(this._repo, this.householdId) {
    _sub = _repo.watch(householdId).listen((items) {
      this.items = items;
      loading = false;
      notifyListeners();
    }, onError: (e) {
      error = 'Dolap yüklenemedi.';
      notifyListeners();
    });
  }
  final PantryRepository _repo;
  final String householdId;
  late final StreamSubscription _sub;

  List<PantryItem> items = [];
  bool loading = true;
  String? error;

  /// Önce bozulacaklar, en yakın tarih en üstte.
  List<PantryItem> get expiringSoon =>
      items.where((i) => i.isExpiringSoon).toList()..sort((a, b) => a.daysLeft!.compareTo(b.daysLeft!));

  List<PantryItem> get others => items.where((i) => !i.isExpiringSoon).toList()
    ..sort((a, b) => a.name.compareTo(b.name));

  PantryItem? byId(String id) {
    for (final i in items) {
      if (i.id == id) return i;
    }
    return null;
  }

  Future<void> update(PantryItem item) => _repo.update(householdId, item);
  Future<void> remove(String id) => _repo.remove(householdId, id);
  Future<void> addAll(List<ScannedItem> scanned) => _repo.addAll(householdId, scanned);
  Future<void> markCooked(Recipe r) => _repo.markCooked(householdId, r);

  @override
  void dispose() {
    _sub.cancel();
    super.dispose();
  }
}
