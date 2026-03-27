# Testing Guide

Guide for writing and running tests in Weeb CLI.

## Test Structure

Tests are located in `tests/` directory:

```
tests/
├── __init__.py
├── conftest.py              # Pytest fixtures
├── test_providers.py        # Provider tests
├── test_cache.py           # Cache tests
├── test_database.py        # Database tests
└── ...
```

## Running Tests

### All Tests

```bash
pytest
```

### Specific Test File

```bash
pytest tests/test_providers.py
```

### Specific Test

```bash
pytest tests/test_providers.py::test_search
```

### With Coverage

```bash
pytest --cov=weeb_cli --cov-report=html
```

View coverage: `open htmlcov/index.html`

## Writing Tests

### Basic Test

```python
def test_function():
    result = function()
    assert result == expected
```

### Using Fixtures

```python
def test_with_fixture(temp_dir):
    # temp_dir provided by conftest.py
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

## Test Categories

### Unit Tests

Test individual functions:
```python
def test_sanitize_filename():
    result = sanitize_filename("test/file.txt")
    assert "/" not in result
```

### Integration Tests

Test component interaction:
```python
def test_provider_search():
    provider = get_provider("animecix")
    results = provider.search("test")
    assert len(results) > 0
```

### End-to-End Tests

Test complete workflows (use sparingly).

## Best Practices

1. One assertion per test when possible
2. Use descriptive test names
3. Mock external dependencies
4. Clean up resources
5. Test edge cases

## Next Steps

- [Contributing](contributing.md): Contribution guide
- [Architecture](architecture.md): System design
