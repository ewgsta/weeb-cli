# Streaming Anime

Learn how to stream anime directly in your media player.

## Starting a Stream

### From Search Results

1. Search for anime
2. Select anime from results
3. Choose "Watch" option
4. Select episode
5. Choose quality/server
6. Video opens in MPV player

### From Watchlist

1. Main Menu → Watchlist
2. Select anime
3. Choose episode
4. Stream starts

## Player Controls

### MPV Keyboard Shortcuts

- Space: Play/Pause
- Left/Right Arrow: Seek backward/forward 5 seconds
- Up/Down Arrow: Seek backward/forward 1 minute
- [ / ]: Decrease/Increase playback speed
- m: Mute/Unmute
- f: Toggle fullscreen
- q: Quit player
- s: Take screenshot
- j: Cycle subtitles

### Progress Tracking

Weeb CLI automatically:
- Saves your position every 15 seconds
- Marks episode as watched at 80% completion
- Syncs progress with trackers (if configured)

### Resume Watching

When you reopen an episode:
- Automatically resumes from last position
- Shows resume prompt if near end
- Clears position after completion

## Quality Selection

### Available Qualities

Depends on provider and server:
- 1080p (Full HD)
- 720p (HD)
- 480p (SD)
- 360p (Low)
- Auto (adaptive)

### Choosing Quality

1. After selecting episode
2. Choose from available qualities
3. Higher quality requires faster connection

### Quality Issues

If buffering:
1. Select lower quality
2. Check internet speed
3. Try different server

## Server Selection

### Multiple Servers

Most providers offer multiple servers:
- Primary server (usually fastest)
- Backup servers
- Different hosting services

### Switching Servers

If stream fails:
1. Go back to episode selection
2. Try different server
3. Different servers may have different qualities

## Subtitles

### Subtitle Support

- Embedded subtitles (if available)
- External subtitle files
- Multiple language support

### Subtitle Controls

In MPV:
- j: Cycle through subtitle tracks
- v: Toggle subtitle visibility
- z/x: Adjust subtitle delay

## Streaming Issues

### Video Won't Play

1. Check MPV installation
2. Try different quality/server
3. Check internet connection
4. Verify stream URL is valid

### Buffering

1. Lower quality setting
2. Pause and let buffer
3. Check network speed
4. Try different server

### Audio/Video Sync

1. Use z/x keys to adjust
2. Try different server
3. Report issue if persistent

### No Subtitles

1. Check if provider offers subtitles
2. Try different server
3. Use j key to cycle subtitle tracks

## Advanced Features

### Discord Rich Presence

If enabled, shows on Discord:
- Currently watching anime
- Episode number
- Elapsed time

Enable in: Settings → Integrations → Discord RPC

### Watch Statistics

View your stats:
- Total watch time
- Episodes watched
- Favorite anime
- Watch history

Access: Main Menu → Watchlist → Statistics

## Tips

1. Use fullscreen (f key) for best experience
2. Adjust playback speed with [ ] keys
3. Take screenshots with s key
4. Use arrow keys for quick seeking
5. Enable Discord RPC to share with friends

## Next Steps

- [Download Guide](downloading.md): Download for offline viewing
- [Tracker Integration](trackers.md): Sync your progress
- [Local Library](library.md): Manage downloaded anime
