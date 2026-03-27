# Base Provider

::: weeb_cli.providers.base
    options:
      show_root_heading: true
      show_source: true
      heading_level: 2

## Overview

The base provider module defines the abstract interface and data structures that all anime providers must implement.

## Data Classes

### AnimeResult

Search result representation.

### Episode

Episode information with metadata.

### StreamLink

Stream URL with quality and server information.

### AnimeDetails

Complete anime information including episodes.

## BaseProvider Interface

Abstract base class that all providers must inherit from.

### Required Methods

- `search()`: Search for anime
- `get_details()`: Get anime details
- `get_episodes()`: Get episode list
- `get_streams()`: Extract stream URLs

### Helper Methods

- `_request()`: HTTP request with retry logic

## Implementation Example

```python
from weeb_cli.providers.base import BaseProvider, AnimeResult
from weeb_cli.providers.registry import register_provider

@register_provider("myprovider", lang="en", region="US")
class MyProvider(BaseProvider):
    def search(self, query: str) -> List[AnimeResult]:
        # Implementation
        pass
```

## API Reference

::: weeb_cli.providers.base.AnimeResult
::: weeb_cli.providers.base.Episode
::: weeb_cli.providers.base.StreamLink
::: weeb_cli.providers.base.AnimeDetails
::: weeb_cli.providers.base.BaseProvider
