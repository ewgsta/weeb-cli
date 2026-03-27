# Local Library Service

Local anime indexing and management.

## Overview

The local library service provides:
- Automatic anime scanning
- Episode detection
- External drive support
- Tracker synchronization

## Features

### Auto-Scanning

Scans directories for anime:
- Detects anime titles
- Counts episodes
- Matches with trackers

### File Patterns

Supported naming patterns:
- `Anime Name - S1E1.mp4`
- `Anime Name - 01.mp4`
- `Anime Name - Episode 1.mp4`
- `[Group] Anime Name - 01.mp4`

### External Drives

- Register USB drives
- Scan external HDDs
- Portable library

## Usage

```python
from weeb_cli.services.local_library import library

# Scan directory
library.scan_directory("/path/to/anime")

# Get indexed anime
anime_list = library.get_all_anime()

# Search library
results = library.search("Naruto")
```

## Virtual Library

Bookmark online anime:
- No download required
- Quick access
- Organized collection

## Next Steps

- [Library Guide](../../user-guide/library.md): User guide
- [Configuration](../../getting-started/configuration.md): Settings
