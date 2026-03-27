# Tracker Service

Integration with AniList, MyAnimeList, and Kitsu.

## Overview

The tracker service provides:
- OAuth authentication
- Progress synchronization
- Offline queue
- Automatic matching

## Supported Trackers

### AniList

- OAuth 2.0
- GraphQL API
- Manga and anime

### MyAnimeList

- OAuth 2.0
- REST API
- Comprehensive database

### Kitsu

- Email/password
- JSON API
- Modern interface

## Usage

```python
from weeb_cli.services.tracker import tracker

# Authenticate
tracker.authenticate_anilist()

# Update progress
tracker.update_progress(
    anime_id="123",
    episode=5,
    status="CURRENT"
)

# Sync offline queue
tracker.sync_offline_queue()
```

## Features

- Automatic progress sync
- Offline queue for updates
- Smart anime matching
- Multiple tracker support

## Next Steps

- [Tracker Guide](../../user-guide/trackers.md): User guide
- [Configuration](../../getting-started/configuration.md): Setup
