# CLI Commands Reference

Complete reference for all Weeb CLI command-line commands.

## Main Commands

### Default (Interactive Mode)

Start interactive mode with main menu.

```bash
weeb-cli
```

This is the default command when no subcommand is provided.

### start

Alternative command for interactive mode (same as default).

```bash
weeb-cli start
```

### api

Non-interactive JSON API for scripts and automation.

```bash
weeb-cli api [SUBCOMMAND]
```

See [API Mode](api-mode.md) for details.

### serve

Start Torznab server for *arr integration.

```bash
weeb-cli serve [OPTIONS]
```

See [Serve Mode](serve-mode.md) for details.

## API Subcommands

### api providers

List all available providers.

```bash
weeb-cli api providers
```

Output:
```json
[
  {
    "name": "animecix",
    "lang": "tr",
    "region": "TR",
    "class": "AnimecixProvider"
  }
]
```

### api search

Search for anime.

```bash
weeb-cli api search QUERY [OPTIONS]
```

Options:
- `--provider, -p`: Provider name (default: animecix)

Example:
```bash
weeb-cli api search "One Piece" --provider hianime
```

Output:
```json
[
  {
    "id": "one-piece-100",
    "title": "One Piece",
    "type": "series",
    "cover": "https://...",
    "year": 1999
  }
]
```

### api episodes

Get episode list for anime.

```bash
weeb-cli api episodes ANIME_ID [OPTIONS]
```

Options:
- `--provider, -p`: Provider name (default: animecix)
- `--season, -s`: Filter by season number

Example:
```bash
weeb-cli api episodes "one-piece-100" --provider hianime --season 1
```

Output:
```json
[
  {
    "id": "ep-1",
    "number": 1,
    "title": "I'm Luffy! The Man Who Will Become Pirate King!",
    "season": 1
  }
]
```

### api streams

Get stream URLs for episode.

```bash
weeb-cli api streams ANIME_ID EPISODE_ID [OPTIONS]
```

Options:
- `--provider, -p`: Provider name (default: animecix)

Example:
```bash
weeb-cli api streams "one-piece-100" "ep-1" --provider hianime
```

Output:
```json
[
  {
    "url": "https://...",
    "quality": "1080p",
    "server": "megacloud",
    "headers": {}
  }
]
```

## Global Options

### --help

Show help message.

```bash
weeb-cli --help
weeb-cli api --help
weeb-cli api search --help
```

### --version

Show version information.

```bash
weeb-cli --version
```

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
weeb-cli
```

## Exit Codes

- 0: Success
- 1: General error
- 2: Invalid arguments
- 130: Interrupted (Ctrl+C)

## Examples

### Search and Stream

```bash
# Search
weeb-cli api search "Naruto" --provider animecix > results.json

# Get anime ID from results
ANIME_ID=$(jq -r '.[0].id' results.json)

# Get episodes
weeb-cli api episodes "$ANIME_ID" --provider animecix > episodes.json

# Get episode ID
EPISODE_ID=$(jq -r '.[0].id' episodes.json)

# Get streams
weeb-cli api streams "$ANIME_ID" "$EPISODE_ID" --provider animecix > streams.json

# Play with mpv
STREAM_URL=$(jq -r '.[0].url' streams.json)
mpv "$STREAM_URL"
```

### Batch Processing

```bash
#!/bin/bash
# Download all episodes of an anime

ANIME_ID="one-piece-100"
PROVIDER="hianime"

# Get episodes
episodes=$(weeb-cli api episodes "$ANIME_ID" --provider "$PROVIDER")

# Loop through episodes
echo "$episodes" | jq -c '.[]' | while read episode; do
    ep_id=$(echo "$episode" | jq -r '.id')
    ep_num=$(echo "$episode" | jq -r '.number')
    
    echo "Processing episode $ep_num..."
    
    # Get streams
    streams=$(weeb-cli api streams "$ANIME_ID" "$ep_id" --provider "$PROVIDER")
    stream_url=$(echo "$streams" | jq -r '.[0].url')
    
    # Download with yt-dlp
    yt-dlp -o "Episode-$ep_num.mp4" "$stream_url"
done
```

## Shell Completion

### Bash

```bash
eval "$(_WEEB_CLI_COMPLETE=bash_source weeb-cli)"
```

### Zsh

```bash
eval "$(_WEEB_CLI_COMPLETE=zsh_source weeb-cli)"
```

### Fish

```bash
eval (env _WEEB_CLI_COMPLETE=fish_source weeb-cli)
```

## Next Steps

- [API Mode Guide](api-mode.md): Detailed API usage
- [Serve Mode Guide](serve-mode.md): Torznab server
- [User Guide](../user-guide/searching.md): Interactive mode
