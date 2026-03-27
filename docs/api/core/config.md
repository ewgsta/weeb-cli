# Configuration Module

::: weeb_cli.config
    options:
      show_root_heading: true
      show_source: true
      heading_level: 2

## Overview

The configuration module provides centralized settings management for Weeb CLI. All configuration is stored in a SQLite database with fallback to sensible defaults.

## Usage Examples

### Getting Configuration Values

```python
from weeb_cli.config import config

# Get with default fallback
language = config.get("language", "en")
download_dir = config.get("download_dir")
aria2_enabled = config.get("aria2_enabled", True)
```

### Setting Configuration Values

```python
from weeb_cli.config import config

# Set language
config.set("language", "tr")

# Set download directory
config.set("download_dir", "/path/to/downloads")

# Enable/disable features
config.set("discord_rpc_enabled", False)
```

### Headless Mode

For API usage without database access:

```python
from weeb_cli.config import config

# Enable headless mode
config.set_headless(True)

# Now config.get() returns only DEFAULT_CONFIG values
language = config.get("language")  # Returns None (default)
```

## Default Configuration

The following default values are used when no database value exists:

| Key | Default Value | Description |
|-----|---------------|-------------|
| `language` | `None` | UI language (tr, en, de, pl) |
| `aria2_enabled` | `True` | Enable Aria2 for downloads |
| `ytdlp_enabled` | `True` | Enable yt-dlp for downloads |
| `aria2_max_connections` | `16` | Max connections per download |
| `max_concurrent_downloads` | `3` | Max simultaneous downloads |
| `download_dir` | `None` | Download directory path |
| `ytdlp_format` | `"bestvideo+bestaudio/best"` | yt-dlp format string |
| `scraping_source` | `None` | Default provider |
| `show_description` | `True` | Show anime descriptions |
| `debug_mode` | `False` | Enable debug logging |
| `download_max_retries` | `3` | Download retry attempts |
| `download_retry_delay` | `10` | Delay between retries (seconds) |
| `discord_rpc_enabled` | `True` | Enable Discord Rich Presence |
| `shortcuts_enabled` | `False` | Enable keyboard shortcuts |

## Configuration Directory

Configuration and data are stored in:

```
~/.weeb-cli/
├── weeb.db          # SQLite database
├── cache/           # Cached data
├── bin/             # Downloaded dependencies
└── logs/            # Debug logs
```

## API Reference

::: weeb_cli.config.Config
    options:
      show_root_heading: false
      members:
        - get
        - set
        - set_headless
