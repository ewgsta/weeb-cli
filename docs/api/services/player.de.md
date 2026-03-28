# Player Service

MPV-Player-Integration mit IPC-Überwachung.

## Übersicht

Der Player-Service bietet:
- MPV-Player-Integration
- IPC-Socket-Kommunikation
- Fortschrittsüberwachung
- Fortsetzungsfunktion

## Player-Klasse

Haupt-Player-Manager.

### Methoden

- `play()`: Wiedergabe starten
- `is_installed()`: MPV-Installation prüfen

## Funktionen

### Fortschrittsverfolgung

- Speichert Position alle 15 Sekunden
- Markiert automatisch als gesehen bei 80%
- Synchronisiert mit Trackern

### Fortsetzungsunterstützung

- Setzt automatisch von letzter Position fort
- Löscht Position nach Abschluss

## Verwendung

```python
from weeb_cli.services.player import player

# Stream abspielen
player.play(
    url="https://stream-url.m3u8",
    title="Anime - Episode 1",
    anime_title="Anime-Name",
    episode_number=1,
    slug="anime-slug"
)
```

## IPC-Überwachung

Überwacht MPV über IPC-Socket:
- Aktuelle Position
- Dauer
- Wiedergabestatus

## Nächste Schritte

- [Streaming-Anleitung](../../user-guide/streaming.md): Benutzerhandbuch
- [Konfiguration](../../getting-started/configuration.md): Einstellungen
