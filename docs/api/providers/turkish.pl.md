# Tureccy dostawcy

Tureccy dostawcy źródeł anime.

## Dostępni dostawcy

### Animecix

Dostawca dla Animecix.net

- Duża biblioteka anime
- Tureckie napisy
- Wiele serwerów
- Jakość HD

### Turkanime

Dostawca dla TurkAnime.co

- Obszerna kolekcja
- Tureckie dubbingi i napisy
- Wiele opcji jakości

### Anizle

Dostawca dla Anizle.com

- Nowoczesny interfejs
- Szybkie serwery
- Strumienie HD

### Weeb

Dostawca dla Weeb.com.tr

- Tureckie treści
- Wiele serwerów
- Dobra jakość

## Użycie

```python
from weeb_cli.providers import get_provider

# Pobierz dostawcę
provider = get_provider("animecix")

# Wyszukaj
results = provider.search("One Piece")

# Pobierz szczegóły
details = provider.get_details(results[0].id)

# Pobierz strumienie
streams = provider.get_streams(details.id, episode_id)
```

## Porównanie dostawców

| Dostawca | Rozmiar biblioteki | Jakość | Prędkość | Napisy |
|----------|-------------|---------|-------|-----------|
| Animecix | Duża | HD | Szybka | Turecki |
| Turkanime | Duża | HD | Średnia | Turecki |
| Anizle | Średnia | HD | Szybka | Turecki |
| Weeb | Średnia | HD | Średnia | Turecki |

## Następne kroki

- [Base Provider](base.md): Interfejs dostawcy
- [Dodawanie dostawców](../../development/adding-providers.md): Utwórz dostawcę
