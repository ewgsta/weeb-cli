# Database Service

SQLite database management for persistent storage.

## Overview

The database service provides thread-safe SQLite operations for:
- Configuration storage
- Watch progress tracking
- Download queue management
- Local library indexing
- Virtual library bookmarks

## Database Location

```
~/.weeb-cli/weeb.db
```

## Tables

- `config`: Key-value configuration
- `progress`: Watch progress and timestamps
- `search_history`: Recent searches
- `download_queue`: Download queue items
- `external_drives`: External drive paths
- `anime_index`: Local anime index
- `virtual_library`: Online anime bookmarks

## Usage

```python
from weeb_cli.services.database import db

# Configuration
db.set_config("key", "value")
value = db.get_config("key")

# Progress
db.save_progress(slug, title, episode, total)
progress = db.get_progress(slug)

# Queue
db.add_to_queue(item)
queue = db.get_queue()
```

## Thread Safety

Database uses:
- RLock for thread safety
- WAL mode for concurrent access
- Connection pooling
- Automatic retry on busy

## Next Steps

- [API Reference](../overview.md): Full API docs
- [Configuration](../../getting-started/configuration.md): Config guide
