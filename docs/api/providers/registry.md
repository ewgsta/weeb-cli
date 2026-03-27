# Provider Registry

::: weeb_cli.providers.registry
    options:
      show_root_heading: true
      show_source: true
      heading_level: 2

## Overview

The registry module provides dynamic provider discovery and management using a registry pattern.

## Functions

### register_provider

Decorator for registering provider classes.

### get_provider

Get provider instance by name.

### get_providers_for_lang

Get all providers for a language.

### list_providers

List all registered providers.

### get_default_provider

Get default provider for a language.

## Usage Examples

### Registering Provider

```python
from weeb_cli.providers.registry import register_provider

@register_provider("myprovider", lang="en", region="US")
class MyProvider(BaseProvider):
    pass
```

### Getting Provider

```python
from weeb_cli.providers import get_provider

provider = get_provider("animecix")
results = provider.search("anime")
```

### Listing Providers

```python
from weeb_cli.providers import list_providers

providers = list_providers()
for p in providers:
    print(f"{p['name']}: {p['lang']}")
```

## API Reference

::: weeb_cli.providers.registry.register_provider
::: weeb_cli.providers.registry.get_provider
::: weeb_cli.providers.registry.get_providers_for_lang
::: weeb_cli.providers.registry.list_providers
::: weeb_cli.providers.registry.get_default_provider
