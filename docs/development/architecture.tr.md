# Mimari Genel Bakış

Bu belge, Weeb CLI'nin mimarisine ve tasarım kararlarına üst düzey bir genel bakış sağlar.

## Sistem Mimarisi

```
┌─────────────────────────────────────────────────────────┐
│                   CLI Katmanı (Typer)                    │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌─────────┐ │
│  │  Arama   │  │İndirmeler│  │İzleme    │  │ Ayarlar │ │
│  │          │  │          │  │Listesi   │  │         │ │
│  └──────────┘  └──────────┘  └──────────┘  └─────────┘ │
└─────────────────────────────────────────────────────────┘
                          │
┌─────────────────────────────────────────────────────────┐
│                    Servis Katmanı                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌─────────┐ │
│  │ İndirici │  │ İzleyici │  │ Oynatıcı │  │Önbellek │ │
│  └──────────┘  └──────────┘  └──────────┘  └─────────┘ │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐              │
│  │Veritabanı│  │ Scraper  │  │Günlükçü  │              │
│  └──────────┘  └──────────┘  └──────────┘              │
└─────────────────────────────────────────────────────────┘
                          │
┌─────────────────────────────────────────────────────────┐
│                  Sağlayıcı Katmanı                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌─────────┐ │
│  │  Türkçe  │  │ İngilizce│  │ Almanca  │  │  Lehçe  │ │
│  │Sağlayıcı │  │Sağlayıcı │  │Sağlayıcı │  │Sağlayıcı│ │
│  └──────────┘  └──────────┘  └──────────┘  └─────────┘ │
└─────────────────────────────────────────────────────────┘
                          │
┌─────────────────────────────────────────────────────────┐
│                     Veri Katmanı                         │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐              │
│  │  SQLite  │  │ Önbellek │  │ Günlük   │              │
│  │Veritabanı│  │Dosyaları │  │Dosyaları │              │
│  └──────────┘  └──────────┘  └──────────┘              │
└─────────────────────────────────────────────────────────┘
```

## Tasarım Desenleri

### 1. Kayıt Deseni (Sağlayıcılar)

Sağlayıcılar dekoratörler kullanılarak otomatik olarak keşfedilir ve kaydedilir:

```python
@register_provider("animecix", lang="tr", region="TR")
class AnimecixProvider(BaseProvider):
    pass
```

**Faydaları:**
- Yeni sağlayıcı eklemek kolay
- Manuel kayıt gerekmez
- Dosya sisteminden otomatik keşif

### 2. Tembel Yükleme (Servisler)

Servisler başlatmayı ertelemek için tembel yükleme kullanır:

```python
@property
def db(self):
    if self._db is None:
        from weeb_cli.services.database import db
        self._db = db
    return self._db
```

**Faydaları:**
- Daha hızlı başlangıç süresi
- Azaltılmış bellek kullanımı
- Döngüsel içe aktarmaları önler

### 3. Tekil Deseni (Global Örnekler)

Paylaşılan kaynaklar için global örnekler:

```python
config = Config()
i18n = I18n()
cache = CacheManager()
```

**Faydaları:**
- Tek doğruluk kaynağı
- Uygulama genelinde kolay erişim
- Tutarlı durum

### 4. Strateji Deseni (İndirme Yöntemleri)

Yedekleme ile birden fazla indirme stratejisi:

```python
def _try_download(self, url, path, item):
    strategies = [
        self._download_aria2,
        self._download_ytdlp,
        self._download_ffmpeg,
        self._download_generic
    ]
    for strategy in strategies:
        if strategy(url, path, item):
            return True
    return False
```

**Faydaları:**
- Zarif bozulma
- Esnek indirme yöntemleri
- Yeni stratejiler eklemek kolay

## Temel Bileşenler

### CLI Katmanı

**Teknoloji:** Typer + Rich + Questionary

**Sorumluluklar:**
- Komut satırı argümanlarını ayrıştır
- Etkileşimli menüleri göster
- Kullanıcı girişini işle
- İlerleme göstergelerini göster

### Servis Katmanı

**Temel Servisler:**

1. **Veritabanı**: WAL modu ile SQLite
   - Yapılandırma depolama
   - İlerleme takibi
   - İndirme kuyruğu
   - Yerel kütüphane dizini

2. **İndirici**: Kuyruk tabanlı indirme yöneticisi
   - Eşzamanlı indirmeler
   - Birden fazla indirme yöntemi
   - Yeniden deneme mantığı
   - İlerleme takibi

3. **İzleyici**: Anime izleme entegrasyonu
   - OAuth kimlik doğrulama
   - İlerleme senkronizasyonu
   - Çevrimdışı kuyruk

4. **Oynatıcı**: MPV entegrasyonu
   - IPC iletişimi
   - İlerleme izleme
   - Devam etme işlevselliği

5. **Önbellek**: İki katmanlı önbellekleme
   - Bellek önbelleği
   - Dosya önbelleği
   - TTL desteği

### Sağlayıcı Katmanı

