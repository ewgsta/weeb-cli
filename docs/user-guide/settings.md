# Settings Guide

Complete guide to configuring Weeb CLI for your preferences.

## Accessing Settings

Main Menu → Settings

## General Settings

### Language

Change UI language:
- Turkish (Türkçe)
- English
- German (Deutsch)
- Polish (Polski)

Path: Settings → Configuration → Language

### Default Provider

Set preferred anime source:
- Based on your language
- Can override manually

Path: Settings → Configuration → Default Provider

### Show Descriptions

Toggle anime descriptions in search:
- On: Shows full synopsis
- Off: Compact view

Path: Settings → Configuration → Show Descriptions

### Debug Mode

Enable detailed logging:
- Logs saved to ~/.weeb-cli/logs/
- Useful for troubleshooting
- May impact performance

Path: Settings → Configuration → Debug Mode

## Download Settings

### Download Directory

Set where anime files are saved:
- Default: ./weeb-downloads
- Can be any writable path
- Supports relative and absolute paths

Path: Settings → Downloads → Download Directory

### Aria2 Settings

Configure Aria2 downloader:
- Enable/Disable Aria2
- Max connections (1-32)
- Default: 16 connections

Path: Settings → Downloads → Aria2

### yt-dlp Settings

Configure yt-dlp:
- Enable/Disable yt-dlp
- Format string
- Default: bestvideo+bestaudio/best

Path: Settings → Downloads → yt-dlp

### Concurrent Downloads

Max simultaneous downloads:
- Range: 1-10
- Default: 3
- Higher uses more bandwidth

Path: Settings → Downloads → Concurrent

### Retry Settings

Configure download retries:
- Max retries: 0-10
- Retry delay: 1-60 seconds
- Exponential backoff

Path: Settings → Downloads → Retry

## Tracker Settings

### AniList

Configure AniList integration:
- Authenticate with OAuth
- View connection status
- Disconnect account

Path: Settings → Trackers → AniList

### MyAnimeList

Configure MAL integration:
- Authenticate with OAuth
- View sync status
- Disconnect account

Path: Settings → Trackers → MyAnimeList

### Kitsu

Configure Kitsu integration:
- Login with email/password
- View connection status
- Logout

Path: Settings → Trackers → Kitsu

## Integration Settings

### Discord Rich Presence

Show what you're watching on Discord:
- Enable/Disable
- Shows anime title
- Shows episode number
- Shows elapsed time

Path: Settings → Integrations → Discord RPC

### AniSkip Auto Skip

Automatically skip anime openings and endings:
- Enable/Disable
- Uses AniSkip API
- Fetches skip times from MyAnimeList
- Automatically seeks during playback
- Supports OP, ED, and mixed-OP types

Path: Settings → Integrations → Auto Skip

### Keyboard Shortcuts

Global keyboard shortcuts (experimental):
- Enable/Disable
- Configure hotkeys
- System-wide controls

Path: Settings → Integrations → Shortcuts

## Cache Settings

### View Cache Stats

See cache information:
- Memory entries
- File entries
- Total size

Path: Settings → Cache → Statistics

### Clear Cache

Remove cached data:
- Clear all cache
- Clear provider cache
- Clear search history

Path: Settings → Cache → Clear

### Cache Cleanup

Remove old cache entries:
- Set max age
- Automatic cleanup
- Manual cleanup

Path: Settings → Cache → Cleanup

## External Drives

### Add Drive

Register external drives:
1. Settings → External Drives
2. Select "Add Drive"
3. Enter path
4. Give name

### Manage Drives

- View all drives
- Remove drives
- Rename drives
- Scan drives

Path: Settings → External Drives

## Backup & Restore

### Create Backup

Backup your data:
- Configuration
- Watch progress
- Download queue
- Library index

Path: Settings → Backup → Create Backup

### Restore Backup

Restore from backup:
1. Settings → Backup → Restore
2. Select backup file
3. Confirm restore

Warning: Overwrites current data

## Advanced Settings

### Reset Settings

Reset to defaults:
1. Settings → Advanced
2. Select "Reset All Settings"
3. Confirm reset

Warning: Cannot be undone

### Export Settings

Export configuration:
- JSON format
- Includes all settings
- Excludes credentials

Path: Settings → Advanced → Export

### Import Settings

Import configuration:
1. Settings → Advanced → Import
2. Select JSON file
3. Confirm import

## Configuration File

Settings stored in:
```
~/.weeb-cli/weeb.db
```

SQLite database with tables:
- config
- progress
- download_queue
- external_drives
- anime_index

## Tips

1. Backup before major changes
2. Test settings with single download
3. Enable debug for troubleshooting
4. Use external drives for large collections
5. Sync trackers regularly

## Next Steps

- [Configuration Guide](../getting-started/configuration.md): Detailed config options
- [Download Guide](downloading.md): Optimize downloads
- [Tracker Guide](trackers.md): Setup trackers
