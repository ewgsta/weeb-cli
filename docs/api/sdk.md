# Python SDK

Programmatic API for integrating Weeb CLI functionality directly into Python applications.

## Overview

The Weeb CLI SDK provides a native Python interface for all anime streaming and downloading functionality. Unlike the CLI API mode which requires spawning processes and parsing JSON, the SDK offers:

- **Direct Python API** - No subprocess overhead
- **Type Safety** - Full type hints for IDE support
- **Thread Safe** - Safe for concurrent operations
- **Headless Mode** - No database or TUI dependencies
- **Same Features** - All CLI functionality available

## Installation

The SDK is included with weeb-cli:

```bash
pip install weeb-cli
```

## Quick Start

```python
from weeb_cli import WeebSDK

# Initialize SDK
sdk = WeebSDK(default_provider="hianime")

# Search for anime
results = sdk.search("One Piece")
print(f"Found {len(results)} results")

# Get first result
anime = results[0]
print(f"{anime.title} ({anime.year})")

# Get episodes
episodes = sdk.get_episodes(anime.id, season=1)
print(f"Season 1 has {len(episodes)} episodes")

# Get stream URLs
streams = sdk.get_streams(
    anime_id=anime.id,
    episode_id=episodes[0].id
)
print(f"Available in {len(streams)} qualities")

# Download episode
path = sdk.download_episode(
    anime_id=anime.id,
    season=1,
    episode=1,
    output_dir="./downloads"
)
print(f"Downloaded to: {path}")
```

## API Reference

### WeebSDK Class

Main SDK interface for all operations.

#### Constructor

```python
WeebSDK(headless: bool = True, default_provider: Optional[str] = None)
```

**Parameters:**
- `headless` (bool): Run in headless mode (no database/TUI). Default: `True`
- `default_provider` (str, optional): Default provider to use. Default: `"animecix"`

**Example:**
```python
# Headless with default provider
sdk = WeebSDK()

# Custom default provider
sdk = WeebSDK(default_provider="hianime")

# With database access (for watch history, etc.)
sdk = WeebSDK(headless=False)
```

#### list_providers()

List all available anime providers.

```python
def list_providers() -> List[Dict[str, Any]]
```

**Returns:** List of provider metadata dictionaries:
- `name` (str): Provider identifier
- `lang` (str): Language code (en, tr, de, pl)
- `region` (str): Region code (US, TR, DE, PL)
- `class` (str): Provider class name
- `disabled` (bool): Whether provider is disabled

**Example:**
```python
providers = sdk.list_providers()
for p in providers:
    print(f"{p['name']}: {p['lang']} ({p['region']})")
```

#### get_provider_info()

Get metadata for a specific provider.

```python
def get_provider_info(provider_name: str) -> Optional[Dict[str, Any]]
```

**Parameters:**
- `provider_name` (str): Provider identifier

**Returns:** Provider metadata dictionary, or `None` if not found

**Example:**
```python
info = sdk.get_provider_info("hianime")
if info:
    print(f"Language: {info['lang']}")
```

#### search()

Search for anime by query string.

```python
def search(
    query: str, 
    provider: Optional[str] = None
) -> List[AnimeResult]
```

**Parameters:**
- `query` (str): Search query (anime title or keywords)
- `provider` (str, optional): Provider to use. Uses `default_provider` if not specified

**Returns:** List of `AnimeResult` objects with:
- `id` (str): Unique anime identifier
- `title` (str): Anime title
- `type` (str): Content type (series, movie, ova)
- `cover` (str, optional): Cover image URL
- `year` (int, optional): Release year

**Raises:**
- `ProviderError`: If provider not found or search fails

**Example:**
```python
results = sdk.search("Naruto", provider="hianime")
for anime in results:
    print(f"{anime.title} - {anime.type} ({anime.year})")
```

#### get_details()

Get detailed information for an anime.

```python
def get_details(
    anime_id: str, 
    provider: Optional[str] = None
) -> Optional[AnimeDetails]
```

**Parameters:**
- `anime_id` (str): Unique anime identifier from search results
- `provider` (str, optional): Provider to use

**Returns:** `AnimeDetails` object with:
- `id` (str): Anime identifier
- `title` (str): Anime title
- `description` (str, optional): Synopsis
- `cover` (str, optional): Cover image URL
- `genres` (List[str]): Genre tags
- `year` (int, optional): Release year
- `status` (str, optional): Airing status
- `episodes` (List[Episode]): Available episodes
- `total_episodes` (int, optional): Total episode count

**Raises:**
- `ProviderError`: If provider not found or fetch fails

**Example:**
```python
details = sdk.get_details("anime-id", provider="hianime")
print(f"{details.title}")
print(f"Description: {details.description}")
print(f"Genres: {', '.join(details.genres)}")
print(f"Episodes: {len(details.episodes)}")
```

#### get_episodes()

Get list of available episodes for an anime.

```python
def get_episodes(
    anime_id: str, 
    season: Optional[int] = None,
    provider: Optional[str] = None
) -> List[Episode]
```

