import 'package:flutter/cupertino.dart';
import 'package:provider/provider.dart';

import '../app/theme.dart';
import '../viewmodels/recipe_view_model.dart';
import 'recipe_cards.dart';
import 'widgets.dart';

class SavedRecipesScreen extends StatelessWidget {
  const SavedRecipesScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final vm = context.watch<RecipeViewModel>();
    final list = vm.filteredSaved;
    return NotebookPage(
      title: 'Tarifler',
      slivers: [
        if (vm.saved.isEmpty)
          const EmptyState(
            sceneKey: 'defter',
            title: 'Kayıtlı tarif yok',
            message: 'Beğendiğin tarifte yer imine dokun, internetsiz de açılsın.',
            doodles: ('kasik', 'dereotu'),
          )
        else ...[
          SliverToBoxAdapter(
            child: Padding(
              padding: const EdgeInsets.symmetric(horizontal: 16),
              child: SketchBox(
                radius: 20,
                seed: 31,
                child: CupertinoSearchTextField(
                  placeholder: 'Ara',
                  style: body(context),
                  backgroundColor: const Color(0x00000000),
                  onChanged: vm.search,
                ),
              ),
            ),
          ),
          const SliverToBoxAdapter(child: SectionHeader('Kayıtlı', doodleKey: 'defne')),
          SliverPadding(
            padding: const EdgeInsets.symmetric(horizontal: 16),
            sliver: SliverGrid.count(
              crossAxisCount: 2,
              mainAxisSpacing: 14,
              crossAxisSpacing: 14,
              childAspectRatio: 0.78,
              children: [for (final r in list) RecipeTile(recipe: r)],
            ),
          ),
          SliverToBoxAdapter(
            child: Padding(
              padding: const EdgeInsets.fromLTRB(32, 12, 32, 0),
              child: Text('Kayıtlı tarifler internet olmadan da açılır.', style: meta(context, size: 14)),
            ),
          ),
        ],
      ],
    );
  }
}
