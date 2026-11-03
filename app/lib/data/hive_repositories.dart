import 'dart:async';

import 'package:hive_ce/hive.dart';

import '../models/models.dart';
import 'repositories.dart';
import 'shelf_life.dart';

/// Hive ile cihazda kalıcı veri. Uygulama kapanıp açılınca dolap, liste,
/// kayıtlı tarifler, tercihler ve oturum yerinde durur.
/// Firebase eklenince aynı sözleşmeler Firestore sürümleriyle değiştirilir.
class HiveStore {
  HiveStore(this.pantry, this.list, this.saved, this.session);
  final Box pantry, list, saved, session;

  static const boxes = ['pantry', 'list', 'saved', 'session'];

  static Future<HiveStore> open() async {
    final b = [for (final n in boxes) await Hive.openBox(n)];
    final store = HiveStore(b[0], b[1], b[2], b[3]);
    await store._seedOnce();
    return store;
  }

  /// İlk açılışta boş bir ekran yerine örnek bir dolap gösterilir.
  Future<void> _seedOnce() async {
    if (session.get('seeded') == true) return;
    final now = DateTime.now();
    DateTime inDays(int d) => DateTime(now.year, now.month, now.day).add(Duration(days: d));
    final items = [
      PantryItem(id: newId(), name: 'Yoğurt', expiresOn: inDays(1), addedBy: 'me', updatedAt: now),
      PantryItem(id: newId(), name: 'Domates', expiresOn: inDays(2), addedBy: 'me', updatedAt: now),
      PantryItem(id: newId(), name: 'Yumurta', expiresOn: inDays(12), addedBy: 'me', updatedAt: now),
      PantryItem(id: newId(), name: 'Peynir', state: ItemState.low, expiresOn: inDays(9), addedBy: 'me', updatedAt: now),
      PantryItem(id: newId(), name: 'Patates', expiresOn: inDays(25), addedBy: 'me', updatedAt: now),
      PantryItem(id: newId(), name: 'Soğan', expiresOn: inDays(28), addedBy: 'me', updatedAt: now),
      PantryItem(id: newId(), name: 'Biber', expiresOn: inDays(5), addedBy: 'me', updatedAt: now),
      PantryItem(id: newId(), name: 'Maydanoz', state: ItemState.low, expiresOn: inDays(4), addedBy: 'me', updatedAt: now),
    ];
    await pantry.putAll({for (final i in items) i.id: i.toJson()});
    final l = [
      ListItem(id: newId(), name: 'Tereyağı', addedBy: 'me', addedByName: 'Sen', createdAt: now),
      ListItem(id: newId(), name: 'Salatalık', addedBy: 'me', addedByName: 'Sen', createdAt: now),
      ListItem(id: newId(), name: 'Ekmek', addedBy: 'me', addedByName: 'Sen', createdAt: now),
    ];
    await list.putAll({for (final i in l) i.id: i.toJson()});
    await session.put('seeded', true);
  }
}

int _counter = 0;
String newId() => '${DateTime.now().microsecondsSinceEpoch}-${_counter++}';

/// Box içeriğini önce bir kez, sonra her değişiklikte yayınlar.
Stream<List<T>> _watch<T>(Box box, T Function(Map) parse) async* {
  List<T> read() => box.values.map((v) => parse(v as Map)).toList();
  yield read();
  await for (final _ in box.watch()) {
    yield read();
  }
}

class HiveAuthService implements AuthService {
  HiveAuthService(this._session) {
    final u = _session.get('user');
    _user = u == null ? null : AppUser.fromJson(u as Map);
  }
  final Box _session;
  AppUser? _user;
  final _changes = StreamController<AppUser?>.broadcast();

  @override
  AppUser? get currentUser => _user;

  @override
  Stream<AppUser?> get userChanges async* {
    yield _user;
    yield* _changes.stream;
  }

  Future<void> _set(AppUser? u) async {
    _user = u;
    u == null ? await _session.delete('user') : await _session.put('user', u.toJson());
    _changes.add(u);
  }

  @override
  Future<void> signIn(String email, String password) async {
    await Future.delayed(const Duration(milliseconds: 300));
    if (!email.contains('@') || password.length < 6) {
      throw Exception('E-posta geçersiz ya da şifre 6 karakterden kısa.');
    }
    await _set(AppUser(uid: 'me', name: email.split('@').first, householdId: 'ev'));
  }

  @override
  Future<void> signUp(String email, String password, String name) => signIn(email, password);

