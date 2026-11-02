# Figma Rehberi: Dolaptan

Dolaptan, birlikte yaşayanlar için ortak bir mutfak uygulaması. Uygulamada üç ortak parça var:

- **Dolap:** Evdeki herkesin gördüğü ortak dolap.
- **Tarifler:** Önce bozulacak malzemeleri kullanan tarif önerileri.
- **Liste:** Ortak alışveriş listesi.

Bu rehber, SVG ekranları Figma'ya aktarmayı, iOS 26 kitiyle tamamlamayı ve tıklanabilir prototipi kurmayı anlatır.

## Dosyalar

Üç klasör var. Her birinde aynı 20 ekran bulunuyor ve hepsi 360x800 boyutunda.

| Klasör | İçerik |
|---|---|
| `wireframes/` | Gri tonlu iskelet ekranlar |
| `mockups/` | Açık mod tasarım |
| `mockups-dark/` | Karanlık mod tasarım |

Ekranlar şu gruplara ayrılır:

- **Ana ekranlar:** Giriş, Dolap, Tarama, Yeni Malzemeler, Tercihler, Tarif önerileri, Tarif detayı, Tarifler, Alışveriş listesi, Çevrimdışı.
- **Ek durumlar:** bozulma bildirimi (`02b`), malzeme düzenleme sheet'i (`02c`), "Pişirdim" onayı (`07b`).
- **Animasyon ara durumları:** `03b` ve `03c`.
- **Boş, hata ve yükleniyor durumları:** `04b`, `06b`, `06c`, `08b`, `09b`.

## Hızlı yol: eklentiyle otomatik kurulum

`figma-eklentisi/` klasöründeki eklenti 2. ve 8. bölümlerdeki işleri senin yerine yapar:

- Sayfaları oluşturur.
- 60 ekranı yerleştirir.
- Prototip bağlantılarını ve akış başlangıçlarını ekler.

Eklenti yalnızca Figma masaüstü uygulamasında çalışır.

1. Figma masaüstü uygulamasını aç ve hesabınla giriş yap.
2. Yeni bir Design dosyası aç ve adını `Dolaptan` yap.
3. Sol üstteki Figma menüsünden **Plugins → Development → Import plugin from manifest…** seç.
4. `mtm4681-dolaptan/design/figma-eklentisi/manifest.json` dosyasını seç. Dosyayı göremezsen pencerede **Cmd + Shift + G** tuşlarına basıp bu yolu yapıştır:

   ```
   /Users/hatice/mtm4681-dolaptan/design/figma-eklentisi/manifest.json
   ```

   Eklentiyi daha önce içe aktardıysan bu adımı atla. Eklenti, dosyalar güncellenince yeni ekranları kendiliğinden kullanır.
5. Menüden **Plugins → Development → Dolaptan ekranları** ile eklentiyi çalıştır.
6. Altta bir özet görünür, örneğin: `60 ekran, 54 bağlantı, akışlar eklendi`.
   - "Bulunamayan katmanlar" yazarsa, o bağlantıları 8. bölümdeki tablodan elle ekle.
   - "Akışları elle ekle" yazarsa, 6. bölümdeki başlangıç noktalarını elle ekle.
7. Present ile prototipi dene.

Eklentiyi Figma'nın kendisinde çalıştıramadım; yalnızca taklit bir ortamda test ettim. Manifest'teki kimlik yüzünden içe aktarma hata verirse:

1. **Plugins → Development → New plugin…** ile boş bir eklenti oluştur.
2. Figma'nın verdiği `id` değerini `manifest.json` dosyasındaki `id` alanına yapıştır.
3. İçe aktarmayı tekrar dene.

Önceki sürümden kalan bir Figma dosyan varsa, eklentiyi yeni ve boş bir dosyada çalıştır. Böylece eski ve yeni ekranlar karışmaz.

Eklentiden sonra 3, 4 ve 10. bölümlere devam et: kit bileşenleri, fotoğraflar ve linkler.

## 1. Dosyayı hazırla

1. Figma'da yeni bir Design dosyası aç ve adını `Dolaptan` yap.
2. Üç sayfa oluştur: `Wireframes`, `Mockups`, `Mockups Koyu`. Eklentiyi kullanıyorsan bu sayfaları eklenti açar.
3. Maildeki **iOS and iPadOS 26** kitini aç ve **Duplicate** ile kendi hesabına kopyala.
   - Bilinen topluluk adresi: `figma.com/community/file/1527721578857867021`
   - Apple'ın kaynak sayfası artık iOS 27 kitini gösteriyor. Maildeki 26 kitini kullan.