**Parameters:**
- `anime_id` (str): Unique anime identifier
- `season` (int, optional): Filter by season number
- `provider` (str, optional): Provider to use

**Returns:** List of `Episode` objects with:
- `id` (str): Episode identifier
- `number` (int): Episode number
- `title` (str, optional): Episode title
- `season` (int): Season number
- `url` (str, optional): Episode page URL

**Raises:**
- `ProviderError`: If provider not found or fetch fails

**Example:**
```python
# Get all episodes
episodes = sdk.get_episodes("anime-id", provider="hianime")

# Get season 2 only
season2 = sdk.get_episodes("anime-id", season=2, provider="hianime")

for ep in season2:
    print(f"S{ep.season:02d}E{ep.number:02d}: {ep.title}")
```

#### get_streams()

Get stream URLs for a specific episode.

```python
def get_streams(
    anime_id: str, 
    episode_id: str,
    provider: Optional[str] = None
) -> List[StreamLink]
```

**Parameters:**
- `anime_id` (str): Unique anime identifier
- `episode_id` (str): Unique episode identifier
- `provider` (str, optional): Provider to use

**Returns:** List of `StreamLink` objects with:
- `url` (str): Direct stream URL
- `quality` (str): Quality label (1080p, 720p, etc.)
- `server` (str): Server name
- `headers` (Dict[str, str]): Required HTTP headers
- `subtitles` (str, optional): Subtitle file URL

**Raises:**
- `ProviderError`: If provider not found or extraction fails

**Example:**
```python
streams = sdk.get_streams("anime-id", "ep-id", provider="hianime")

# Find best quality
best = max(streams, key=lambda s: s.quality)
print(f"Best quality: {best.quality}")
print(f"URL: {best.url}")

# Use with video player
import subprocess
subprocess.run(["mpv", best.url])
```

#### download_episode()

Download an episode to local storage.

```python
def download_episode(
    anime_id: str,
    season: int,
    episode: int,
    provider: Optional[str] = None,
    output_dir: str = ".",
    anime_title: Optional[str] = None
) -> Optional[str]
```

**Parameters:**
- `anime_id` (str): Unique anime identifier
- `season` (int): Season number
- `episode` (int): Episode number
- `provider` (str, optional): Provider to use
- `output_dir` (str): Directory to save file. Default: current directory
- `anime_title` (str, optional): Custom title for filename. Auto-fetched if not provided

**Returns:** Path to downloaded file, or `None` if failed

**Raises:**
- `ProviderError`: If provider not found or no streams available
- `WeebCLIError`: If download fails

**Example:**
```python
# Basic download
path = sdk.download_episode(
    anime_id="anime-id",
    season=1,
    episode=1,
    provider="hianime"
)

# Custom output directory and title
path = sdk.download_episode(
    anime_id="anime-id",
    season=2,
    episode=5,
    provider="hianime",
    output_dir="/media/anime",
    anime_title="My Favorite Anime"
)
print(f"Downloaded to: {path}")
```

#### download_url()

Download a video from a direct stream URL.

```python
def download_url(
    stream_url: str,
    title: str,
    season: int,
    episode: int,
    output_dir: str = "."
) -> Optional[str]
```

**Parameters:**
- `stream_url` (str): Direct stream URL (HLS, MP4, etc.)
- `title` (str): Series title for filename
- `season` (int): Season number
- `episode` (int): Episode number
- `output_dir` (str): Directory to save file

**Returns:** Path to downloaded file, or `None` if failed

**Example:**
```python
path = sdk.download_url(
    stream_url="https://example.com/video.m3u8",
    title="My Anime",
    season=1,
    episode=1,
    output_dir="./downloads"
)
```

## Convenience Functions

For quick access without creating an SDK instance:

### list_providers()

```python
from weeb_cli.sdk import list_providers

providers = list_providers()
print([p['name'] for p in providers])
```

### get_provider_info()

```python
from weeb_cli.sdk import get_provider_info

info = get_provider_info("hianime")
print(info['lang'])
```

## Advanced Usage

### Multi-Provider Search

Search across multiple providers and combine results:

```python
from weeb_cli import WeebSDK

sdk = WeebSDK()
query = "One Piece"

# Search multiple providers
providers = ["hianime", "animecix", "aniworld"]
all_results = []

for provider in providers:
    try:
        results = sdk.search(query, provider=provider)
        all_results.extend(results)
        print(f"{provider}: {len(results)} results")
    except Exception as e:
        print(f"{provider} failed: {e}")

print(f"Total: {len(all_results)} results")
```

### Batch Download

Download multiple episodes:

```python
from weeb_cli import WeebSDK

sdk = WeebSDK(default_provider="hianime")

# Search and get anime
results = sdk.search("Naruto")
anime_id = results[0].id

# Download season 1
for episode_num in range(1, 26):
    try:
        path = sdk.download_episode(
            anime_id=anime_id,
            season=1,
            episode=episode_num,
            output_dir="./naruto_s1"
        )
        print(f"✓ Episode {episode_num}: {path}")
    except Exception as e:
        print(f"✗ Episode {episode_num}: {e}")
```

### Concurrent Downloads

