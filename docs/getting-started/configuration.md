# Configuration Guide

This guide covers all configuration options available in Weeb CLI.

## Configuration Storage

All configuration is stored in a SQLite database at:

```
~/.weeb-cli/weeb.db
```

Configuration can be managed through:
- Interactive settings menu
- Direct database access
- Configuration API

## Accessing Settings

### Interactive Mode

```bash
weeb-cli
# Select "Settings" from main menu
```

### API Mode

```python
from weeb_cli.config import config

# Get value
language = config.get("language")

# Set value
config.set("language", "tr")
```

## Configuration Options

### General Settings

#### Language

Set the UI language.

- **Key**: `language`
- **Values**: `tr`, `en`, `de`, `pl`
- **Default**: `None` (prompts on first run)

```python
config.set("language", "tr")
```

#### Debug Mode

Enable debug logging.

- **Key**: `debug_mode`
- **Values**: `True`, `False`
- **Default**: `False`

```python
config.set("debug_mode", True)
```

#### Show Description

Show anime descriptions in search results.

- **Key**: `show_description`
- **Values**: `True`, `False`
- **Default**: `True`

### Download Settings

#### Download Directory

Set where anime files are downloaded.

- **Key**: `download_dir`
- **Default**: `./weeb-downloads`

```python
config.set("download_dir", "/path/to/downloads")
```

#### Aria2 Settings

Enable Aria2 for fast multi-connection downloads.

- **Key**: `aria2_enabled`
- **Values**: `True`, `False`
- **Default**: `True`

```python
config.set("aria2_enabled", True)
```

Maximum connections per download:

- **Key**: `aria2_max_connections`
- **Values**: `1-32`
- **Default**: `16`

```python
config.set("aria2_max_connections", 16)
```

#### yt-dlp Settings

Enable yt-dlp for complex stream downloads.

- **Key**: `ytdlp_enabled`
- **Values**: `True`, `False`
- **Default**: `True`

```python
config.set("ytdlp_enabled", True)
```

Format string for yt-dlp:

- **Key**: `ytdlp_format`
- **Default**: `"bestvideo+bestaudio/best"`

```python
config.set("ytdlp_format", "bestvideo+bestaudio/best")
```

#### Concurrent Downloads

Maximum number of simultaneous downloads.

- **Key**: `max_concurrent_downloads`
- **Values**: `1-10`
- **Default**: `3`

```python
config.set("max_concurrent_downloads", 3)
```

#### Retry Settings

Maximum retry attempts for failed downloads:

- **Key**: `download_max_retries`
- **Values**: `0-10`
- **Default**: `3`

Delay between retries (seconds):

- **Key**: `download_retry_delay`
- **Values**: `1-60`
- **Default**: `10`

### Provider Settings

#### Default Provider

Set default anime source.

- **Key**: `scraping_source`
- **Values**: Provider names (e.g., `animecix`, `hianime`)
- **Default**: `None` (uses first available for language)

```python
config.set("scraping_source", "animecix")
```

### Integration Settings

#### Discord Rich Presence

Enable Discord integration to show what you're watching.

- **Key**: `discord_rpc_enabled`
- **Values**: `True`, `False`
- **Default**: `True`

```python
config.set("discord_rpc_enabled", True)
```

#### Keyboard Shortcuts

Enable global keyboard shortcuts (experimental).

- **Key**: `shortcuts_enabled`
- **Values**: `True`, `False`
- **Default**: `False`

### Tracker Settings

Tracker credentials are stored securely in the database:

- **AniList**: OAuth token
- **MyAnimeList**: OAuth token
- **Kitsu**: Email and password (hashed)

Configure through Settings → Trackers menu.

## Environment Variables

### WEEB_CLI_CONFIG_DIR

Override configuration directory:

```bash
export WEEB_CLI_CONFIG_DIR="/custom/path"
weeb-cli
```

### WEEB_CLI_DEBUG

Enable debug mode:

```bash
export WEEB_CLI_DEBUG=1
weeb-cli start
```

## Configuration Files

### Database Schema

The SQLite database contains these tables:

- `config`: Key-value configuration
- `progress`: Watch progress
- `search_history`: Search queries
- `download_queue`: Download queue
- `external_drives`: External drive paths
- `anime_index`: Local library index
- `virtual_library`: Online anime bookmarks

### Backup and Restore

#### Backup

```bash
# Through settings menu
Settings → Backup & Restore → Create Backup

# Manual backup
cp ~/.weeb-cli/weeb.db ~/backup/weeb.db
```

#### Restore

```bash
# Through settings menu
Settings → Backup & Restore → Restore Backup

# Manual restore
cp ~/backup/weeb.db ~/.weeb-cli/weeb.db
```

## Advanced Configuration

### Custom Cache Directory

```python
from weeb_cli.services.cache import CacheManager
from pathlib import Path

cache = CacheManager(Path("/custom/cache/dir"))
```

### Custom Download Manager

```python
from weeb_cli.services.downloader import QueueManager

queue = QueueManager()
queue.start_queue()
```

## Troubleshooting

### Reset Configuration

Delete the database to reset all settings:

```bash
rm ~/.weeb-cli/weeb.db
weeb-cli  # Will run setup wizard
```

### View Current Configuration

```python
from weeb_cli.config import config

# Get all config
all_config = config.db.get_all_config()
for key, value in all_config.items():
    print(f"{key}: {value}")
```

### Debug Configuration Issues

Enable debug mode to see configuration loading:

```bash
export WEEB_CLI_DEBUG=1
weeb-cli
```

Check logs at:
```
~/.weeb-cli/logs/debug.log
```

## Best Practices

1. **Backup Regularly**: Backup your database before major updates
2. **Use Aria2**: Enable Aria2 for faster downloads
3. **Adjust Concurrency**: Lower concurrent downloads on slower connections
4. **Enable Trackers**: Sync progress across devices
5. **Clean Cache**: Periodically clean cache in settings

## Next Steps

- [User Guide](../user-guide/searching.md): Learn how to use Weeb CLI
- [API Reference](../api/core/config.md): Configuration API documentation
