# German Providers

German anime source providers.

## Available Providers

### AniWorld

Provider for AniWorld.to

- Large German anime library
- German dubs and subtitles
- Multiple quality options
- Fast servers

## Usage

```python
from weeb_cli.providers import get_provider

# Get provider
provider = get_provider("aniworld")

# Search
results = provider.search("One Piece")

# Get details
details = provider.get_details(results[0].id)

# Get streams
streams = provider.get_streams(details.id, episode_id)
```

## Provider Details

| Provider | Library Size | Quality | Speed | Subtitles |
|----------|-------------|---------|-------|-----------|
| AniWorld | Large | HD | Fast | German |

## Next Steps

- [Base Provider](base.md): Provider interface
- [Adding Providers](../../development/adding-providers.md): Create provider
