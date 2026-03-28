# Konfigurationsanleitung

Diese Anleitung behandelt alle verfügbaren Konfigurationsoptionen in Weeb CLI.

## Konfigurationsspeicherung

Alle Konfigurationen werden in einer SQLite-Datenbank gespeichert unter:

```
~/.weeb-cli/weeb.db
```

Die Konfiguration kann verwaltet werden über:
- Interaktives Einstellungsmenü
- Direkter Datenbankzugriff
- Konfigurations-API

## Zugriff auf Einstellungen

### Interaktiver Modus

```bash
weeb-cli
# Wählen Sie "Einstellungen" aus dem Hauptmenü
```

### API-Modus

```python
from weeb_cli.config import config

# Wert abrufen
language = config.get("language")

# Wert setzen
config.set("language", "tr")
```

## Konfigurationsoptionen

### Allgemeine Einstellungen

#### Sprache

Legen Sie die UI-Sprache fest.

- **Schlüssel**: `language`
- **Werte**: `tr`, `en`, `de`, `pl`
- **Standard**: `None` (fragt beim ersten Start)

```python
config.set("language", "tr")
```

#### Debug-Modus

Aktivieren Sie Debug-Protokollierung.

- **Schlüssel**: `debug_mode`
- **Werte**: `True`, `False`
- **Standard**: `False`

```python
config.set("debug_mode", True)
```

#### Beschreibung anzeigen

Zeigen Sie Anime-Beschreibungen in Suchergebnissen an.

- **Schlüssel**: `show_description`
- **Werte**: `True`, `False`
- **Standard**: `True`

### Download-Einstellungen

#### Download-Verzeichnis

Legen Sie fest, wo Anime-Dateien heruntergeladen werden.

- **Schlüssel**: `download_dir`
- **Standard**: `./weeb-downloads`

```python
config.set("download_dir", "/path/to/downloads")
```

#### Aria2-Einstellungen

Aktivieren Sie Aria2 für schnelle Multi-Verbindungs-Downloads.

- **Schlüssel**: `aria2_enabled`
- **Werte**: `True`, `False`
- **Standard**: `True`

```python
config.set("aria2_enabled", True)
```

Maximale Verbindungen pro Download:

- **Schlüssel**: `aria2_max_connections`
- **Werte**: `1-32`
- **Standard**: `16`

```python
config.set("aria2_max_connections", 16)
```

#### yt-dlp-Einstellungen

Aktivieren Sie yt-dlp für komplexe Stream-Downloads.

- **Schlüssel**: `ytdlp_enabled`
- **Werte**: `True`, `False`
- **Standard**: `True`

```python
config.set("ytdlp_enabled", True)
```

Format-String für yt-dlp:

- **Schlüssel**: `ytdlp_format`
- **Standard**: `"bestvideo+bestaudio/best"`

```python
config.set("ytdlp_format", "bestvideo+bestaudio/best")
```

#### Gleichzeitige Downloads

Maximale Anzahl gleichzeitiger Downloads.

- **Schlüssel**: `max_concurrent_downloads`
- **Werte**: `1-10`
- **Standard**: `3`

```python
config.set("max_concurrent_downloads", 3)
```

#### Wiederholungseinstellungen

Maximale Wiederholungsversuche für fehlgeschlagene Downloads:

- **Schlüssel**: `download_max_retries`
- **Werte**: `0-10`
- **Standard**: `3`

Verzögerung zwischen Wiederholungen (Sekunden):

- **Schlüssel**: `download_retry_delay`
- **Werte**: `1-60`
- **Standard**: `10`

### Anbieter-Einstellungen

#### Standard-Anbieter

Legen Sie die Standard-Anime-Quelle fest.

- **Schlüssel**: `scraping_source`
- **Werte**: Anbieternamen (z.B. `animecix`, `hianime`)
- **Standard**: `None` (verwendet den ersten verfügbaren für die Sprache)

```python
config.set("scraping_source", "animecix")
```

### Integrations-Einstellungen

#### Discord Rich Presence

Aktivieren Sie die Discord-Integration, um anzuzeigen, was Sie gerade ansehen.

