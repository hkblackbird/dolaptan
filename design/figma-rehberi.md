# Figma Rehberi: Dolaptan

Bu rehber, SVG ekranları Figma'ya aktarmayı, iOS 26 kitiyle tamamlamayı ve tıklanabilir prototipi kurmayı anlatır.

## Dosyalar

Üç klasör var. Her birinde aynı 17 ekran bulunuyor ve hepsi 360x800 boyutunda.

| Klasör | İçerik |
|---|---|
| `wireframes/` | Gri tonlu iskelet ekranlar |
| `mockups/` | Açık mod tasarım |
| `mockups-dark/` | Karanlık mod tasarım |

Bu 17 ekranın 10'u uygulamanın ana ekranlarıdır. Diğerleri tarama animasyonu için iki ara durum (`03b`, `03c`) ve beş ek durumdur: boş, hata ve yükleniyor (`04b`, `06b`, `06c`, `08b`, `09b`).

## Hızlı yol: eklentiyle otomatik kurulum

`figma-eklentisi/` klasöründeki eklenti 2. ve 8. bölümlerdeki işleri senin yerine yapar. Sayfaları oluşturur, 51 ekranı yerleştirir, 45 prototip bağlantısını ve akış başlangıçlarını ekler. Eklenti yalnızca Figma masaüstü uygulamasında çalışır.

1. Figma masaüstü uygulamasını aç ve hesabınla giriş yap.
2. Yeni bir Design dosyası aç ve adını `Dolaptan` yap.
3. Sol üstteki Figma menüsünden **Plugins → Development → Import plugin from manifest…** seç.
4. `mtm4681-dolaptan/design/figma-eklentisi/manifest.json` dosyasını seç.
5. Yine menüden **Plugins → Development → Dolaptan ekranları** ile eklentiyi çalıştır.
6. Alt kısımda şu özet görünür: `51 ekran, 45 bağlantı, akışlar eklendi`.
   - "Bulunamayan katmanlar" yazarsa, o bağlantıları 8. bölümdeki tablodan elle ekle.
   - "Akışları elle ekle" yazarsa, 6. bölümdeki başlangıç noktalarını elle ekle.
7. Present ile prototipi dene.

Eklentiyi Figma'nın kendisinde çalıştıramadım; yalnızca taklit bir ortamda test ettim. Manifest'teki kimlik yüzünden içe aktarma hata verirse:

1. **Plugins → Development → New plugin…** ile boş bir eklenti oluştur.
2. Figma'nın verdiği `id` değerini `manifest.json` dosyasındaki `id` alanına yapıştır.
3. İçe aktarmayı tekrar dene.

Eklentiden sonra 3, 4 ve 10. bölümlere devam et: kit bileşenleri, fotoğraflar ve linkler.

## 1. Dosyayı hazırla

1. Figma'da yeni bir Design dosyası aç ve adını `Dolaptan` yap.
2. Üç sayfa oluştur: `Wireframes`, `Mockups`, `Mockups Koyu`.
3. Maildeki **iOS and iPadOS 26** kitini aç ve **Duplicate** ile kendi hesabına kopyala.
   - Bilinen topluluk adresi: `figma.com/community/file/1527721578857867021`
   - Apple'ın kaynak sayfası artık iOS 27 kitini gösteriyor. Maildeki 26 kitini kullan.
4. Kitin kütüphanesini `Dolaptan` dosyasına ekle: **Assets → Libraries → kit → Add to file**.

## 2. SVG'leri aktar

1. Her klasördeki 17 dosyayı kendi sayfasına sürükle: `wireframes/` → `Wireframes`, `mockups/` → `Mockups`, `mockups-dark/` → `Mockups Koyu`.
2. Her dosya, dosya adını taşıyan 360x800 boyutunda bir çerçeve (frame) olarak gelir.
3. Çerçeveleri dosya adı sırasıyla diz. Hepsini seçip hizalama menüsünden **Tidy up** ile aralarını eşitle.

**Kontrol et:**

