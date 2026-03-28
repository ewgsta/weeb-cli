# API-Modus

Nicht-interaktive JSON-API für Skripte, Automatisierung und Integration mit anderen Tools.

## Übersicht

Der API-Modus bietet JSON-Ausgabe für alle Operationen und erleichtert:
- Integration mit Skripten
- Automatisierung von Workflows
- Erstellung benutzerdefinierter Schnittstellen
- Verbindung mit anderen Tools

## Grundlegende Verwendung

Alle API-Befehle folgen diesem Muster:

```bash
weeb-cli api [BEFEHL] [ARGS] [OPTIONEN]
```

Die Ausgabe ist immer gültiges JSON.

## Befehle

### providers

Alle verfügbaren Anbieter mit Metadaten auflisten.

```bash
weeb-cli api providers
```

Antwort:
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

Anime über Anbieter suchen.

```bash
weeb-cli api search "anime name" --provider animecix
```

Antwort:
```json
[
  {
    "id": "anime-slug",
    "title": "Anime-Titel",
    "type": "series",
    "cover": "https://cover-url.jpg",
    "year": 2024
  }
]
```

### episodes

Episodenliste für einen Anime abrufen.

```bash
weeb-cli api episodes "anime-id" --provider animecix
```

Optional: Nach Staffel filtern
```bash
weeb-cli api episodes "anime-id" --season 2 --provider animecix
```

Antwort:
```json
[
  {
    "id": "episode-id",
    "number": 1,
    "title": "Episodentitel",
    "season": 1,
    "url": "https://episode-url"
  }
]
```

### streams

Stream-URLs für eine Episode abrufen.

```bash
weeb-cli api streams "anime-id" "episode-id" --provider animecix
```

Antwort:
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

## Fehlerbehandlung

### Fehlerantwort

Fehler werden als JSON an stderr zurückgegeben:

```json
{
  "error": "Anbieter nicht gefunden: ungültiger-anbieter"
}
```

Exit-Code ist bei Fehler ungleich null.

### Fehler prüfen

```bash
if weeb-cli api search "anime" --provider ungültig 2>/dev/null; then
    echo "Erfolg"
else
    echo "Fehlgeschlagen"
fi
```

## Integrationsbeispiele

### Python-Skript

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

# Verwendung
results = search_anime("One Piece", "hianime")
for anime in results:
    print(f"{anime['title']} ({anime['year']})")
```

### Bash-Skript

```bash
#!/bin/bash

PROVIDER="animecix"
QUERY="Naruto"

# Suchen
results=$(weeb-cli api search "$QUERY" --provider "$PROVIDER")

# Mit jq parsen
echo "$results" | jq -r '.[] | "\(.title) - \(.year)"'

# Erste Ergebnis-ID holen
anime_id=$(echo "$results" | jq -r '.[0].id')

# Episoden abrufen
episodes=$(weeb-cli api episodes "$anime_id" --provider "$PROVIDER")
echo "$episodes" | jq -r '.[] | "Episode \(.number): \(.title)"'
```

### Node.js-Skript

```javascript
const { exec } = require('child_process');
const util = require('util');
const execPromise = util.promisify(exec);

async function searchAnime(query, provider = 'animecix') {
    const cmd = `weeb-cli api search "${query}" --provider ${provider}`;
    const { stdout } = await execPromise(cmd);
    return JSON.parse(stdout);
}

// Verwendung
searchAnime('One Piece', 'hianime')
    .then(results => {
        results.forEach(anime => {
            console.log(`${anime.title} (${anime.year})`);
        });
    })
    .catch(console.error);
```

## Erweiterte Verwendung

### Ergebnisse weiterleiten

```bash
# Mit jq suchen und filtern
weeb-cli api search "anime" --provider animecix | \
    jq '.[] | select(.year >= 2020)'

# Alle Episoden abrufen und zählen
weeb-cli api episodes "anime-id" --provider animecix | \
    jq 'length'

# Besten Qualitäts-Stream abrufen
weeb-cli api streams "anime-id" "ep-id" --provider animecix | \
    jq -r '.[0].url'
```

### Befehle verketten

```bash
# Suchen, erstes Ergebnis holen, Episoden abrufen
ANIME_ID=$(weeb-cli api search "Naruto" --provider animecix | jq -r '.[0].id')
weeb-cli api episodes "$ANIME_ID" --provider animecix
```

### Fehlerbehandlung

```bash
# Fehler erfassen
if ! output=$(weeb-cli api search "anime" --provider ungültig 2>&1); then
    echo "Fehler aufgetreten: $output"
    exit 1
fi
```

## Leistung

### Caching

API-Modus verwendet denselben Cache wie interaktiver Modus:
- Suchergebnisse für 1 Stunde gecacht
- Details für 6 Stunden gecacht
- Streams nicht gecacht

### Headless-Modus

API-Modus läuft im Headless-Modus:
- Keine TUI-Abhängigkeiten geladen
- Schnellerer Start
- Geringere Speichernutzung

## Einschränkungen

### Keine interaktiven Funktionen

API-Modus unterstützt nicht:
- Menüs und Eingabeaufforderungen
- Fortschrittsbalken
- Benutzereingabe
- Farbausgabe

### Keine Zustandsverwaltung

Jeder Befehl ist unabhängig:
- Kein Sitzungsstatus
- Keine Wiedergabeverlauf-Updates
- Keine Fortschrittsverfolgung

Verwenden Sie den interaktiven Modus für diese Funktionen.

## Best Practices

1. Anbieter immer explizit angeben
2. Fehler ordnungsgemäß behandeln
3. JSON mit geeigneten Tools parsen (jq, Python json)
4. Ergebnisse wenn möglich cachen
5. Angemessene Timeouts verwenden

## Nächste Schritte

- [Befehls-Referenz](commands.md): Alle CLI-Befehle
- [Serve-Modus](serve-mode.md): Torznab-Server
- [Entwicklung](../development/contributing.md): API-Entwicklung
