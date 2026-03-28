# Base Provider

::: weeb_cli.providers.base
    options:
      show_root_heading: true
      show_source: true
      heading_level: 2

## Genel Bakış

Base provider modülü, tüm anime sağlayıcılarının uygulaması gereken soyut arayüzü ve veri yapılarını tanımlar.

## Veri Sınıfları

### AnimeResult

Arama sonucu temsili.

### Episode

Meta verilerle birlikte bölüm bilgisi.

### StreamLink

Kalite ve sunucu bilgisiyle birlikte yayın URL'si.

### AnimeDetails

Bölümler dahil eksiksiz anime bilgisi.

## BaseProvider Arayüzü

Tüm sağlayıcıların miras alması gereken soyut temel sınıf.

### Gerekli Metodlar

- `search()`: Anime ara
- `get_details()`: Anime detaylarını al
- `get_episodes()`: Bölüm listesini al
- `get_streams()`: Yayın URL'lerini çıkar

### Yardımcı Metodlar

- `_request()`: Yeniden deneme mantığıyla HTTP isteği

## Uygulama Örneği

```python
from weeb_cli.providers.base import BaseProvider, AnimeResult
from weeb_cli.providers.registry import register_provider

@register_provider("myprovider", lang="en", region="US")
class MyProvider(BaseProvider):
    def search(self, query: str) -> List[AnimeResult]:
        # Implementation
        pass
```

## API Referansı

::: weeb_cli.providers.base.AnimeResult
::: weeb_cli.providers.base.Episode
::: weeb_cli.providers.base.StreamLink
::: weeb_cli.providers.base.AnimeDetails
::: weeb_cli.providers.base.BaseProvider