**Yapı:**
- Dile göre düzenlenmiş dizinler
- Temel sağlayıcı arayüzü
- Kayıt sistemi
- Yayın çıkarıcılar

**Sağlayıcı Yaşam Döngüsü:**
1. Keşif (dosya sistemi taraması)
2. Kayıt (dekoratör)
3. Örnekleme (talep üzerine)
4. Önbellekleme (sonuçlar)

### Veri Katmanı

**Depolama:**
- SQLite veritabanı (~/.weeb-cli/weeb.db)
- Önbellek dosyaları (~/.weeb-cli/cache/)
- Günlük dosyaları (~/.weeb-cli/logs/)
- İndirilen ikili dosyalar (~/.weeb-cli/bin/)

## Veri Akışı

### Arama Akışı

```
Kullanıcı Girişi → CLI → Scraper → Sağlayıcı → Önbellek → API
                                        ↓
                                    Sonuçlar
                                        ↓
                                  CLI Gösterimi
```

### İndirme Akışı

```
Kullanıcı Seçimi → Kuyruk Yöneticisi → İndirme İşçisi
                                            ↓
                                    Stratejileri Dene
                                            ↓
                         ┌─────────────────────────┐
                         │  Aria2 → yt-dlp →       │
                         │  FFmpeg → Genel         │
                         └─────────────────────────┘
                                            ↓
                                    İlerleme Güncelle
                                            ↓
                                    Veritabanına Kaydet
```

### İzleme Akışı

```
Kullanıcı Seçimi → Yayın Çıkarma → Oynatıcı (MPV)
                                        ↓
                                   IPC İzleyici
                                        ↓
                                İlerlemeyi Kaydet
                                        ↓
                                İzleyici Senkronize Et
```

## İş Parçacığı Güvenliği

### Kilitleme Stratejisi

1. **Veritabanı**: Bağlantı yönetimi için RLock
2. **İndirme Kuyruğu**: Kuyruk işlemleri için Lock
3. **Önbellek**: Kilitleme yok (tek iş parçacıklı erişim)

### Eşzamanlı İşlemler

- İndirme işçileri ayrı iş parçacıklarında çalışır
- MPV izleyici daemon iş parçacığında çalışır
- İzleyici senkronizasyonu arka planda çalışır

## Hata İşleme

### İstisna Hiyerarşisi

```
WeebCLIError (temel)
├── ProviderError
├── DownloadError
├── NetworkError
├── AuthenticationError
├── DatabaseError
├── ValidationError
└── DependencyError
```

### Hata Kurtarma

1. **Yeniden Deneme Mantığı**: Geçici hatalar için üstel geri çekilme
2. **Yedekleme**: Birincil başarısız olduğunda alternatif yöntemler
3. **Zarif Bozulma**: Azaltılmış işlevsellikle devam et
4. **Kullanıcı Bildirimi**: i18n ile net hata mesajları

## Performans Optimizasyonları

### 1. Önbellekleme

- Arama sonuçları 1 saat önbelleğe alınır
- Detaylar 6 saat önbelleğe alınır
- Hız için iki katmanlı (bellek + dosya)

### 2. Tembel Yükleme

- Servisler ilk kullanımda yüklenir
- Sağlayıcılar talep üzerine keşfedilir
- Veritabanı bağlantı havuzu

### 3. Eşzamanlı İndirmeler

- Paralel olarak birden fazla indirme
- Yapılandırılabilir eşzamanlılık sınırı
- Kaynak farkında zamanlama

### 4. Veritabanı Optimizasyonu

- Eşzamanlı erişim için WAL modu
- Hazırlanmış ifadeler
- İndekslenmiş sorgular
- Toplu işlemler

## Güvenlik Hususları

### 1. Girdi Temizleme

- Dosya adı temizleme
- URL doğrulama
- SQL enjeksiyonu önleme (parametreli sorgular)

### 2. Kimlik Bilgisi Depolama

- Veritabanında OAuth token'ları
- Düz metin şifre yok
- Güvenli token yenileme

### 3. Ağ Güvenliği

- API çağrıları için HTTPS
- Sertifika doğrulama
- Zaman aşımı sınırları

## Genişletilebilirlik

### Yeni Özellikler Ekleme

1. **Yeni Sağlayıcı**: BaseProvider arayüzünü uygula
2. **Yeni İzleyici**: TrackerBase arayüzünü uygula
3. **Yeni Komut**: Typer komutu ekle
4. **Yeni Servis**: Servis desenini takip et

### Eklenti Sistemi

Şu anda uygulanmamış, ancak mimari destekliyor:
- Sağlayıcı eklentileri
- Çıkarıcı eklentileri
- Komut eklentileri

## Gelecek İyileştirmeler

1. **Eklenti Sistemi**: Dinamik eklenti yükleme
2. **API Sunucusu**: Uzaktan kontrol için REST API
3. **Web Arayüzü**: Tarayıcı tabanlı arayüz
4. **Mobil Uygulama**: Yardımcı mobil uygulama
5. **Bulut Senkronizasyonu**: Cihazlar arası senkronizasyon
