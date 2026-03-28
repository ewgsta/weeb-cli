# Almanca Sağlayıcılar

Almanca anime kaynak sağlayıcıları.

## Mevcut Sağlayıcılar

### AniWorld

AniWorld.to için sağlayıcı

- Geniş Almanca anime kütüphanesi
- Almanca dublaj ve altyazılar
- Çoklu kalite seçenekleri
- Hızlı sunucular

## Kullanım

```python
from weeb_cli.providers import get_provider

# Sağlayıcı al
provider = get_provider("aniworld")

# Ara
results = provider.search("One Piece")

# Detayları al
details = provider.get_details(results[0].id)

# Yayınları al
streams = provider.get_streams(details.id, episode_id)
```

## Sağlayıcı Detayları

| Sağlayıcı | Kütüphane Boyutu | Kalite | Hız | Altyazılar |
|----------|-------------|---------|-------|-----------|
| AniWorld | Geniş | HD | Hızlı | Almanca |

## Sonraki Adımlar

- [Base Provider](base.md): Sağlayıcı arayüzü
- [Sağlayıcı Ekleme](../../development/adding-providers.md): Sağlayıcı oluştur
