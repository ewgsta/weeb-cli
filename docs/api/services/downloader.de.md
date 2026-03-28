# Downloader Service

Warteschlangenbasierter Download-Manager mit mehreren Download-Methoden.

## Übersicht

Der Downloader-Service bietet:
- Warteschlangenbasiertes Download-Management
- Gleichzeitige Downloads
- Mehrere Download-Methoden (Aria2, yt-dlp, FFmpeg)
- Automatische Wiederholung mit Backoff
- Fortschrittsverfolgung

## QueueManager

Haupt-Download-Warteschlangenmanager.

### Methoden

- `start_queue()`: Download-Worker starten
- `stop_queue()`: Alle Downloads stoppen
- `add_to_queue()`: Episoden zur Warteschlange hinzufügen
- `retry_failed()`: Fehlgeschlagene Downloads wiederholen
- `clear_completed()`: Abgeschlossene Elemente entfernen

## Download-Methoden

### Prioritätsreihenfolge

1. Aria2 (am schnellsten, Multi-Verbindung)
2. yt-dlp (komplexe Streams)
3. FFmpeg (HLS-Konvertierung)
4. Generic HTTP (Fallback)

## Verwendung

```python
from weeb_cli.services.downloader import queue_manager

# Warteschlange starten
queue_manager.start_queue()

# Zur Warteschlange hinzufügen
queue_manager.add_to_queue(
    anime_title="Anime-Name",
    episodes=[episode_data],
    slug="anime-slug"
)

# Status prüfen
if queue_manager.is_running():
    print("Warteschlange aktiv")
```

## Konfiguration

- Maximale gleichzeitige Downloads
- Aria2-Verbindungen
- Wiederholungsversuche
- Wiederholungsverzögerung

## Nächste Schritte

- [Download-Anleitung](../../user-guide/downloading.md): Benutzerhandbuch
- [Konfiguration](../../getting-started/configuration.md): Einstellungen