4. Kitin kütüphanesini `Dolaptan` dosyasına ekle: **Assets → Libraries → kit → Add to file**.

## 2. SVG'leri aktar (eklenti kullanmıyorsan)

1. Her klasördeki 20 dosyayı kendi sayfasına sürükle: `wireframes/` → `Wireframes`, `mockups/` → `Mockups`, `mockups-dark/` → `Mockups Koyu`.
2. Her dosya, dosya adını taşıyan 360x800 boyutunda bir çerçeve (frame) olarak gelir.
3. Çerçeveleri dosya adı sırasıyla diz ve hizalama menüsünden **Tidy up** ile aralarını eşitle.

**Kontrol et:**

- Metinler Inter fontuyla görünmeli. Türkçe harfler (ç, ğ, ı, İ, ö, ş, ü) doğru olmalı.
- SF Pro yüklüyse **Edit → Replace fonts** ile Inter'i SF Pro ile değiştirebilirsin.
- SF Pro'nun lisansı onu yalnızca Apple platformlarına ait tasarımlarla sınırlar. Uygulamanın Android sürümünde Inter kalacak.

## 3. Kit bileşenleriyle değiştir

SVG'lerdeki sistem parçaları kitin gerçek bileşenleriyle değiştirilince Liquid Glass görünümü ve doğru ölçüler gelir. Bunu `Mockups` ve `Mockups Koyu` sayfalarında yap.

Kitin iç adlarını Figma'da açarak doğrulayamadım. Aşağıdaki adlar Apple'ın kılavuzundaki bileşen adlarıdır. **Assets** panelinde bu kelimeleri ara; kitte adı biraz farklı olabilir.

Bir bileşeni değiştirmek için:

1. SVG'deki katmanı seç ve konumunu not et.
2. Kitteki bileşeni aynı yere koy.
3. Eski katmanı sil.
4. Bileşenin **Appearance** özelliğini sayfaya göre `Light` veya `Dark` yap.

### Tüm ekranlarda ortak

| SVG katmanı | Kit bileşeni |
|---|---|
| `durum-cubugu` | Status Bar |
| `ana-ekran-cubugu` | Home Indicator |
| `geri`, `btn-kapat` ve diğer yuvarlak bar düğmeleri | Navigation Bar (Liquid Glass bar düğmeleri) |
| `sekme-cubugu` ve `sekme-*` | Tab Bar, 3 sekme: Dolap, Tarifler, Liste |

### Ekran ekran

| Ekran | Kit bileşenleri |
|---|---|
| 01-giris | Navigation Bar (büyük başlık), Lists (metin alanı satırları), Buttons (prominent ve plain) |
| 02-dolap | Navigation Bar (büyük başlık, sağda iki bar düğmesi), Lists (değer gösteren satırlar), Buttons (prominent), Tab Bar |
| 02b-bozulma-bildirimi | 02 ile aynı, üstte Notification (bildirim kutusu) |
| 02c-malzeme-duzenle | Sheet, Navigation Bar (Close ve prominent düğme), Segmented Controls, Lists, Date Picker (compact), Toggles |
| 03-tarama | Kamera ekranı tam ekran açılır; yalnızca Buttons (glass, daire) kullanılır |
| 03b, 03c | Progress Indicators (activity indicator), Buttons (glass, kapsül) |
| 04-yeni-malzemeler | Navigation Bar, Lists (alt yazılı satır, değer, swipe action), Buttons (prominent) |
| 04b-malzeme-yok | Navigation Bar, Content Unavailable, Buttons |
| 05-tercihler | Sheet, Navigation Bar (sheet içinde), Segmented Controls, Lists, Toggles |
| 06-tarif-onerileri | Navigation Bar, Lists (görselli satır, disclosure indicator), Buttons (plain) |
| 06b-tarifler-yukleniyor | Navigation Bar, Progress Indicators |
| 06c-tarif-hatasi | Navigation Bar, Content Unavailable, Buttons (plain) |
| 07-tarif-detay | Navigation Bar (fotoğraf üzerinde glass düğmeler), Lists, Buttons (prominent) |
| 07b-pisirdim | Alert (iki düğmeli) |
| 08-tarifler | Navigation Bar, Search Fields, Lists (görselli satır), Tab Bar |
| 08b-tarifler-bos | Navigation Bar, Content Unavailable, Tab Bar |
| 09-alisveris-listesi | Navigation Bar, Lists (onay dairesi satırları, değer gösteren satır), Tab Bar |
| 09b-liste-bos | Navigation Bar, Content Unavailable, Buttons (plain), Tab Bar |
| 10-cevrimdisi | 02 ile aynı, üstte bilgi satırı |

