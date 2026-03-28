# Provider Registry

::: weeb_cli.providers.registry
    options:
      show_root_heading: true
      show_source: true
      heading_level: 2

## Übersicht

Das Registry-Modul bietet dynamische Provider-Erkennung und -Verwaltung unter Verwendung eines Registry-Musters.

## Funktionen

### register_provider

Dekorator zum Registrieren von Provider-Klassen.

### get_provider

Provider-Instanz nach Namen abrufen.

### get_providers_for_lang

Alle Provider für eine Sprache abrufen.

### list_providers

Alle registrierten Provider auflisten.

### get_default_provider

Standard-Provider für eine Sprache abrufen.

## Verwendungsbeispiele

### Provider registrieren

```python
from weeb_cli.providers.registry import register_provider

@register_provider("myprovider", lang="en", region="US")
class MyProvider(BaseProvider):
    pass
```

### Provider abrufen

```python
from weeb_cli.providers import get_provider

provider = get_provider("animecix")
results = provider.search("anime")
```

### Provider auflisten

```python
from weeb_cli.providers import list_providers

providers = list_providers()
for p in providers:
    print(f"{p['name']}: {p['lang']}")
```

## API-Referenz

::: weeb_cli.providers.registry.register_provider
::: weeb_cli.providers.registry.get_provider
::: weeb_cli.providers.registry.get_providers_for_lang
::: weeb_cli.providers.registry.list_providers
::: weeb_cli.providers.registry.get_default_provider
