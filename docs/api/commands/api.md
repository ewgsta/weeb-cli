# API Commands

Non-interactive JSON API commands.

## Overview

API commands provide JSON output for:
- Scripts and automation
- Integration with tools
- Headless operation

## Commands

### providers

List all providers.

```bash
weeb-cli api providers
```

### search

Search for anime.

```bash
weeb-cli api search "query" --provider animecix
```

### episodes

Get episode list.

```bash
weeb-cli api episodes "anime-id" --provider animecix
```

### streams

Get stream URLs.

```bash
weeb-cli api streams "anime-id" "episode-id" --provider animecix
```

## Implementation

All commands in `weeb_cli/commands/api.py`.

## Next Steps

- [API Mode Guide](../../cli/api-mode.md): Detailed usage
- [Commands Reference](../../cli/commands.md): All commands
