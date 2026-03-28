# Polscy dostawcy

Polscy dostawcy źródeł anime.

## Dostępni dostawcy

### Docchi

Dostawca dla Docchi.pl

- Polska biblioteka anime
- Polskie napisy
- Wiele serwerów
- Dobra jakość

## Użycie

```python
from weeb_cli.providers import get_provider

# Pobierz dostawcę
provider = get_provider("docchi")

# Wyszukaj
results = provider.search("Naruto")

# Pobierz szczegóły
details = provider.get_details(results[0].id)

# Pobierz strumienie
streams = provider.get_streams(details.id, episode_id)
```

## Szczegóły dostawcy

| Dostawca | Rozmiar biblioteki | Jakość | Prędkość | Napisy |
|----------|-------------|---------|-------|-----------|
| Docchi | Średnia | HD | Średnia | Polski |

## Następne kroki

- [Base Provider](base.md): Interfejs dostawcy
- [Dodawanie dostawców](../../development/adding-providers.md): Utwórz dostawcę
