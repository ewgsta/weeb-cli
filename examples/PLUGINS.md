# Weeb CLI - Plugin Development Guide

This document explains how to create, build, and install custom source plugins for Weeb CLI.

## Overview

Weeb CLI supports user-created plugins that add custom anime sources. Plugins are distributed as `.weeb-plugin` files (ZIP archives) containing a manifest and provider code.

## Plugin Structure

A plugin directory must have the following structure:

```
my-plugin/
  manifest.json     # Plugin metadata (required)
  provider.py       # Provider implementation (required)
  extractors/       # Custom extractors (optional)
```

## manifest.json

The manifest file defines plugin metadata and entry point information.

### Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Unique plugin identifier. Lowercase, 3-50 chars, allows digits, hyphens, underscores. |
| `version` | string | Semantic version (e.g. `1.0.0`). |
| `lang` | string | 2-letter ISO 639-1 language code (e.g. `tr`, `en`, `de`). |
| `entry_point` | string | Path to the main Python file (e.g. `provider.py`). |
| `entry_class` | string | Name of the class extending `BaseProvider`. |

### Optional Fields

| Field | Type | Description |
|-------|------|-------------|
| `display_name` | string | Human-readable name shown in the UI. |
| `author` | string | Plugin author name. |
| `description` | string | Short description of the plugin. |
| `region` | string | Region code (e.g. `TR`, `US`). |
| `min_weeb_version` | string | Minimum required Weeb CLI version. |
| `permissions` | list | List of permissions. Currently supports: `http`. |
| `homepage` | string | URL to the plugin homepage or repository. |

### Example

```json
{
    "name": "my-source",
    "display_name": "My Source",
    "version": "1.0.0",
    "author": "username",
    "description": "A custom anime source.",
    "lang": "tr",
    "region": "TR",
    "min_weeb_version": "2.12.0",
    "entry_point": "provider.py",
    "entry_class": "MySourceProvider",
    "permissions": ["http"],
    "homepage": "https://github.com/username/my-source"
}
```

## Provider Implementation

Your provider must extend `BaseProvider` and implement four methods:

```python
from typing import List, Optional
from weeb_cli.providers.base import (
    BaseProvider,
    AnimeResult,
    AnimeDetails,
    Episode,
    StreamLink,
)


class MySourceProvider(BaseProvider):

    def __init__(self):
        super().__init__()
        self.base_url = "https://my-anime-site.com"

    def search(self, query: str) -> List[AnimeResult]:
        # Search for anime by query string.
        # Return a list of AnimeResult objects.
        pass

    def get_details(self, anime_id: str) -> Optional[AnimeDetails]:
        # Fetch anime details by ID.
        # Return an AnimeDetails object or None.
        pass

    def get_episodes(self, anime_id: str) -> List[Episode]:
        # Fetch episode list for an anime.
        # Return a list of Episode objects.
        pass

    def get_streams(self, anime_id: str, episode_id: str) -> List[StreamLink]:
        # Fetch stream links for a specific episode.
        # Return a list of StreamLink objects.
        pass
```

### Data Models

**AnimeResult** - Search result item:
- `id` (str): Unique anime identifier
- `title` (str): Anime title
- `type` (str): Type (`series`, `movie`, `ova`, etc.)

**AnimeDetails** - Full anime information:
- `id` (str): Unique identifier
- `title` (str): Title
- `description` (str): Synopsis
- `genres` (list): Genre list
- `year` (int): Release year
- `status` (str): Airing status
- `episodes` (list): Episode list
- `total_episodes` (int): Total episode count

**Episode** - Single episode:
- `id` (str): Episode identifier
- `number` (int): Episode number
- `title` (str): Episode title

**StreamLink** - Video stream:
- `url` (str): Stream URL (m3u8, mp4, etc.)
- `quality` (str): Quality label (e.g. `1080p`, `720p`)
- `server` (str): Server/CDN name

### Making HTTP Requests

Use the built-in `self._request()` method from `BaseProvider` or the `requests` library directly:

```python
import requests
from bs4 import BeautifulSoup

# Using requests directly
response = requests.get(f"{self.base_url}/search?q={query}")
data = response.json()

# Parsing HTML with BeautifulSoup
soup = BeautifulSoup(response.text, "html.parser")
items = soup.select(".anime-card")
```

## Security Sandbox

Plugins run inside a security sandbox. The following restrictions apply:

### Allowed Modules

```
json, re, time, math, string, collections
urllib, urllib.request, urllib.parse
requests, bs4, lxml
hashlib, base64, html, html.parser
typing, dataclasses
xml, xml.etree, xml.etree.ElementTree
weeb_cli.providers.base
weeb_cli.services.logger
```

### Blocked Operations

- `os.system`, `subprocess` - No shell command execution
- `eval()`, `exec()`, `compile()` - No dynamic code execution
- `open()` - No filesystem access
- `socket`, `ctypes`, `cffi` - No low-level access
- `sys.exit`, `shutil` - No system modifications
- `setattr()`, `delattr()` - No attribute manipulation

Any code using blocked operations will be rejected during installation.

## Building a Plugin

Use the included build script to package your plugin:

```bash
# Build from the plugin directory
python examples/build_plugin.py examples/sample-plugin/

# Specify a custom output path
python examples/build_plugin.py my-plugin/ output/my-plugin.weeb-plugin
```

This creates a `.weeb-plugin` file (ZIP archive) ready for distribution.

## Installing a Plugin

1. Open Weeb CLI and go to **Settings**
2. Select **Plugin Manager** (or your locale's equivalent)
3. Choose **Install Plugin**
4. Enter the full path to the `.weeb-plugin` file
5. The plugin will be validated, extracted, and registered

Once installed, the plugin source will appear in the source selection menu as `plugin:<name>`.

## Managing Plugins

From the Plugin Manager menu you can:

- **Enable/Disable** - Toggle a plugin without removing it
- **Uninstall** - Remove a plugin completely

Plugin data is stored in `~/.weeb-cli/plugins/` and plugin records are kept in the SQLite database at `~/.weeb-cli/weeb.db`.

## Sample Plugin

A complete example plugin is available at `examples/sample-plugin/`. Use it as a starting point:

```bash
# Copy the sample
cp -r examples/sample-plugin/ my-new-source/

# Edit manifest.json and provider.py
# ...

# Build
python examples/build_plugin.py my-new-source/

# Install in Weeb CLI
# Settings > Plugin Manager > Install Plugin > enter path
```

## Tips

- Keep your `name` field short and descriptive (e.g. `turkanime`, `aniwatch`)
- Set `min_weeb_version` if your plugin uses features from a specific version
- Test your provider methods individually before building the plugin
- Use `debug()` from `weeb_cli.services.logger` for logging during development
- Check `examples/sample-plugin/` for a working reference
