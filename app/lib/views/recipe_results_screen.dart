import 'package:flutter/cupertino.dart';
import 'package:provider/provider.dart';

import '../app/theme.dart';
import '../viewmodels/pantry_view_model.dart';
import '../viewmodels/recipe_view_model.dart';
import 'preferences_sheet.dart';
import 'recipe_cards.dart';
import 'widgets.dart';

class RecipeResultsScreen extends StatelessWidget {
  const RecipeResultsScreen({super.key});

  @override
  Widget build(BuildContext context) {
    final vm = context.watch<RecipeViewModel>();
    void again() => vm.suggest(context.read<PantryViewModel>().items);
    return NotebookPage(
      title: 'Öneriler',
      subtitle: 'Önce bozulacaklara göre',
      back: true,
      coverArt: cover('kitap'),
      slivers: [
        if (vm.loading)
          SliverToBoxAdapter(
            child: Padding(
              padding: const EdgeInsets.only(top: 60),
              child: Column(children: [
                Image.asset(scene('tencere'), width: 110),
                const SizedBox(height: 12),
                const CupertinoActivityIndicator(radius: 13),
                const SizedBox(height: 8),
                Text('Tarifler hazırlanıyor…', style: meta(context, size: 18)),
              ]),
            ),
          )
        else if (vm.error != null)
          EmptyState(
            sceneKey: 'tencere',
            title: 'Tarifler alınamadı',
            message: vm.error!,
            doodles: ('defne', 'karabiber'),
            action: TextInkButton(label: 'Tekrar Dene', bold: true, onPressed: again),
          )
        else if (vm.suggestions.isEmpty)
          EmptyState(
            sceneKey: 'tencere',
            title: 'Uygun tarif yok',
            message: 'Süreyi uzat ya da "Eksik malzeme" seçimini gevşet.',
            doodles: ('defne', 'karabiber'),
            action: TextInkButton(label: 'Tercihleri Değiştir', bold: true, onPressed: () => showPreferencesSheet(context)),
          )
        else ...[
          const SliverToBoxAdapter(child: SizedBox(height: 8)),
          SliverList.list(children: [for (final r in vm.suggestions) RecipeCard(recipe: r)]),
          SliverToBoxAdapter(child: TextInkButton(label: 'Başka Tarifler Öner', onPressed: again)),
        ],
      ],
    );
  }
}
