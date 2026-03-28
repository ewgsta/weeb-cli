# Wkład w Weeb CLI

Dziękujemy za zainteresowanie wkładem w Weeb CLI! Ten przewodnik pomoże Ci zacząć.

## Konfiguracja rozwoju

### Wymagania wstępne

- Python 3.8 lub nowszy
- Git
- pip lub pipenv

### Klonowanie i instalacja

```bash
# Sklonuj repozytorium
git clone https://github.com/ewgsta/weeb-cli.git
cd weeb-cli

# Zainstaluj w trybie edytowalnym
pip install -e .

# Zainstaluj zależności deweloperskie
pip install -r requirements.txt
```

### Uruchamianie testów

```bash
# Uruchom wszystkie testy
pytest

# Uruchom z pokryciem
pytest --cov=weeb_cli --cov-report=html

# Uruchom konkretny plik testowy
pytest tests/test_providers.py
```

## Styl kodu

### Przewodnik stylu Python

Przestrzegamy PEP 8 z pewnymi modyfikacjami:

- Długość linii: 100 znaków (nie 79)
- Używaj wskazówek typu dla wszystkich sygnatur funkcji
- Używaj docstringów (styl Google) dla wszystkich publicznych funkcji i klas

### Wskazówki typu

Wszystkie funkcje powinny mieć wskazówki typu:

```python
def search(self, query: str) -> List[AnimeResult]:
    """Wyszukaj anime według zapytania.
    
    Args:
        query: Ciąg zapytania wyszukiwania.
    
    Returns:
        Lista wyników wyszukiwania anime.
    """
    pass
```

### Docstringi

Używaj docstringów w stylu Google:

```python
def function_name(param1: str, param2: int) -> bool:
    """Krótki opis.
    
    Dłuższy opis w razie potrzeby.
    
    Args:
        param1: Opis param1.
        param2: Opis param2.
    
    Returns:
        Opis wartości zwracanej.
    
    Raises:
        ValueError: Gdy param1 jest nieprawidłowy.
    
    Example:
        >>> function_name("test", 42)
        True
    """
    pass
```

## Dodawanie nowego dostawcy

### 1. Utwórz plik dostawcy

Utwórz nowy plik w odpowiednim katalogu językowym:

```
weeb_cli/providers/<lang>/<nazwa_dostawcy>.py
```

### 2. Zaimplementuj klasę dostawcy

```python
from weeb_cli.providers.base import BaseProvider, AnimeResult, AnimeDetails, Episode, StreamLink
from weeb_cli.providers.registry import register_provider
from typing import List, Optional

@register_provider("myprovider", lang="en", region="US")
class MyProvider(BaseProvider):
    """Dostawca dla MyAnimeSource.com.
    
    Zapewnia treści anime z MyAnimeSource z wyszukiwaniem,
    szczegółami i ekstrakcją strumieni.
    """
    
    BASE_URL = "https://myanimesource.com"
    
    def search(self, query: str) -> List[AnimeResult]:
        """Wyszukaj anime."""
        # Implementacja
        pass
    
    def get_details(self, anime_id: str) -> Optional[AnimeDetails]:
        """Pobierz szczegóły anime."""
        # Implementacja
        pass
    
    def get_episodes(self, anime_id: str) -> List[Episode]:
        """Pobierz listę odcinków."""
        # Implementacja
        pass
    
    def get_streams(self, anime_id: str, episode_id: str) -> List[StreamLink]:
        """Wyodrębnij adresy URL strumieni."""
        # Implementacja
        pass
```

### 3. Dodaj testy

Utwórz plik testowy w `tests/`:

```python
import pytest
from weeb_cli.providers import get_provider

def test_myprovider_search():
    provider = get_provider("myprovider")
    results = provider.search("test")
    assert len(results) > 0
    assert results[0].title is not None
```

### 4. Zaktualizuj dokumentację

Dodaj dokumentację dostawcy w `docs/api/providers/`.

## Proces Pull Request

### 1. Utwórz gałąź

```bash
git checkout -b feature/moja-nowa-funkcja
```

### 2. Wprowadź zmiany

- Pisz kod zgodnie z wytycznymi stylu
- Dodaj wskazówki typu i docstringi
- Napisz testy dla nowej funkcjonalności
- Zaktualizuj dokumentację

### 3. Przetestuj swoje zmiany

```bash
# Uruchom testy
pytest

# Sprawdź styl kodu
flake8 weeb_cli/

# Sprawdzanie typu (opcjonalne)
mypy weeb_cli/
```

### 4. Zatwierdź zmiany

Używaj konwencjonalnych komunikatów commit:

```bash
git commit -m "feat: dodaj nowego dostawcę dla XYZ"
git commit -m "fix: rozwiąż problem z ekstrakcją strumienia"
git commit -m "docs: zaktualizuj przewodnik instalacji"
```

Typy commitów:
- `feat`: Nowa funkcja
- `fix`: Poprawka błędu
- `docs`: Zmiany w dokumentacji
- `style`: Zmiany stylu kodu (formatowanie)
- `refactor`: Refaktoryzacja kodu
- `test`: Dodawanie lub aktualizacja testów
- `chore`: Zadania konserwacyjne

### 5. Wypchnij i utwórz PR

```bash
git push origin feature/moja-nowa-funkcja
```

Następnie utwórz Pull Request na GitHub z:
- Jasnym opisem zmian
- Odniesieniem do powiązanych problemów
- Zrzutami ekranu (jeśli zmiany UI)

## Przegląd kodu

Wszystkie zgłoszenia wymagają przeglądu. Przejrzymy Twój PR i możemy poprosić o zmiany. Prosimy o cierpliwość i reagowanie na opinie.

## Wytyczne społeczności

- Bądź pełen szacunku i konstruktywny
- Pomagaj innym w dyskusjach
- Zgłaszaj błędy ze szczegółowymi informacjami
- Sugeruj funkcje z jasnymi przypadkami użycia

## Pytania?

- Otwórz problem dla błędów lub próśb o funkcje
- Rozpocznij dyskusję dla pytań
- Sprawdź istniejące problemy przed utworzeniem nowych

Dziękujemy za wkład w Weeb CLI!
