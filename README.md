# thyrowise.github.io — site

Statik, JS'siz, bağımlılıksız. LLM tarayıcılarının çoğu JavaScript çalıştırmıyor;
sunucuda üretilmeyen sayfa görünmeyen sayfadır. Bu yüzden her şey düz HTML.

Şu anki adres **`https://thyrowise.github.io`** — bedava. Kendi alan adına
geçmek tek komut, aşağıda.

## Dosyalar

```
index.html                          ana sayfa (MobileApplication + Organization + WebSite schema)
best-thyroid-tracker-apps/          "en iyi tiroid uygulaması" sorgusunun karşılığı
levothyroxine-coffee-timing/        en yüksek niyetli sorgu — levotiroksin/kahve penceresi
what-is-a-normal-tsh/               TSH referans aralıkları
hashimotos-symptom-tracking/        semptom takibi
faq/                                uygulama hakkında sorular (FAQPage schema)
support/                            iletişim + her tıbbi iddianın kaynağı
style.css                           palet Shared/Theme.swift ile birebir aynı
robots.txt                          AI tarayıcılarına açık izin
llms.txt                            asistanlar için yapılandırılmış indeks
llms-full.txt   (üretilen)          tüm site tek düz metin dosyada
sitemap.xml     (üretilen)
build.py                            sitemap.xml + llms-full.txt üretir
set-url.py                          sitenin adresini tek komutla değiştirir
.nojekyll                           GitHub Pages'in Jekyll'e sokmasını engeller
```

Bir sayfayı değiştirdikten sonra `python3 build.py`.

Yerelde bakmak için (mutlak `/style.css` yolu yüzünden `file://` çalışmaz):

```
python3 -m http.server 8731
```

## Yayına alma — ücretsiz yol

Bunların hepsi bedava ve bir akşamda biter.

1. **GitHub'da `thyrowise` adında bir organization açın.** (Ücretsiz. İkinci bir
   kişisel hesap açmayın — GitHub bunu hoş karşılamıyor, organization ise
   normal.) 10 Eylül 2026 itibarıyla `github.com/thyrowise` boştu; kapılmadan
   alın, asıl değerli olan şey isim.

2. **İçinde `thyrowise.github.io` adında public bir repo açın**, bu klasörün
   içindekileri köküne koyun, Settings → Pages'ten `main` dalını yayınlayın.
   Adres: `https://thyrowise.github.io`.

   Klasör değil kök olması şart: `robots.txt`, `llms.txt` ve `sitemap.xml`
   sadece alan adının kökünde çalışır. Eski adresteki asıl sorun da buydu.

3. **privacy ve terms sayfalarını da buraya taşıyın.** Şu an footer'daki iki
   bağlantı hâlâ `mjkfxjbx9h-ux.github.io` adresine gidiyor — bilerek, site bugün
   de kırık bağlantısız yayınlanabilsin diye. Taşıdıktan sonra bu iki bağlantıyı
   `/privacy/` ve `/terms/` yapın (`llms.txt` içinde de var).

4. **Eski sayfaları yönlendirin.** GitHub Pages gerçek 301 vermiyor; eski
   sayfaların `<head>`'ine:
   ```html
   <link rel="canonical" href="https://thyrowise.github.io/KARŞILIĞI/">
   <meta http-equiv="refresh" content="0; url=https://thyrowise.github.io/KARŞILIĞI/">
   ```

5. **Search Console + Bing Webmaster Tools.** İkisi de ücretsiz, ikisine de
   ekleyin, sitemap'i verin. Bing önemli: ChatGPT'nin arama katmanı orayı
   kullanıyor.

6. **App Store Connect URL'leri.** Privacy Policy URL App Information'dan her an
   değişir. Support ve Marketing URL sürüm sayfasında — bir sonraki sürüm
   gönderiminde. `appstore/asc_push_metadata.py` içindeki adresler de değişmeli.

## Sonradan kendi alan adına geçmek

```
python3 set-url.py https://thyrowise.com
```

Sonra repoya bir `CNAME` dosyası ekleyip Settings → Pages'ten alan adını
tanıtmak yeterli.

**Bedava başlamak çıkmaz sokak değil**, ama bir uyarı: GitHub'ın
`thyrowise.github.io` adresinden yeni alan adınıza otomatik 301 verdiği pratikte
gözlenen bir davranış — GitHub'ın dokümanında açıkça yazmıyor, kontrol ettim.
Yani birikmiş bağlantı değerinin bir kısmını kaybetme ihtimali var. Buna karşılık
asıl varlığınız bağlantı değeri değil, **anılma**: Reddit yorumları, dizin
kayıtları, derleme yazıları. Onların hepsi güncellenebilir.

## Ücretli alan adı ne satın alır

Yılda ~12 dolar şunları alır, fazlasını değil:

- **Güvenilirlik.** Sağlık uygulaması için `thyrowise.github.io` biraz amatör
  durur; bazı derleme yazarları ve dizinler github.io adreslerini ciddiye almaz.
- **`support@thyrowise.com`.** github.io ile e-posta kuramazsınız.
- **Kalıcılık.** Adres sizin; platform değiştirirseniz bağlantılar ölmez.

Bunlar önemsiz değil ama hiçbiri *bugün* engel değil. Önce yayına alın.

## Bakım

`best-thyroid-tracker-apps/` sayfasındaki rakip listesi **Eylül 2026**'da
kontrol edildi ve sayfada öyle yazıyor. Altı ayda bir bakın; yanlış rakip bilgisi
o sayfanın tek gerçek riski.

Tıbbi iddialar `Shared/MedicalSources.swift` ile aynı cümleler. Uygulamada bir
iddia değişirse burada da değişmeli — iki yerde farklı şey yazması, App Review'un
1.4.1 altında bir kez zaten uyardığı konu.
