# Türkçe Sağlayıcılar

Türkçe anime kaynak sağlayıcıları.

## Mevcut Sağlayıcılar

### Animecix

Animecix.net için sağlayıcı

- Geniş anime kütüphanesi
- Türkçe altyazılar
- Çoklu sunucular
- HD kalite

### Turkanime

TurkAnime.co için sağlayıcı

- Kapsamlı koleksiyon
- Türkçe dublaj ve altyazı
- Çoklu kalite seçenekleri

### Anizle

Anizle.com için sağlayıcı

- Modern arayüz
- Hızlı sunucular
- HD yayınlar

### Weeb

Weeb.com.tr için sağlayıcı

- Türkçe içerik
- Çoklu sunucular
- İyi kalite

## Kullanım

```python
from weeb_cli.providers import get_provider

# Sağlayıcı al
provider = get_provider("animecix")

# Ara
results = provider.search("One Piece")

# Detayları al
details = provider.get_details(results[0].id)

# Yayınları al
streams = provider.get_streams(details.id, episode_id)
```

## Sağlayıcı Karşılaştırması

| Sağlayıcı | Kütüphane Boyutu | Kalite | Hız | Altyazılar |
|----------|-------------|---------|-------|-----------|
| Animecix | Geniş | HD | Hızlı | Türkçe |
| Turkanime | Geniş | HD | Orta | Türkçe |
| Anizle | Orta | HD | Hızlı | Türkçe |
| Weeb | Orta | HD | Orta | Türkçe |

## Sonraki Adımlar

- [Base Provider](base.md): Sağlayıcı arayüzü
- [Sağlayıcı Ekleme](../../development/adding-providers.md): Sağlayıcı oluştur
