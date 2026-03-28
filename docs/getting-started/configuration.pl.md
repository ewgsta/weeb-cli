# Przewodnik konfiguracji

Ten przewodnik obejmuje wszystkie opcje konfiguracji dostępne w Weeb CLI.

## Przechowywanie konfiguracji

Cała konfiguracja jest przechowywana w bazie danych SQLite w:

```
~/.weeb-cli/weeb.db
```

Konfigurację można zarządzać poprzez:
- Interaktywne menu ustawień
- Bezpośredni dostęp do bazy danych
- API konfiguracji

## Dostęp do ustawień

### Tryb interaktywny

```bash
weeb-cli
# Wybierz "Ustawienia" z menu głównego
```

### Tryb API

```python
from weeb_cli.config import config

# Pobierz wartość
language = config.get("language")

# Ustaw wartość
config.set("language", "tr")
```

## Opcje konfiguracji

### Ustawienia ogólne

#### Język

Ustaw język interfejsu użytkownika.

- **Klucz**: `language`
- **Wartości**: `tr`, `en`, `de`, `pl`
- **Domyślnie**: `None` (pyta przy pierwszym uruchomieniu)

```python
config.set("language", "tr")
```

#### Tryb debugowania

Włącz logowanie debugowania.

- **Klucz**: `debug_mode`
- **Wartości**: `True`, `False`
- **Domyślnie**: `False`

```python
config.set("debug_mode", True)
```

#### Pokaż opis

Pokaż opisy anime w wynikach wyszukiwania.

- **Klucz**: `show_description`
- **Wartości**: `True`, `False`
- **Domyślnie**: `True`

### Ustawienia pobierania

#### Katalog pobierania

Ustaw, gdzie pliki anime są pobierane.

- **Klucz**: `download_dir`
- **Domyślnie**: `./weeb-downloads`

```python
config.set("download_dir", "/path/to/downloads")
```

#### Ustawienia Aria2

Włącz Aria2 dla szybkich pobierań wielopołączeniowych.

- **Klucz**: `aria2_enabled`
- **Wartości**: `True`, `False`
- **Domyślnie**: `True`

```python
config.set("aria2_enabled", True)
```

Maksymalna liczba połączeń na pobieranie:

- **Klucz**: `aria2_max_connections`
- **Wartości**: `1-32`
- **Domyślnie**: `16`

```python
config.set("aria2_max_connections", 16)
```

#### Ustawienia yt-dlp

Włącz yt-dlp dla złożonych pobierań strumieni.

- **Klucz**: `ytdlp_enabled`
- **Wartości**: `True`, `False`
- **Domyślnie**: `True`

```python
config.set("ytdlp_enabled", True)
```

Ciąg formatu dla yt-dlp:

- **Klucz**: `ytdlp_format`
- **Domyślnie**: `"bestvideo+bestaudio/best"`

```python
config.set("ytdlp_format", "bestvideo+bestaudio/best")
```

#### Równoczesne pobierania

Maksymalna liczba jednoczesnych pobierań.

- **Klucz**: `max_concurrent_downloads`
- **Wartości**: `1-10`
- **Domyślnie**: `3`

```python
config.set("max_concurrent_downloads", 3)
```

#### Ustawienia ponownych prób

Maksymalna liczba ponownych prób dla nieudanych pobierań:

- **Klucz**: `download_max_retries`
- **Wartości**: `0-10`
- **Domyślnie**: `3`

Opóźnienie między ponownymi próbami (sekundy):

- **Klucz**: `download_retry_delay`
- **Wartości**: `1-60`
- **Domyślnie**: `10`

### Ustawienia dostawcy

#### Domyślny dostawca

Ustaw domyślne źródło anime.

- **Klucz**: `scraping_source`
- **Wartości**: Nazwy dostawców (np. `animecix`, `hianime`)
- **Domyślnie**: `None` (używa pierwszego dostępnego dla języka)

```python
config.set("scraping_source", "animecix")
```

### Ustawienia integracji

#### Discord Rich Presence

Włącz integrację z Discord, aby pokazać, co oglądasz.

