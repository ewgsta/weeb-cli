# Database Service

SQLite-Datenbankverwaltung für persistente Speicherung.

## Übersicht

Der Database-Service bietet thread-sichere SQLite-Operationen für:
- Konfigurationsspeicherung
- Fortschrittsverfolgung beim Ansehen
- Download-Warteschlangenverwaltung
- Lokale Bibliotheksindizierung
- Virtuelle Bibliotheks-Lesezeichen

## Datenbankspeicherort

```
~/.weeb-cli/weeb.db
```

## Tabellen

- `config`: Schlüssel-Wert-Konfiguration
- `progress`: Fortschritt und Zeitstempel beim Ansehen
- `search_history`: Letzte Suchen
- `download_queue`: Download-Warteschlangenelemente
- `external_drives`: Externe Laufwerkspfade
- `anime_index`: Lokaler Anime-Index
- `virtual_library`: Online-Anime-Lesezeichen

## Verwendung

```python
from weeb_cli.services.database import db

# Konfiguration
db.set_config("key", "value")
value = db.get_config("key")

# Fortschritt
db.save_progress(slug, title, episode, total)
progress = db.get_progress(slug)

# Warteschlange
db.add_to_queue(item)
queue = db.get_queue()
```

## Thread-Sicherheit

Die Datenbank verwendet:
- RLock für Thread-Sicherheit
- WAL-Modus für gleichzeitigen Zugriff
- Verbindungspooling
- Automatische Wiederholung bei Auslastung

## Nächste Schritte

- [API-Referenz](../overview.md): Vollständige API-Dokumentation
- [Konfiguration](../../getting-started/configuration.md): Konfigurationsanleitung
