# Tryb API

Nieinteraktywne API JSON dla skryptów, automatyzacji i integracji z innymi narzędziami.

## Przegląd

Tryb API zapewnia wyjście JSON dla wszystkich operacji, ułatwiając:
- Integrację ze skryptami
- Automatyzację przepływów pracy
- Tworzenie niestandardowych interfejsów
- Łączenie z innymi narzędziami

## Podstawowe użycie

Wszystkie polecenia API są zgodne z tym wzorcem:

```bash
weeb-cli api [POLECENIE] [ARGUMENTY] [OPCJE]
```

Wyjście jest zawsze prawidłowym JSON.

## Polecenia

### providers

Wyświetl wszystkich dostępnych dostawców z metadanymi.

```bash
weeb-cli api providers
```

Odpowiedź:
```json
[
  {
    "name": "animecix",
    "lang": "tr",
    "region": "TR",
    "class": "AnimecixProvider"
  },
  {
    "name": "hianime",
    "lang": "en",
    "region": "US",
    "class": "HiAnimeProvider"
  }
]
```

### search

Wyszukaj anime u dostawców.

```bash
weeb-cli api search "nazwa anime" --provider animecix
```

Odpowiedź:
```json
[
  {
    "id": "anime-slug",
    "title": "Tytuł anime",
    "type": "series",
    "cover": "https://cover-url.jpg",
    "year": 2024
  }
]
```

### episodes

Pobierz listę odcinków dla anime.

```bash
weeb-cli api episodes "anime-id" --provider animecix
```

Opcjonalnie: Filtruj według sezonu
```bash
weeb-cli api episodes "anime-id" --season 2 --provider animecix
```

Odpowiedź:
```json
[
  {
    "id": "episode-id",
    "number": 1,
    "title": "Tytuł odcinka",
    "season": 1,
    "url": "https://episode-url"
  }
]
```

### streams

Pobierz adresy URL strumieni dla odcinka.

```bash
weeb-cli api streams "anime-id" "episode-id" --provider animecix
```

Odpowiedź:
```json
[
  {
    "url": "https://stream-url.m3u8",
    "quality": "1080p",
    "server": "megacloud",
    "headers": {
      "Referer": "https://..."
    },
    "subtitles": null
  }
]
```

## Obsługa błędów

### Odpowiedź błędu

Błędy są zwracane jako JSON do stderr:

```json
{
  "error": "Nie znaleziono dostawcy: nieprawidłowy-dostawca"
}
```

Kod wyjścia jest niezerowy w przypadku błędu.

### Sprawdzanie błędów

```bash
if weeb-cli api search "anime" --provider nieprawidłowy 2>/dev/null; then
    echo "Sukces"
else
    echo "Niepowodzenie"
fi
```

## Przykłady integracji

### Skrypt Python

```python
import subprocess
import json

def search_anime(query, provider="animecix"):
    result = subprocess.run(
        ["weeb-cli", "api", "search", query, "--provider", provider],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        return json.loads(result.stdout)
    else:
        error = json.loads(result.stderr)
        raise Exception(error["error"])

# Użycie
results = search_anime("One Piece", "hianime")
for anime in results:
    print(f"{anime['title']} ({anime['year']})")
```

### Skrypt Bash

```bash
#!/bin/bash

PROVIDER="animecix"
QUERY="Naruto"

# Wyszukaj
results=$(weeb-cli api search "$QUERY" --provider "$PROVIDER")

# Parsuj za pomocą jq
echo "$results" | jq -r '.[] | "\(.title) - \(.year)"'

# Pobierz ID pierwszego wyniku
anime_id=$(echo "$results" | jq -r '.[0].id')

# Pobierz odcinki
episodes=$(weeb-cli api episodes "$anime_id" --provider "$PROVIDER")
echo "$episodes" | jq -r '.[] | "Odcinek \(.number): \(.title)"'
```

### Skrypt Node.js

```javascript
const { exec } = require('child_process');
const util = require('util');
const execPromise = util.promisify(exec);

async function searchAnime(query, provider = 'animecix') {
    const cmd = `weeb-cli api search "${query}" --provider ${provider}`;
    const { stdout } = await execPromise(cmd);
    return JSON.parse(stdout);
}

// Użycie
searchAnime('One Piece', 'hianime')
    .then(results => {
        results.forEach(anime => {
            console.log(`${anime.title} (${anime.year})`);
        });
    })
    .catch(console.error);
```

## Zaawansowane użycie

### Przekierowywanie wyników

```bash
# Wyszukaj i filtruj za pomocą jq
weeb-cli api search "anime" --provider animecix | \
    jq '.[] | select(.year >= 2020)'

# Pobierz wszystkie odcinki i policz
weeb-cli api episodes "anime-id" --provider animecix | \
    jq 'length'

# Pobierz strumień najlepszej jakości
weeb-cli api streams "anime-id" "ep-id" --provider animecix | \
    jq -r '.[0].url'
```

### Łączenie poleceń

```bash
# Wyszukaj, pobierz pierwszy wynik, pobierz odcinki
ANIME_ID=$(weeb-cli api search "Naruto" --provider animecix | jq -r '.[0].id')
weeb-cli api episodes "$ANIME_ID" --provider animecix
```

### Obsługa błędów

```bash
# Przechwytuj błędy
if ! output=$(weeb-cli api search "anime" --provider nieprawidłowy 2>&1); then
    echo "Wystąpił błąd: $output"
    exit 1
fi
```

## Wydajność

### Buforowanie

Tryb API używa tej samej pamięci podręcznej co tryb interaktywny:
- Wyniki wyszukiwania buforowane przez 1 godzinę
- Szczegóły buforowane przez 6 godzin
- Strumienie nie są buforowane

### Tryb bezgłowy

Tryb API działa w trybie bezgłowym:
- Nie ładowane zależności TUI
- Szybszy start
- Mniejsze zużycie pamięci

## Ograniczenia

### Brak funkcji interaktywnych

Tryb API nie obsługuje:
- Menu i monitów
- Pasków postępu
- Wprowadzania użytkownika
- Kolorowego wyjścia

### Brak zarządzania stanem

Każde polecenie jest niezależne:
- Brak stanu sesji
- Brak aktualizacji historii oglądania
- Brak śledzenia postępu

Użyj trybu interaktywnego dla tych funkcji.

## Najlepsze praktyki

1. Zawsze jawnie określaj dostawcę
2. Prawidłowo obsługuj błędy
3. Parsuj JSON odpowiednimi narzędziami (jq, Python json)
4. Buforuj wyniki, gdy to możliwe
5. Używaj odpowiednich limitów czasu

## Następne kroki

- [Dokumentacja poleceń](commands.md): Wszystkie polecenia CLI
- [Tryb Serve](serve-mode.md): Serwer Torznab
- [Rozwój](../development/contributing.md): Rozwój API
