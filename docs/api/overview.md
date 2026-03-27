# API Reference Overview

Welcome to the Weeb CLI API reference documentation. This section provides detailed documentation for all modules, classes, and functions in the codebase.

## Organization

The API documentation is organized by package:

### Core Modules

Essential modules that provide foundational functionality:

- **[Config](core/config.md)**: Configuration management system
- **[I18n](core/i18n.md)**: Internationalization and localization
- **[Exceptions](core/exceptions.md)**: Custom exception hierarchy

### Providers

Anime source provider implementations:

- **[Base Provider](providers/base.md)**: Abstract base class and data structures
- **[Registry](providers/registry.md)**: Provider discovery and management
- **[Turkish Providers](providers/turkish.md)**: Animecix, Turkanime, Anizle, Weeb
- **[English Providers](providers/english.md)**: HiAnime, AllAnime
- **[German Providers](providers/german.md)**: AniWorld
- **[Polish Providers](providers/polish.md)**: Docchi

### Services

Business logic and core functionality:

- **[Database](services/database.md)**: SQLite database management
- **[Downloader](services/downloader.md)**: Queue-based download system
- **[Tracker](services/tracker.md)**: AniList, MAL, Kitsu integration
- **[Player](services/player.md)**: MPV player integration
- **[Cache](services/cache.md)**: Caching system
- **[Local Library](services/local_library.md)**: Local anime management

### Commands

CLI command implementations:

- **[API Commands](commands/api.md)**: Non-interactive JSON API
- **[Search](commands/search.md)**: Anime search functionality
- **[Downloads](commands/downloads.md)**: Download management
- **[Watchlist](commands/watchlist.md)**: Watch history and progress

### UI Components

Terminal user interface elements:

- **[Menu](ui/menu.md)**: Interactive menu system
- **[Prompt](ui/prompt.md)**: User input prompts
- **[Header](ui/header.md)**: Application header display

## Quick Links

### Common Tasks

- [Implementing a Provider](../development/adding-providers.md)
- [Using the Cache System](services/cache.md)
- [Database Operations](services/database.md)
- [Error Handling](core/exceptions.md)

### Type Hints

All modules use comprehensive type hints for better IDE support and code clarity:

```python
from typing import List, Optional, Dict

def search(query: str) -> List[AnimeResult]:
    """Search with full type information."""
    pass
```

### Docstring Style

We use Google-style docstrings throughout:

```python
def function(param: str) -> bool:
    """Short description.
    
    Args:
        param: Parameter description.
    
    Returns:
        Return value description.
    
    Example:
        >>> function("test")
        True
    """
    pass
```

## Navigation

Use the sidebar to navigate through the API documentation. Each page includes:

- Module overview
- Class and function signatures
- Detailed descriptions
- Usage examples
- Type information

## Contributing

Found an issue with the documentation? Please [open an issue](https://github.com/ewgsta/weeb-cli/issues) or submit a pull request.
