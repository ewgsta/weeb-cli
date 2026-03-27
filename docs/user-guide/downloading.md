# Download Management

Learn how to download anime for offline viewing with Weeb CLI's powerful download system.

## Starting Downloads

### From Search

1. Search for anime
2. Select anime
3. Choose "Download" option
4. Select episodes:
   - Single episode
   - Episode range (e.g., 1-12)
   - All episodes
5. Downloads added to queue

### From Watchlist

1. Main Menu → Watchlist
2. Select anime
3. Choose "Download Episodes"
4. Select episodes

## Download Queue

### Viewing Queue

Main Menu → Downloads

Shows:
- Active downloads with progress
- Pending downloads
- Completed downloads
- Failed downloads

### Queue Information

For each download:
- Anime title and episode
- Progress percentage
- Download speed
- ETA (estimated time)
- Status (pending/processing/completed/failed)

## Managing Downloads

### Pause/Resume

The queue can be:
- Paused: Stops all active downloads
- Resumed: Continues from where stopped

### Retry Failed

If downloads fail:
1. Go to Downloads menu
2. Select "Retry Failed"
3. Failed downloads restart

### Clear Completed

Remove completed downloads from queue:
1. Downloads menu
2. Select "Clear Completed"

## Download Methods

Weeb CLI uses multiple download methods with automatic fallback:

### 1. Aria2 (Fastest)

- Multi-connection downloads
- Resume support
- Progress tracking
- Default: 16 connections

Configure: Settings → Downloads → Aria2 Settings

### 2. yt-dlp

- Complex stream support
- Format selection
- Subtitle download
- Fallback for HLS streams

Configure: Settings → Downloads → yt-dlp Settings

### 3. FFmpeg

- HLS stream conversion
- Format conversion
- Fallback method

### 4. Generic HTTP

- Simple HTTP downloads
- Last resort fallback

## Download Settings

### Concurrent Downloads

Maximum simultaneous downloads:
- Default: 3
- Range: 1-10
- Higher = faster but more resources

Settings → Downloads → Concurrent Downloads

### Download Directory

Set where files are saved:
- Default: `./weeb-downloads`
- Can be any writable directory

Settings → Downloads → Download Directory

### Retry Settings

Configure retry behavior:
- Max retries: 0-10 (default: 3)
- Retry delay: 1-60 seconds (default: 10)

Settings → Downloads → Retry Settings

## File Naming

### Default Format

```
Anime Name - S1E1.mp4
Anime Name - S1E2.mp4
```

### Custom Naming

Files are automatically named:
- Sanitized for filesystem
- Season and episode numbers
- .mp4 extension

## Download Issues

### Insufficient Disk Space

Weeb CLI checks available space before downloading:
- Requires minimum 1GB free
- Shows error if insufficient
- Clears space or change directory

### Download Fails

Common causes:
1. Network interruption
2. Invalid stream URL
3. Provider issues
4. Disk space

Solutions:
1. Retry download
2. Try different quality
3. Try different provider
4. Check logs for details

### Slow Downloads

Improve speed:
1. Enable Aria2
2. Increase max connections
3. Check network speed
4. Try different server

### Resume Interrupted

Downloads automatically resume:
- Aria2 supports resume
- Partial files preserved
- Continues from last byte

## Advanced Features

### Batch Downloads

Download multiple anime:
1. Search and add to queue
2. Repeat for other anime
3. All download concurrently

### Quality Preference

Weeb CLI automatically selects:
- Highest available quality
- Best available server
- Fallback to lower quality if needed

### Progress Notifications

System notifications when:
- Download completes
- Download fails
- Queue finishes

Enable: Settings → Notifications

## Monitoring Downloads

### Real-time Progress

Downloads menu shows:
- Current speed (MB/s)
- Downloaded size / Total size
- Progress bar
- ETA

### Download Statistics

After completion:
- Total downloaded
- Average speed
- Time taken
- Success rate

## Tips

1. Enable Aria2 for fastest downloads
2. Download during off-peak hours
3. Use episode ranges for batch downloads
4. Monitor disk space regularly
5. Retry failed downloads before giving up

## Next Steps

- [Local Library](library.md): Manage downloaded anime
- [Tracker Integration](trackers.md): Sync download progress
- [Configuration](../getting-started/configuration.md): Optimize settings
