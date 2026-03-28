# Lehçe Sağlayıcılar

Lehçe anime kaynak sağlayıcıları.

## Mevcut Sağlayıcılar

### Docchi

Docchi.pl için sağlayıcı

- Lehçe anime kütüphanesi
- Lehçe altyazılar
- Çoklu sunucular
- İyi kalite

## Kullanım

```python
from weeb_cli.providers import get_provider

# Sağlayıcı al
provider = get_provider("docchi")

# Ara
results = provider.search("Naruto")

# Detayları al
details = provider.get_details(results[0].id)

# Yayınları al
streams = provider.get_streams(details.id, episode_id)
```

## Sağlayıcı Detayları

| Sağlayıcı | Kütüphane Boyutu | Kalite | Hız | Altyazılar |
|----------|-------------|---------|-------|-----------|
| Docchi | Orta | HD | Orta | Lehçe |

## Sonraki Adımlar

- [Base Provider](base.md): Sağlayıcı arayüzü
- [Sağlayıcı Ekleme](../../development/adding-providers.md): Sağlayıcı oluştur
