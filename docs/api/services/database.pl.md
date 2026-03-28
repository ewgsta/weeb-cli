# Database Service

Zarządzanie bazą danych SQLite dla trwałego przechowywania.

## Przegląd

Usługa Database zapewnia bezpieczne wątkowo operacje SQLite dla:
- Przechowywania konfiguracji
- Śledzenia postępu oglądania
- Zarządzania kolejką pobierania
- Indeksowania lokalnej biblioteki
- Zakładek wirtualnej biblioteki

## Lokalizacja bazy danych

```
~/.weeb-cli/weeb.db
```

## Tabele

- `config`: Konfiguracja klucz-wartość
- `progress`: Postęp oglądania i znaczniki czasu
- `search_history`: Ostatnie wyszukiwania
- `download_queue`: Elementy kolejki pobierania
- `external_drives`: Ścieżki dysków zewnętrznych
- `anime_index`: Lokalny indeks anime
- `virtual_library`: Zakładki anime online

## Użycie

```python
from weeb_cli.services.database import db

# Konfiguracja
db.set_config("key", "value")
value = db.get_config("key")

# Postęp
db.save_progress(slug, title, episode, total)
progress = db.get_progress(slug)

# Kolejka
db.add_to_queue(item)
queue = db.get_queue()
```

## Bezpieczeństwo wątków

Baza danych używa:
- RLock dla bezpieczeństwa wątków
- Tryb WAL dla współbieżnego dostępu
- Puli połączeń
- Automatycznego ponawiania przy zajętości

## Następne kroki

- [Dokumentacja API](../overview.md): Pełna dokumentacja API
- [Konfiguracja](../../getting-started/configuration.md): Przewodnik konfiguracji
