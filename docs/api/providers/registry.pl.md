# Provider Registry

::: weeb_cli.providers.registry
    options:
      show_root_heading: true
      show_source: true
      heading_level: 2

## Przegląd

Moduł registry zapewnia dynamiczne wykrywanie i zarządzanie dostawcami przy użyciu wzorca rejestru.

## Funkcje

### register_provider

Dekorator do rejestrowania klas dostawców.

### get_provider

Pobierz instancję dostawcy według nazwy.

### get_providers_for_lang

Pobierz wszystkich dostawców dla języka.

### list_providers

Wyświetl wszystkich zarejestrowanych dostawców.

### get_default_provider

Pobierz domyślnego dostawcę dla języka.

## Przykłady użycia

### Rejestrowanie dostawcy

```python
from weeb_cli.providers.registry import register_provider

@register_provider("myprovider", lang="en", region="US")
class MyProvider(BaseProvider):
    pass
```

### Pobieranie dostawcy

```python
from weeb_cli.providers import get_provider

provider = get_provider("animecix")
results = provider.search("anime")
```

### Listowanie dostawców

```python
from weeb_cli.providers import list_providers

providers = list_providers()
for p in providers:
    print(f"{p['name']}: {p['lang']}")
```

## Dokumentacja API

::: weeb_cli.providers.registry.register_provider
::: weeb_cli.providers.registry.get_provider
::: weeb_cli.providers.registry.get_providers_for_lang
::: weeb_cli.providers.registry.list_providers
::: weeb_cli.providers.registry.get_default_provider
