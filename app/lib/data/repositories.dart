import 'dart:typed_data';

import '../models/models.dart';

/// Sözleşmeler. ViewModel'ler yalnızca bunlara bağlıdır;
/// şimdilik fake_repositories.dart, sonra Firebase/Hive sürümleri takılır.
abstract class AuthService {
  Stream<AppUser?> get userChanges;
  AppUser? get currentUser;
  Future<void> signIn(String email, String password);
  Future<void> signUp(String email, String password, String name);
  Future<void> signInAsGuest(); // hesapsız dene
  Future<void> signOut();
}

abstract class PantryRepository {
  Stream<List<PantryItem>> watch(String householdId);
  Future<void> addAll(String householdId, List<ScannedItem> items);
  Future<void> update(String householdId, PantryItem item);
  Future<void> markCooked(String householdId, Recipe recipe); // tek batched write
  Future<void> remove(String householdId, String itemId);
}

abstract class ShoppingListRepository {
  Stream<List<ListItem>> watchItems(String householdId);
  Future<void> add(String householdId, String name);
  Future<void> markBought(String householdId, ListItem item); // dolaba da ekler
}

abstract class RecipeAiService {
  Future<List<ScannedItem>> detectItems(Uint8List photo);
  Future<List<Recipe>> suggestRecipes(List<PantryItem> pantry, Preferences prefs);
}

abstract class SavedRecipeRepository {
  Stream<List<Recipe>> watchAll();
  Future<void> save(Recipe recipe);
  Future<void> delete(String recipeId);
}

abstract class PreferencesRepository {
  Preferences load();
  Future<void> save(Preferences prefs);
}