  @override
  Future<void> signInAsGuest() => _set(const AppUser(uid: 'me', name: 'Misafir', householdId: 'ev', guest: true));

  @override
  Future<void> signOut() => _set(null);
}

class HivePantryRepository implements PantryRepository {
  HivePantryRepository(this.store);
  final HiveStore store;

  @override
  Stream<List<PantryItem>> watch(String householdId) => _watch(store.pantry, PantryItem.fromJson);

  @override
  Future<void> addAll(String householdId, List<ScannedItem> items) async {
    final now = DateTime.now();
    final existing = {
      for (final v in store.pantry.values) norm((v as Map)['name'] as String): PantryItem.fromJson(v)
    };
    final writes = <String, Map>{};
    for (final s in items) {
      final old = existing[norm(s.name)];
      // Aynı ürün zaten varsa yenisi onun yerine geçer (Var, yeni tarih).
      final item = PantryItem(
        id: old?.id ?? newId(),
        name: s.name,
        expiresOn: s.expiresOn ?? estimateExpiry(s.name),
        addedBy: 'me',
        updatedAt: now,
      );
      writes[item.id] = item.toJson();
    }
    await store.pantry.putAll(writes);
  }

  @override
  Future<void> update(String householdId, PantryItem item) => store.pantry.put(item.id, item.toJson());

  @override
  Future<void> remove(String householdId, String itemId) => store.pantry.delete(itemId);

  /// Pişirdim: kullanılan her malzeme Var -> Azaldı, Azaldı -> Bitti.
  /// Biten malzeme dolaptan çıkar ve alışveriş listesine eklenir.
  @override
  Future<void> markCooked(String householdId, Recipe recipe) async {
    final used = recipe.usedIngredients.map(norm).toSet();
    final updates = <String, Map>{};
    final removed = <String>[];
    final finished = <String>[];
    for (final v in store.pantry.values) {
      final p = PantryItem.fromJson(v as Map);
      if (!used.contains(norm(p.name))) continue;
      if (p.state == ItemState.have) {
        updates[p.id] = p.copyWith(state: ItemState.low).toJson();
      } else {
        removed.add(p.id);
        finished.add(p.name);
      }
    }
    await store.pantry.putAll(updates);
    await store.pantry.deleteAll(removed);
    final onList = store.list.values.map((v) => norm((v as Map)['name'] as String)).toSet();
    final now = DateTime.now();
    final toList = <String, Map>{};
    for (final n in finished.where((n) => !onList.contains(norm(n)))) {
      final id = newId();
      toList[id] = ListItem(id: id, name: n, addedBy: 'me', addedByName: 'Sen', createdAt: now).toJson();
    }
    await store.list.putAll(toList);
  }
}

class HiveShoppingListRepository implements ShoppingListRepository {
  HiveShoppingListRepository(this.store);
  final HiveStore store;

  @override
  Stream<List<ListItem>> watchItems(String householdId) =>
      _watch(store.list, ListItem.fromJson).map((l) => l..sort((a, b) => a.createdAt.compareTo(b.createdAt)));

  @override
  Future<void> add(String householdId, String name) async {
    final exists = store.list.values.any((v) => norm((v as Map)['name'] as String) == norm(name));
    if (exists) return;
    final id = newId();
    await store.list.put(id, ListItem(id: id, name: name, addedBy: 'me', addedByName: 'Sen', createdAt: DateTime.now()).toJson());
  }

  /// Alındı: listeden çıkar, dolaba Var olarak (tahmini tarihle) girer.
  @override
  Future<void> markBought(String householdId, ListItem item) async {
    await store.list.delete(item.id);
    await HivePantryRepository(store).addAll(householdId, [ScannedItem(name: item.name)]);
  }
}

class HiveSavedRecipeRepository implements SavedRecipeRepository {
  HiveSavedRecipeRepository(this.store);
  final HiveStore store;

  @override
  Stream<List<Recipe>> watchAll() => _watch(store.saved, Recipe.fromJson);

  @override
  Future<void> save(Recipe recipe) => store.saved.put(recipe.id, recipe.toJson());

  @override
  Future<void> delete(String recipeId) => store.saved.delete(recipeId);
}

class HivePreferencesRepository implements PreferencesRepository {
  HivePreferencesRepository(this.store);
  final HiveStore store;

  @override
  Preferences load() {
    final p = store.session.get('prefs');
    return p == null ? const Preferences() : Preferences.fromJson(p as Map);
  }

  @override
  Future<void> save(Preferences prefs) => store.session.put('prefs', prefs.toJson());
}
