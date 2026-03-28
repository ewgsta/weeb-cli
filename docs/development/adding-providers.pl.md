# Dodawanie nowych dostawców

Przewodnik po implementacji nowych dostawców źródeł anime.

## Struktura dostawcy

Dostawcy są zorganizowani według języka:

```
weeb_cli/providers/
├── base.py              # Interfejs bazowego dostawcy
├── registry.py          # Rejestracja dostawcy
├── tr/                  # Dostawcy tureccy
├── en/                  # Dostawcy angielscy
├── de/                  # Dostawcy niemieccy
└── pl/                  # Dostawcy polscy
```

## Kroki implementacji

### 1. Utwórz plik dostawcy

Utwórz plik w odpowiednim katalogu językowym:

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
    """Dostawca dla MyAnimeSource.com."""
    
    BASE_URL = "https://myanimesource.com"
```

### 2. Zaimplementuj wyszukiwanie

```python
def search(self, query: str) -> List[AnimeResult]:
    """Wyszukaj anime według zapytania."""
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

### 3. Zaimplementuj pobieranie szczegółów

```python
def get_details(self, anime_id: str) -> Optional[AnimeDetails]:
    """Pobierz szczegóły anime."""
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

### 4. Zaimplementuj pobieranie odcinków

```python
def get_episodes(self, anime_id: str) -> List[Episode]:
    """Pobierz listę odcinków."""
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

### 5. Zaimplementuj pobieranie strumieni

```python
def get_streams(
    self, 
    anime_id: str, 
    episode_id: str
) -> List[StreamLink]:
    """Wyodrębnij adresy URL strumieni."""
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

## Testowanie dostawcy

### Testowanie ręczne

```bash
weeb-cli api search "test" --provider myprovider
```

### Testy jednostkowe

```python
# tests/test_myprovider.py

def test_myprovider_search():
    provider = get_provider("myprovider")
    results = provider.search("test")
    assert len(results) > 0
```

## Najlepsze praktyki

1. Używaj `_request()` do wywołań HTTP
2. Obsługuj błędy łagodnie
3. Zwracaj puste listy, nie None
4. Dołącz wskazówki typu
5. Dodaj docstringi
6. Testuj dokładnie

## Następne kroki

- [Wkład](contributing.md): Prześlij swojego dostawcę
- [Testowanie](testing.md): Napisz testy
- [Architektura](architecture.md): Zrozum system
