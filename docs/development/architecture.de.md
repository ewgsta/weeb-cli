# Architektur-Übersicht

Dieses Dokument bietet einen Überblick über die Architektur und Designentscheidungen von Weeb CLI.

## Systemarchitektur

```
┌─────────────────────────────────────────────────────────┐
│                   CLI-Schicht (Typer)                    │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌─────────┐ │
│  │  Suche   │  │Downloads │  │Watchlist │  │Einst.   │ │
│  └──────────┘  └──────────┘  └──────────┘  └─────────┘ │
└─────────────────────────────────────────────────────────┘
                          │
┌─────────────────────────────────────────────────────────┐
│                   Service-Schicht                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌─────────┐ │
│  │Downloader│  │ Tracker  │  │  Player  │  │  Cache  │ │
│  └──────────┘  └──────────┘  └──────────┘  └─────────┘ │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐              │
│  │ Database │  │  Scraper │  │  Logger  │              │
│  └──────────┘  └──────────┘  └──────────┘              │
└─────────────────────────────────────────────────────────┘
                          │
┌─────────────────────────────────────────────────────────┐
│                  Provider-Schicht                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌─────────┐ │
│  │Türkisch  │  │ Englisch │  │  Deutsch │  │ Polnisch│ │
│  │Provider  │  │ Provider │  │ Provider │  │ Provider│ │
│  └──────────┘  └──────────┘  └──────────┘  └─────────┘ │
└─────────────────────────────────────────────────────────┘
                          │
┌─────────────────────────────────────────────────────────┐
│                    Datenschicht                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐              │
│  │  SQLite  │  │   Cache  │  │   Logs   │              │
│  │ Database │  │  Dateien │  │ Dateien  │              │
│  └──────────┘  └──────────┘  └──────────┘              │
└─────────────────────────────────────────────────────────┘
```

## Design-Muster

### 1. Registry-Muster (Provider)

Provider werden automatisch mit Dekoratoren entdeckt und registriert:

```python
@register_provider("animecix", lang="tr", region="TR")
class AnimecixProvider(BaseProvider):
    pass
```

**Vorteile:**
- Einfaches Hinzufügen neuer Provider
- Keine manuelle Registrierung erforderlich
- Automatische Erkennung aus Dateisystem

### 2. Lazy Loading (Services)

Services verwenden Lazy Loading zur verzögerten Initialisierung:

```python
@property
def db(self):
    if self._db is None:
        from weeb_cli.services.database import db
        self._db = db
    return self._db
```

**Vorteile:**
- Schnellere Startzeit
- Reduzierte Speichernutzung
- Vermeidung zirkulärer Importe

### 3. Singleton-Muster (Globale Instanzen)

Globale Instanzen für gemeinsame Ressourcen:

```python
config = Config()
i18n = I18n()
cache = CacheManager()
```

**Vorteile:**
- Einzige Quelle der Wahrheit
- Einfacher Zugriff in der gesamten Anwendung
- Konsistenter Zustand

### 4. Strategy-Muster (Download-Methoden)

Mehrere Download-Strategien mit Fallback:

```python
def _try_download(self, url, path, item):
    strategies = [
        self._download_aria2,
        self._download_ytdlp,
        self._download_ffmpeg,
        self._download_generic
    ]
    for strategy in strategies:
        if strategy(url, path, item):
            return True
    return False
```

**Vorteile:**
- Graceful Degradation
- Flexible Download-Methoden
- Einfaches Hinzufügen neuer Strategien

## Hauptkomponenten

### CLI-Schicht

**Technologie:** Typer + Rich + Questionary

**Verantwortlichkeiten:**
- Befehlszeilenargumente parsen
- Interaktive Menüs anzeigen
- Benutzereingaben verarbeiten
- Fortschrittsindikatoren anzeigen

### Service-Schicht

**Kern-Services:**

1. **Database**: SQLite mit WAL-Modus
   - Konfigurationsspeicherung
   - Fortschrittsverfolgung
   - Download-Warteschlange
   - Lokaler Bibliotheksindex

2. **Downloader**: Warteschlangenbasierter Download-Manager
   - Gleichzeitige Downloads
   - Mehrere Download-Methoden
   - Wiederholungslogik
   - Fortschrittsverfolgung

3. **Tracker**: Anime-Tracking-Integration
   - OAuth-Authentifizierung
   - Fortschrittssynchronisierung
   - Offline-Warteschlange

4. **Player**: MPV-Integration
   - IPC-Kommunikation
   - Fortschrittsüberwachung
   - Fortsetzungsfunktionalität

5. **Cache**: Zweistufiges Caching
   - Speicher-Cache
   - Datei-Cache
   - TTL-Unterstützung

### Provider-Schicht

