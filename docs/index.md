# Weeb CLI Documentation

**No browser, no ads, no distractions. Just you and an unparalleled anime viewing experience.**

## Welcome

Weeb CLI is a powerful terminal-based anime streaming and downloading application that provides a browser-free, ad-free anime viewing experience. With support for multiple anime sources across different languages, integrated tracking services, and advanced download management, Weeb CLI is your all-in-one anime companion.

## Key Features

### Multi-Source Support
- Turkish: Animecix, Turkanime, Anizle, Weeb
- English: HiAnime, AllAnime
- German: AniWorld
- Polish: Docchi

### Smart Streaming
- High-quality HLS/MP4 playback with MPV
- Resume from where you left off
- Watch history and statistics
- Episode progress tracking

### Advanced Downloads
- Multi-connection fast downloads with Aria2
- Complex stream support with yt-dlp
- Queue system with concurrent downloads
- Resume interrupted downloads
- Smart file naming

### Tracker Integration
- AniList, MyAnimeList, and Kitsu support
- OAuth authentication
- Automatic progress sync
- Offline queue for pending updates

### Local Library
- Auto-scan downloaded anime
- External drive support (USB, HDD)
- Offline anime indexing
- Smart title matching

### Additional Features
- Multi-language support (TR, EN, DE, PL)
- Discord Rich Presence
- System notifications
- Non-interactive JSON API
- Torznab server for *arr integration

## Quick Start

```bash
# Install via pip
pip install weeb-cli

# Start interactive mode
weeb-cli

# Use API mode
weeb-cli api search "anime name"
```

## Documentation Structure

- **[Getting Started](getting-started/installation.md)**: Installation and initial setup
- **[User Guide](user-guide/searching.md)**: Detailed usage instructions
- **[API Reference](api/overview.md)**: Complete API documentation
- **[Development](development/contributing.md)**: Contributing and development guide
- **[CLI Reference](cli/commands.md)**: Command-line interface documentation

## Support

- **GitHub**: [ewgsta/weeb-cli](https://github.com/ewgsta/weeb-cli)
- **Issues**: [Report bugs](https://github.com/ewgsta/weeb-cli/issues)
- **PyPI**: [weeb-cli](https://pypi.org/project/weeb-cli/)

## License

Weeb CLI is licensed under the GPL-3.0 License. See [LICENSE](https://github.com/ewgsta/weeb-cli/blob/main/LICENSE) for details.