- Metinler Inter fontuyla görünmeli. Türkçe harfler (ç, ğ, ı, İ, ö, ş, ü) doğru olmalı.
- SF Pro yüklüyse **Edit → Replace fonts** ile Inter'i SF Pro ile değiştirebilirsin. Görünüm Apple'a daha da yaklaşır.
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
| `sekme-cubugu` ve `sekme-*` | Tab Bar, 3 sekme |

### Ekran ekran

| Ekran | Kit bileşenleri |
|---|---|
| 01-giris | Navigation Bar (büyük başlık), Lists (inset grouped, metin alanı satırları), Buttons (prominent ve plain) |
| 02-ana-sayfa | Navigation Bar (büyük başlık ve sağda bar düğmesi), Buttons (prominent ve plain), Lists (görselli satır), Tab Bar |
| 03-tarama | Kamera ekranı tam ekran açılır; yalnızca Buttons (glass, daire) kullanılır |
| 03b, 03c | Progress Indicators (activity indicator), Buttons (glass, kapsül) |
| 04-malzemeler | Navigation Bar, Lists (inset grouped, alt yazılı satır, swipe action), Buttons (prominent) |
| 04b-malzeme-yok | Navigation Bar, Content Unavailable, Buttons |
| 05-tercihler | Sheet (tutamaçlı), Navigation Bar (sheet içinde: Close ve prominent düğme), Segmented Controls, Lists, Toggles |
| 06-tarif-onerileri | Navigation Bar, Lists (görselli ve iki satır alt yazılı satır, disclosure indicator), Buttons (plain) |
| 06b-tarifler-yukleniyor | Navigation Bar, Progress Indicators (activity indicator) |
| 06c-tarif-hatasi | Navigation Bar, Content Unavailable, Buttons (plain) |
| 07-tarif-detay | Navigation Bar (fotoğraf üzerinde glass düğmeler), Lists |
| 08-kayitli | Navigation Bar, Search Fields, Lists (görselli satır), Tab Bar |
| 08b-kayitli-bos | Navigation Bar, Content Unavailable, Tab Bar |
| 09-alisveris-listesi | Navigation Bar, Lists (onay dairesi satırları, değer gösteren satır), Tab Bar |
| 09b-liste-bos | Navigation Bar, Content Unavailable, Buttons (plain), Tab Bar |
| 10-cevrimdisi | Navigation Bar, Content Unavailable (kısa sürüm), Lists, Tab Bar |

**Dikkat:**

- Kitin iPhone çerçeveleri 360x800 değil, daha büyük olabilir. Biz dersin istediği 360x800 boyutunu koruduk. Bileşenler genişliğe göre esner; ekleyince sağ ve sol kenarlarını çerçeveye sabitle.
- Tab Bar'ı kitten koyunca etiketleri `Ana Sayfa`, `Kayıtlı`, `Liste` yap ve seçili sekmeyi ekrana göre ayarla.

## 4. Fotoğraf alanları

Yemek fotoğrafları için boş alanlar bırakıldı. İçlerine görsel koymadım, çünkü uydurma veya yapay görsel kullanmıyoruz.

| Katman | Oran | Nerede |
|---|---|---|
| `foto-alani-16x9` | 16:9 | 07-tarif-detay, en üst |
| `foto-alani-1x1` | 1:1 | 02, 06, 08 ve 10'daki tarif satırları |

Kendi çektiğiniz gerçek bir fotoğraf varsa:

1. Alanı seç.
2. **Fill → Image** ile fotoğrafı yükle ve **Fill** modunu seç.

Fotoğraf yoksa alanı olduğu gibi bırak. Uygulamada fotoğrafı olmayan tarifte bu alan gizlenir.

## 5. İkonlar (SF Symbols)

SVG'deki her ikon `sf-<ad>` adlı bir katmandır. Ad, SF Symbols'taki adla aynıdır. Kit veya SF Symbols uygulaması yüklüyse ikonu aynı adlı sembolle değiştirebilirsin. Flutter kodunda bu ikonların `cupertino_icons` karşılıkları kullanılacak.

