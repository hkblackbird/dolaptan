import 'package:flutter/cupertino.dart';
import 'package:go_router/go_router.dart';
import 'package:hive_ce_flutter/hive_ce_flutter.dart';
import 'package:provider/provider.dart';

import 'app/dependencies.dart';
import 'app/router.dart';
import 'app/theme.dart';
import 'data/hive_repositories.dart';
import 'data/local_recipe_service.dart';
import 'viewmodels/auth_view_model.dart';
import 'viewmodels/pantry_view_model.dart';
import 'viewmodels/recipe_view_model.dart';
import 'viewmodels/scan_view_model.dart';
import 'viewmodels/shopping_list_view_model.dart';

Future<void> main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await Hive.initFlutter();
  final store = await HiveStore.open();
  runApp(DolaptanRoot(
    deps: Dependencies(
      auth: HiveAuthService(store.session),
      pantry: HivePantryRepository(store),
      list: HiveShoppingListRepository(store),
      recipes: LocalRecipeService(),
      saved: HiveSavedRecipeRepository(store),
      prefs: HivePreferencesRepository(store),
    ),
  ));
}

/// Provider ağacı: her ViewModel yalnızca sözleşmelere bağlıdır (MVVM).
class DolaptanRoot extends StatelessWidget {
  const DolaptanRoot({super.key, required this.deps});
  final Dependencies deps;
  static const householdId = 'ev';

  @override
  Widget build(BuildContext context) {
    return MultiProvider(
      providers: [
        ChangeNotifierProvider(create: (_) => AuthViewModel(deps.auth)),
        ChangeNotifierProvider(create: (_) => PantryViewModel(deps.pantry, householdId)),
        ChangeNotifierProvider(create: (_) => ShoppingListViewModel(deps.list, householdId)),
        ChangeNotifierProvider(create: (_) => RecipeViewModel(deps.recipes, deps.saved, deps.prefs)),
        ChangeNotifierProvider(create: (_) => ScanViewModel(deps.recipes)),
      ],
      child: const DolaptanApp(),
    );
  }
}

class DolaptanApp extends StatefulWidget {
  const DolaptanApp({super.key});
  @override
  State<DolaptanApp> createState() => _DolaptanAppState();
}

class _DolaptanAppState extends State<DolaptanApp> {
  late final GoRouter _router = buildRouter(context.read<AuthViewModel>());

  @override
  Widget build(BuildContext context) {
    return CupertinoApp.router(
      title: 'Dolaptan',
      debugShowCheckedModeBanner: false,
      theme: appTheme,
      routerConfig: _router,
    );
  }
}
