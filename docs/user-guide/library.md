# Local Library Management

Manage your downloaded anime collection with Weeb CLI's local library features.

## Overview

The local library allows you to:
- Index downloaded anime
- Browse offline content
- Sync with trackers
- Manage external drives

## Scanning Library

### Auto-Scan

Weeb CLI automatically scans your download directory:

1. Main Menu → Library
2. Select "Scan Library"
3. Wait for scan to complete

### Scan Results

Shows:
- Detected anime titles
- Episode counts
- Source location
- Tracker match status

### File Format

For best results, use this format:

```
Anime Name - S1E1.mp4
Anime Name - S1E2.mp4
Anime Name - S2E1.mp4
```

Supported patterns:
- `Anime Name - S1E1.mp4`
- `Anime Name - 01.mp4`
- `Anime Name - Episode 1.mp4`
- `[Group] Anime Name - 01.mp4`

## External Drives

### Adding Drives

Add USB drives or external HDDs:

1. Settings → External Drives
2. Select "Add Drive"
3. Enter drive path
4. Give it a name

### Scanning Drives

1. Library → External Drives
2. Select drive
3. Choose "Scan Drive"

### Drive Management

- View all registered drives
- Remove drives
- Rename drives
- Scan individual drives

## Virtual Library

### What is Virtual Library?

Bookmark online anime for quick access:
- No download required
- Quick access to favorites
- Organized collection

### Adding to Virtual Library

1. Search for anime
2. View details
3. Select "Add to Library"

### Accessing Virtual Library

1. Main Menu → Library
2. Select "Virtual Library"
3. Browse bookmarked anime

## Browsing Library

### Local Anime

View downloaded anime:
- Sorted by title
- Shows episode count
- Indicates completion status

### Playing from Library

1. Select anime
2. Choose episode
3. Plays in MPV

### Library Statistics

View stats:
- Total anime count
- Total episodes
- Total storage used
- Most watched

## Tracker Sync

### Auto-Sync

When scanning library:
- Matches anime with tracker database
- Syncs watch progress
- Updates completion status

### Manual Sync

Force sync:
1. Library → Settings
2. Select "Sync with Trackers"

### Match Accuracy

Improve matching:
- Use standard file naming
- Include season numbers
- Use full anime titles

## Library Organization

### Folder Structure

Recommended structure:

```
downloads/
├── Anime 1/
│   ├── S1E1.mp4
│   ├── S1E2.mp4
│   └── ...
├── Anime 2/
│   ├── S1E1.mp4
│   └── ...
```

### Cleaning Up

Remove anime from index:
1. Library → Manage
2. Select anime
3. Choose "Remove from Index"

Note: This only removes from index, not files.

## Advanced Features

### Multi-Source Library

Combine anime from:
- Download directory
- External drives
- Network shares (if mounted)

### Search Library

Quick search in library:
1. Library menu
2. Type to search
3. Filters results in real-time

### Export Library

Export library list:
1. Library → Export
2. Choose format (JSON/CSV)
3. Save to file

## Troubleshooting

### Anime Not Detected

1. Check file naming format
2. Ensure files are in download directory
3. Re-scan library
4. Check file extensions (.mp4, .mkv)

### Wrong Episode Count

1. Verify file naming
2. Check for duplicate files
3. Re-scan library

### Tracker Not Matching

1. Use exact anime title
2. Include year in folder name
3. Manual match in tracker settings

### External Drive Not Found

1. Verify drive is mounted
2. Check path is correct
3. Re-add drive in settings

## Best Practices

1. Use consistent file naming
2. Organize by anime folders
3. Include season numbers
4. Scan after downloads complete
5. Backup library database regularly

## Next Steps

- [Tracker Integration](trackers.md): Sync with online trackers
- [Download Guide](downloading.md): Download more anime
- [Configuration](../getting-started/configuration.md): Library settings
