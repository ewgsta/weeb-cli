# Cache Service

::: weeb_cli.services.cache
    options:
      show_root_heading: true
      show_source: true
      heading_level: 2

## Overview

Two-tier caching system with memory and file-based storage for improved performance.

## CacheManager

Main cache manager class.

### Methods

- `get()`: Retrieve cached value
- `set()`: Store value in cache
- `delete()`: Remove cached value
- `clear()`: Clear all cache
- `clear_pattern()`: Clear by pattern
- `invalidate_provider()`: Clear provider cache
- `cleanup()`: Remove expired entries
- `get_stats()`: Get cache statistics

## Usage Examples

### Basic Caching

```python
from weeb_cli.services.cache import get_cache

cache = get_cache()

# Store
cache.set("key", {"data": "value"})

# Retrieve
data = cache.get("key", max_age=3600)
```

### Using Decorator

```python
from weeb_cli.services.cache import cached

@cached(max_age=1800)
def expensive_function(param):
    # Result cached for 30 minutes
    return compute_result(param)
```

## API Reference

::: weeb_cli.services.cache.CacheManager
::: weeb_cli.services.cache.cached
::: weeb_cli.services.cache.get_cache