- **Schlüssel**: `discord_rpc_enabled`
- **Werte**: `True`, `False`
- **Standard**: `True`

```python
config.set("discord_rpc_enabled", True)
```

#### Tastaturkürzel

Aktivieren Sie globale Tastaturkürzel (experimentell).

- **Schlüssel**: `shortcuts_enabled`
- **Werte**: `True`, `False`
- **Standard**: `False`

### Tracker-Einstellungen

Tracker-Anmeldedaten werden sicher in der Datenbank gespeichert:

- **AniList**: OAuth-Token
- **MyAnimeList**: OAuth-Token
- **Kitsu**: E-Mail und Passwort (gehasht)

Konfigurieren Sie über Einstellungen → Tracker-Menü.

## Umgebungsvariablen

### WEEB_CLI_CONFIG_DIR

Konfigurationsverzeichnis überschreiben:

```bash
export WEEB_CLI_CONFIG_DIR="/custom/path"
weeb-cli
```

### WEEB_CLI_DEBUG

Debug-Modus aktivieren:

```bash
export WEEB_CLI_DEBUG=1
weeb-cli start
```

## Konfigurationsdateien

### Datenbankschema

Die SQLite-Datenbank enthält diese Tabellen:

- `config`: Schlüssel-Wert-Konfiguration
- `progress`: Wiedergabefortschritt
- `search_history`: Suchanfragen
- `download_queue`: Download-Warteschlange
- `external_drives`: Externe Laufwerkspfade
- `anime_index`: Lokaler Bibliotheksindex
- `virtual_library`: Online-Anime-Lesezeichen

### Sicherung und Wiederherstellung

#### Sicherung

```bash
# Über das Einstellungsmenü
Einstellungen → Sicherung & Wiederherstellung → Sicherung erstellen

# Manuelle Sicherung
cp ~/.weeb-cli/weeb.db ~/backup/weeb.db
```

#### Wiederherstellung

```bash
# Über das Einstellungsmenü
Einstellungen → Sicherung & Wiederherstellung → Sicherung wiederherstellen

# Manuelle Wiederherstellung
cp ~/backup/weeb.db ~/.weeb-cli/weeb.db
```

## Erweiterte Konfiguration

### Benutzerdefiniertes Cache-Verzeichnis

```python
from weeb_cli.services.cache import CacheManager
from pathlib import Path

cache = CacheManager(Path("/custom/cache/dir"))
```

### Benutzerdefinierter Download-Manager

```python
from weeb_cli.services.downloader import QueueManager

queue = QueueManager()
queue.start_queue()
```

## Fehlerbehebung

### Konfiguration zurücksetzen

Löschen Sie die Datenbank, um alle Einstellungen zurückzusetzen:

```bash
rm ~/.weeb-cli/weeb.db
weeb-cli  # Führt den Setup-Assistenten aus
```

### Aktuelle Konfiguration anzeigen

```python
from weeb_cli.config import config

# Alle Konfigurationen abrufen
all_config = config.db.get_all_config()
for key, value in all_config.items():
    print(f"{key}: {value}")
```

### Konfigurationsprobleme debuggen

Aktivieren Sie den Debug-Modus, um das Laden der Konfiguration zu sehen:

```bash
export WEEB_CLI_DEBUG=1
weeb-cli
```

Überprüfen Sie die Protokolle unter:
```
~/.weeb-cli/logs/debug.log
```

## Best Practices

1. **Regelmäßig sichern**: Sichern Sie Ihre Datenbank vor größeren Updates
2. **Aria2 verwenden**: Aktivieren Sie Aria2 für schnellere Downloads
3. **Parallelität anpassen**: Reduzieren Sie gleichzeitige Downloads bei langsameren Verbindungen
4. **Tracker aktivieren**: Synchronisieren Sie den Fortschritt über Geräte hinweg
5. **Cache bereinigen**: Bereinigen Sie den Cache regelmäßig in den Einstellungen

## Nächste Schritte

- [Benutzerhandbuch](../user-guide/searching.md): Erfahren Sie, wie Sie Weeb CLI verwenden
- [API-Referenz](../api/core/config.md): Konfigurations-API-Dokumentation