Use threading for parallel downloads:

```python
from weeb_cli import WeebSDK
from concurrent.futures import ThreadPoolExecutor, as_completed

sdk = WeebSDK(default_provider="hianime")

def download_ep(anime_id, season, episode):
    return sdk.download_episode(
        anime_id=anime_id,
        season=season,
        episode=episode,
        output_dir="./downloads"
    )

# Download episodes 1-10 concurrently
anime_id = "anime-id"
episodes = range(1, 11)

with ThreadPoolExecutor(max_workers=3) as executor:
    futures = {
        executor.submit(download_ep, anime_id, 1, ep): ep 
        for ep in episodes
    }
    
    for future in as_completed(futures):
        ep = futures[future]
        try:
            path = future.result()
            print(f"✓ Episode {ep}: {path}")
        except Exception as e:
            print(f"✗ Episode {ep}: {e}")
```

### Custom Provider Selection

Let users choose provider interactively:

```python
from weeb_cli import WeebSDK

sdk = WeebSDK()

# Show available providers
providers = sdk.list_providers()
print("Available providers:")
for i, p in enumerate(providers, 1):
    print(f"{i}. {p['name']} ({p['lang']})")

# Get user choice
choice = int(input("Select provider: ")) - 1
provider = providers[choice]['name']

# Search with selected provider
query = input("Search: ")
results = sdk.search(query, provider=provider)

for i, anime in enumerate(results, 1):
    print(f"{i}. {anime.title} ({anime.year})")
```

### Error Handling

Proper error handling for production use:

```python
from weeb_cli import WeebSDK
from weeb_cli.exceptions import ProviderError, WeebCLIError

sdk = WeebSDK()

try:
    results = sdk.search("anime", provider="invalid")
except ProviderError as e:
    print(f"Provider error: {e}")
    print(f"Error code: {e.error_code}")
except WeebCLIError as e:
    print(f"General error: {e}")
except Exception as e:
    print(f"Unexpected error: {e}")
```

## Integration Examples

### Flask Web API

```python
from flask import Flask, jsonify, request
from weeb_cli import WeebSDK

app = Flask(__name__)
sdk = WeebSDK()

@app.route('/api/search')
def search():
    query = request.args.get('q')
    provider = request.args.get('provider', 'hianime')
    
    results = sdk.search(query, provider=provider)
    return jsonify([
        {
            'id': r.id,
            'title': r.title,
            'year': r.year,
            'cover': r.cover
        }
        for r in results
    ])

@app.route('/api/episodes/<anime_id>')
def episodes(anime_id):
    provider = request.args.get('provider', 'hianime')
    episodes = sdk.get_episodes(anime_id, provider=provider)
    
    return jsonify([
        {
            'id': e.id,
            'number': e.number,
            'title': e.title,
            'season': e.season
        }
        for e in episodes
    ])

if __name__ == '__main__':
    app.run(port=5000)
```

### Discord Bot

```python
import discord
from discord.ext import commands
from weeb_cli import WeebSDK

bot = commands.Bot(command_prefix='!')
sdk = WeebSDK(default_provider="hianime")

@bot.command()
async def anime(ctx, *, query):
    """Search for anime"""
    results = sdk.search(query)
    
    if not results:
        await ctx.send("No results found")
        return
    
    anime = results[0]
    embed = discord.Embed(
        title=anime.title,
        description=f"Year: {anime.year}"
    )
    if anime.cover:
        embed.set_thumbnail(url=anime.cover)
    
    await ctx.send(embed=embed)

bot.run('YOUR_TOKEN')
```

### Telegram Bot

```python
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
from weeb_cli import WeebSDK

sdk = WeebSDK(default_provider="hianime")

async def search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = ' '.join(context.args)
    results = sdk.search(query)
    
    if not results:
        await update.message.reply_text("No results found")
        return
    
    response = "\n".join([
        f"{i}. {r.title} ({r.year})"
        for i, r in enumerate(results[:5], 1)
    ])
    
    await update.message.reply_text(response)

app = Application.builder().token("YOUR_TOKEN").build()
app.add_handler(CommandHandler("search", search))
app.run_polling()
```

## Best Practices

1. **Reuse SDK Instance**: Create one SDK instance and reuse it
2. **Handle Errors**: Always wrap SDK calls in try-except blocks
3. **Provider Selection**: Let users choose provider or use language-appropriate defaults
4. **Concurrent Operations**: Use threading for batch operations
5. **Caching**: SDK uses same cache as CLI - results are cached automatically
6. **Headless Mode**: Keep headless=True for stateless applications

## Limitations

- **No Watch History**: Headless mode doesn't track watch progress
- **No Tracker Sync**: AniList/MAL sync requires non-headless mode
- **No Notifications**: System notifications not available in headless mode
- **No Discord RPC**: Discord integration requires non-headless mode

For these features, initialize SDK with `headless=False` and ensure database is accessible.

## Next Steps

- [API Mode Documentation](../cli/api-mode.md): CLI JSON API
- [Provider Development](../development/adding-providers.md): Create custom providers
- [Architecture](../development/architecture.md): System design overview
