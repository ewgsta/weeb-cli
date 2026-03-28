# Exceptions-Modul

::: weeb_cli.exceptions
    options:
      show_root_heading: true
      show_source: true
      heading_level: 2

## Übersicht

Benutzerdefinierte Exception-Hierarchie für strukturierte Fehlerbehandlung in Weeb CLI. Alle Exceptions erben von der `WeebCLIError`-Basisklasse.

## Exception-Hierarchie

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

## Verwendungsbeispiele

### Exceptions auslösen

```python
from weeb_cli.exceptions import ProviderError, DownloadError

# Nur mit Nachricht
raise ProviderError("Anime-Details konnten nicht abgerufen werden")

# Mit Fehlercode
raise ProviderError("Suche fehlgeschlagen", code="PROVIDER_001")

# Download-Fehler
raise DownloadError("Unzureichender Speicherplatz", code="DISK_FULL")
```

### Exceptions abfangen

```python
from weeb_cli.exceptions import (
    ProviderError, 
    NetworkError, 
    WeebCLIError
)

try:
    provider.search("anime")
except ProviderError as e:
    print(f"Provider-Fehler: {e.message} ({e.code})")
except NetworkError as e:
    print(f"Netzwerkfehler: {e.message}")
except WeebCLIError as e:
    print(f"Allgemeiner Fehler: {e}")
```

### Spezifische Exception-Behandlung

```python
from weeb_cli.exceptions import (
    AuthenticationError,
    DatabaseError,
    ValidationError
)

# Authentifizierung
try:
    tracker.authenticate()
except AuthenticationError as e:
    print(f"Authentifizierung fehlgeschlagen: {e.message}")
    # Erneut authentifizieren

# Datenbank
try:
    db.save_progress()
except DatabaseError as e:
    print(f"Datenbankfehler: {e.code}")
    # Wiederholen oder sichern

# Validierung
try:
    validate_input(user_input)
except ValidationError as e:
    print(f"Ungültige Eingabe: {e.message}")
    # Erneut abfragen
```

## Exception-Typen

### WeebCLIError

Basis-Exception für alle Weeb CLI-Fehler. Bietet strukturierte Fehlerbehandlung mit optionalen Fehlercodes.

**Attribute:**
- `message` (str): Menschenlesbare Fehlermeldung
- `code` (str): Optionaler Fehlercode zur Kategorisierung

### ProviderError

Ausgelöst für Anime-Provider-bezogene Fehler:
- Suchfehler
- Anime-Details konnten nicht abgerufen werden
- Episodenliste nicht verfügbar
- Stream-Extraktionsfehler

### DownloadError

Ausgelöst für Download-Operationsfehler:
- Netzwerkprobleme während des Downloads
- Unzureichender Speicherplatz
- Ungültige Stream-URLs
- Aria2/yt-dlp-Fehler

### NetworkError

Ausgelöst für Netzwerkverbindungsprobleme:
- HTTP-Anfragefehler
- Verbindungs-Timeouts
- DNS-Auflösungsfehler
- Netzwerk nicht verfügbar

### AuthenticationError

Ausgelöst für Tracker-Authentifizierungsfehler:
- OAuth-Flow-Fehler
- Ungültige Anmeldedaten
- Token-Ablauf
- API-Authentifizierungsfehler

### DatabaseError

Ausgelöst für Datenbankoperationsfehler:
- SQLite-Fehler
- Datenbankbeschädigung
- Migrationsfehler
- Abfragefehler

### ValidationError

Ausgelöst für Eingabevalidierungsfehler:
- Ungültige Konfigurationswerte
- Fehlerhafte Benutzereingabe
- Ungültige Dateipfade
- URL-Validierungsfehler

### DependencyError

Ausgelöst für externe Abhängigkeitsprobleme:
- Fehlende erforderliche Tools (FFmpeg, MPV, Aria2)
- Tool-Ausführungsfehler
- Versionsinkompatibilitäten
- Installationsfehler

## Fehlercodes

Häufige Fehlercodes, die in der gesamten Anwendung verwendet werden:

| Code | Exception | Beschreibung |
|------|-----------|--------------|
| `PROVIDER_001` | ProviderError | Suche fehlgeschlagen |
| `PROVIDER_002` | ProviderError | Details-Abruf fehlgeschlagen |
| `PROVIDER_003` | ProviderError | Stream-Extraktion fehlgeschlagen |
| `DOWNLOAD_001` | DownloadError | Speicherplatz unzureichend |
| `DOWNLOAD_002` | DownloadError | Download fehlgeschlagen |
| `NETWORK_001` | NetworkError | Verbindungs-Timeout |
| `AUTH_001` | AuthenticationError | OAuth fehlgeschlagen |
| `DB_001` | DatabaseError | Abfrage fehlgeschlagen |
| `VALIDATION_001` | ValidationError | Ungültige Eingabe |
| `DEP_001` | DependencyError | Tool fehlt |

## Best Practices

1. **Spezifische Exceptions verwenden**: Spezifische Exceptions vor allgemeinen abfangen
2. **Fehlercodes einschließen**: Fehlercodes für Protokollierung und Debugging verwenden
3. **Kontext bereitstellen**: Relevante Informationen in Fehlermeldungen einschließen
4. **Graceful behandeln**: Fallback-Verhalten wenn möglich bereitstellen
5. **Fehler protokollieren**: Exceptions mit vollem Kontext für Debugging protokollieren

## API-Referenz

::: weeb_cli.exceptions.WeebCLIError
::: weeb_cli.exceptions.ProviderError
::: weeb_cli.exceptions.DownloadError
::: weeb_cli.exceptions.NetworkError
::: weeb_cli.exceptions.AuthenticationError
::: weeb_cli.exceptions.DatabaseError
::: weeb_cli.exceptions.ValidationError
::: weeb_cli.exceptions.DependencyError