**Dikkat:**

- Kitin iPhone çerçeveleri 360x800 değil, daha büyük olabilir. Biz dersin istediği 360x800 boyutunu koruduk. Bileşenler genişliğe göre esner; ekleyince sağ ve sol kenarlarını çerçeveye sabitle.
- Tab Bar'ı kitten koyunca etiketleri `Dolap`, `Tarifler`, `Liste` yap ve seçili sekmeyi ekrana göre ayarla.

## 4. Fotoğraf alanları

Yemek fotoğrafları için boş alanlar bırakıldı. İçlerine görsel koymadım, çünkü uydurma veya yapay görsel kullanmıyoruz.

| Katman | Oran | Nerede |
|---|---|---|
| `foto-alani-16x9` | 16:9 | 07-tarif-detay, en üst |
| `foto-alani-1x1` | 1:1 | 06 ve 08'deki tarif satırları |

Kendi çektiğiniz gerçek bir fotoğraf varsa:

1. Alanı seç.
2. **Fill → Image** ile fotoğrafı yükle ve **Fill** modunu seç.

Fotoğraf yoksa alanı olduğu gibi bırak. Uygulamada fotoğrafı olmayan tarifte bu alan gizlenir.

## 5. İkonlar (SF Symbols)

SVG'deki her ikon `sf-<ad>` adlı bir katmandır. Ad, SF Symbols'taki adla aynıdır. Kit veya SF Symbols uygulaması yüklüyse ikonu aynı adlı sembolle değiştirebilirsin. Flutter kodunda bu ikonların `cupertino_icons` karşılıkları kullanılacak.

| SF Symbols adı | Ekran | Anlamı |
|---|---|---|
| `refrigerator.fill` | Sekme çubuğu, 02b | Dolap |
| `book.fill` | Sekme çubuğu | Tarifler |
| `list.bullet` | Sekme çubuğu | Liste |
| `chevron.backward` | Geri düğmesi | Geri |
| `chevron.forward` | Tarif satırları | Detaya git |
| `camera` | 02, 10 | Dolaba fotoğrafla ekle |
| `rectangle.portrait.and.arrow.right` | 02, 10 | Çıkış |
| `xmark` | 02c, 03, 05 | Kapat |
| `photo.on.rectangle` | 03 | Galeriden seç |
| `questionmark.circle` | 04 | Emin olunmayan malzeme |
| `plus` | 02, 09 | Ekle |
| `magnifyingglass` | 04b, 08 | Bulunamadı, Ara |
| `exclamationmark.triangle` | 06c | Hata |
| `bookmark` | 07 | Kaydet |
| `book` | 08b | Kayıtlı tarif yok |
| `square.and.arrow.up` | 09, 09b | Davet kodunu paylaş |
| `cart` | 09b | Boş liste |
| `wifi.slash` | 10 | İnternet yok |

`refrigerator.fill` adını SF Symbols uygulamasında doğrulayamadım. Uygulamada bulamazsan dolabı en iyi anlatan sembolü seç.

Onay daireleri 09'da elle çizildi; kitteki liste satırının onay öğesiyle değiştirebilirsin.

## 6. Prototip ayarları

Prototipi `Mockups` sayfasında kur, çünkü bir prototip tek sayfa içinde çalışır.

1. Sağ panelde **Prototype** sekmesine geç.
2. Tuvalde boş bir yere tıkla. **Device** için `Custom size` seçip 360x800 yaz.
3. Şu çerçevelere **Flow starting point** ekle:

| Başlangıç | Çerçeve | Ne gösterir |
|---|---|---|
| `Ana akış` | 01-giris | Giriş, dolap, tarama, tarif ve "Pişirdim" döngüsü |
| `Bozulma bildirimi` | 02b-bozulma-bildirimi | Bildirimden tarife geçiş |
| `Çevrimdışı` | 10-cevrimdisi | İnternet yokken dolap |
| `Boş ve hata durumları` | 04b-malzeme-yok | Boş ve hata ekranları |

## 7. Geçişler

iOS'taki temel geçişleri kullan. Tabloda aksi yazmadıkça tetikleyici **On tap**.

