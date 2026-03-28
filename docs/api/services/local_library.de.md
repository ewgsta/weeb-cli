# Local Library Service

Lokale Anime-Indizierung und -Verwaltung.

## Übersicht

Der Local-Library-Service bietet:
- Automatisches Anime-Scannen
- Episodenerkennung
- Unterstützung für externe Laufwerke
- Tracker-Synchronisierung

## Funktionen

### Auto-Scanning

Scannt Verzeichnisse nach Anime:
- Erkennt Anime-Titel
- Zählt Episoden
- Gleicht mit Trackern ab

### Dateimuster

Unterstützte Benennungsmuster:
- `Anime Name - S1E1.mp4`
- `Anime Name - 01.mp4`
- `Anime Name - Episode 1.mp4`
- `[Group] Anime Name - 01.mp4`

### Externe Laufwerke

- USB-Laufwerke registrieren
- Externe HDDs scannen
- Portable Bibliothek

## Verwendung

```python
from weeb_cli.services.local_library import library

# Verzeichnis scannen
library.scan_directory("/path/to/anime")

# Indizierte Anime abrufen
anime_list = library.get_all_anime()

# Bibliothek durchsuchen
results = library.search("Naruto")
```

## Virtuelle Bibliothek

Online-Anime als Lesezeichen speichern:
- Kein Download erforderlich
- Schneller Zugriff
- Organisierte Sammlung

## Nächste Schritte

- [Bibliotheksanleitung](../../user-guide/library.md): Benutzerhandbuch
- [Konfiguration](../../getting-started/configuration.md): Einstellungen
