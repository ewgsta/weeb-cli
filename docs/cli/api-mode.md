# API Mode

Non-interactive JSON API for scripts, automation, and integration with other tools.

## Overview

API mode provides JSON output for all operations, making it easy to:
- Integrate with scripts
- Automate workflows
- Build custom interfaces
- Connect with other tools

## Basic Usage

All API commands follow this pattern:

```bash
weeb-cli api [COMMAND] [ARGS] [OPTIONS]
```

Output is always valid JSON.

## Commands

### providers

List all available providers with metadata.

```bash
weeb-cli api providers
```

Response:
```json
[
  {
    "name": "animecix",
    "lang": "tr",
    "region": "TR",
    "class": "AnimecixProvider"
  },
  {
    "name": "hianime",
    "lang": "en",
    "region": "US",
    "class": "HiAnimeProvider"
  }
]
```

### search

Search for anime across providers.

```bash
weeb-cli api search "anime name" --provider animecix
```

Response:
```json
[
  {
    "id": "anime-slug",
    "title": "Anime Title",
    "type": "series",
    "cover": "https://cover-url.jpg",
    "year": 2024
  }
]
```

### episodes

Get episode list for an anime.

```bash
weeb-cli api episodes "anime-id" --provider animecix
```

Optional: Filter by season
```bash
weeb-cli api episodes "anime-id" --season 2 --provider animecix
```

Response:
```json
[
  {
    "id": "episode-id",
    "number": 1,
    "title": "Episode Title",
    "season": 1,
    "url": "https://episode-url"
  }
]
```

### streams

Get stream URLs for an episode.

```bash
weeb-cli api streams "anime-id" "episode-id" --provider animecix
```

Response:
```json
[
  {
    "url": "https://stream-url.m3u8",
    "quality": "1080p",
    "server": "megacloud",
    "headers": {
      "Referer": "https://..."
    },
    "subtitles": null
  }
]
```

## Error Handling

### Error Response

Errors are returned as JSON to stderr:

```json
{
  "error": "Provider not found: invalid-provider"
}
```

Exit code is non-zero on error.

### Checking Errors

```bash
if weeb-cli api search "anime" --provider invalid 2>/dev/null; then
    echo "Success"
else
    echo "Failed"
fi
```

## Integration Examples

### Python Script

```python
import subprocess
import json

def search_anime(query, provider="animecix"):
    result = subprocess.run(
        ["weeb-cli", "api", "search", query, "--provider", provider],
        capture_output=True,
        text=True
    )
    
    if result.returncode == 0:
        return json.loads(result.stdout)
    else:
        error = json.loads(result.stderr)
        raise Exception(error["error"])

# Usage
results = search_anime("One Piece", "hianime")
for anime in results:
    print(f"{anime['title']} ({anime['year']})")
```

### Bash Script

```bash
#!/bin/bash

PROVIDER="animecix"
QUERY="Naruto"

# Search
results=$(weeb-cli api search "$QUERY" --provider "$PROVIDER")

# Parse with jq
echo "$results" | jq -r '.[] | "\(.title) - \(.year)"'

# Get first result ID
anime_id=$(echo "$results" | jq -r '.[0].id')

# Get episodes
episodes=$(weeb-cli api episodes "$anime_id" --provider "$PROVIDER")
echo "$episodes" | jq -r '.[] | "Episode \(.number): \(.title)"'
```

### Node.js Script

```javascript
const { exec } = require('child_process');
const util = require('util');
const execPromise = util.promisify(exec);

async function searchAnime(query, provider = 'animecix') {
    const cmd = `weeb-cli api search "${query}" --provider ${provider}`;
    const { stdout } = await execPromise(cmd);
    return JSON.parse(stdout);
}

// Usage
searchAnime('One Piece', 'hianime')
    .then(results => {
        results.forEach(anime => {
            console.log(`${anime.title} (${anime.year})`);
        });
    })
    .catch(console.error);
```

## Advanced Usage

### Piping Results

```bash
# Search and filter with jq
weeb-cli api search "anime" --provider animecix | \
    jq '.[] | select(.year >= 2020)'

# Get all episodes and count
weeb-cli api episodes "anime-id" --provider animecix | \
    jq 'length'

# Get best quality stream
weeb-cli api streams "anime-id" "ep-id" --provider animecix | \
    jq -r '.[0].url'
```

### Chaining Commands

```bash
# Search, get first result, get episodes
ANIME_ID=$(weeb-cli api search "Naruto" --provider animecix | jq -r '.[0].id')
weeb-cli api episodes "$ANIME_ID" --provider animecix
```

### Error Handling

```bash
# Capture errors
if ! output=$(weeb-cli api search "anime" --provider invalid 2>&1); then
    echo "Error occurred: $output"
    exit 1
fi
```

## Performance

### Caching

API mode uses same cache as interactive mode:
- Search results cached for 1 hour
- Details cached for 6 hours
- Streams not cached

### Headless Mode

API mode runs in headless mode:
- No TUI dependencies loaded
- Faster startup
- Lower memory usage

## Limitations

### No Interactive Features

API mode does not support:
- Menus and prompts
- Progress bars
- User input
- Color output

### No State Management

Each command is independent:
- No session state
- No watch history updates
- No progress tracking

Use interactive mode for these features.

## Best Practices

1. Always specify provider explicitly
2. Handle errors properly
3. Parse JSON with proper tools (jq, Python json)
4. Cache results when possible
5. Use appropriate timeouts

## Next Steps

- [Commands Reference](commands.md): All CLI commands
- [Serve Mode](serve-mode.md): Torznab server
- [Development](../development/contributing.md): API development
