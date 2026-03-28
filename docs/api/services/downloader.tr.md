# Downloader Service

Çoklu indirme yöntemleriyle kuyruk tabanlı indirme yöneticisi.

## Genel Bakış

Downloader servisi şunları sağlar:
- Kuyruk tabanlı indirme yönetimi
- Eşzamanlı indirmeler
- Çoklu indirme yöntemleri (Aria2, yt-dlp, FFmpeg)
- Geri çekilme ile otomatik yeniden deneme
- İlerleme takibi

## QueueManager

Ana indirme kuyruğu yöneticisi.

### Metodlar

- `start_queue()`: İndirme işçilerini başlat
- `stop_queue()`: Tüm indirmeleri durdur
- `add_to_queue()`: Kuyruğa bölüm ekle
- `retry_failed()`: Başarısız indirmeleri yeniden dene
- `clear_completed()`: Tamamlanan öğeleri kaldır

## İndirme Yöntemleri

### Öncelik Sırası

1. Aria2 (en hızlı, çoklu bağlantı)
2. yt-dlp (karmaşık yayınlar)
3. FFmpeg (HLS dönüşümü)
4. Generic HTTP (yedek)

## Kullanım

```python
from weeb_cli.services.downloader import queue_manager

# Kuyruğu başlat
queue_manager.start_queue()

# Kuyruğa ekle
queue_manager.add_to_queue(
    anime_title="Anime Adı",
    episodes=[episode_data],
    slug="anime-slug"
)

# Durumu kontrol et
if queue_manager.is_running():
    print("Kuyruk aktif")
```

## Yapılandırma

- Maksimum eşzamanlı indirmeler
- Aria2 bağlantıları
- Yeniden deneme girişimleri
- Yeniden deneme gecikmesi

## Sonraki Adımlar

- [İndirme Rehberi](../../user-guide/downloading.md): Kullanıcı rehberi
- [Yapılandırma](../../getting-started/configuration.md): Ayarlar
