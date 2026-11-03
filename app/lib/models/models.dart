/// Dolaptan veri modelleri (docs/architecture-protocols.pdf ile aynı alanlar).
/// Her model Hive'da saklanmak için JSON'a (Map) çevrilebilir.
enum ItemState { have, low, out }

extension ItemStateLabel on ItemState {
  String get label => switch (this) {
        ItemState.have => 'Var',
        ItemState.low => 'Azaldı',
        ItemState.out => 'Bitti',
      };
}

DateTime _today() {
  final n = DateTime.now();
  return DateTime(n.year, n.month, n.day);
}

class PantryItem {
  final String id;
  final String name;
  final ItemState state;
  final DateTime? expiresOn;
  final bool remind;
  final String addedBy;
  final DateTime updatedAt;

  const PantryItem({
    required this.id,
    required this.name,
    this.state = ItemState.have,
    this.expiresOn,
    this.remind = true,
    required this.addedBy,
    required this.updatedAt,
  });

  /// Son kullanma tarihine kalan gün (tarih yoksa null).
  int? get daysLeft {
    if (expiresOn == null) return null;
    final e = DateTime(expiresOn!.year, expiresOn!.month, expiresOn!.day);
    return e.difference(_today()).inDays;
  }

  bool get isExpiringSoon => daysLeft != null && daysLeft! <= 3;

  PantryItem copyWith({String? name, ItemState? state, DateTime? expiresOn, bool clearExpiry = false, bool? remind}) =>
      PantryItem(
        id: id,
        name: name ?? this.name,
        state: state ?? this.state,
        expiresOn: clearExpiry ? null : (expiresOn ?? this.expiresOn),
        remind: remind ?? this.remind,
        addedBy: addedBy,
        updatedAt: DateTime.now(),
      );

  Map<String, dynamic> toJson() => {
        'id': id,
        'name': name,
        'state': state.name,
        'expiresOn': expiresOn?.toIso8601String(),
        'remind': remind,
        'addedBy': addedBy,
        'updatedAt': updatedAt.toIso8601String(),
      };

  factory PantryItem.fromJson(Map j) => PantryItem(
        id: j['id'] as String,
        name: j['name'] as String,
        state: ItemState.values.byName(j['state'] as String),
        expiresOn: j['expiresOn'] == null ? null : DateTime.parse(j['expiresOn'] as String),
        remind: j['remind'] as bool? ?? true,
        addedBy: j['addedBy'] as String? ?? 'me',
        updatedAt: DateTime.parse(j['updatedAt'] as String),
      );
}

class ScannedItem {
  String name;
  bool isUncertain;
  DateTime? expiresOn;

  /// true: tarih ürün türüne göre tahmin edildi, kullanıcı düzeltebilir.
  bool estimated;
  ScannedItem({required this.name, this.isUncertain = false, this.expiresOn, this.estimated = false});
}

class Preferences {
  final int minutes;
  final int servings;
  final List<String> allergies;

  /// Kabul edilen en fazla eksik malzeme: 0, 1 ya da null (fark etmez).
  final int? maxMissing;

  const Preferences({this.minutes = 30, this.servings = 2, this.allergies = const [], this.maxMissing = 1});

  Preferences copyWith({int? minutes, int? servings, List<String>? allergies, int? Function()? maxMissing}) =>
      Preferences(
        minutes: minutes ?? this.minutes,
        servings: servings ?? this.servings,
        allergies: allergies ?? this.allergies,
        maxMissing: maxMissing != null ? maxMissing() : this.maxMissing,
      );

  Map<String, dynamic> toJson() =>
      {'minutes': minutes, 'servings': servings, 'allergies': allergies, 'maxMissing': maxMissing};

  factory Preferences.fromJson(Map j) => Preferences(
        minutes: j['minutes'] as int? ?? 30,
        servings: j['servings'] as int? ?? 2,
        allergies: List<String>.from(j['allergies'] as List? ?? const []),
        maxMissing: j['maxMissing'] as int?,
      );
}

class Recipe {
  final String id;
  final String title;
  final int minutes;
  final int servings;
  final List<String> usedIngredients;
  final List<String> usesExpiring;
  final List<String> missingIngredients;
  final List<String> steps;

  /// Kare tarif çizimi (assets). Yoksa tencere çizimi gösterilir.
  final String? photoPath;

  const Recipe({
    required this.id,
    required this.title,
    required this.minutes,
    required this.servings,
    required this.usedIngredients,
    this.usesExpiring = const [],
    this.missingIngredients = const [],
    required this.steps,
    this.photoPath,
  });

  Map<String, dynamic> toJson() => {
        'id': id,
        'title': title,
        'minutes': minutes,
        'servings': servings,
        'usedIngredients': usedIngredients,
        'usesExpiring': usesExpiring,
        'missingIngredients': missingIngredients,
        'steps': steps,
        'photoPath': photoPath,
      };

  factory Recipe.fromJson(Map j) => Recipe(
        id: j['id'] as String,
        title: j['title'] as String,
        minutes: j['minutes'] as int,
        servings: j['servings'] as int,
        usedIngredients: List<String>.from(j['usedIngredients'] as List),
        usesExpiring: List<String>.from(j['usesExpiring'] as List? ?? const []),
        missingIngredients: List<String>.from(j['missingIngredients'] as List? ?? const []),
        steps: List<String>.from(j['steps'] as List),
        photoPath: j['photoPath'] as String?,
      );
}

class ListItem {
  final String id;
  final String name;
  final String addedBy;
  final String addedByName;
  final bool checked;
  final DateTime createdAt;
  const ListItem({
    required this.id,
    required this.name,
    required this.addedBy,
    required this.addedByName,
    this.checked = false,
    required this.createdAt,
  });

  Map<String, dynamic> toJson() => {
        'id': id,
        'name': name,
        'addedBy': addedBy,
        'addedByName': addedByName,
        'checked': checked,
        'createdAt': createdAt.toIso8601String(),
      };

  factory ListItem.fromJson(Map j) => ListItem(
        id: j['id'] as String,
        name: j['name'] as String,
        addedBy: j['addedBy'] as String? ?? 'me',
        addedByName: j['addedByName'] as String? ?? 'Sen',
        checked: j['checked'] as bool? ?? false,
        createdAt: DateTime.parse(j['createdAt'] as String),
      );
}

class AppUser {
  final String uid;
  final String name;
  final String householdId;
  final bool guest;
  const AppUser({required this.uid, required this.name, required this.householdId, this.guest = false});

  Map<String, dynamic> toJson() => {'uid': uid, 'name': name, 'householdId': householdId, 'guest': guest};

  factory AppUser.fromJson(Map j) => AppUser(
        uid: j['uid'] as String,
        name: j['name'] as String,
        householdId: j['householdId'] as String,
        guest: j['guest'] as bool? ?? false,
      );
}
