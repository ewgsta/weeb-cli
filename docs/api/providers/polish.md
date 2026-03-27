# Polish Providers

Polish anime source providers.

## Available Providers

### Docchi

Provider for Docchi.pl

- Polish anime library
- Polish subtitles
- Multiple servers
- Good quality

## Usage

```python
from weeb_cli.providers import get_provider

# Get provider
provider = get_provider("docchi")

# Search
results = provider.search("Naruto")

# Get details
details = provider.get_details(results[0].id)

# Get streams
streams = provider.get_streams(details.id, episode_id)
```

## Provider Details

| Provider | Library Size | Quality | Speed | Subtitles |
|----------|-------------|---------|-------|-----------|
| Docchi | Medium | HD | Medium | Polish |

## Next Steps

- [Base Provider](base.md): Provider interface
- [Adding Providers](../../development/adding-providers.md): Create provider