| Ad | iOS'taki karşılığı | Figma ayarı |
|---|---|---|
| Push | Listeden detaya geçiş | Animation: **Push**, yön sola (`←`), Ease In and Out, 350 ms |
| Sheet | Alttan açılan sayfa | Animation: **Move in**, yön yukarı (`↑`), Ease Out, 350 ms |
| Tam ekran | Kameranın açılması | Animation: **Move in**, yön yukarı (`↑`), Ease Out, 350 ms |
| Fade | Durum değişimi, uyarı | Animation: **Dissolve**, Ease Out, 200 ms |
| Sekme | Sekmeler arası geçiş | **Instant** |
| Geri | Geri, Kapat, sheet'i kapatma | Action: **Back** (Figma gelinen geçişi tersine oynatır) |
| Tarif | Başlığın detay ekranına kayması | **Smart Animate**, Ease In and Out, 350 ms |

## 8. Bağlantılar

### 01-giris

| Katman | Hedef | Geçiş |
|---|---|---|
| `btn-giris` | 02-dolap | Fade |
| `btn-hesap-olustur` | 02-dolap | Fade |

### 02-dolap

| Katman | Hedef | Geçiş |
|---|---|---|
| `btn-tara` | 03-tarama | Tam ekran |
| `btn-malzeme-yaz` | 04-yeni-malzemeler | Push |
| `satir-yogurt` | 02c-malzeme-duzenle | Sheet |
| `btn-ne-pisirsem` | 05-tercihler | Sheet |
| `btn-cikis` | 01-giris | Fade |
| `sekme-tarifler` | 08-tarifler | Sekme |
| `sekme-liste` | 09-alisveris-listesi | Sekme |

### 02b-bozulma-bildirimi

| Katman | Hedef | Geçiş |
|---|---|---|
| `bildirim` | 05-tercihler | Sheet |
| `sekme-tarifler` | 08-tarifler | Sekme |
| `sekme-liste` | 09-alisveris-listesi | Sekme |

### 02c-malzeme-duzenle

| Katman | Hedef | Geçiş |
|---|---|---|
| `btn-kaydet` | Önceki ekran | Geri |
| `btn-kapat` | Önceki ekran | Geri |
| `btn-dolaptan-cikar` | Önceki ekran | Geri |

### 03-tarama

| Katman | Hedef | Geçiş |
|---|---|---|
| `btn-deklansor` | 03b-tarama-analiz-1 | Fade |
| `btn-galeri` | 03b-tarama-analiz-1 | Fade |
| `btn-kapat` | Önceki ekran | Geri |

### 03b-tarama-analiz-1

| Katman | Tetikleyici | Hedef | Geçiş |
|---|---|---|---|
| Çerçevenin kendisi | After delay, 1 ms | 03c-tarama-analiz-2 | Smart Animate, Linear, 1400 ms |
| `btn-iptal` | On tap | 03-tarama | Fade |

Beyaz `tarama-cizgisi` katmanı iki çerçevede aynı adı taşıdığı için Figma onu yukarıdan aşağı kaydırır.

### 03c-tarama-analiz-2

| Katman | Tetikleyici | Hedef | Geçiş |
|---|---|---|---|
| Çerçevenin kendisi | After delay, 300 ms | 04-yeni-malzemeler | Fade |
| `btn-iptal` | On tap | 03-tarama | Fade |

### 04-yeni-malzemeler

| Katman | Hedef | Geçiş |
|---|---|---|
| `btn-dolaba-ekle` | 02-dolap | Fade |
| `geri` | Önceki ekran | Geri |

Kaydırarak silme, `Domates` satırında açık hâlde gösteriliyor. Figma'da kaydırma hareketi eklemek gerekmiyor.

### 04b-malzeme-yok

| Katman | Hedef | Geçiş |
|---|---|---|
| `btn-malzeme-ekle` | 04-yeni-malzemeler | Fade |
| `btn-yeniden-cek` | 03-tarama | Tam ekran |
| `geri` | Önceki ekran | Geri |

### 05-tercihler

| Katman | Hedef | Geçiş |
|---|---|---|
| `btn-tarif-oner` | 06b-tarifler-yukleniyor | Fade |
| `btn-kapat` | Önceki ekran | Geri |

### 06b-tarifler-yukleniyor

| Katman | Tetikleyici | Hedef | Geçiş |
|---|---|---|---|
| Çerçevenin kendisi | After delay, 1500 ms | 06-tarif-onerileri | Fade |

