# Adding New Providers

Guide for implementing new anime source providers.

## Provider Structure

Providers are organized by language:

```
weeb_cli/providers/
├── base.py              # Base provider interface
├── registry.py          # Provider registration
├── tr/                  # Turkish providers
├── en/                  # English providers
├── de/                  # German providers
└── pl/                  # Polish providers
```

## Implementation Steps

### 1. Create Provider File

Create file in appropriate language directory:

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
    """Provider for MyAnimeSource.com."""
    
    BASE_URL = "https://myanimesource.com"
```

### 2. Implement Search

```python
def search(self, query: str) -> List[AnimeResult]:
    """Search for anime by query."""
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

### 3. Implement Get Details

```python
def get_details(self, anime_id: str) -> Optional[AnimeDetails]:
    """Get anime details."""
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

### 4. Implement Get Episodes

```python
def get_episodes(self, anime_id: str) -> List[Episode]:
    """Get episode list."""
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

### 5. Implement Get Streams

```python
def get_streams(
    self, 
    anime_id: str, 
    episode_id: str
) -> List[StreamLink]:
    """Extract stream URLs."""
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

## Testing Provider

### Manual Testing

```bash
weeb-cli api search "test" --provider myprovider
```

### Unit Tests

```python
# tests/test_myprovider.py

def test_myprovider_search():
    provider = get_provider("myprovider")
    results = provider.search("test")
    assert len(results) > 0
```

## Best Practices

1. Use `_request()` for HTTP calls
2. Handle errors gracefully
3. Return empty lists, not None
4. Include type hints
5. Add docstrings
6. Test thoroughly

## Next Steps

- [Contributing](contributing.md): Submit your provider
- [Testing](testing.md): Write tests
- [Architecture](architecture.md): Understand system
