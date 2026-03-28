# Niemieccy dostawcy

Niemieccy dostawcy źródeł anime.

## Dostępni dostawcy

### AniWorld

Dostawca dla AniWorld.to

- Duża niemiecka biblioteka anime
- Niemieckie dubbingi i napisy
- Wiele opcji jakości
- Szybkie serwery

## Użycie

```python
from weeb_cli.providers import get_provider

# Pobierz dostawcę
provider = get_provider("aniworld")

# Wyszukaj
results = provider.search("One Piece")

# Pobierz szczegóły
details = provider.get_details(results[0].id)

# Pobierz strumienie
streams = provider.get_streams(details.id, episode_id)
```

## Szczegóły dostawcy

| Dostawca | Rozmiar biblioteki | Jakość | Prędkość | Napisy |
|----------|-------------|---------|-------|-----------|
| AniWorld | Duża | HD | Szybka | Niemiecki |

## Następne kroki

- [Base Provider](base.md): Interfejs dostawcy
- [Dodawanie dostawców](../../development/adding-providers.md): Utwórz dostawcę
