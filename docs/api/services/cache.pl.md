# Cache Service

::: weeb_cli.services.cache
    options:
      show_root_heading: true
      show_source: true
      heading_level: 2

## Przegląd

Dwupoziomowy system buforowania z pamięcią i przechowywaniem opartym na plikach dla lepszej wydajności.

## CacheManager

Główna klasa menedżera pamięci podręcznej.

### Metody

- `get()`: Pobierz wartość z pamięci podręcznej
- `set()`: Zapisz wartość w pamięci podręcznej
- `delete()`: Usuń wartość z pamięci podręcznej
- `clear()`: Wyczyść całą pamięć podręczną
- `clear_pattern()`: Wyczyść według wzorca
- `invalidate_provider()`: Wyczyść pamięć podręczną dostawcy
- `cleanup()`: Usuń wygasłe wpisy
- `get_stats()`: Pobierz statystyki pamięci podręcznej

## Przykłady użycia

### Podstawowe buforowanie

```python
from weeb_cli.services.cache import get_cache

cache = get_cache()

# Zapisz
cache.set("key", {"data": "value"})

# Pobierz
data = cache.get("key", max_age=3600)
```

### Użycie dekoratora

```python
from weeb_cli.services.cache import cached

@cached(max_age=1800)
def expensive_function(param):
    # Wynik buforowany przez 30 minut
    return compute_result(param)
```

## Dokumentacja API

::: weeb_cli.services.cache.CacheManager
::: weeb_cli.services.cache.cached
::: weeb_cli.services.cache.get_cache
