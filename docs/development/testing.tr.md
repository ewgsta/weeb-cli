# Test Rehberi

Weeb CLI'de test yazma ve çalıştırma rehberi.

## Test Yapısı

Testler `tests/` dizininde bulunur:

```
tests/
├── __init__.py
├── conftest.py              # Pytest fixture'ları
├── test_providers.py        # Sağlayıcı testleri
├── test_cache.py           # Önbellek testleri
├── test_database.py        # Veritabanı testleri
└── ...
```

## Testleri Çalıştırma

### Tüm Testler

```bash
pytest
```

### Belirli Test Dosyası

```bash
pytest tests/test_providers.py
```

### Belirli Test

```bash
pytest tests/test_providers.py::test_search
```

### Kapsam İle

```bash
pytest --cov=weeb_cli --cov-report=html
```

Kapsamı görüntüle: `open htmlcov/index.html`

## Test Yazma

### Temel Test

```python
def test_function():
    result = function()
    assert result == expected
```

### Fixture'ları Kullanma

```python
def test_with_fixture(temp_dir):
    # temp_dir conftest.py tarafından sağlanır
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

## Test Kategorileri

### Birim Testleri

Bireysel fonksiyonları test edin:
```python
def test_sanitize_filename():
    result = sanitize_filename("test/file.txt")
    assert "/" not in result
```

### Entegrasyon Testleri

Bileşen etkileşimini test edin:
```python
def test_provider_search():
    provider = get_provider("animecix")
    results = provider.search("test")
    assert len(results) > 0
```

### Uçtan Uca Testler

Tam iş akışlarını test edin (az kullanın).

## En İyi Uygulamalar

1. Mümkün olduğunda test başına bir iddia
2. Açıklayıcı test adları kullanın
3. Harici bağımlılıkları mock'layın
4. Kaynakları temizleyin
5. Uç durumları test edin

## Sonraki Adımlar

- [Katkıda Bulunma](contributing.md): Katkı rehberi
- [Mimari](architecture.md): Sistem tasarımı
