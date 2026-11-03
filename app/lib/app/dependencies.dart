import '../data/repositories.dart';

/// Uygulamanın bağlı olduğu servisler. main.dart Hive sürümlerini,
/// testler sahte sürümleri verir; Firebase gelince yalnızca burası değişir.
class Dependencies {
  const Dependencies({
    required this.auth,
    required this.pantry,
    required this.list,
    required this.recipes,
    required this.saved,
    required this.prefs,
  });
  final AuthService auth;
  final PantryRepository pantry;
  final ShoppingListRepository list;
  final RecipeAiService recipes;
  final SavedRecipeRepository saved;
  final PreferencesRepository prefs;
}
