# CLI-Befehle-Referenz

Vollständige Referenz für alle Weeb CLI-Befehlszeilenbefehle.

## Hauptbefehle

### Standard (Interaktiver Modus)

Interaktiven Modus mit Hauptmenü starten.

```bash
weeb-cli
```

Dies ist der Standardbefehl, wenn kein Unterbefehl angegeben wird.

### start

Alternativer Befehl für interaktiven Modus (gleich wie Standard).

```bash
weeb-cli start
```

### api

Nicht-interaktive JSON-API für Skripte und Automatisierung.

```bash
weeb-cli api [UNTERBEFEHL]
```

Siehe [API-Modus](api-mode.md) für Details.

### serve

Torznab-Server für *arr-Integration starten.

```bash
weeb-cli serve [OPTIONEN]
```

Siehe [Serve-Modus](serve-mode.md) für Details.

## API-Unterbefehle

### api providers

Alle verfügbaren Anbieter auflisten.

```bash
weeb-cli api providers
```

Ausgabe:
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

Nach Anime suchen.

```bash
weeb-cli api search ABFRAGE [OPTIONEN]
```

Optionen:
- `--provider, -p`: Anbietername (Standard: animecix)

Beispiel:
```bash
weeb-cli api search "One Piece" --provider hianime
```

Ausgabe:
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

Episodenliste für Anime abrufen.

```bash
weeb-cli api episodes ANIME_ID [OPTIONEN]
```

Optionen:
- `--provider, -p`: Anbietername (Standard: animecix)
- `--season, -s`: Nach Staffelnummer filtern

Beispiel:
```bash
weeb-cli api episodes "one-piece-100" --provider hianime --season 1
```

Ausgabe:
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

Stream-URLs für Episode abrufen.

```bash
weeb-cli api streams ANIME_ID EPISODE_ID [OPTIONEN]
```

Optionen:
- `--provider, -p`: Anbietername (Standard: animecix)

Beispiel:
```bash
weeb-cli api streams "one-piece-100" "ep-1" --provider hianime
```

Ausgabe:
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

## Globale Optionen

### --help

Hilfemeldung anzeigen.

```bash
weeb-cli --help
weeb-cli api --help
weeb-cli api search --help
```

### --version

Versionsinformationen anzeigen.

```bash
weeb-cli --version
```

## Umgebungsvariablen

### WEEB_CLI_CONFIG_DIR

Konfigurationsverzeichnis überschreiben:

```bash
export WEEB_CLI_CONFIG_DIR="/eigener/pfad"
weeb-cli
```

### WEEB_CLI_DEBUG

Debug-Modus aktivieren:

```bash
export WEEB_CLI_DEBUG=1
weeb-cli
```

## Exit-Codes

- 0: Erfolg
- 1: Allgemeiner Fehler
- 2: Ungültige Argumente
- 130: Unterbrochen (Strg+C)

## Beispiele

### Suchen und Streamen

```bash
# Suchen
weeb-cli api search "Naruto" --provider animecix > ergebnisse.json

# Anime-ID aus Ergebnissen holen
ANIME_ID=$(jq -r '.[0].id' ergebnisse.json)

# Episoden abrufen
weeb-cli api episodes "$ANIME_ID" --provider animecix > episoden.json

# Episoden-ID holen
EPISODE_ID=$(jq -r '.[0].id' episoden.json)

# Streams abrufen
weeb-cli api streams "$ANIME_ID" "$EPISODE_ID" --provider animecix > streams.json

# Mit mpv abspielen
STREAM_URL=$(jq -r '.[0].url' streams.json)
mpv "$STREAM_URL"
```

### Stapelverarbeitung

```bash
#!/bin/bash
# Alle Episoden eines Anime herunterladen

ANIME_ID="one-piece-100"
PROVIDER="hianime"

# Episoden abrufen
episodes=$(weeb-cli api episodes "$ANIME_ID" --provider "$PROVIDER")

# Durch Episoden iterieren
echo "$episodes" | jq -c '.[]' | while read episode; do
    ep_id=$(echo "$episode" | jq -r '.id')
    ep_num=$(echo "$episode" | jq -r '.number')
    
    echo "Verarbeite Episode $ep_num..."
    
    # Streams abrufen
    streams=$(weeb-cli api streams "$ANIME_ID" "$ep_id" --provider "$PROVIDER")
    stream_url=$(echo "$streams" | jq -r '.[0].url')
    
    # Mit yt-dlp herunterladen
    yt-dlp -o "Episode-$ep_num.mp4" "$stream_url"
done
```

## Shell-Vervollständigung

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

## Nächste Schritte

- [API-Modus-Leitfaden](api-mode.md): Detaillierte API-Nutzung
- [Serve-Modus-Leitfaden](serve-mode.md): Torznab-Server
- [Benutzerleitfaden](../user-guide/searching.md): Interaktiver Modus
