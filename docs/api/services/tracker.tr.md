# Tracker Service

AniList, MyAnimeList ve Kitsu ile entegrasyon.

## Genel Bakış

Tracker servisi şunları sağlar:
- OAuth kimlik doğrulama
- İlerleme senkronizasyonu
- Çevrimdışı kuyruk
- Otomatik eşleştirme

## Desteklenen Tracker'lar

### AniList

- OAuth 2.0
- GraphQL API
- Manga ve anime

### MyAnimeList

- OAuth 2.0
- REST API
- Kapsamlı veritabanı

### Kitsu

- E-posta/şifre
- JSON API
- Modern arayüz

## Kullanım

```python
from weeb_cli.services.tracker import tracker

# Kimlik doğrula
tracker.authenticate_anilist()

# İlerlemeyi güncelle
tracker.update_progress(
    anime_id="123",
    episode=5,
    status="CURRENT"
)

# Çevrimdışı kuyruğu senkronize et
tracker.sync_offline_queue()
```

## Özellikler

- Otomatik ilerleme senkronizasyonu
- Güncellemeler için çevrimdışı kuyruk
- Akıllı anime eşleştirme
- Çoklu tracker desteği

## Sonraki Adımlar

- [Tracker Rehberi](../../user-guide/trackers.md): Kullanıcı rehberi
- [Yapılandırma](../../getting-started/configuration.md): Kurulum
