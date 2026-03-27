# Searching for Anime

Learn how to search for anime across multiple providers and find what you want to watch.

## Basic Search

### From Main Menu

1. Start Weeb CLI: `weeb-cli`
2. Select "Search Anime" from the main menu
3. Enter your search query
4. Browse results

### Search Tips

- Use English or native language titles
- Try alternative spellings if not found
- Use partial titles for broader results
- Search is case-insensitive

## Search Results

Results display:
- Anime title
- Type (Series, Movie, OVA, etc.)
- Release year
- Cover image (if terminal supports)
- Provider source

### Navigating Results

- Use arrow keys to navigate
- Press Enter to select
- Press Ctrl+C to go back

## Provider Selection

### Default Provider

The default provider is based on your language setting:
- Turkish: Animecix
- English: HiAnime
- German: AniWorld
- Polish: Docchi

### Changing Provider

1. Go to Settings → Configuration
2. Select "Default Provider"
3. Choose from available providers

### Provider-Specific Search

Different providers may have different content:
- Try multiple providers if not found
- Some providers have exclusive content
- Quality and availability varies

## Search History

### Viewing History

1. From main menu, select "Search Anime"
2. Press Up arrow to see recent searches
3. Select from history to repeat search

### Clearing History

Settings → Cache → Clear Search History

## Advanced Search

### API Mode

For scripting and automation:

```bash
# Search with specific provider
weeb-cli api search "One Piece" --provider animecix

# Output is JSON
weeb-cli api search "Naruto" --provider hianime | jq
```

### Filtering Results

Currently, filtering is done by provider. Future versions may include:
- Genre filtering
- Year filtering
- Type filtering (Series/Movie/OVA)

## Troubleshooting

### No Results Found

1. Check spelling
2. Try alternative title (English/Japanese/Native)
3. Try different provider
4. Check internet connection

### Slow Search

1. Check network speed
2. Try different provider
3. Clear cache: Settings → Cache → Clear Provider Cache

### Provider Errors

If a provider fails:
1. Try another provider
2. Check if provider website is accessible
3. Report issue on GitHub if persistent

## Next Steps

- [Streaming Guide](streaming.md): Learn how to watch anime
- [Download Guide](downloading.md): Learn how to download anime
- [Tracker Integration](trackers.md): Sync your progress