**Struktur:**
- Sprachlich organisierte Verzeichnisse
- Basis-Provider-Schnittstelle
- Registry-System
- Stream-Extraktoren

**Provider-Lebenszyklus:**
1. Erkennung (Dateisystem-Scan)
2. Registrierung (Dekorator)
3. Instanziierung (auf Anfrage)
4. Caching (Ergebnisse)

### Datenschicht

**Speicherung:**
- SQLite-Datenbank (~/.weeb-cli/weeb.db)
- Cache-Dateien (~/.weeb-cli/cache/)
- Log-Dateien (~/.weeb-cli/logs/)
- Heruntergeladene Binärdateien (~/.weeb-cli/bin/)

## Datenfluss

### Suchfluss

```
Benutzereingabe → CLI → Scraper → Provider → Cache → API
                                      ↓
                                  Ergebnisse
                                      ↓
                                CLI-Anzeige
```

### Download-Fluss

```
Benutzerauswahl → Warteschlangen-Manager → Download-Worker
                                                ↓
                                        Strategien versuchen
                                                ↓
                         ┌─────────────────────────┐
                         │  Aria2 → yt-dlp →       │
                         │  FFmpeg → Generic       │
                         └─────────────────────────┘
                                                ↓
                                        Fortschritt aktualisieren
                                                ↓
                                        In Datenbank speichern
```

### Wiedergabefluss

```
Benutzerauswahl → Stream-Extraktion → Player (MPV)
                                          ↓
                                   IPC-Monitor
                                          ↓
                                  Fortschritt speichern
                                          ↓
                                  Tracker synchronisieren
```

## Thread-Sicherheit

### Locking-Strategie

1. **Database**: RLock für Verbindungsverwaltung
2. **Download-Warteschlange**: Lock für Warteschlangenoperationen
3. **Cache**: Kein Locking (Single-Threaded-Zugriff)

### Gleichzeitige Operationen

- Download-Worker laufen in separaten Threads
- MPV-Monitor läuft in Daemon-Thread
- Tracker-Sync läuft im Hintergrund

## Fehlerbehandlung

### Exception-Hierarchie

```
WeebCLIError (Basis)
├── ProviderError
├── DownloadError
├── NetworkError
├── AuthenticationError
├── DatabaseError
├── ValidationError
└── DependencyError
```

### Fehlerwiederherstellung

1. **Wiederholungslogik**: Exponentieller Backoff für vorübergehende Fehler
2. **Fallback**: Alternative Methoden bei Primärausfall
3. **Graceful Degradation**: Mit reduzierter Funktionalität fortfahren
4. **Benutzerbenachrichtigung**: Klare Fehlermeldungen mit i18n

## Leistungsoptimierungen

### 1. Caching

- Suchergebnisse für 1 Stunde gecacht
- Details für 6 Stunden gecacht
- Zweistufig (Speicher + Datei) für Geschwindigkeit

### 2. Lazy Loading

- Services bei erster Verwendung geladen
- Provider bei Bedarf entdeckt
- Datenbank-Verbindungspooling

### 3. Gleichzeitige Downloads

- Mehrere Downloads parallel
- Konfigurierbares Gleichzeitigkeitslimit
- Ressourcenbewusste Planung

### 4. Datenbankoptimierung

- WAL-Modus für gleichzeitigen Zugriff
- Vorbereitete Anweisungen
- Indizierte Abfragen
- Batch-Operationen

## Sicherheitsüberlegungen

### 1. Eingabebereinigung

- Dateinamenbereinigung
- URL-Validierung
- SQL-Injection-Prävention (parametrisierte Abfragen)

### 2. Anmeldedatenspeicherung

- OAuth-Token in Datenbank
- Keine Klartext-Passwörter
- Sichere Token-Aktualisierung

### 3. Netzwerksicherheit

- HTTPS für API-Aufrufe
- Zertifikatsüberprüfung
- Timeout-Limits

## Erweiterbarkeit

### Neue Features hinzufügen

1. **Neuer Provider**: BaseProvider-Schnittstelle implementieren
2. **Neuer Tracker**: TrackerBase-Schnittstelle implementieren
3. **Neuer Befehl**: Typer-Befehl hinzufügen
4. **Neuer Service**: Service-Muster folgen

### Plugin-System

Derzeit nicht implementiert, aber Architektur unterstützt:
- Provider-Plugins
- Extraktor-Plugins
- Befehls-Plugins

## Zukünftige Verbesserungen

1. **Plugin-System**: Dynamisches Plugin-Laden
2. **API-Server**: REST-API für Fernsteuerung
3. **Web-UI**: Browserbasierte Schnittstelle
4. **Mobile App**: Begleit-Mobile-Anwendung
5. **Cloud-Sync**: Geräteübergreifende Synchronisierung
