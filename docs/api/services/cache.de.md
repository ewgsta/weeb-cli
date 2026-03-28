# Cache Service

::: weeb_cli.services.cache
    options:
      show_root_heading: true
      show_source: true
      heading_level: 2

## Übersicht

Zweistufiges Caching-System mit Speicher- und dateibasierter Speicherung für verbesserte Leistung.

## CacheManager

Haupt-Cache-Manager-Klasse.

### Methoden

- `get()`: Zwischengespeicherten Wert abrufen
- `set()`: Wert im Cache speichern
- `delete()`: Zwischengespeicherten Wert entfernen
- `clear()`: Gesamten Cache leeren
- `clear_pattern()`: Nach Muster leeren
- `invalidate_provider()`: Provider-Cache leeren
- `cleanup()`: Abgelaufene Einträge entfernen
- `get_stats()`: Cache-Statistiken abrufen

## Verwendungsbeispiele

### Grundlegendes Caching

```python
from weeb_cli.services.cache import get_cache

cache = get_cache()

# Speichern
cache.set("key", {"data": "value"})

# Abrufen
data = cache.get("key", max_age=3600)
```

### Verwendung des Dekorators

```python
from weeb_cli.services.cache import cached

@cached(max_age=1800)
def expensive_function(param):
    # Ergebnis wird 30 Minuten zwischengespeichert
    return compute_result(param)
```

## API-Referenz

::: weeb_cli.services.cache.CacheManager
::: weeb_cli.services.cache.cached
::: weeb_cli.services.cache.get_cache
