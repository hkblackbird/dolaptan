import 'dart:async';

import 'package:flutter/foundation.dart';

import '../data/repositories.dart';
import '../models/models.dart';

class ShoppingListViewModel extends ChangeNotifier {
  ShoppingListViewModel(this._repo, this.householdId) {
    _sub = _repo.watchItems(householdId).listen((i) {
      items = i;
      notifyListeners();
    });
  }
  final ShoppingListRepository _repo;
  final String householdId;
  late final StreamSubscription _sub;

  List<ListItem> items = [];

  Future<void> add(String name) async {
    if (name.trim().isEmpty) return;
    await _repo.add(householdId, name.trim());
  }

  Future<void> addMissing(List<String> names) async {
    final have = items.map((e) => e.name.toLowerCase()).toSet();
    for (final n in names) {
      if (!have.contains(n.toLowerCase())) await _repo.add(householdId, n);
    }
  }

  Future<void> markBought(ListItem item) => _repo.markBought(householdId, item);

  /// Paylaşmak için düz metin liste.
  String asText() => ['Dolaptan alışveriş listesi', for (final i in items) '- ${i.name}'].join('\n');

  @override
  void dispose() {
    _sub.cancel();
    super.dispose();
  }
}
