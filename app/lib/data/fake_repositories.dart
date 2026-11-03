import 'dart:async';
import 'dart:typed_data';

import '../models/models.dart';
import 'repositories.dart';

/// Firebase gelene kadar bellekte çalışan sahte veri.
/// Dolap ve liste aynı [FakeHouseStore] üzerinden çalışır, böylece
/// Pişirdim ve Alındı döngüsü şimdiden denenebilir.

class _Live<T> {
  _Live(this._value);
  T _value;
  final _c = StreamController<T>.broadcast();
  T get value => _value;
  set value(T v) {
    _value = v;
    _c.add(v);
  }

  Stream<T> get stream async* {
    yield _value;
    yield* _c.stream;
  }
}

int _id = 100;
String _nextId() => '${_id++}';
DateTime _inDays(int d) => DateTime.now().add(Duration(days: d));

class FakeHouseStore {
  final pantry = _Live<List<PantryItem>>([
    PantryItem(id: '1', name: 'Yoğurt', expiresOn: _inDays(1), addedBy: 'me', updatedAt: DateTime.now()),
    PantryItem(id: '2', name: 'Domates', expiresOn: _inDays(2), addedBy: 'ayse', updatedAt: DateTime.now()),
    PantryItem(id: '3', name: 'Yumurta', expiresOn: _inDays(9), addedBy: 'me', updatedAt: DateTime.now()),
    PantryItem(id: '4', name: 'Patates', state: ItemState.low, addedBy: 'ayse', updatedAt: DateTime.now()),
    PantryItem(id: '5', name: 'Soğan', addedBy: 'me', updatedAt: DateTime.now()),
    PantryItem(id: '6', name: 'Beyaz peynir', expiresOn: _inDays(6), addedBy: 'ayse', updatedAt: DateTime.now()),
    PantryItem(id: '7', name: 'Biber', expiresOn: _inDays(4), addedBy: 'me', updatedAt: DateTime.now()),
  ]);
  final list = _Live<List<ListItem>>([
    ListItem(id: 'l1', name: 'Tereyağı', addedBy: 'me', addedByName: 'Sen', createdAt: DateTime.now()),
    ListItem(id: 'l2', name: 'Salatalık', addedBy: 'ayse', addedByName: 'Ayşe', createdAt: DateTime.now()),
    ListItem(id: 'l3', name: 'Ekmek', addedBy: 'ayse', addedByName: 'Ayşe', createdAt: DateTime.now()),
  ]);
}

class FakeAuthService implements AuthService {
  final _user = _Live<AppUser?>(null);
  @override
  AppUser? get currentUser => _user.value;
  @override
  Stream<AppUser?> get userChanges => _user.stream;

  @override
  Future<void> signIn(String email, String password) async {
    await Future.delayed(const Duration(milliseconds: 400));
    if (email.isEmpty || password.length < 6) {
      throw Exception('E-posta veya şifre hatalı.');
    }
    _user.value = const AppUser(uid: 'me', name: 'Sen', householdId: 'ev');
  }

  @override
  Future<void> signUp(String email, String password, String name) => signIn(email, password);

  @override
  Future<void> signInAsGuest() async =>
      _user.value = const AppUser(uid: 'me', name: 'Misafir', householdId: 'ev', guest: true);

  @override
  Future<void> signOut() async => _user.value = null;
}

class FakePreferencesRepository implements PreferencesRepository {
  Preferences _p = const Preferences();
  @override
  Preferences load() => _p;
  @override
  Future<void> save(Preferences prefs) async => _p = prefs;
}

class FakePantryRepository implements PantryRepository {
  FakePantryRepository(this.store);
  final FakeHouseStore store;

  @override
  Stream<List<PantryItem>> watch(String householdId) => store.pantry.stream;

  @override
  Future<void> addAll(String householdId, List<ScannedItem> items) async {
    store.pantry.value = [
      ...store.pantry.value,
      for (final s in items)
        PantryItem(id: _nextId(), name: s.name, expiresOn: s.expiresOn, addedBy: 'me', updatedAt: DateTime.now()),
    ];
  }

  @override
  Future<void> update(String householdId, PantryItem item) async {
    store.pantry.value = [for (final p in store.pantry.value) p.id == item.id ? item : p];
  }

  @override
  Future<void> remove(String householdId, String itemId) async {
    store.pantry.value = store.pantry.value.where((p) => p.id != itemId).toList();
  }

