# Cache Service

::: weeb_cli.services.cache
    options:
      show_root_heading: true
      show_source: true
      heading_level: 2

## Genel Bakış

Geliştirilmiş performans için bellek ve dosya tabanlı depolama ile iki katmanlı önbellekleme sistemi.

## CacheManager

Ana önbellek yöneticisi sınıfı.

### Metodlar

- `get()`: Önbelleğe alınmış değeri al
- `set()`: Önbellekte değer sakla
- `delete()`: Önbelleğe alınmış değeri kaldır
- `clear()`: Tüm önbelleği temizle
- `clear_pattern()`: Desene göre temizle
- `invalidate_provider()`: Sağlayıcı önbelleğini temizle
- `cleanup()`: Süresi dolmuş girişleri kaldır
- `get_stats()`: Önbellek istatistiklerini al

## Kullanım Örnekleri

### Temel Önbellekleme

```python
from weeb_cli.services.cache import get_cache

cache = get_cache()

# Sakla
cache.set("key", {"data": "value"})

# Al
data = cache.get("key", max_age=3600)
```

### Dekoratör Kullanımı

```python
from weeb_cli.services.cache import cached

@cached(max_age=1800)
def expensive_function(param):
    # Sonuç 30 dakika önbelleğe alınır
    return compute_result(param)
```

## API Referansı

::: weeb_cli.services.cache.CacheManager
::: weeb_cli.services.cache.cached
::: weeb_cli.services.cache.get_cache
