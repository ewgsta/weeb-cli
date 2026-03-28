# Przewodnik testowania

Przewodnik po pisaniu i uruchamianiu testów w Weeb CLI.

## Struktura testów

Testy znajdują się w katalogu `tests/`:

```
tests/
├── __init__.py
├── conftest.py              # Fixtures Pytest
├── test_providers.py        # Testy dostawców
├── test_cache.py           # Testy cache
├── test_database.py        # Testy bazy danych
└── ...
```

## Uruchamianie testów

### Wszystkie testy

```bash
pytest
```

### Konkretny plik testowy

```bash
pytest tests/test_providers.py
```

### Konkretny test

```bash
pytest tests/test_providers.py::test_search
```

### Z pokryciem

```bash
pytest --cov=weeb_cli --cov-report=html
```

Zobacz pokrycie: `open htmlcov/index.html`

## Pisanie testów

### Test podstawowy

```python
def test_function():
    result = function()
    assert result == expected
```

### Używanie fixtures

```python
def test_with_fixture(temp_dir):
    # temp_dir dostarczony przez conftest.py
    file_path = temp_dir / "test.txt"
    assert file_path.parent.exists()
```

### Mockowanie

```python
from unittest.mock import Mock, patch

def test_with_mock():
    with patch('module.function') as mock_func:
        mock_func.return_value = "mocked"
        result = call_function()
        assert result == "mocked"
```

## Kategorie testów

### Testy jednostkowe

Testuj pojedyncze funkcje:
```python
def test_sanitize_filename():
    result = sanitize_filename("test/file.txt")
    assert "/" not in result
```

### Testy integracyjne

Testuj interakcję komponentów:
```python
def test_provider_search():
    provider = get_provider("animecix")
    results = provider.search("test")
    assert len(results) > 0
```

### Testy end-to-end

Testuj kompletne przepływy pracy (używaj oszczędnie).

## Najlepsze praktyki

1. Jedna asercja na test, gdy to możliwe
2. Używaj opisowych nazw testów
3. Mockuj zewnętrzne zależności
4. Sprzątaj zasoby
5. Testuj przypadki brzegowe

## Następne kroki

- [Wkład](contributing.md): Przewodnik wkładu
- [Architektura](architecture.md): Projekt systemu
