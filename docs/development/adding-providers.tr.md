# Yeni Sağlayıcı Ekleme

Yeni anime kaynak sağlayıcıları uygulamak için rehber.

## Sağlayıcı Yapısı

Sağlayıcılar dile göre düzenlenmiştir:

```
weeb_cli/providers/
├── base.py              # Temel sağlayıcı arayüzü
├── registry.py          # Sağlayıcı kaydı
├── tr/                  # Türkçe sağlayıcılar
├── en/                  # İngilizce sağlayıcılar
├── de/                  # Almanca sağlayıcılar
└── pl/                  # Lehçe sağlayıcılar
```

## Uygulama Adımları

### 1. Sağlayıcı Dosyası Oluştur

Uygun dil dizininde dosya oluşturun:

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
    """MyAnimeSource.com için sağlayıcı."""
    
    BASE_URL = "https://myanimesource.com"
```

### 2. Arama Uygula

```python
def search(self, query: str) -> List[AnimeResult]:
    """Sorguya göre anime ara."""
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

### 3. Detayları Al Uygula

```python
def get_details(self, anime_id: str) -> Optional[AnimeDetails]:
    """Anime detaylarını al."""
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

### 4. Bölümleri Al Uygula

```python
def get_episodes(self, anime_id: str) -> List[Episode]:
    """Bölüm listesini al."""
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

### 5. Yayınları Al Uygula

```python
def get_streams(
    self, 
    anime_id: str, 
    episode_id: str
) -> List[StreamLink]:
    """Yayın URL'lerini çıkar."""
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

## Sağlayıcıyı Test Etme

### Manuel Test

```bash
weeb-cli api search "test" --provider myprovider
```

### Birim Testleri

```python
# tests/test_myprovider.py

def test_myprovider_search():
    provider = get_provider("myprovider")
    results = provider.search("test")
    assert len(results) > 0
```

## En İyi Uygulamalar

1. HTTP çağrıları için `_request()` kullanın
2. Hataları zarif bir şekilde işleyin
3. None değil, boş listeler döndürün
4. Tip ipuçları ekleyin
5. Docstring'ler ekleyin
6. Kapsamlı test edin

## Sonraki Adımlar

- [Katkıda Bulunma](contributing.md): Sağlayıcınızı gönderin
- [Test Etme](testing.md): Testler yazın
- [Mimari](architecture.md): Sistemi anlayın
