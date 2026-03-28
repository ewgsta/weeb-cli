# Test-Leitfaden

Leitfaden zum Schreiben und Ausführen von Tests in Weeb CLI.

## Test-Struktur

Tests befinden sich im Verzeichnis `tests/`:

```
tests/
├── __init__.py
├── conftest.py              # Pytest-Fixtures
├── test_providers.py        # Provider-Tests
├── test_cache.py           # Cache-Tests
├── test_database.py        # Datenbank-Tests
└── ...
```

## Tests ausführen

### Alle Tests

```bash
pytest
```

### Spezifische Testdatei

```bash
pytest tests/test_providers.py
```

### Spezifischer Test

```bash
pytest tests/test_providers.py::test_search
```

### Mit Coverage

```bash
pytest --cov=weeb_cli --cov-report=html
```

Coverage anzeigen: `open htmlcov/index.html`

## Tests schreiben

### Basis-Test

```python
def test_function():
    result = function()
    assert result == expected
```

### Fixtures verwenden

```python
def test_with_fixture(temp_dir):
    # temp_dir von conftest.py bereitgestellt
    file_path = temp_dir / "test.txt"
    assert file_path.parent.exists()
```

### Mocking

```python
from unittest.mock import Mock, patch

def test_with_mock():
    with patch('module.function') as mock_func:
        mock_func.return_value = "mocked"
        result = call_function()
        assert result == "mocked"
```

## Test-Kategorien

### Unit-Tests

Einzelne Funktionen testen:
```python
def test_sanitize_filename():
    result = sanitize_filename("test/file.txt")
    assert "/" not in result
```

### Integrationstests

Komponenteninteraktion testen:
```python
def test_provider_search():
    provider = get_provider("animecix")
    results = provider.search("test")
    assert len(results) > 0
```

### End-to-End-Tests

Vollständige Workflows testen (sparsam verwenden).

## Best Practices

1. Wenn möglich eine Assertion pro Test
2. Beschreibende Testnamen verwenden
3. Externe Abhängigkeiten mocken
4. Ressourcen aufräumen
5. Grenzfälle testen

## Nächste Schritte

- [Beitragen](contributing.md): Beitragsleitfaden
- [Architektur](architecture.md): Systemdesign
