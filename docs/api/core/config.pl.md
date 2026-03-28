# Moduł konfiguracji

::: weeb_cli.config
    options:
      show_root_heading: true
      show_source: true
      heading_level: 2

## Przegląd

Moduł konfiguracji zapewnia scentralizowane zarządzanie ustawieniami dla Weeb CLI. Cała konfiguracja jest przechowywana w bazie danych SQLite z powrotem do rozsądnych wartości domyślnych.

## Przykłady użycia

### Pobieranie wartości konfiguracji

```python
from weeb_cli.config import config

# Pobierz z domyślnym powrotem
language = config.get("language", "en")
download_dir = config.get("download_dir")
aria2_enabled = config.get("aria2_enabled", True)
```

### Ustawianie wartości konfiguracji

```python
from weeb_cli.config import config

# Ustaw język
config.set("language", "tr")

# Ustaw katalog pobierania
config.set("download_dir", "/ścieżka/do/pobierania")

# Włącz/wyłącz funkcje
config.set("discord_rpc_enabled", False)
```

### Tryb bezgłowy

Do użycia API bez dostępu do bazy danych:

```python
from weeb_cli.config import config

# Włącz tryb bezgłowy
config.set_headless(True)

# Teraz config.get() zwraca tylko wartości DEFAULT_CONFIG
language = config.get("language")  # Zwraca None (domyślnie)
```

## Konfiguracja domyślna

Następujące wartości domyślne są używane, gdy nie istnieje wartość w bazie danych:

| Klucz | Wartość domyślna | Opis |
|-------|------------------|------|
| `language` | `None` | Język UI (tr, en, de, pl) |
| `aria2_enabled` | `True` | Włącz Aria2 do pobierania |
| `ytdlp_enabled` | `True` | Włącz yt-dlp do pobierania |
| `aria2_max_connections` | `16` | Maks. połączenia na pobieranie |
| `max_concurrent_downloads` | `3` | Maks. równoczesne pobieranie |
| `download_dir` | `None` | Ścieżka katalogu pobierania |
| `ytdlp_format` | `"bestvideo+bestaudio/best"` | Ciąg formatu yt-dlp |
| `scraping_source` | `None` | Domyślny dostawca |
| `show_description` | `True` | Pokaż opisy anime |
| `debug_mode` | `False` | Włącz logowanie debugowania |
| `download_max_retries` | `3` | Próby ponowienia pobierania |
| `download_retry_delay` | `10` | Opóźnienie między ponownymi próbami (sekundy) |
| `discord_rpc_enabled` | `True` | Włącz Discord Rich Presence |
| `shortcuts_enabled` | `False` | Włącz skróty klawiszowe |

## Katalog konfiguracji

Konfiguracja i dane są przechowywane w:

```
~/.weeb-cli/
├── weeb.db          # Baza danych SQLite
├── cache/           # Dane w pamięci podręcznej
├── bin/             # Pobrane zależności
└── logs/            # Logi debugowania
```

## Dokumentacja API

::: weeb_cli.config.Config
    options:
      show_root_heading: false
      members:
        - get
        - set
        - set_headless
