# İstisnalar Modülü

::: weeb_cli.exceptions
    options:
      show_root_heading: true
      show_source: true
      heading_level: 2

## Genel Bakış

Weeb CLI genelinde yapılandırılmış hata işleme için özel istisna hiyerarşisi. Tüm istisnalar `WeebCLIError` temel sınıfından türetilir.

## İstisna Hiyerarşisi

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

## Kullanım Örnekleri

### İstisna Fırlatma

```python
from weeb_cli.exceptions import ProviderError, DownloadError

# Yalnızca mesajla
raise ProviderError("Anime detayları alınamadı")

# Hata koduyla
raise ProviderError("Arama başarısız", code="PROVIDER_001")

# İndirme hataları
raise DownloadError("Yetersiz disk alanı", code="DISK_FULL")
```

### İstisnaları Yakalama

```python
from weeb_cli.exceptions import (
    ProviderError, 
    NetworkError, 
    WeebCLIError
)

try:
    provider.search("anime")
except ProviderError as e:
    print(f"Sağlayıcı hatası: {e.message} ({e.code})")
except NetworkError as e:
    print(f"Ağ hatası: {e.message}")
except WeebCLIError as e:
    print(f"Genel hata: {e}")
```

### Belirli İstisna İşleme

```python
from weeb_cli.exceptions import (
    AuthenticationError,
    DatabaseError,
    ValidationError
)

# Kimlik doğrulama
try:
    tracker.authenticate()
except AuthenticationError as e:
    print(f"Kimlik doğrulama başarısız: {e.message}")
    # Yeniden kimlik doğrula

# Veritabanı
try:
    db.save_progress()
except DatabaseError as e:
    print(f"Veritabanı hatası: {e.code}")
    # Yeniden dene veya yedekle

# Doğrulama
try:
    validate_input(user_input)
except ValidationError as e:
    print(f"Geçersiz girdi: {e.message}")
    # Tekrar iste
```

## İstisna Türleri

### WeebCLIError

Tüm Weeb CLI hataları için temel istisna. İsteğe bağlı hata kodlarıyla yapılandırılmış hata işleme sağlar.

**Özellikler:**
- `message` (str): İnsan tarafından okunabilir hata mesajı
- `code` (str): Kategorizasyon için isteğe bağlı hata kodu

### ProviderError

Anime sağlayıcı ile ilgili hatalar için fırlatılır:
- Arama başarısızlıkları
- Anime detayları alınamadı
- Bölüm listesi kullanılamıyor
- Yayın çıkarma hataları

### DownloadError

İndirme işlemi başarısızlıkları için fırlatılır:
- İndirme sırasında ağ sorunları
- Yetersiz disk alanı
- Geçersiz yayın URL'leri
- Aria2/yt-dlp hataları

### NetworkError

Ağ bağlantısı sorunları için fırlatılır:
- HTTP istek başarısızlıkları
- Bağlantı zaman aşımları
- DNS çözümleme hataları
- Ağ kullanılamıyor

### AuthenticationError

İzleyici kimlik doğrulama başarısızlıkları için fırlatılır:
- OAuth akış hataları
- Geçersiz kimlik bilgileri
- Token süresi dolması
- API kimlik doğrulama başarısızlıkları

### DatabaseError

Veritabanı işlem hataları için fırlatılır:
- SQLite hataları
- Veritabanı bozulması
- Migrasyon başarısızlıkları
- Sorgu hataları

### ValidationError

Girdi doğrulama başarısızlıkları için fırlatılır:
- Geçersiz yapılandırma değerleri
- Hatalı biçimlendirilmiş kullanıcı girişi
- Geçersiz dosya yolları
- URL doğrulama hataları

### DependencyError

Harici bağımlılık sorunları için fırlatılır:
- Eksik gerekli araçlar (FFmpeg, MPV, Aria2)
- Araç yürütme başarısızlıkları
- Sürüm uyumsuzlukları
- Kurulum hataları

## Hata Kodları

Uygulama genelinde kullanılan yaygın hata kodları:

| Kod | İstisna | Açıklama |
|-----|---------|----------|
| `PROVIDER_001` | ProviderError | Arama başarısız |
| `PROVIDER_002` | ProviderError | Detay alma başarısız |
| `PROVIDER_003` | ProviderError | Yayın çıkarma başarısız |
| `DOWNLOAD_001` | DownloadError | Disk alanı yetersiz |
| `DOWNLOAD_002` | DownloadError | İndirme başarısız |
| `NETWORK_001` | NetworkError | Bağlantı zaman aşımı |
| `AUTH_001` | AuthenticationError | OAuth başarısız |
| `DB_001` | DatabaseError | Sorgu başarısız |
| `VALIDATION_001` | ValidationError | Geçersiz girdi |
| `DEP_001` | DependencyError | Araç eksik |

## En İyi Uygulamalar

1. **Belirli İstisnalar Kullanın**: Genel olanlardan önce belirli istisnaları yakalayın
2. **Hata Kodları Ekleyin**: Günlükleme ve hata ayıklama için hata kodları kullanın
3. **Bağlam Sağlayın**: Hata mesajlarına ilgili bilgileri ekleyin
4. **Zarif İşleyin**: Mümkün olduğunda yedek davranış sağlayın
5. **Hataları Günlükleyin**: Hata ayıklama için tam bağlamla istisnaları günlükleyin

## API Referansı

::: weeb_cli.exceptions.WeebCLIError
::: weeb_cli.exceptions.ProviderError
::: weeb_cli.exceptions.DownloadError
::: weeb_cli.exceptions.NetworkError
::: weeb_cli.exceptions.AuthenticationError
::: weeb_cli.exceptions.DatabaseError
::: weeb_cli.exceptions.ValidationError
::: weeb_cli.exceptions.DependencyError