| SF Symbols adı | Ekran | Anlamı |
|---|---|---|
| `house.fill` | Sekme çubuğu | Ana Sayfa |
| `bookmark.fill` | Sekme çubuğu | Kayıtlı |
| `list.bullet` | Sekme çubuğu | Liste |
| `chevron.backward` | Geri düğmesi | Geri |
| `chevron.forward` | Tarif satırları | Detaya git |
| `rectangle.portrait.and.arrow.right` | 02, 10 | Çıkış |
| `xmark` | 03, 05 | Kapat |
| `photo.on.rectangle` | 03 | Galeriden seç |
| `questionmark.circle` | 04 | Emin olunmayan malzeme |
| `plus` | 04, 09 | Ekle |
| `magnifyingglass` | 04b, 08 | Bulunamadı, Ara |
| `exclamationmark.triangle` | 06c | Hata |
| `bookmark` | 07, 08b | Kaydet, Kayıtlı yok |
| `square.and.arrow.up` | 09, 09b | Paylaş |
| `cart` | 09b | Boş liste |
| `wifi.slash` | 10 | İnternet yok |

Onay daireleri (`circle`, `checkmark.circle.fill`) 09'da elle çizildi; kitteki liste satırının onay öğesiyle değiştirebilirsin.

## 6. Prototip ayarları

Prototipi `Mockups` sayfasında kur, çünkü bir prototip tek sayfa içinde çalışır.

1. Sağ panelde **Prototype** sekmesine geç.
2. Tuvalde boş bir yere tıkla. **Device** için `Custom size` seçip 360x800 yaz.
3. Şu çerçevelere **Flow starting point** ekle:

| Başlangıç | Çerçeve |
|---|---|
| `Ana akış` | 01-giris |
| `Çevrimdışı` | 10-cevrimdisi |
| `Boş ve hata durumları` | 04b-malzeme-yok |

## 7. Geçişler

iOS'taki üç temel geçişi kullan. Tabloda aksi yazmadıkça tetikleyici **On tap**.

| Ad | iOS'taki karşılığı | Figma ayarı |
|---|---|---|
| Push | Listeden detaya geçiş | Animation: **Push**, yön sola (`←`), Ease In and Out, 350 ms |
| Sheet | Alttan açılan sayfa | Animation: **Move in**, yön yukarı (`↑`), Ease Out, 350 ms |
| Tam ekran | Kameranın açılması | Animation: **Move in**, yön yukarı (`↑`), Ease Out, 350 ms |
| Fade | Durum değişimi | Animation: **Dissolve**, Ease Out, 200 ms |
| Sekme | Sekmeler arası geçiş | **Instant** |
| Geri | Geri, Kapat, sheet'i kapatma | Action: **Back** (Figma gelinen geçişi tersine oynatır) |
| Tarif | Başlığın detay ekranına kayması | **Smart Animate**, Ease In and Out, 350 ms |

## 8. Bağlantılar

### 01-giris

| Katman | Hedef | Geçiş |
|---|---|---|
| `btn-giris` | 02-ana-sayfa | Fade |
| `btn-hesap-olustur` | 02-ana-sayfa | Fade |

### 02-ana-sayfa

| Katman | Hedef | Geçiş |
|---|---|---|
| `btn-fotograf-cek` | 03-tarama | Tam ekran |
| `btn-malzeme-yaz` | 04-malzemeler | Push |
| `satir-omlet` | 07-tarif-detay | Push |
| `btn-cikis` | 01-giris | Fade |
| `sekme-kayitli` | 08-kayitli | Sekme |
| `sekme-liste` | 09-alisveris-listesi | Sekme |

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

Beyaz `tarama-cizgisi` katmanı iki çerçevede aynı adı taşıdığı için Figma onu yukarıdan aşağı kaydırır. Çizgi hareket etmezse adların aynı olduğunu kontrol et.

### 03c-tarama-analiz-2

| Katman | Tetikleyici | Hedef | Geçiş |
|---|---|---|---|
| Çerçevenin kendisi | After delay, 300 ms | 04-malzemeler | Fade |
| `btn-iptal` | On tap | 03-tarama | Fade |

### 04-malzemeler

