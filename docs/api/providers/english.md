# English Providers

English anime source providers.

## Available Providers

### HiAnime

Provider for HiAnime.to

- Huge anime library
- Multiple quality options
- Fast servers
- English subtitles and dubs

### AllAnime

Provider for AllAnime.to

- Large collection
- Multiple servers
- HD quality
- Sub and dub options

## Usage

```python
from weeb_cli.providers import get_provider

# Get provider
provider = get_provider("hianime")

# Search
results = provider.search("Naruto")

# Get details
details = provider.get_details(results[0].id)

# Get streams
streams = provider.get_streams(details.id, episode_id)
```

## Provider Comparison

| Provider | Library Size | Quality | Speed | Subtitles |
|----------|-------------|---------|-------|-----------|
| HiAnime | Very Large | 1080p | Fast | English |
| AllAnime | Large | 1080p | Fast | English |

## Next Steps

- [Base Provider](base.md): Provider interface
- [Adding Providers](../../development/adding-providers.md): Create provider
