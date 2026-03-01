<p align="center">
  <img src="https://8upload.com/image/a6cdd79fc5a25c99/wl-512x512.jpg" alt="Weeb CLI Logo" width="120">
</p>

<h1 align="center">Weeb CLI</h1>

<p align="center">
  <strong>No browser, no ads, no distractions. Just you and an unparalleled anime viewing experience.</strong>
</p>

<p align="center">
  <a href="https://github.com/ewgsta/weeb-cli/releases"><img src="https://img.shields.io/github/v/release/ewgsta/weeb-cli?style=flat-square" alt="Release"></a>
  <a 
  <a href="https://github.com/ewgsta/weeb-cli/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-GPL--3.0-blue?style=flat-square" alt="License"></a>
  <a href="https://github.com/ewgsta/weeb-cli/stargazers"><img src="https://img.shields.io/github/stars/ewgsta/weeb-cli?style=flat-square" alt="Stars"></a>
  <a href="https://github.com/ewgsta/weeb-cli/actions"><img src="https://img.shields.io/github/actions/workflow/status/ewgsta/weeb-cli/tests.yml?style=flat-square" alt="Tests"></a>
</p>

<p align="center">
  <a href="#installation">Installation</a> •
  <a href="#features">Features</a> •
  <a href="#usage">Usage</a> •
  <a href="#sources">Sources</a> •
  <a href="README-TR.md">Türkçe</a>
</p>

---

## Features

### Multiple Sources
- **Turkish**: Animecix, Turkanime, Anizle
- **English**: HiAnime, AllAnime

### Smart Streaming
- High-quality HLS/MP4 playback with MPV
- Resume from where you left off (timestamp-based)
- Watch history and statistics
- Completed (✓) and in-progress (●) episode markers

### Powerful Download System
- **Aria2** for multi-connection fast downloads
- **yt-dlp** for complex stream support
- Queue system with concurrent downloads
- Resume interrupted downloads
- Smart file naming (`Anime Name - S1E1.mp4`)

### Tracking & Sync
- **AniList** integration with OAuth
- **MyAnimeList** integration with OAuth
- **Kitsu** integration with email/password
- Automatic progress sync
- Offline queue for pending updates

### Local Library
- Auto-scan downloaded anime
- External drive support (USB, HDD)
- Offline anime indexing
- Search across all sources

