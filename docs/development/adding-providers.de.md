# Neue Provider hinzufügen

Leitfaden zur Implementierung neuer Anime-Quellen-Provider.

## Provider-Struktur

Provider sind nach Sprache organisiert:

```
weeb_cli/providers/
├── base.py              # Basis-Provider-Schnittstelle
├── registry.py          # Provider-Registrierung
├── tr/                  # Türkische Provider
├── en/                  # Englische Provider
├── de/                  # Deutsche Provider
└── pl/                  # Polnische Provider
```

## Implementierungsschritte

### 1. Provider-Datei erstellen

Datei im entsprechenden Sprachverzeichnis erstellen:

```python
# weeb_cli/providers/en/myprovider.py

from weeb_cli.providers.base import (
    BaseProvider,
    AnimeResult,
    AnimeDetails,
    Episode,
    StreamLink
)
from weeb_cli.providers.registry import register_provider
from typing import List, Optional

@register_provider("myprovider", lang="en", region="US")
class MyProvider(BaseProvider):
    """Provider für MyAnimeSource.com."""
    
    BASE_URL = "https://myanimesource.com"
```

### 2. Suche implementieren

```python
def search(self, query: str) -> List[AnimeResult]:
    """Nach Anime nach Abfrage suchen."""
    url = f"{self.BASE_URL}/search"
    data = self._request(url, params={"q": query})
    
    results = []
    for item in data.get("results", []):
        results.append(AnimeResult(
            id=item["id"],
            title=item["title"],
            type=item.get("type", "series"),
            cover=item.get("cover"),
            year=item.get("year")
        ))
    
    return results
```

### 3. Details abrufen implementieren

```python
def get_details(self, anime_id: str) -> Optional[AnimeDetails]:
    """Anime-Details abrufen."""
    url = f"{self.BASE_URL}/anime/{anime_id}"
    data = self._request(url)
    
    if not data:
        return None
    
    return AnimeDetails(
        id=anime_id,
        title=data["title"],
        description=data.get("description"),
        cover=data.get("cover"),
        genres=data.get("genres", []),
        year=data.get("year"),
        status=data.get("status")
    )
```

### 4. Episoden abrufen implementieren

```python
def get_episodes(self, anime_id: str) -> List[Episode]:
    """Episodenliste abrufen."""
    url = f"{self.BASE_URL}/anime/{anime_id}/episodes"
    data = self._request(url)
    
    episodes = []
    for ep in data.get("episodes", []):
        episodes.append(Episode(
            id=ep["id"],
            number=ep["number"],
            title=ep.get("title"),
            season=ep.get("season", 1)
        ))
    
    return episodes
```

### 5. Streams abrufen implementieren

```python
def get_streams(
    self, 
    anime_id: str, 
    episode_id: str
) -> List[StreamLink]:
    """Stream-URLs extrahieren."""
    url = f"{self.BASE_URL}/watch/{episode_id}"
    data = self._request(url)
    
    streams = []
    for stream in data.get("streams", []):
        streams.append(StreamLink(
            url=stream["url"],
            quality=stream.get("quality", "auto"),
            server=stream.get("server", "default"),
            headers=stream.get("headers", {})
        ))
    
    return streams
```

## Provider testen

### Manuelles Testen

```bash
weeb-cli api search "test" --provider myprovider
```

### Unit-Tests

```python
# tests/test_myprovider.py

def test_myprovider_search():
    provider = get_provider("myprovider")
    results = provider.search("test")
    assert len(results) > 0
```

## Best Practices

1. `_request()` für HTTP-Aufrufe verwenden
2. Fehler graceful behandeln
3. Leere Listen zurückgeben, nicht None
4. Typ-Hinweise einschließen
5. Docstrings hinzufügen
6. Gründlich testen

## Nächste Schritte

- [Beitragen](contributing.md): Provider einreichen
- [Testen](testing.md): Tests schreiben
- [Architektur](architecture.md): System verstehen
