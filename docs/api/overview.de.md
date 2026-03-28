# API-Referenz-Übersicht

Willkommen zur Weeb CLI API-Referenzdokumentation. Dieser Abschnitt bietet detaillierte Dokumentation für alle Module, Klassen und Funktionen in der Codebasis.

## Organisation

Die API-Dokumentation ist nach Paketen organisiert:

### Kern-Module

Wesentliche Module, die grundlegende Funktionalität bieten:

- **[Config](core/config.md)**: Konfigurationsverwaltungssystem
- **[I18n](core/i18n.md)**: Internationalisierung und Lokalisierung
- **[Exceptions](core/exceptions.md)**: Benutzerdefinierte Exception-Hierarchie

### Provider

Anime-Quellen-Provider-Implementierungen:

- **[Basis-Provider](providers/base.md)**: Abstrakte Basisklasse und Datenstrukturen
- **[Registry](providers/registry.md)**: Provider-Erkennung und -Verwaltung
- **[Türkische Provider](providers/turkish.md)**: Animecix, Turkanime, Anizle, Weeb
- **[Englische Provider](providers/english.md)**: HiAnime, AllAnime
- **[Deutsche Provider](providers/german.md)**: AniWorld
- **[Polnische Provider](providers/polish.md)**: Docchi

### Services

Geschäftslogik und Kernfunktionalität:

- **[Database](services/database.md)**: SQLite-Datenbankverwaltung
- **[Downloader](services/downloader.md)**: Warteschlangenbasiertes Download-System
- **[Tracker](services/tracker.md)**: AniList-, MAL-, Kitsu-Integration
- **[Player](services/player.md)**: MPV-Player-Integration
- **[Cache](services/cache.md)**: Caching-System
- **[Local Library](services/local_library.md)**: Lokale Anime-Verwaltung

### Befehle

CLI-Befehlsimplementierungen:

- **[API-Befehle](commands/api.md)**: Nicht-interaktive JSON-API
- **[Suche](commands/search.md)**: Anime-Suchfunktionalität
- **[Downloads](commands/downloads.md)**: Download-Verwaltung
- **[Watchlist](commands/watchlist.md)**: Wiedergabeverlauf und Fortschritt

### UI-Komponenten

Terminal-Benutzeroberflächenelemente:

- **[Menü](ui/menu.md)**: Interaktives Menüsystem
- **[Prompt](ui/prompt.md)**: Benutzereingabe-Prompts
- **[Header](ui/header.md)**: Anwendungsheader-Anzeige

## Schnelllinks

### Häufige Aufgaben

- [Provider implementieren](../development/adding-providers.md)
- [Cache-System verwenden](services/cache.md)
- [Datenbankoperationen](services/database.md)
- [Fehlerbehandlung](core/exceptions.md)

### Typ-Hinweise

Alle Module verwenden umfassende Typ-Hinweise für bessere IDE-Unterstützung und Code-Klarheit:

```python
from typing import List, Optional, Dict

def search(query: str) -> List[AnimeResult]:
    """Suche mit vollständigen Typ-Informationen."""
    pass
```

### Docstring-Stil

Wir verwenden durchgehend Google-Stil-Docstrings:

```python
def function(param: str) -> bool:
    """Kurze Beschreibung.
    
    Args:
        param: Parameter-Beschreibung.
    
    Returns:
        Rückgabewert-Beschreibung.
    
    Example:
        >>> function("test")
        True
    """
    pass
```

## Navigation

Verwenden Sie die Seitenleiste, um durch die API-Dokumentation zu navigieren. Jede Seite enthält:

- Modul-Übersicht
- Klassen- und Funktionssignaturen
- Detaillierte Beschreibungen
- Verwendungsbeispiele
- Typ-Informationen

## Beitragen

Problem mit der Dokumentation gefunden? Bitte [öffnen Sie ein Issue](https://github.com/ewgsta/weeb-cli/issues) oder reichen Sie einen Pull Request ein.
