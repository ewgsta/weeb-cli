# Tracker Service

Integration mit AniList, MyAnimeList und Kitsu.

## Übersicht

Der Tracker-Service bietet:
- OAuth-Authentifizierung
- Fortschrittssynchronisierung
- Offline-Warteschlange
- Automatisches Matching

## Unterstützte Tracker

### AniList

- OAuth 2.0
- GraphQL API
- Manga und Anime

### MyAnimeList

- OAuth 2.0
- REST API
- Umfassende Datenbank

### Kitsu

- E-Mail/Passwort
- JSON API
- Moderne Oberfläche

## Verwendung

```python
from weeb_cli.services.tracker import tracker

# Authentifizieren
tracker.authenticate_anilist()

# Fortschritt aktualisieren
tracker.update_progress(
    anime_id="123",
    episode=5,
    status="CURRENT"
)

# Offline-Warteschlange synchronisieren
tracker.sync_offline_queue()
```

## Funktionen

- Automatische Fortschrittssynchronisierung
- Offline-Warteschlange für Updates
- Intelligentes Anime-Matching
- Unterstützung mehrerer Tracker

## Nächste Schritte

- [Tracker-Anleitung](../../user-guide/trackers.md): Benutzerhandbuch
- [Konfiguration](../../getting-started/configuration.md): Einrichtung
