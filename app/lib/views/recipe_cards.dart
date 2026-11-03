import 'package:flutter/cupertino.dart';
import 'package:go_router/go_router.dart';

import '../app/theme.dart';
import '../models/models.dart';
import 'widgets.dart';

/// Öneriler: büyük resimli, yatay kart.
class RecipeCard extends StatelessWidget {
  const RecipeCard({super.key, required this.recipe});
  final Recipe recipe;

  @override
  Widget build(BuildContext context) {
    final r = recipe;
    final note = r.missingIngredients.isNotEmpty
        ? ('Eksik: ${r.missingIngredients.join(', ')}', AppColors.text2)
        : r.usesExpiring.isNotEmpty
            ? ('${r.usesExpiring.join(', ')} bozulmadan kullanılır', AppColors.accent)
            : ('Tüm malzemeler dolapta', AppColors.herb);
    return Padding(
      padding: const EdgeInsets.fromLTRB(16, 0, 16, 12),
      child: GestureDetector(
        onTap: () => context.push('/recipe/${r.id}'),
        child: SketchBox(
          radius: 18,
          seed: r.id.hashCode,
          padding: const EdgeInsets.all(8),
          child: Row(children: [
            Hero(
              tag: 'photo-${r.id}',
              child: ClipRRect(
                borderRadius: BorderRadius.circular(12),
                child: Image.asset(dishSquare(r.photoPath), width: 96, height: 96, fit: BoxFit.cover),
              ),
            ),
            const SizedBox(width: 12),
            Expanded(
              child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
                Text(r.title, style: script(context, size: 23)),
                const SizedBox(height: 2),
                Text('${r.minutes} dk · ${r.servings} kişilik', style: meta(context)),
                const SizedBox(height: 4),
                Text(note.$1, style: body(context, size: 14.5, color: note.$2.resolveFrom(context)), maxLines: 2),
              ]),
            ),
            Icon(CupertinoIcons.chevron_forward, color: AppColors.text2.resolveFrom(context), size: 18),
          ]),
        ),
      ),
    );
  }
}

/// Kayıtlı tarifler: 2 x 2 ızgarada çizimli kart.
class RecipeTile extends StatelessWidget {
  const RecipeTile({super.key, required this.recipe});
  final Recipe recipe;

  @override
  Widget build(BuildContext context) {
    final r = recipe;
    return GestureDetector(
      onTap: () => context.push('/recipe/${r.id}'),
      child: SketchBox(
        radius: 16,
        seed: r.id.hashCode + 7,
        padding: const EdgeInsets.all(10),
        child: Column(crossAxisAlignment: CrossAxisAlignment.start, children: [
          Expanded(
            child: Hero(
              tag: 'photo-${r.id}',
              child: ClipRRect(
                borderRadius: BorderRadius.circular(10),
                child: Image.asset(dishSquare(r.photoPath), width: double.infinity, fit: BoxFit.cover),
              ),
            ),
          ),
          const SizedBox(height: 8),
          Text(r.title, style: script(context, size: 21), maxLines: 2, overflow: TextOverflow.ellipsis),
          Text('${r.minutes} dk · ${r.servings} kişilik', style: meta(context, size: 13.5)),
        ]),
      ),
    );
  }
}
