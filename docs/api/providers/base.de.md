# Base Provider

::: weeb_cli.providers.base
    options:
      show_root_heading: true
      show_source: true
      heading_level: 2

## Übersicht

Das Base-Provider-Modul definiert die abstrakte Schnittstelle und Datenstrukturen, die alle Anime-Provider implementieren müssen.

## Datenklassen

### AnimeResult

Darstellung des Suchergebnisses.

### Episode

Episodeninformationen mit Metadaten.

### StreamLink

Stream-URL mit Qualitäts- und Serverinformationen.

### AnimeDetails

Vollständige Anime-Informationen einschließlich Episoden.

## BaseProvider-Schnittstelle

Abstrakte Basisklasse, von der alle Provider erben müssen.

### Erforderliche Methoden

- `search()`: Nach Anime suchen
- `get_details()`: Anime-Details abrufen
- `get_episodes()`: Episodenliste abrufen
- `get_streams()`: Stream-URLs extrahieren

### Hilfsmethoden

- `_request()`: HTTP-Anfrage mit Wiederholungslogik

## Implementierungsbeispiel

```python
from weeb_cli.providers.base import BaseProvider, AnimeResult
from weeb_cli.providers.registry import register_provider

@register_provider("myprovider", lang="en", region="US")
class MyProvider(BaseProvider):
    def search(self, query: str) -> List[AnimeResult]:
        # Implementation
        pass
```

## API-Referenz

::: weeb_cli.providers.base.AnimeResult
::: weeb_cli.providers.base.Episode
::: weeb_cli.providers.base.StreamLink
::: weeb_cli.providers.base.AnimeDetails
::: weeb_cli.providers.base.BaseProvider
