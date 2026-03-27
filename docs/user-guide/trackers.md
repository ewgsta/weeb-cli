# Tracker Integration

Sync your anime watching progress with AniList, MyAnimeList, and Kitsu.

## Supported Trackers

### AniList

- OAuth authentication
- Automatic progress sync
- Manga and anime tracking
- Social features

### MyAnimeList

- OAuth authentication
- Comprehensive database
- Community features
- Recommendations

### Kitsu

- Email/password authentication
- Modern interface
- Social features
- Progress tracking

## Setting Up Trackers

### AniList Setup

1. Settings → Trackers → AniList
2. Select "Authenticate"
3. Browser opens for OAuth
4. Authorize application
5. Return to CLI (auto-detects)

### MyAnimeList Setup

1. Settings → Trackers → MyAnimeList
2. Select "Authenticate"
3. Browser opens for OAuth
4. Authorize application
5. Return to CLI

### Kitsu Setup

1. Settings → Trackers → Kitsu
2. Enter email
3. Enter password
4. Credentials saved securely

## Progress Syncing

### Automatic Sync

Progress syncs automatically when:
- Watching anime (at 80% completion)
- Downloading episodes
- Scanning local library
- Starting application

### Manual Sync

Force sync:
1. Settings → Trackers
2. Select tracker
3. Choose "Sync Now"

### Offline Queue

When offline:
- Updates queued locally
- Synced when connection restored
- No progress lost

## Matching Anime

### Auto-Matching

Weeb CLI automatically matches:
- By anime title
- By alternative titles
- By year and type

### Match Accuracy

Improve matching:
- Use exact titles
- Include year in search
- Use English titles when possible

### Manual Matching

If auto-match fails:
1. Watchlist → Select anime
2. Choose "Link to Tracker"
3. Search tracker database
4. Select correct match

## Managing Trackers

### View Status

Check tracker status:
- Authentication status
- Last sync time
- Pending updates
- Sync errors

Access: Settings → Trackers → Status

### Disconnect

Remove tracker:
1. Settings → Trackers
2. Select tracker
3. Choose "Disconnect"
4. Confirm removal

### Re-authenticate

If token expires:
1. Settings → Trackers
2. Select tracker
3. Choose "Re-authenticate"

## Tracker Features

### Progress Updates

Automatically updates:
- Current episode
- Watch status (watching/completed/dropped)
- Score (if set)
- Watch count

### Status Management

Set anime status:
- Watching
- Completed
- On Hold
- Dropped
- Plan to Watch

### Scoring

Rate anime:
- 1-10 scale (AniList/Kitsu)
- 1-10 scale (MyAnimeList)
- Updates on tracker

## Privacy

### Data Shared

Only shares:
- Watch progress
- Episode numbers
- Completion status
- Scores (if set)

### Data Not Shared

Never shares:
- Downloaded files
- Stream sources
- Search history
- Local paths

## Troubleshooting

### Authentication Failed

1. Check internet connection
2. Verify credentials
3. Try re-authenticating
4. Check tracker website status

### Progress Not Syncing

1. Check tracker connection
2. Verify anime is matched
3. Check offline queue
4. Manual sync

### Wrong Anime Matched

1. Unlink current match
2. Search tracker manually
3. Select correct anime
4. Confirm match

### Sync Errors

Check logs:
```bash
~/.weeb-cli/logs/debug.log
```

Enable debug mode:
Settings → Configuration → Debug Mode

## Multiple Trackers

### Using Multiple

You can use all three trackers simultaneously:
- Progress syncs to all
- Independent authentication
- Separate offline queues

### Sync Priority

If conflicts:
1. Most recent update wins
2. Manual updates override auto
3. Check each tracker separately

## Best Practices

1. Authenticate all trackers you use
2. Use consistent anime titles
3. Check sync status regularly
4. Clear offline queue periodically
5. Re-authenticate if issues persist

## Next Steps

- [Watchlist Guide](../cli/commands.md): Manage watch history
- [Library Guide](library.md): Local library sync
- [Configuration](../getting-started/configuration.md): Tracker settings