- **Klucz**: `discord_rpc_enabled`
- **Wartości**: `True`, `False`
- **Domyślnie**: `True`

```python
config.set("discord_rpc_enabled", True)
```

#### Skróty klawiszowe

Włącz globalne skróty klawiszowe (eksperymentalne).

- **Klucz**: `shortcuts_enabled`
- **Wartości**: `True`, `False`
- **Domyślnie**: `False`

### Ustawienia trackerów

Dane uwierzytelniające trackerów są bezpiecznie przechowywane w bazie danych:

- **AniList**: Token OAuth
- **MyAnimeList**: Token OAuth
- **Kitsu**: E-mail i hasło (zahashowane)

Skonfiguruj przez menu Ustawienia → Trackery.

## Zmienne środowiskowe

### WEEB_CLI_CONFIG_DIR

Nadpisz katalog konfiguracji:

```bash
export WEEB_CLI_CONFIG_DIR="/custom/path"
weeb-cli
```

### WEEB_CLI_DEBUG

Włącz tryb debugowania:

```bash
export WEEB_CLI_DEBUG=1
weeb-cli start
```

## Pliki konfiguracyjne

### Schemat bazy danych

Baza danych SQLite zawiera te tabele:

- `config`: Konfiguracja klucz-wartość
- `progress`: Postęp oglądania
- `search_history`: Zapytania wyszukiwania
- `download_queue`: Kolejka pobierania
- `external_drives`: Ścieżki dysków zewnętrznych
- `anime_index`: Indeks lokalnej biblioteki
- `virtual_library`: Zakładki anime online

### Kopia zapasowa i przywracanie

#### Kopia zapasowa

```bash
# Przez menu ustawień
Ustawienia → Kopia zapasowa i przywracanie → Utwórz kopię zapasową

# Ręczna kopia zapasowa
cp ~/.weeb-cli/weeb.db ~/backup/weeb.db
```

#### Przywracanie

```bash
# Przez menu ustawień
Ustawienia → Kopia zapasowa i przywracanie → Przywróć kopię zapasową

# Ręczne przywracanie
cp ~/backup/weeb.db ~/.weeb-cli/weeb.db
```

## Zaawansowana konfiguracja

### Niestandardowy katalog pamięci podręcznej

```python
from weeb_cli.services.cache import CacheManager
from pathlib import Path

cache = CacheManager(Path("/custom/cache/dir"))
```

### Niestandardowy menedżer pobierania

```python
from weeb_cli.services.downloader import QueueManager

queue = QueueManager()
queue.start_queue()
```

## Rozwiązywanie problemów

### Resetuj konfigurację

Usuń bazę danych, aby zresetować wszystkie ustawienia:

```bash
rm ~/.weeb-cli/weeb.db
weeb-cli  # Uruchomi kreatora konfiguracji
```

### Wyświetl bieżącą konfigurację

```python
from weeb_cli.config import config

# Pobierz całą konfigurację
all_config = config.db.get_all_config()
for key, value in all_config.items():
    print(f"{key}: {value}")
```

### Debuguj problemy z konfiguracją

Włącz tryb debugowania, aby zobaczyć ładowanie konfiguracji:

```bash
export WEEB_CLI_DEBUG=1
weeb-cli
```

Sprawdź logi w:
```
~/.weeb-cli/logs/debug.log
```

## Najlepsze praktyki

1. **Regularnie twórz kopie zapasowe**: Twórz kopie zapasowe bazy danych przed większymi aktualizacjami
2. **Używaj Aria2**: Włącz Aria2 dla szybszych pobierań
3. **Dostosuj współbieżność**: Zmniejsz równoczesne pobierania przy wolniejszych połączeniach
4. **Włącz trackery**: Synchronizuj postęp między urządzeniami
5. **Czyść pamięć podręczną**: Okresowo czyść pamięć podręczną w ustawieniach

## Następne kroki

- [Podręcznik użytkownika](../user-guide/searching.md): Dowiedz się, jak używać Weeb CLI
- [Dokumentacja API](../api/core/config.md): Dokumentacja API konfiguracji
