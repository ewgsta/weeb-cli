# İngilizce Sağlayıcılar

İngilizce anime kaynak sağlayıcıları.

## Mevcut Sağlayıcılar

### HiAnime

HiAnime.to için sağlayıcı

- Devasa anime kütüphanesi
- Çoklu kalite seçenekleri
- Hızlı sunucular
- İngilizce altyazı ve dublaj

### AllAnime

AllAnime.to için sağlayıcı

- Geniş koleksiyon
- Çoklu sunucular
- HD kalite
- Altyazı ve dublaj seçenekleri

## Kullanım

```python
from weeb_cli.providers import get_provider

# Sağlayıcı al
provider = get_provider("hianime")

# Ara
results = provider.search("Naruto")

# Detayları al
details = provider.get_details(results[0].id)

# Yayınları al
streams = provider.get_streams(details.id, episode_id)
```

## Sağlayıcı Karşılaştırması

| Sağlayıcı | Kütüphane Boyutu | Kalite | Hız | Altyazılar |
|----------|-------------|---------|-------|-----------|
| HiAnime | Çok Geniş | 1080p | Hızlı | İngilizce |
| AllAnime | Geniş | 1080p | Hızlı | İngilizce |

## Sonraki Adımlar

- [Base Provider](base.md): Sağlayıcı arayüzü
- [Sağlayıcı Ekleme](../../development/adding-providers.md): Sağlayıcı oluştur
