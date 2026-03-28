# Yapılandırma Kılavuzu

Bu kılavuz, Weeb CLI'da mevcut tüm yapılandırma seçeneklerini kapsar.

## Yapılandırma Depolama

Tüm yapılandırma şu konumdaki bir SQLite veritabanında saklanır:

```
~/.weeb-cli/weeb.db
```

Yapılandırma şu yollarla yönetilebilir:
- Etkileşimli ayarlar menüsü
- Doğrudan veritabanı erişimi
- Yapılandırma API'si

## Ayarlara Erişim

### Etkileşimli Mod

```bash
weeb-cli
# Ana menüden "Ayarlar"ı seçin
```

### API Modu

```python
from weeb_cli.config import config

# Değer al
language = config.get("language")

# Değer ayarla
config.set("language", "tr")
```

## Yapılandırma Seçenekleri

### Genel Ayarlar

#### Dil

Arayüz dilini ayarlayın.

- **Anahtar**: `language`
- **Değerler**: `tr`, `en`, `de`, `pl`
- **Varsayılan**: `None` (ilk çalıştırmada sorar)

```python
config.set("language", "tr")
```

#### Hata Ayıklama Modu

Hata ayıklama günlüğünü etkinleştirin.

- **Anahtar**: `debug_mode`
- **Değerler**: `True`, `False`
- **Varsayılan**: `False`

```python
config.set("debug_mode", True)
```

#### Açıklama Göster

Arama sonuçlarında anime açıklamalarını gösterin.

- **Anahtar**: `show_description`
- **Değerler**: `True`, `False`
- **Varsayılan**: `True`

### İndirme Ayarları

#### İndirme Dizini

Anime dosyalarının nereye indirileceğini ayarlayın.

- **Anahtar**: `download_dir`
- **Varsayılan**: `./weeb-downloads`

```python
config.set("download_dir", "/path/to/downloads")
```

#### Aria2 Ayarları

Hızlı çoklu bağlantı indirmeleri için Aria2'yi etkinleştirin.

- **Anahtar**: `aria2_enabled`
- **Değerler**: `True`, `False`
- **Varsayılan**: `True`

```python
config.set("aria2_enabled", True)
```

İndirme başına maksimum bağlantı:

- **Anahtar**: `aria2_max_connections`
- **Değerler**: `1-32`
- **Varsayılan**: `16`

```python
config.set("aria2_max_connections", 16)
```

#### yt-dlp Ayarları

Karmaşık akış indirmeleri için yt-dlp'yi etkinleştirin.

- **Anahtar**: `ytdlp_enabled`
- **Değerler**: `True`, `False`
- **Varsayılan**: `True`

```python
config.set("ytdlp_enabled", True)
```

yt-dlp için format dizesi:

- **Anahtar**: `ytdlp_format`
- **Varsayılan**: `"bestvideo+bestaudio/best"`

```python
config.set("ytdlp_format", "bestvideo+bestaudio/best")
```

#### Eşzamanlı İndirmeler

Maksimum eşzamanlı indirme sayısı.

- **Anahtar**: `max_concurrent_downloads`
- **Değerler**: `1-10`
- **Varsayılan**: `3`

```python
config.set("max_concurrent_downloads", 3)
```

#### Yeniden Deneme Ayarları

Başarısız indirmeler için maksimum yeniden deneme sayısı:

- **Anahtar**: `download_max_retries`
- **Değerler**: `0-10`
- **Varsayılan**: `3`

Yeniden denemeler arasındaki gecikme (saniye):

- **Anahtar**: `download_retry_delay`
- **Değerler**: `1-60`
- **Varsayılan**: `10`

### Sağlayıcı Ayarları

#### Varsayılan Sağlayıcı

Varsayılan anime kaynağını ayarlayın.

- **Anahtar**: `scraping_source`
- **Değerler**: Sağlayıcı adları (örn. `animecix`, `hianime`)
- **Varsayılan**: `None` (dil için ilk kullanılabilir olanı kullanır)

```python
config.set("scraping_source", "animecix")
```

### Entegrasyon Ayarları

#### Discord Rich Presence

Ne izlediğinizi göstermek için Discord entegrasyonunu etkinleştirin.

