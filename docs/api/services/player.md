# Player Service

MPV player integration with IPC monitoring.

## Overview

The player service provides:
- MPV player integration
- IPC socket communication
- Progress monitoring
- Resume functionality

## Player Class

Main player manager.

### Methods

- `play()`: Start playback
- `is_installed()`: Check MPV installation

## Features

### Progress Tracking

- Saves position every 15 seconds
- Auto-marks watched at 80%
- Syncs with trackers

### Resume Support

- Automatically resumes from last position
- Clears position after completion

## Usage

```python
from weeb_cli.services.player import player

# Play stream
player.play(
    url="https://stream-url.m3u8",
    title="Anime - Episode 1",
    anime_title="Anime Name",
    episode_number=1,
    slug="anime-slug"
)
```

## IPC Monitoring

Monitors MPV via IPC socket:
- Current position
- Duration
- Playback status

## Next Steps

- [Streaming Guide](../../user-guide/streaming.md): User guide
- [Configuration](../../getting-started/configuration.md): Settings
