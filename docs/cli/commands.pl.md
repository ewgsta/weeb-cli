# Dokumentacja poleceń CLI

Kompletna dokumentacja wszystkich poleceń wiersza poleceń Weeb CLI.

## Główne polecenia

### Domyślne (Tryb interaktywny)

Uruchom tryb interaktywny z menu głównym.

```bash
weeb-cli
```

To jest domyślne polecenie, gdy nie podano podpolecenia.

### start

Alternatywne polecenie dla trybu interaktywnego (takie samo jak domyślne).

```bash
weeb-cli start
```

### api

Nieinteraktywne API JSON dla skryptów i automatyzacji.

```bash
weeb-cli api [PODPOLECENIE]
```

Zobacz [Tryb API](api-mode.md) dla szczegółów.

### serve

Uruchom serwer Torznab dla integracji z *arr.

```bash
weeb-cli serve [OPCJE]
```

Zobacz [Tryb Serve](serve-mode.md) dla szczegółów.

## Podpolecenia API

### api providers

Wyświetl wszystkich dostępnych dostawców.

```bash
weeb-cli api providers
```

Wyjście:
```json
[
  {
    "name": "animecix",
    "lang": "tr",
    "region": "TR",
    "class": "AnimecixProvider"
  }
]
```

### api search

Wyszukaj anime.

```bash
weeb-cli api search ZAPYTANIE [OPCJE]
```

Opcje:
- `--provider, -p`: Nazwa dostawcy (domyślnie: animecix)

Przykład:
```bash
weeb-cli api search "One Piece" --provider hianime
```

Wyjście:
```json
[
  {
    "id": "one-piece-100",
    "title": "One Piece",
    "type": "series",
    "cover": "https://...",
    "year": 1999
  }
]
```

### api episodes

Pobierz listę odcinków dla anime.

```bash
weeb-cli api episodes ANIME_ID [OPCJE]
```

Opcje:
- `--provider, -p`: Nazwa dostawcy (domyślnie: animecix)
- `--season, -s`: Filtruj według numeru sezonu

Przykład:
```bash
weeb-cli api episodes "one-piece-100" --provider hianime --season 1
```

Wyjście:
```json
[
  {
    "id": "ep-1",
    "number": 1,
    "title": "I'm Luffy! The Man Who Will Become Pirate King!",
    "season": 1
  }
]
```

### api streams

Pobierz adresy URL strumieni dla odcinka.

```bash
weeb-cli api streams ANIME_ID EPISODE_ID [OPCJE]
```

Opcje:
- `--provider, -p`: Nazwa dostawcy (domyślnie: animecix)

Przykład:
```bash
weeb-cli api streams "one-piece-100" "ep-1" --provider hianime
```

Wyjście:
```json
[
  {
    "url": "https://...",
    "quality": "1080p",
    "server": "megacloud",
    "headers": {}
  }
]
```

## Opcje globalne

### --help

Pokaż wiadomość pomocy.

```bash
weeb-cli --help
weeb-cli api --help
weeb-cli api search --help
```

### --version

Pokaż informacje o wersji.

```bash
weeb-cli --version
```

## Zmienne środowiskowe

### WEEB_CLI_CONFIG_DIR

Nadpisz katalog konfiguracji:

```bash
export WEEB_CLI_CONFIG_DIR="/własna/ścieżka"
weeb-cli
```

### WEEB_CLI_DEBUG

Włącz tryb debugowania:

```bash
export WEEB_CLI_DEBUG=1
weeb-cli
```

## Kody wyjścia

- 0: Sukces
- 1: Ogólny błąd
- 2: Nieprawidłowe argumenty
- 130: Przerwane (Ctrl+C)

## Przykłady

### Wyszukiwanie i strumieniowanie

```bash
# Wyszukaj
weeb-cli api search "Naruto" --provider animecix > wyniki.json

# Pobierz ID anime z wyników
ANIME_ID=$(jq -r '.[0].id' wyniki.json)

# Pobierz odcinki
weeb-cli api episodes "$ANIME_ID" --provider animecix > odcinki.json

# Pobierz ID odcinka
EPISODE_ID=$(jq -r '.[0].id' odcinki.json)

# Pobierz strumienie
weeb-cli api streams "$ANIME_ID" "$EPISODE_ID" --provider animecix > strumienie.json

# Odtwórz za pomocą mpv
STREAM_URL=$(jq -r '.[0].url' strumienie.json)
mpv "$STREAM_URL"
```

### Przetwarzanie wsadowe

```bash
#!/bin/bash
# Pobierz wszystkie odcinki anime

ANIME_ID="one-piece-100"
PROVIDER="hianime"

# Pobierz odcinki
episodes=$(weeb-cli api episodes "$ANIME_ID" --provider "$PROVIDER")

# Pętla przez odcinki
echo "$episodes" | jq -c '.[]' | while read episode; do
    ep_id=$(echo "$episode" | jq -r '.id')
    ep_num=$(echo "$episode" | jq -r '.number')
    
    echo "Przetwarzanie odcinka $ep_num..."
    
    # Pobierz strumienie
    streams=$(weeb-cli api streams "$ANIME_ID" "$ep_id" --provider "$PROVIDER")
    stream_url=$(echo "$streams" | jq -r '.[0].url')
    
    # Pobierz za pomocą yt-dlp
    yt-dlp -o "Odcinek-$ep_num.mp4" "$stream_url"
done
```

## Uzupełnianie powłoki

### Bash

```bash
eval "$(_WEEB_CLI_COMPLETE=bash_source weeb-cli)"
```

### Zsh

```bash
eval "$(_WEEB_CLI_COMPLETE=zsh_source weeb-cli)"
```

### Fish

```bash
eval (env _WEEB_CLI_COMPLETE=fish_source weeb-cli)
```

## Następne kroki

- [Przewodnik trybu API](api-mode.md): Szczegółowe użycie API
- [Przewodnik trybu Serve](serve-mode.md): Serwer Torznab
- [Przewodnik użytkownika](../user-guide/searching.md): Tryb interaktywny
