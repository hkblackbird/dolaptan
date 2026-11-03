/// Internetsiz çalışan küçük Türk mutfağı kataloğu.
/// Yapay zeka servisi bağlanana kadar öneriler buradan gelir.
class CatalogRecipe {
  final String id;
  final String title;
  final int minutes;
  final List<String> ingredients;
  final List<String> allergens;
  final List<String> steps;
  final String? image;
  const CatalogRecipe(this.id, this.title, this.minutes, this.ingredients, this.allergens, this.steps, [this.image]);
}

/// Her evde olduğu varsayılan, eksik sayılmayan malzemeler.
const staples = {'tuz', 'karabiber', 'pul biber', 'sıvı yağ', 'zeytinyağı', 'su', 'şeker', 'nane'};

const catalog = <CatalogRecipe>[
  CatalogRecipe('menemen', 'Menemen', 15, ['Domates', 'Yumurta', 'Biber', 'Soğan'], ['Yumurta'], [
    'Soğanı ve biberi doğrayıp tavada yağla 3 dk kavur.',
    'Rendelenmiş domatesi ekle, suyunu çekene kadar pişir.',
    'Yumurtaları kır, hafifçe karıştırıp 2 dk pişir.',
  ], 'assets/img/yemek/menemen'),
  CatalogRecipe('omlet', 'Patatesli Omlet', 20, ['Patates', 'Yumurta', 'Soğan', 'Peynir', 'Tereyağı'],
      ['Yumurta', 'Süt'], [
    'Patatesleri küp küp doğra.',
    'Tereyağında kızarana dek kavur.',
    'Soğanı ekleyip karıştır.',
    'Yumurtaları çırpıp dök.',
    'Peyniri ekle, 5 dk pişir.',
  ], 'assets/img/yemek/omlet'),
  CatalogRecipe('cacik', 'Cacık', 10, ['Yoğurt', 'Salatalık', 'Sarımsak'], ['Süt'], [
    'Salatalığı rendele ya da küçük doğra.',
    'Yoğurdu biraz su ve ezilmiş sarımsakla aç.',
    'Salatalığı ekle, nane ve zeytinyağıyla servis et.',
  ], 'assets/img/yemek/cacik'),
  CatalogRecipe('mercimek', 'Mercimek Çorbası', 30, ['Kırmızı mercimek', 'Soğan', 'Havuç', 'Tereyağı'], ['Süt'], [
    'Soğanı ve havucu tereyağında 5 dk kavur.',
    'Yıkanmış mercimeği ve 6 su bardağı sıcak su ekle.',
    'Kısık ateşte 20 dk pişir.',
    'Blenderdan geçir, pul biberli yağla servis et.',
  ], 'assets/img/yemek/mercimek'),
  CatalogRecipe('fasulye', 'Zeytinyağlı Fasulye', 40, ['Taze fasulye', 'Domates', 'Soğan'], [], [
    'Soğanı zeytinyağında pembeleşene kadar kavur.',
    'Ayıklanmış fasulyeyi ekle, 5 dk çevir.',
    'Doğranmış domatesi ve yarım bardak su ekle.',
    'Kapağı kapalı, kısık ateşte 30 dk pişir.',
  ], 'assets/img/yemek/fasulye'),
  CatalogRecipe('coban', 'Çoban Salata', 10, ['Domates', 'Salatalık', 'Biber', 'Soğan', 'Maydanoz'], [], [
    'Domatesi, salatalığı ve biberi küçük doğra.',
    'Soğanı ince doğrayıp tuzla ov.',
    'Maydanozu ekle, zeytinyağı ve limonla karıştır.',
  ]),
  CatalogRecipe('cilbir', 'Çılbır', 15, ['Yumurta', 'Yoğurt', 'Sarımsak', 'Tereyağı'], ['Yumurta', 'Süt'], [
    'Yoğurdu ezilmiş sarımsakla karıştır.',
    'Yumurtaları sirkeli kaynar suda 3 dk haşla.',
    'Yumurtaları yoğurdun üstüne al.',
    'Tereyağında pul biber kızdırıp gezdir.',
  ]),
  CatalogRecipe('yogurtlu-patates', 'Yoğurtlu Patates', 30, ['Patates', 'Yoğurt', 'Sarımsak'], ['Süt'], [
    'Patatesleri küp doğrayıp fırında 20 dk kızart.',
    'Yoğurdu sarımsakla karıştır.',
    'Patateslerin üstüne yoğurt dök, pul biberli yağ gezdir.',
  ]),
  CatalogRecipe('patates-salatasi', 'Patates Salatası', 25, ['Patates', 'Soğan', 'Maydanoz', 'Limon'], [], [
    'Patatesleri haşla, 20 dk.',
    'Soyup küp doğra.',
    'Soğan, maydanoz, limon ve zeytinyağıyla karıştır.',
  ]),
  CatalogRecipe('tost', 'Peynirli Tost', 10, ['Ekmek', 'Peynir', 'Tereyağı'], ['Gluten', 'Süt'], [
    'Ekmeğin arasına peynir koy.',
    'Dışına ince tereyağı sür.',
    'Tavada iki yüzü kızarana dek 5 dk pişir.',
  ]),
  CatalogRecipe('domates-corbasi', 'Domates Çorbası', 25, ['Domates', 'Tereyağı', 'Un', 'Süt'], ['Gluten', 'Süt'], [
    'Tereyağında unu 2 dk kavur.',
    'Rendelenmiş domatesi ekle, 5 dk pişir.',
    'Su ekle, 15 dk kaynat.',
    'Sütü ekleyip bir taşım kaynat.',
  ]),
  CatalogRecipe('sut-ekmek', 'Sütlü Ekmek Tatlısı', 20, ['Ekmek', 'Süt', 'Yumurta'], ['Gluten', 'Süt', 'Yumurta'], [
    'Bayat ekmekleri dilimle.',
    'Süt, yumurta ve şekeri çırp.',
    'Ekmekleri karışıma bulayıp tavada kızart, 10 dk.',
  ]),
];