  /// Pişirdim: kullanılan her malzeme Var -> Azaldı, Azaldı -> Bitti.
  /// Biten malzeme dolaptan çıkar ve listeye eklenir.
  @override
  Future<void> markCooked(String householdId, Recipe recipe) async {
    final used = recipe.usedIngredients.map((e) => e.toLowerCase()).toSet();
    final pantry = <PantryItem>[];
    final finished = <String>[];
    for (final p in store.pantry.value) {
      if (!used.contains(p.name.toLowerCase())) {
        pantry.add(p);
      } else if (p.state == ItemState.have) {
        pantry.add(p.copyWith(state: ItemState.low));
      } else {
        finished.add(p.name);
      }
    }
    store.pantry.value = pantry;
    final onList = store.list.value.map((l) => l.name.toLowerCase()).toSet();
    store.list.value = [
      ...store.list.value,
      for (final n in finished)
        if (!onList.contains(n.toLowerCase()))
          ListItem(id: _nextId(), name: n, addedBy: 'me', addedByName: 'Sen', createdAt: DateTime.now()),
    ];
  }
}

class FakeShoppingListRepository implements ShoppingListRepository {
  FakeShoppingListRepository(this.store);
  final FakeHouseStore store;

  @override
  Stream<List<ListItem>> watchItems(String householdId) => store.list.stream;

  @override
  Future<void> add(String householdId, String name) async {
    store.list.value = [
      ...store.list.value,
      ListItem(id: _nextId(), name: name, addedBy: 'me', addedByName: 'Sen', createdAt: DateTime.now()),
    ];
  }

  /// Alındı: malzeme dolaba Var olarak döner ve listeden çıkar.
  @override
  Future<void> markBought(String householdId, ListItem item) async {
    store.list.value = store.list.value.where((l) => l.id != item.id).toList();
    final pantry = store.pantry.value.where((p) => p.name.toLowerCase() != item.name.toLowerCase()).toList();
    store.pantry.value = [
      ...pantry,
      PantryItem(id: _nextId(), name: item.name, addedBy: 'me', updatedAt: DateTime.now()),
    ];
  }
}

class FakeRecipeAiService implements RecipeAiService {
  @override
  Future<List<ScannedItem>> detectItems(Uint8List photo) async {
    await Future.delayed(const Duration(seconds: 2));
    return [
      ScannedItem(name: 'Süt', expiresOn: _inDays(5)),
      ScannedItem(name: 'Kaşar peyniri', expiresOn: _inDays(14)),
      ScannedItem(name: 'Ispanak', isUncertain: true, expiresOn: _inDays(3)),
    ];
  }

  @override
  Future<List<Recipe>> suggestRecipes(List<PantryItem> pantry, Preferences prefs) async {
    await Future.delayed(const Duration(milliseconds: 1500));
    return [
      Recipe(
        id: 'r1',
        title: 'Menemen',
        photoPath: 'assets/img/yemek/menemen',
        minutes: 15,
        servings: prefs.servings,
        usedIngredients: ['Domates', 'Yumurta', 'Biber', 'Soğan'],
        usesExpiring: ['Domates'],
        steps: [
          'Soğanı ve biberi doğrayıp tavada yağla 3 dakika kavurun.',
          'Rendelenmiş domatesi ekleyin, suyunu çekene kadar pişirin.',
          'Yumurtaları kırın, hafifçe karıştırıp kısık ateşte pişirin.',
        ],
      ),
      Recipe(
        id: 'r2',
        title: 'Patatesli Omlet',
        photoPath: 'assets/img/yemek/omlet',
        minutes: 20,
        servings: prefs.servings,
        usedIngredients: ['Patates', 'Yumurta', 'Soğan', 'Beyaz peynir'],
        steps: [
          'Patatesleri küp doğrayıp yumuşayana kadar kızartın.',
          'Soğanı ekleyip 2 dakika çevirin.',
          'Çırpılmış yumurta ve ufalanmış peyniri dökün, kapağı kapalı pişirin.',
        ],
      ),
      Recipe(
        id: 'r3',
        title: 'Cacık',
        photoPath: 'assets/img/yemek/cacik',
        minutes: 10,
        servings: prefs.servings,
        usedIngredients: ['Yoğurt'],
        usesExpiring: ['Yoğurt'],
        missingIngredients: ['Salatalık', 'Sarımsak'],
        steps: [
          'Salatalığı rendeleyin ya da küçük doğrayın.',
          'Yoğurdu su ve ezilmiş sarımsakla açın.',
          'Salatalığı ekleyin, nane ve zeytinyağı ile servis edin.',
        ],
      ),
    ];
  }
}

class FakeSavedRecipeRepository implements SavedRecipeRepository {
  final _saved = _Live<List<Recipe>>([]);
  @override
  Stream<List<Recipe>> watchAll() => _saved.stream;
  @override
  Future<void> save(Recipe recipe) async {
    if (_saved.value.any((r) => r.id == recipe.id)) return;
    _saved.value = [..._saved.value, recipe];
  }

  @override
  Future<void> delete(String recipeId) async {
    _saved.value = _saved.value.where((r) => r.id != recipeId).toList();
  }
}
