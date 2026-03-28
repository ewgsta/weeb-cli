# Konfigurationsmodul

::: weeb_cli.config
    options:
      show_root_heading: true
      show_source: true
      heading_level: 2

## Übersicht

Das Konfigurationsmodul bietet zentralisierte Einstellungsverwaltung für Weeb CLI. Alle Konfiguration wird in einer SQLite-Datenbank mit Fallback auf sinnvolle Standardwerte gespeichert.

## Verwendungsbeispiele

### Konfigurationswerte abrufen

```python
from weeb_cli.config import config

# Mit Standard-Fallback abrufen
language = config.get("language", "en")
download_dir = config.get("download_dir")
aria2_enabled = config.get("aria2_enabled", True)
```

### Konfigurationswerte setzen

```python
from weeb_cli.config import config

# Sprache setzen
config.set("language", "tr")

# Download-Verzeichnis setzen
config.set("download_dir", "/pfad/zu/downloads")

# Features aktivieren/deaktivieren
config.set("discord_rpc_enabled", False)
```

### Headless-Modus

Für API-Nutzung ohne Datenbankzugriff:

```python
from weeb_cli.config import config

# Headless-Modus aktivieren
config.set_headless(True)

# Jetzt gibt config.get() nur DEFAULT_CONFIG-Werte zurück
language = config.get("language")  # Gibt None zurück (Standard)
```

## Standardkonfiguration

Die folgenden Standardwerte werden verwendet, wenn kein Datenbankwert existiert:

| Schlüssel | Standardwert | Beschreibung |
|-----------|--------------|--------------|
| `language` | `None` | UI-Sprache (tr, en, de, pl) |
| `aria2_enabled` | `True` | Aria2 für Downloads aktivieren |
| `ytdlp_enabled` | `True` | yt-dlp für Downloads aktivieren |
| `aria2_max_connections` | `16` | Max. Verbindungen pro Download |
| `max_concurrent_downloads` | `3` | Max. gleichzeitige Downloads |
| `download_dir` | `None` | Download-Verzeichnispfad |
| `ytdlp_format` | `"bestvideo+bestaudio/best"` | yt-dlp-Format-String |
| `scraping_source` | `None` | Standard-Provider |
| `show_description` | `True` | Anime-Beschreibungen anzeigen |
| `debug_mode` | `False` | Debug-Protokollierung aktivieren |
| `download_max_retries` | `3` | Download-Wiederholungsversuche |
| `download_retry_delay` | `10` | Verzögerung zwischen Wiederholungen (Sekunden) |
| `discord_rpc_enabled` | `True` | Discord Rich Presence aktivieren |
| `shortcuts_enabled` | `False` | Tastaturkürzel aktivieren |

## Konfigurationsverzeichnis

Konfiguration und Daten werden gespeichert in:

```
~/.weeb-cli/
├── weeb.db          # SQLite-Datenbank
├── cache/           # Zwischengespeicherte Daten
├── bin/             # Heruntergeladene Abhängigkeiten
└── logs/            # Debug-Protokolle
```

## API-Referenz

::: weeb_cli.config.Config
    options:
      show_root_heading: false
      members:
        - get
        - set
        - set_headless
