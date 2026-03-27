# Downloader Service

Queue-based download manager with multiple download methods.

## Overview

The downloader service provides:
- Queue-based download management
- Concurrent downloads
- Multiple download methods (Aria2, yt-dlp, FFmpeg)
- Automatic retry with backoff
- Progress tracking

## QueueManager

Main download queue manager.

### Methods

- `start_queue()`: Start download workers
- `stop_queue()`: Stop all downloads
- `add_to_queue()`: Add episodes to queue
- `retry_failed()`: Retry failed downloads
- `clear_completed()`: Remove completed items

## Download Methods

### Priority Order

1. Aria2 (fastest, multi-connection)
2. yt-dlp (complex streams)
3. FFmpeg (HLS conversion)
4. Generic HTTP (fallback)

## Usage

```python
from weeb_cli.services.downloader import queue_manager

# Start queue
queue_manager.start_queue()

# Add to queue
queue_manager.add_to_queue(
    anime_title="Anime Name",
    episodes=[episode_data],
    slug="anime-slug"
)

# Check status
if queue_manager.is_running():
    print("Queue active")
```

## Configuration

- Max concurrent downloads
- Aria2 connections
- Retry attempts
- Retry delay

## Next Steps

- [Download Guide](../../user-guide/downloading.md): User guide
- [Configuration](../../getting-started/configuration.md): Settings
