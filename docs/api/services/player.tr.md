# Player Service

IPC izleme ile MPV oynatıcı entegrasyonu.

## Genel Bakış

Player servisi şunları sağlar:
- MPV oynatıcı entegrasyonu
- IPC soket iletişimi
- İlerleme izleme
- Devam etme işlevselliği

## Player Sınıfı

Ana oynatıcı yöneticisi.

### Metodlar

- `play()`: Oynatmayı başlat
- `is_installed()`: MPV kurulumunu kontrol et

## Özellikler

### İlerleme Takibi

- Her 15 saniyede bir konumu kaydeder
- %80'de otomatik olarak izlendi işaretler
- Tracker'larla senkronize eder

### Devam Etme Desteği

- Son konumdan otomatik olarak devam eder
- Tamamlandıktan sonra konumu temizler

## Kullanım

```python
from weeb_cli.services.player import player

# Yayını oynat
player.play(
    url="https://stream-url.m3u8",
    title="Anime - Bölüm 1",
    anime_title="Anime Adı",
    episode_number=1,
    slug="anime-slug"
)
```

## IPC İzleme

IPC soketi üzerinden MPV'yi izler:
- Mevcut konum
- Süre
- Oynatma durumu

## Sonraki Adımlar

- [Yayın Rehberi](../../user-guide/streaming.md): Kullanıcı rehberi
- [Yapılandırma](../../getting-started/configuration.md): Ayarlar
