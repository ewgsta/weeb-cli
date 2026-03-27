# Quick Start Guide

This guide will help you get started with Weeb CLI in just a few minutes.

## First Run

When you run Weeb CLI for the first time, you'll be guided through a setup wizard:

```bash
weeb-cli
```

### Setup Wizard

1. **Language Selection**: Choose your preferred language (Turkish, English, German, or Polish)
2. **Download Directory**: Set where anime files will be downloaded
3. **Provider Selection**: Choose your default anime source
4. **Optional Settings**: Configure trackers, Discord RPC, etc.

## Basic Usage

### Searching for Anime

1. From the main menu, select "Search Anime"
2. Enter the anime name
3. Browse search results
4. Select an anime to view details

### Streaming

1. After selecting an anime, choose "Watch"
2. Select an episode
3. Choose stream quality
4. The video will open in MPV player

### Downloading

1. After selecting an anime, choose "Download"
2. Select episodes to download (single, range, or all)
3. Downloads are added to the queue
4. Monitor progress from "Downloads" menu

### Managing Downloads

Access the downloads menu to:

- View active downloads with progress
- Pause/resume downloads
- Retry failed downloads
- Clear completed downloads

## Common Tasks

### Viewing Watch History

```
Main Menu → Watchlist → View History
```

Your watch history shows:
- Recently watched anime
- Episode progress
- Completion status

### Configuring Trackers

```
Main Menu → Settings → Trackers
```

Connect your accounts:
- AniList (OAuth)
- MyAnimeList (OAuth)
- Kitsu (Email/Password)

Progress syncs automatically when watching or downloading.

### Managing Local Library

```
Main Menu → Library → Scan Library
```

Weeb CLI can index your downloaded anime:
- Auto-detect anime from filenames
- Sync with trackers
- Browse offline content

## Keyboard Shortcuts

- `Ctrl+C`: Cancel current operation / Go back
- `↑/↓`: Navigate menus
- `Enter`: Select option
- `Space`: Toggle selection (multi-select)

## API Mode

For scripting and automation:

```bash
# Search anime
weeb-cli api search "One Piece" --provider animecix

# Get episodes
weeb-cli api episodes <anime-id> --provider animecix

# Get stream links
weeb-cli api streams <anime-id> <episode-id> --provider animecix
```

Output is in JSON format for easy parsing.

## Tips

1. **Resume Watching**: Weeb CLI automatically saves your position. Just select the same episode to continue.

2. **Quality Selection**: Higher quality streams may buffer on slower connections. Try a lower quality if experiencing issues.

3. **Download Queue**: You can queue multiple anime and episodes. They'll download concurrently based on your settings.

4. **External Drives**: Add external drives in settings to scan anime from USB drives or external HDDs.

5. **Offline Mode**: Downloaded anime and local library work without internet connection.

## Troubleshooting

### Video Won't Play
- Ensure MPV is installed (auto-installed on first run)
- Check your internet connection
- Try a different stream quality or server

### Download Fails
- Check available disk space
- Verify internet connection
- Try a different provider
- Check download settings (Aria2/yt-dlp)

### Tracker Not Syncing
- Re-authenticate in Settings → Trackers
- Check internet connection
- Verify anime title matches tracker database

## Next Steps

- [Configuration Guide](configuration.md): Customize Weeb CLI
- [User Guide](../user-guide/searching.md): Detailed feature documentation
- [CLI Reference](../cli/commands.md): Command-line options
