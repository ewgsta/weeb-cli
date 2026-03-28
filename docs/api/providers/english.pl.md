# Angielscy dostawcy

Angielscy dostawcy źródeł anime.

## Dostępni dostawcy

### HiAnime

Dostawca dla HiAnime.to

- Ogromna biblioteka anime
- Wiele opcji jakości
- Szybkie serwery
- Angielskie napisy i dubbingi

### AllAnime

Dostawca dla AllAnime.to

- Duża kolekcja
- Wiele serwerów
- Jakość HD
- Opcje napisów i dubbingu

## Użycie

```python
from weeb_cli.providers import get_provider

# Pobierz dostawcę
provider = get_provider("hianime")

# Wyszukaj
results = provider.search("Naruto")

# Pobierz szczegóły
details = provider.get_details(results[0].id)

# Pobierz strumienie
streams = provider.get_streams(details.id, episode_id)
```

## Porównanie dostawców

| Dostawca | Rozmiar biblioteki | Jakość | Prędkość | Napisy |
|----------|-------------|---------|-------|-----------|
| HiAnime | Bardzo duża | 1080p | Szybka | Angielski |
| AllAnime | Duża | 1080p | Szybka | Angielski |

## Następne kroki

- [Base Provider](base.md): Interfejs dostawcy
- [Dodawanie dostawców](../../development/adding-providers.md): Utwórz dostawcę
