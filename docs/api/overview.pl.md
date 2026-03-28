# Przegląd dokumentacji API

Witamy w dokumentacji referencyjnej API Weeb CLI. Ta sekcja zapewnia szczegółową dokumentację dla wszystkich modułów, klas i funkcji w bazie kodu.

## Organizacja

Dokumentacja API jest zorganizowana według pakietów:

### Moduły podstawowe

Podstawowe moduły zapewniające fundamentalną funkcjonalność:

- **[Config](core/config.md)**: System zarządzania konfiguracją
- **[I18n](core/i18n.md)**: Internacjonalizacja i lokalizacja
- **[Exceptions](core/exceptions.md)**: Niestandardowa hierarchia wyjątków

### Dostawcy

Implementacje dostawców źródeł anime:

- **[Dostawca bazowy](providers/base.md)**: Abstrakcyjna klasa bazowa i struktury danych
- **[Rejestr](providers/registry.md)**: Wykrywanie i zarządzanie dostawcami
- **[Dostawcy tureccy](providers/turkish.md)**: Animecix, Turkanime, Anizle, Weeb
- **[Dostawcy angielscy](providers/english.md)**: HiAnime, AllAnime
- **[Dostawcy niemieccy](providers/german.md)**: AniWorld
- **[Dostawcy polscy](providers/polish.md)**: Docchi

### Serwisy

Logika biznesowa i podstawowa funkcjonalność:

- **[Database](services/database.md)**: Zarządzanie bazą danych SQLite
- **[Downloader](services/downloader.md)**: System pobierania oparty na kolejce
- **[Tracker](services/tracker.md)**: Integracja AniList, MAL, Kitsu
- **[Player](services/player.md)**: Integracja odtwarzacza MPV
- **[Cache](services/cache.md)**: System buforowania
- **[Local Library](services/local_library.md)**: Zarządzanie lokalnym anime

### Polecenia

Implementacje poleceń CLI:

- **[Polecenia API](commands/api.md)**: Nieinteraktywne API JSON
- **[Wyszukiwanie](commands/search.md)**: Funkcjonalność wyszukiwania anime
- **[Pobieranie](commands/downloads.md)**: Zarządzanie pobieraniem
- **[Lista oglądania](commands/watchlist.md)**: Historia oglądania i postęp

### Komponenty UI

Elementy interfejsu użytkownika terminala:

- **[Menu](ui/menu.md)**: Interaktywny system menu
- **[Prompt](ui/prompt.md)**: Monity wprowadzania użytkownika
- **[Header](ui/header.md)**: Wyświetlanie nagłówka aplikacji

## Szybkie linki

### Typowe zadania

- [Implementacja dostawcy](../development/adding-providers.md)
- [Używanie systemu cache](services/cache.md)
- [Operacje bazy danych](services/database.md)
- [Obsługa błędów](core/exceptions.md)

### Wskazówki typu

Wszystkie moduły używają kompleksowych wskazówek typu dla lepszego wsparcia IDE i przejrzystości kodu:

```python
from typing import List, Optional, Dict

def search(query: str) -> List[AnimeResult]:
    """Wyszukiwanie z pełnymi informacjami o typie."""
    pass
```

### Styl docstring

Używamy docstringów w stylu Google wszędzie:

```python
def function(param: str) -> bool:
    """Krótki opis.
    
    Args:
        param: Opis parametru.
    
    Returns:
        Opis wartości zwracanej.
    
    Example:
        >>> function("test")
        True
    """
    pass
```

## Nawigacja

Użyj paska bocznego, aby nawigować przez dokumentację API. Każda strona zawiera:

- Przegląd modułu
- Sygnatury klas i funkcji
- Szczegółowe opisy
- Przykłady użycia
- Informacje o typach

## Wkład

Znalazłeś problem z dokumentacją? Proszę [otwórz problem](https://github.com/ewgsta/weeb-cli/issues) lub prześlij pull request.