### 06-tarif-onerileri

| Katman | Hedef | Geçiş |
|---|---|---|
| `satir-omlet` | 07-tarif-detay | Tarif |
| `btn-baska-tarif` | 06b-tarifler-yukleniyor | Fade |
| `geri` | Önceki ekran | Geri |

Detay ekranı Patatesli Omlet'i gösterdiği için yalnızca bu satır bağlanır. `tarif-baslik` katmanı iki ekranda da aynı adı taşır, bu yüzden başlık satırdan detay ekranına kayar.

### 06c-tarif-hatasi

| Katman | Hedef | Geçiş |
|---|---|---|
| `btn-tekrar-dene` | 06b-tarifler-yukleniyor | Fade |
| `geri` | Önceki ekran | Geri |

### 07-tarif-detay

| Katman | Hedef | Geçiş |
|---|---|---|
| `btn-pisirdim` | 07b-pisirdim | Fade |
| `btn-listeye-ekle` | 09-alisveris-listesi | Push |
| `btn-kaydet` | 08-tarifler | Push |
| `geri` | Önceki ekran | Geri |

### 07b-pisirdim

| Katman | Hedef | Geçiş |
|---|---|---|
| `btn-tamam` | 02-dolap | Fade |
| `btn-vazgec` | Önceki ekran | Geri |

### 08-tarifler

| Katman | Hedef | Geçiş |
|---|---|---|
| `satir-omlet` | 07-tarif-detay | Push |
| `sekme-dolap` | 02-dolap | Sekme |
| `sekme-liste` | 09-alisveris-listesi | Sekme |

### 08b-tarifler-bos

| Katman | Hedef | Geçiş |
|---|---|---|
| `sekme-dolap` | 02-dolap | Sekme |
| `sekme-liste` | 09-alisveris-listesi | Sekme |

### 09-alisveris-listesi

| Katman | Hedef | Geçiş |
|---|---|---|
| `sekme-dolap` | 02-dolap | Sekme |
| `sekme-tarifler` | 08-tarifler | Sekme |

### 09b-liste-bos

| Katman | Hedef | Geçiş |
|---|---|---|
| `btn-urun-ekle` | 09-alisveris-listesi | Fade |
| `sekme-dolap` | 02-dolap | Sekme |
| `sekme-tarifler` | 08-tarifler | Sekme |

### 10-cevrimdisi

| Katman | Hedef | Geçiş |
|---|---|---|
| `btn-tekrar-dene` | 02-dolap | Fade |
| `sekme-tarifler` | 08-tarifler | Sekme |
| `sekme-liste` | 09-alisveris-listesi | Sekme |

## 9. Katman adları hakkında

Bağlantı noktalarına anlamlı adlar verdim (`btn-…`, `satir-…`, `sekme-…`, `geri`). Bir katmanın adı farklı gelirse:

1. Katmanı görselinden seç ve tablodaki adı ver.
2. Tıklanamayan bir alan olursa üzerine dolgusu %0 olan bir dikdörtgen çiz ve bağlantıyı ondan başlat.

Metin düğmelerinin çevresinde, 44 pt dokunma alanını gösteren görünmez dikdörtgenler var. Bağlantıyı bunlardan başlatmak daha kolaydır.

## 10. Prototipi dene ve linkleri al

1. **Present** ile ana döngüyü izle: Giriş → Dolap → kamera → deklanşör → (animasyon) → Yeni Malzemeler → Dolaba Ekle → Ne Pişirsem? → Tarif Öner → (yükleniyor) → Patatesli Omlet → Pişirdim → Tamam → Dolap.
2. `Bozulma bildirimi` akışında bildirime dokunup tarif ekranına geçişi dene.
3. Alt sekmelerin üç sekme arasında çalıştığını kontrol et.
4. Paylaşım iznini **Anyone with the link: can view** yap.
5. Linkleri al ve kökteki `README.md` dosyasına yapıştır:

| Yer tutucu | Nasıl alınır |
|---|---|
| `[FIGMA WIREFRAME LİNKİ]` | `Wireframes` sayfası açıkken **Share → Copy link** |
| `[FIGMA MOCKUP LİNKİ]` | `Mockups` sayfası açıkken **Share → Copy link** |
| `[FIGMA PROTOTİP LİNKİ]` | Present ekranında **Share prototype → Copy link** |

6. Linkleri gizli pencerede açıp giriş yapmadan göründüğünü kontrol et.