### Additional Features
- SQLite database (fast and reliable)
- System notifications on download completion
- Discord RPC integration (show what you're watching on Discord)
- Search history
- Debug mode and logging
- Automatic update checks
- Non-interactive JSON API for scripts and AI agents
- Torznab server mode for Sonarr/*arr integration

---

## Installation

### PyPI (Universal)
```bash
pip install weeb-cli
```

### Arch Linux (AUR)
```bash
yay -S weeb-cli
```

### Portable
Download the appropriate file for your platform from [Releases](https://github.com/ewgsta/weeb-cli/releases).

### Developer Setup
```bash
git clone https://github.com/ewgsta/weeb-cli.git
cd weeb-cli
pip install -e .
```

---

## Usage

```bash
weeb-cli
```

### API Mode (Non-interactive)

For scripts, automation, and AI agents, weeb-cli provides JSON API commands that work headlessly without a database or TUI:

```bash
# List available providers
weeb-cli api providers

# Search for anime (returns IDs)
weeb-cli api search "Angel Beats"
# Returns: [{"id": "12345", "title": "Angel Beats!", ...}]

# List episodes (use ID from search)
weeb-cli api episodes 12345 --season 1

# Get stream URLs for an episode
weeb-cli api streams 12345 --season 1 --episode 1

# Get anime details
weeb-cli api details 12345

# Download an episode
weeb-cli api download 12345 --season 1 --episode 1 --output ./downloads
```

All API commands output JSON to stdout.

### Sonarr/*arr Integration (Serve Mode)

weeb-cli can run as a Torznab-compatible server for Sonarr and other *arr applications:

```bash
pip install weeb-cli[serve]

weeb-cli serve --port 9876 \
  --watch-dir /downloads/watch \
  --completed-dir /downloads/completed \
  --sonarr-url http://sonarr:8989 \
  --sonarr-api-key YOUR_KEY \
  --providers animecix,anizle,turkanime
```

Then add `http://weeb-cli-host:9876` as a Torznab indexer in Sonarr with category 5070 (TV/Anime). The server includes a blackhole download worker that automatically processes grabbed episodes.

#### Docker

```dockerfile
FROM python:3.13-slim
RUN apt-get update && apt-get install -y --no-install-recommends aria2 ffmpeg && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir weeb-cli[serve] yt-dlp
EXPOSE 9876
CMD ["weeb-cli", "serve", "--port", "9876", "--watch-dir", "/downloads/watch", "--completed-dir", "/downloads/completed"]
```

### Keyboard Controls
| Key | Action |
|-----|--------|
| `↑` `↓` | Navigate menu |
| `Enter` | Select |
| `s` | Search Anime (Main menu) |
| `d` | Downloads (Main menu) |
| `w` | Watchlist (Main menu) |
| `c` | Settings (Main menu) |
| `q` | Exit (Main menu) |
| `Ctrl+C` | Go back / Exit |

**Note:** All shortcuts can be customized in Settings > Keyboard Shortcuts.

---

## Sources

| Source | Language |
|--------|----------|
| Animecix | Turkish |
| Turkanime | Turkish |
| Anizle | Turkish |
| HiAnime | English |
| AllAnime | English |

---

## Configuration

Config location: `~/.weeb-cli/weeb.db` (SQLite)

### Available Settings

| Setting | Description | Default | Type |
|---------|-------------|---------|------|
| `language` | Interface language (tr/en) | `null` (asks on first run) | string |
| `scraping_source` | Active anime source | `animecix` | string |
| `aria2_enabled` | Use Aria2 for downloads | `true` | boolean |
| `aria2_max_connections` | Max connections per download | `16` | integer |
| `ytdlp_enabled` | Use yt-dlp for HLS streams | `true` | boolean |
| `ytdlp_format` | yt-dlp format string | `bestvideo+bestaudio/best` | string |
| `max_concurrent_downloads` | Simultaneous downloads | `3` | integer |
| `download_dir` | Download folder path | `./weeb-downloads` | string |
| `download_max_retries` | Retry failed downloads | `3` | integer |
| `download_retry_delay` | Delay between retries (seconds) | `10` | integer |
| `show_description` | Show anime descriptions | `true` | boolean |
| `discord_rpc_enabled` | Discord Rich Presence | `false` | boolean |
| `shortcuts_enabled` | Keyboard shortcuts | `true` | boolean |
| `debug_mode` | Debug logging | `false` | boolean |

### Tracker Settings (stored separately)
- `anilist_token` - AniList OAuth token
- `anilist_user_id` - AniList user ID
- `mal_token` - MyAnimeList OAuth token
- `mal_refresh_token` - MAL refresh token
- `mal_username` - MAL username

### External Drives
Managed via Settings > External Drives menu. Each drive stores:
- Path (e.g., `D:\Anime`)
- Custom name/nickname
- Added timestamp

All settings can be modified through the interactive Settings menu.

---

## Roadmap

### Completed
- [x] Multiple source support (TR/EN)
- [x] MPV streaming
- [x] Watch history and progress tracking
- [x] Aria2/yt-dlp download integration
- [x] External drives and local library
- [x] SQLite database
- [x] Notification system
- [x] Debug mode
- [x] MAL/AniList integration
- [x] Database backup/restore
- [x] Keyboard shortcuts
- [x] Non-interactive API mode (JSON output)
- [x] Torznab server for Sonarr/*arr integration


### Planned
- [ ] Anime recommendations
- [ ] Batch operations
- [ ] Watch statistics (graphs)
- [ ] Theme support
- [ ] Subtitle downloads
- [ ] Torrent support (nyaa.si)
- [ ] Watch party

---

## Project Structure

```
weeb-cli/
├── weeb_cli/                    # Main application package
│   ├── commands/                # CLI command handlers
│   │   ├── api.py               # Non-interactive JSON API commands
│   │   ├── downloads.py         # Download management commands
│   │   ├── search.py            # Anime search functionality
│   │   ├── serve.py             # Torznab server for *arr integration
│   │   ├── settings.py          # Settings menu and configuration
│   │   ├── setup.py             # Initial setup wizard
│   │   └── watchlist.py         # Watch history and progress
│   │
│   ├── providers/               # Anime source integrations
│   │   ├── extractors/          # Video stream extractors
│   │   │   └── megacloud.py     # Megacloud extractor
│   │   ├── allanime.py          # AllAnime provider (EN)
│   │   ├── animecix.py          # Animecix provider (TR)
│   │   ├── anizle.py            # Anizle provider (TR)
│   │   ├── base.py              # Base provider interface
│   │   ├── hianime.py           # HiAnime provider (EN)
│   │   ├── registry.py          # Provider registration system
│   │   └── turkanime.py         # Turkanime provider (TR)
│   │
│   ├── services/                # Business logic layer
│   │   ├── cache.py             # File-based caching system
│   │   ├── database.py          # SQLite database manager
│   │   ├── dependency_manager.py # Auto-install FFmpeg, MPV, etc.
│   │   ├── details.py           # Anime details fetcher
│   │   ├── discord_rpc.py       # Discord Rich Presence
│   │   ├── downloader.py        # Queue-based download manager
│   │   ├── error_handler.py     # Global error handling
│   │   ├── headless_downloader.py # Headless download (no DB/TUI deps)
│   │   ├── local_library.py     # Local anime indexing
│   │   ├── logger.py            # Debug logging system
│   │   ├── notifier.py          # System notifications
│   │   ├── player.py            # MPV video player integration
│   │   ├── progress.py          # Watch progress tracking
│   │   ├── scraper.py           # Provider facade
│   │   ├── search.py            # Search service
│   │   ├── shortcuts.py         # Keyboard shortcuts manager
│   │   ├── tracker.py           # MAL/AniList integration
│   │   ├── updater.py           # Auto-update checker
│   │   ├── watch.py             # Streaming service
│   │   ├── _base.py             # Base service class
│   │   └── _tracker_base.py     # Base tracker interface
│   │
│   ├── ui/                      # Terminal UI components
│   │   ├── header.py            # Header display
│   │   ├── menu.py              # Main menu
│   │   └── prompt.py            # Custom prompts
│   │
│   ├── utils/                   # Utility functions
│   │   └── sanitizer.py         # Filename/path sanitization
│   │
│   ├── locales/                 # Internationalization
│   │   ├── en.json              # English translations
│   │   └── tr.json              # Turkish translations
│   │
│   ├── templates/               # HTML templates
│   │   ├── anilist_error.html   # AniList OAuth error page
│   │   ├── anilist_success.html # AniList OAuth success page
│   │   ├── mal_error.html       # MAL OAuth error page
│   │   └── mal_success.html     # MAL OAuth success page
│   │
│   ├── config.py                # Configuration management
│   ├── exceptions.py            # Custom exception hierarchy
│   ├── i18n.py                  # Internationalization system
│   ├── main.py                  # CLI entry point
│   └── __main__.py              # Package execution entry
│
├── tests/                       # Test suite
│   ├── test_api.py              # API commands and headless downloader tests
│   ├── test_cache.py            # Cache manager tests
│   ├── test_exceptions.py       # Exception tests
│   ├── test_sanitizer.py        # Sanitizer tests
│   └── conftest.py              # Pytest fixtures
│
├── weeb_landing/                # Landing page assets
│   ├── logo/                    # Logo files (various sizes)
│   └── index.html               # Landing page
│
├── distribution/                # Build and distribution files
├── pyproject.toml               # Project metadata and dependencies
├── requirements.txt             # Python dependencies
├── pytest.ini                   # Pytest configuration
├── LICENSE                      # GPL License 
└── README.md                    # This file
```

---

## Tech Stack

### Core Technologies
- **Python 3.8+** - Main programming language
- **Typer** - CLI framework with rich terminal support
- **Rich** - Terminal formatting and styling
- **Questionary** - Interactive prompts and menus
- **SQLite** - Local database (WAL mode)

### Web & Networking
- **requests** - HTTP client
- **curl_cffi** - Advanced HTTP with browser impersonation
- **BeautifulSoup4** - HTML parsing
- **lxml** - Fast XML/HTML processing

### Media & Download
- **FFmpeg** - Video processing and conversion
- **MPV** - High-quality video player
- **Aria2** - Multi-connection downloader
- **yt-dlp** - Complex stream downloader (HLS, DASH)

### Encryption & Security
- **pycryptodome** - Encryption/decryption (Turkanime)

### Additional Features
- **pypresence** - Discord Rich Presence
- **py7zr** - 7z archive handling
- **winotify** - Windows notifications
- **pyfiglet** - ASCII art headers
- **packaging** - Version comparison

### Development & Testing
- **pytest** - Testing framework
- **pyinstaller** - Executable builder
- **build** - Python package builder

### Architecture Patterns
- **Provider Pattern** - Pluggable anime sources
- **Registry Pattern** - Dynamic provider registration
- **Service Locator** - Lazy-loaded services
- **Queue Pattern** - Thread-safe download queue
- **Decorator Pattern** - Caching decorator
- **Observer Pattern** - Progress tracking
- **Strategy Pattern** - Multiple download strategies

---

## License

This project is licensed under the **GNU General Public License v3.0**.  
See the [LICENSE](LICENSE) file for the full license text.

Weeb-CLI (C) 2026
