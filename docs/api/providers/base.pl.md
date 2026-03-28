# Base Provider

::: weeb_cli.providers.base
    options:
      show_root_heading: true
      show_source: true
      heading_level: 2

## Przegląd

Moduł base provider definiuje abstrakcyjny interfejs i struktury danych, które muszą implementować wszyscy dostawcy anime.

## Klasy danych

### AnimeResult

Reprezentacja wyniku wyszukiwania.

### Episode

Informacje o odcinku z metadanymi.

### StreamLink

URL strumienia z informacjami o jakości i serwerze.

### AnimeDetails

Pełne informacje o anime wraz z odcinkami.

## Interfejs BaseProvider

Abstrakcyjna klasa bazowa, z której muszą dziedziczyć wszyscy dostawcy.

### Wymagane metody

- `search()`: Wyszukaj anime
- `get_details()`: Pobierz szczegóły anime
- `get_episodes()`: Pobierz listę odcinków
- `get_streams()`: Wyodrębnij adresy URL strumieni

### Metody pomocnicze

- `_request()`: Żądanie HTTP z logiką ponawiania

## Przykład implementacji

```python
from weeb_cli.providers.base import BaseProvider, AnimeResult
from weeb_cli.providers.registry import register_provider

@register_provider("myprovider", lang="en", region="US")
class MyProvider(BaseProvider):
    def search(self, query: str) -> List[AnimeResult]:
        # Implementation
        pass
```

## Dokumentacja API

::: weeb_cli.providers.base.AnimeResult
::: weeb_cli.providers.base.Episode
::: weeb_cli.providers.base.StreamLink
::: weeb_cli.providers.base.AnimeDetails
::: weeb_cli.providers.base.BaseProvider
