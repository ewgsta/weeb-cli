# İzleyici Entegrasyonu

Anime izleme ilerlemenizi AniList, MyAnimeList ve Kitsu ile senkronize edin.

## Desteklenen İzleyiciler

### AniList

- OAuth kimlik doğrulama
- Otomatik ilerleme senkronizasyonu
- Manga ve anime takibi
- Sosyal özellikler

### MyAnimeList

- OAuth kimlik doğrulama
- Kapsamlı veritabanı
- Topluluk özellikleri
- Öneriler

### Kitsu

- E-posta/şifre kimlik doğrulama
- Modern arayüz
- Sosyal özellikler
- İlerleme takibi

## İzleyicileri Kurma

### AniList Kurulumu

1. Ayarlar → İzleyiciler → AniList
2. "Kimlik Doğrula"yı seçin
3. OAuth için tarayıcı açılır
4. Uygulamayı yetkilendirin
5. CLI'ya dönün (otomatik algılar)

### MyAnimeList Kurulumu

1. Ayarlar → İzleyiciler → MyAnimeList
2. "Kimlik Doğrula"yı seçin
3. OAuth için tarayıcı açılır
4. Uygulamayı yetkilendirin
5. CLI'ya dönün

### Kitsu Kurulumu

1. Ayarlar → İzleyiciler → Kitsu
2. E-posta girin
3. Şifre girin
4. Kimlik bilgileri güvenli bir şekilde kaydedilir

## İlerleme Senkronizasyonu

### Otomatik Senkronizasyon

İlerleme otomatik olarak senkronize edilir:
- Anime izlerken (%80 tamamlandığında)
- Bölümleri indirirken
- Yerel kütüphaneyi tararken
- Uygulamayı başlatırken

### Manuel Senkronizasyon

Senkronizasyonu zorla:
1. Ayarlar → İzleyiciler
2. İzleyici seçin
3. "Şimdi Senkronize Et"i seçin

### Çevrimdışı Kuyruk

Çevrimdışıyken:
- Güncellemeler yerel olarak kuyruğa alınır
- Bağlantı geri geldiğinde senkronize edilir
- İlerleme kaybedilmez

## Anime Eşleştirme

### Otomatik Eşleştirme

Weeb CLI otomatik olarak eşleştirir:
- Anime başlığına göre
- Alternatif başlıklara göre
- Yıl ve türe göre

### Eşleştirme Doğruluğu

Eşleştirmeyi iyileştirin:
- Tam başlıkları kullanın
- Aramaya yılı dahil edin
- Mümkün olduğunda İngilizce başlıkları kullanın

### Manuel Eşleştirme

Otomatik eşleştirme başarısız olursa:
1. İzleme Listesi → Anime seçin
2. "İzleyiciye Bağla"yı seçin
3. İzleyici veritabanında arayın
4. Doğru eşleşmeyi seçin

## İzleyicileri Yönetme

### Durumu Görüntüle

İzleyici durumunu kontrol edin:
- Kimlik doğrulama durumu
- Son senkronizasyon zamanı
- Bekleyen güncellemeler
- Senkronizasyon hataları

Erişim: Ayarlar → İzleyiciler → Durum

### Bağlantıyı Kes

İzleyiciyi kaldır:
1. Ayarlar → İzleyiciler
2. İzleyici seçin
3. "Bağlantıyı Kes"i seçin
4. Kaldırmayı onayla

### Yeniden Kimlik Doğrula

Token süresi dolarsa:
1. Ayarlar → İzleyiciler
2. İzleyici seçin
3. "Yeniden Kimlik Doğrula"yı seçin

## İzleyici Özellikleri

### İlerleme Güncellemeleri

Otomatik olarak günceller:
- Mevcut bölüm
- İzleme durumu (izliyor/tamamlandı/bırakıldı)
- Puan (ayarlanmışsa)
- İzleme sayısı

### Durum Yönetimi

Anime durumunu ayarla:
- İzliyor
- Tamamlandı
- Beklemede
- Bırakıldı
- İzlemeyi Planlıyor

### Puanlama

Anime'yi değerlendir:
- 1-10 ölçeği (AniList/Kitsu)
- 1-10 ölçeği (MyAnimeList)
- İzleyicide güncellenir

## Gizlilik

### Paylaşılan Veriler

Sadece şunları paylaşır:
- İzleme ilerlemesi
- Bölüm numaraları
- Tamamlanma durumu
- Puanlar (ayarlanmışsa)

### Paylaşılmayan Veriler

Asla paylaşmaz:
- İndirilen dosyalar
- Akış kaynakları
- Arama geçmişi
- Yerel yollar

## Sorun Giderme

### Kimlik Doğrulama Başarısız

1. İnternet bağlantısını kontrol edin
2. Kimlik bilgilerini doğrulayın
3. Yeniden kimlik doğrulamayı deneyin
4. İzleyici web sitesi durumunu kontrol edin

### İlerleme Senkronize Olmuyor

1. İzleyici bağlantısını kontrol edin
2. Anime'nin eşleştirildiğini doğrulayın
3. Çevrimdışı kuyruğu kontrol edin
4. Manuel senkronizasyon

### Yanlış Anime Eşleşti

1. Mevcut eşleşmenin bağlantısını kesin
2. İzleyicide manuel arama yapın
3. Doğru anime'yi seçin
4. Eşleşmeyi onaylayın

### Senkronizasyon Hataları

Günlükleri kontrol edin:
```bash
~/.weeb-cli/logs/debug.log
```

Hata ayıklama modunu etkinleştirin:
Ayarlar → Yapılandırma → Hata Ayıklama Modu

## Birden Fazla İzleyici

### Birden Fazla Kullanma

Üç izleyiciyi de aynı anda kullanabilirsiniz:
- İlerleme hepsine senkronize edilir
- Bağımsız kimlik doğrulama
- Ayrı çevrimdışı kuyruklar

### Senkronizasyon Önceliği

Çakışma durumunda:
1. En son güncelleme kazanır
2. Manuel güncellemeler otomatik olanları geçersiz kılar
3. Her izleyiciyi ayrı ayrı kontrol edin

## En İyi Uygulamalar

1. Kullandığınız tüm izleyicilerde kimlik doğrulayın
2. Tutarlı anime başlıkları kullanın
3. Senkronizasyon durumunu düzenli olarak kontrol edin
4. Çevrimdışı kuyruğu periyodik olarak temizleyin
5. Sorun devam ederse yeniden kimlik doğrulayın

## Sonraki Adımlar

- [İzleme Listesi Kılavuzu](../cli/commands.md): İzleme geçmişini yönetin
- [Kütüphane Kılavuzu](library.md): Yerel kütüphane senkronizasyonu
- [Yapılandırma](../getting-started/configuration.md): İzleyici ayarları