- **Anahtar**: `discord_rpc_enabled`
- **Değerler**: `True`, `False`
- **Varsayılan**: `True`

```python
config.set("discord_rpc_enabled", True)
```

#### Klavye Kısayolları

Global klavye kısayollarını etkinleştirin (deneysel).

- **Anahtar**: `shortcuts_enabled`
- **Değerler**: `True`, `False`
- **Varsayılan**: `False`

### İzleyici Ayarları

İzleyici kimlik bilgileri veritabanında güvenli bir şekilde saklanır:

- **AniList**: OAuth token
- **MyAnimeList**: OAuth token
- **Kitsu**: E-posta ve şifre (hash'lenmiş)

Ayarlar → İzleyiciler menüsünden yapılandırın.

## Ortam Değişkenleri

### WEEB_CLI_CONFIG_DIR

Yapılandırma dizinini geçersiz kılın:

```bash
export WEEB_CLI_CONFIG_DIR="/custom/path"
weeb-cli
```

### WEEB_CLI_DEBUG

Hata ayıklama modunu etkinleştirin:

```bash
export WEEB_CLI_DEBUG=1
weeb-cli start
```

## Yapılandırma Dosyaları

### Veritabanı Şeması

SQLite veritabanı şu tabloları içerir:

- `config`: Anahtar-değer yapılandırması
- `progress`: İzleme ilerlemesi
- `search_history`: Arama sorguları
- `download_queue`: İndirme kuyruğu
- `external_drives`: Harici sürücü yolları
- `anime_index`: Yerel kütüphane dizini
- `virtual_library`: Çevrimiçi anime yer imleri

### Yedekleme ve Geri Yükleme

#### Yedekleme

```bash
# Ayarlar menüsünden
Ayarlar → Yedekleme & Geri Yükleme → Yedek Oluştur

# Manuel yedekleme
cp ~/.weeb-cli/weeb.db ~/backup/weeb.db
```

#### Geri Yükleme

```bash
# Ayarlar menüsünden
Ayarlar → Yedekleme & Geri Yükleme → Yedeği Geri Yükle

# Manuel geri yükleme
cp ~/backup/weeb.db ~/.weeb-cli/weeb.db
```

## Gelişmiş Yapılandırma

### Özel Önbellek Dizini

```python
from weeb_cli.services.cache import CacheManager
from pathlib import Path

cache = CacheManager(Path("/custom/cache/dir"))
```

### Özel İndirme Yöneticisi

```python
from weeb_cli.services.downloader import QueueManager

queue = QueueManager()
queue.start_queue()
```

## Sorun Giderme

### Yapılandırmayı Sıfırla

Tüm ayarları sıfırlamak için veritabanını silin:

```bash
rm ~/.weeb-cli/weeb.db
weeb-cli  # Kurulum sihirbazını çalıştırır
```

### Mevcut Yapılandırmayı Görüntüle

```python
from weeb_cli.config import config

# Tüm yapılandırmayı al
all_config = config.db.get_all_config()
for key, value in all_config.items():
    print(f"{key}: {value}")
```

### Yapılandırma Sorunlarını Gider

Yapılandırma yüklemesini görmek için hata ayıklama modunu etkinleştirin:

```bash
export WEEB_CLI_DEBUG=1
weeb-cli
```

Günlükleri kontrol edin:
```
~/.weeb-cli/logs/debug.log
```

## En İyi Uygulamalar

1. **Düzenli Yedekleme**: Büyük güncellemelerden önce veritabanınızı yedekleyin
2. **Aria2 Kullanın**: Daha hızlı indirmeler için Aria2'yi etkinleştirin
3. **Eşzamanlılığı Ayarlayın**: Yavaş bağlantılarda eşzamanlı indirmeleri azaltın
4. **İzleyicileri Etkinleştirin**: Cihazlar arasında ilerlemeyi senkronize edin
5. **Önbelleği Temizleyin**: Ayarlarda önbelleği periyodik olarak temizleyin

## Sonraki Adımlar

- [Kullanıcı Kılavuzu](../user-guide/searching.md): Weeb CLI'ı nasıl kullanacağınızı öğrenin
- [API Referansı](../api/core/config.md): Yapılandırma API dokümantasyonu
