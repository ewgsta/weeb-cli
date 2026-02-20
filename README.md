<p align="center">
  <img src="weeb_landing/logo/512x512.webp" alt="Weeb CLI Logo" width="120">
</p>

<h1 align="center">Weeb CLI</h1>

<p align="center">
  <strong>No browser, no ads, no distractions. Just you and an unparalleled anime viewing experience.</strong>
</p>

<p align="center">
  <a href="https://github.com/ewgsta/weeb-cli/releases"><img src="https://img.shields.io/github/v/release/ewgsta/weeb-cli?style=flat-square" alt="Release"></a>
  <a href="https://github.com/ewgsta/weeb-cli/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-CC%20BY--NC--ND%204.0-blue?style=flat-square" alt="License"></a>
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

| Setting | Description | Default |
|---------|-------------|---------|
| `aria2_enabled` | Use Aria2 | `true` |
| `max_concurrent_downloads` | Concurrent downloads | `3` |
| `download_dir` | Download folder | `./weeb-downloads` |
| `discord_rpc_enabled` | Discord RPC | `false` |
| `debug_mode` | Debug logging | `false` |

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


### Planned
- [ ] Anime recommendations
- [ ] Batch operations
- [ ] Watch statistics (graphs)
- [ ] Theme support
- [ ] Subtitle downloads
- [ ] Torrent support (nyaa.si)
- [ ] Watch party

---

## License

This project is licensed under [CC BY-NC-ND 4.0](LICENSE).

---

## Project Structure

```
weeb-cli/
├── weeb_cli/                    # Main application package
│   ├── commands/                # CLI command handlers
│   │   ├── downloads.py         # Download management commands
│   │   ├── search.py            # Anime search functionality
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
├── LICENSE                      # CC BY-NC-ND 4.0 license
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

<p align="center">
  <a href="https://weeb-cli.ewgsta.me">Website</a> •
  <a href="https://github.com/ewgsta/weeb-cli/issues">Report Issue</a>
</p>
