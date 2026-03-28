# Yapılandırma Modülü

::: weeb_cli.config
    options:
      show_root_heading: true
      show_source: true
      heading_level: 2

## Genel Bakış

Yapılandırma modülü, Weeb CLI için merkezi ayar yönetimi sağlar. Tüm yapılandırma, mantıklı varsayılanlara geri dönüşle birlikte bir SQLite veritabanında saklanır.

## Kullanım Örnekleri

### Yapılandırma Değerlerini Alma

```python
from weeb_cli.config import config

# Varsayılan geri dönüşle al
language = config.get("language", "en")
download_dir = config.get("download_dir")
aria2_enabled = config.get("aria2_enabled", True)
```

### Yapılandırma Değerlerini Ayarlama

```python
from weeb_cli.config import config

# Dili ayarla
config.set("language", "tr")

# İndirme dizinini ayarla
config.set("download_dir", "/yol/indirmeler")

# Özellikleri etkinleştir/devre dışı bırak
config.set("discord_rpc_enabled", False)
```

### Headless Modu

Veritabanı erişimi olmadan API kullanımı için:

```python
from weeb_cli.config import config

# Headless modunu etkinleştir
config.set_headless(True)

# Şimdi config.get() yalnızca DEFAULT_CONFIG değerlerini döndürür
language = config.get("language")  # None döndürür (varsayılan)
```

## Varsayılan Yapılandırma

Veritabanı değeri olmadığında aşağıdaki varsayılan değerler kullanılır:

| Anahtar | Varsayılan Değer | Açıklama |
|---------|------------------|----------|
| `language` | `None` | Arayüz dili (tr, en, de, pl) |
| `aria2_enabled` | `True` | İndirmeler için Aria2'yi etkinleştir |
| `ytdlp_enabled` | `True` | İndirmeler için yt-dlp'yi etkinleştir |
| `aria2_max_connections` | `16` | İndirme başına maksimum bağlantı |
| `max_concurrent_downloads` | `3` | Maksimum eşzamanlı indirme |
| `download_dir` | `None` | İndirme dizini yolu |
| `ytdlp_format` | `"bestvideo+bestaudio/best"` | yt-dlp format dizesi |
| `scraping_source` | `None` | Varsayılan sağlayıcı |
| `show_description` | `True` | Anime açıklamalarını göster |
| `debug_mode` | `False` | Hata ayıklama günlüğünü etkinleştir |
| `download_max_retries` | `3` | İndirme yeniden deneme sayısı |
| `download_retry_delay` | `10` | Denemeler arası gecikme (saniye) |
| `discord_rpc_enabled` | `True` | Discord Rich Presence'ı etkinleştir |
| `shortcuts_enabled` | `False` | Klavye kısayollarını etkinleştir |

## Yapılandırma Dizini

Yapılandırma ve veri şurada saklanır:

```
~/.weeb-cli/
├── weeb.db          # SQLite veritabanı
├── cache/           # Önbelleğe alınmış veri
├── bin/             # İndirilen bağımlılıklar
└── logs/            # Hata ayıklama günlükleri
```

## API Referansı

::: weeb_cli.config.Config
    options:
      show_root_heading: false
      members:
        - get
        - set
        - set_headless
