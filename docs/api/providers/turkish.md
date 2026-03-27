# Turkish Providers

Turkish anime source providers.

## Available Providers

### Animecix

Provider for Animecix.net

- Large anime library
- Turkish subtitles
- Multiple servers
- HD quality

### Turkanime

Provider for TurkAnime.co

- Extensive collection
- Turkish dubs and subs
- Multiple quality options

### Anizle

Provider for Anizle.com

- Modern interface
- Fast servers
- HD streams

### Weeb

Provider for Weeb.com.tr

- Turkish content
- Multiple servers
- Good quality

## Usage

```python
from weeb_cli.providers import get_provider

# Get provider
provider = get_provider("animecix")

# Search
results = provider.search("One Piece")

# Get details
details = provider.get_details(results[0].id)

# Get streams
streams = provider.get_streams(details.id, episode_id)
```

## Provider Comparison

| Provider | Library Size | Quality | Speed | Subtitles |
|----------|-------------|---------|-------|-----------|
| Animecix | Large | HD | Fast | Turkish |
| Turkanime | Large | HD | Medium | Turkish |
| Anizle | Medium | HD | Fast | Turkish |
| Weeb | Medium | HD | Medium | Turkish |

## Next Steps

- [Base Provider](base.md): Provider interface
- [Adding Providers](../../development/adding-providers.md): Create provider
