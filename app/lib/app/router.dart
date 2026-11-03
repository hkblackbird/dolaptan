import 'package:flutter/cupertino.dart';
import 'package:go_router/go_router.dart';

import '../viewmodels/auth_view_model.dart';
import '../views/home_shell.dart';
import '../views/login_screen.dart';
import '../views/pantry_screen.dart';
import '../views/recipe_detail_screen.dart';
import '../views/recipe_results_screen.dart';
import '../views/saved_recipes_screen.dart';
import '../views/scan_review_screen.dart';
import '../views/scan_screen.dart';
import '../views/shopping_list_screen.dart';

GoRouter buildRouter(AuthViewModel auth) {
  CupertinoPage<void> page(GoRouterState s, Widget child) => CupertinoPage(key: s.pageKey, child: child);

  return GoRouter(
    initialLocation: '/pantry',
    refreshListenable: auth,
    redirect: (context, state) {
      final atLogin = state.matchedLocation == '/login';
      if (!auth.signedIn) return atLogin ? null : '/login';
      if (atLogin) return '/pantry';
      return null;
    },
    routes: [
      GoRoute(path: '/login', pageBuilder: (c, s) => page(s, const LoginScreen())),
      StatefulShellRoute.indexedStack(
        builder: (c, s, shell) => HomeShell(shell: shell),
        branches: [
          StatefulShellBranch(routes: [
            GoRoute(path: '/pantry', pageBuilder: (c, s) => page(s, const PantryScreen())),
          ]),
          StatefulShellBranch(routes: [
            GoRoute(path: '/recipes', pageBuilder: (c, s) => page(s, const SavedRecipesScreen())),
          ]),
          StatefulShellBranch(routes: [
            GoRoute(path: '/list', pageBuilder: (c, s) => page(s, const ShoppingListScreen())),
          ]),
        ],
      ),
      GoRoute(path: '/scan', pageBuilder: (c, s) => page(s, const ScanScreen())),
      GoRoute(path: '/scan/review', pageBuilder: (c, s) => page(s, const ScanReviewScreen())),
      GoRoute(path: '/cook/results', pageBuilder: (c, s) => page(s, const RecipeResultsScreen())),
      GoRoute(
        path: '/recipe/:id',
        pageBuilder: (c, s) => page(s, RecipeDetailScreen(id: s.pathParameters['id']!)),
      ),
    ],
  );
}