| Katman | Hedef | Geçiş |
|---|---|---|
| `btn-devam` | 05-tercihler | Sheet |
| `geri` | Önceki ekran | Geri |

Kaydırarak silme, prototipte `Domates` satırında açık hâlde gösteriliyor. Figma'da kaydırma hareketi eklemek gerekmiyor.

### 04b-malzeme-yok

| Katman | Hedef | Geçiş |
|---|---|---|
| `btn-malzeme-ekle` | 04-malzemeler | Fade |
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
| `btn-listeye-ekle` | 09-alisveris-listesi | Push |
| `btn-kaydet` | 08-kayitli | Push |
| `geri` | Önceki ekran | Geri |

### 08-kayitli

| Katman | Hedef | Geçiş |
|---|---|---|
| `satir-omlet` | 07-tarif-detay | Push |
| `sekme-ana-sayfa` | 02-ana-sayfa | Sekme |
| `sekme-liste` | 09-alisveris-listesi | Sekme |

### 08b-kayitli-bos

| Katman | Hedef | Geçiş |
|---|---|---|
| `sekme-ana-sayfa` | 02-ana-sayfa | Sekme |
| `sekme-liste` | 09-alisveris-listesi | Sekme |

### 09-alisveris-listesi

| Katman | Hedef | Geçiş |
|---|---|---|
| `sekme-ana-sayfa` | 02-ana-sayfa | Sekme |
| `sekme-kayitli` | 08-kayitli | Sekme |

### 09b-liste-bos

| Katman | Hedef | Geçiş |
|---|---|---|
| `btn-urun-ekle` | 09-alisveris-listesi | Fade |
| `sekme-ana-sayfa` | 02-ana-sayfa | Sekme |
| `sekme-kayitli` | 08-kayitli | Sekme |

### 10-cevrimdisi

| Katman | Hedef | Geçiş |
|---|---|---|
| `btn-tekrar-dene` | 02-ana-sayfa | Fade |
| `satir-omlet` | 07-tarif-detay | Push |
| `sekme-kayitli` | 08-kayitli | Sekme |
| `sekme-liste` | 09-alisveris-listesi | Sekme |

### Boş ve hata durumlarını gezmek

`Boş ve hata durumları` akışında 04b'den başla. 06c, 08b ve 09b ekranlarını görmek için sol listeden ilgili çerçeveyi seç ya da her birine ayrı bir başlangıç noktası ekle.

## 9. Katman adları hakkında

Bağlantı noktalarına anlamlı adlar verdim (`btn-…`, `satir-…`, `sekme-…`, `geri`). SVG aktarımını Figma'da deneyemedim. Bir katmanın adı farklı gelirse:

1. Katmanı görselinden seç ve tablodaki adı ver.
2. Tıklanamayan bir alan olursa üzerine dolgusu %0 olan bir dikdörtgen çiz ve bağlantıyı ondan başlat.

Metin düğmelerinin çevresinde, 44 pt dokunma alanını gösteren görünmez dikdörtgenler var. Bağlantıyı bunlardan başlatmak daha kolaydır.

## 10. Prototipi dene ve linkleri al

1. **Present** ile şu yolu izle: Giriş → Ana Sayfa → Fotoğraf Çek → deklanşör → (animasyon) → Malzemeler → Devam Et → Tarif Öner → (yükleniyor) → Patatesli Omlet → kaydet.
2. Alt sekmelerin üç sekme arasında çalıştığını kontrol et.
3. Paylaşım iznini **Anyone with the link: can view** yap.
4. Linkleri al ve kökteki `README.md` dosyasına yapıştır:

| Yer tutucu | Nasıl alınır |
|---|---|
| `[FIGMA WIREFRAME LİNKİ]` | `Wireframes` sayfası açıkken **Share → Copy link** |
| `[FIGMA MOCKUP LİNKİ]` | `Mockups` sayfası açıkken **Share → Copy link** |
| `[FIGMA PROTOTİP LİNKİ]` | Present ekranında **Share prototype → Copy link** |

5. Linkleri gizli pencerede açıp giriş yapmadan göründüğünü kontrol et.
