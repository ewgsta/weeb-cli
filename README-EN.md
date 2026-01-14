<p align="center">
  <img src="weeb_landing/logo/512x512.webp" alt="Weeb CLI Logo" width="120">
</p>

<h1 align="center">Weeb CLI</h1>

<p align="center">
  <strong>A powerful, cross-platform command-line tool for anime enthusiasts</strong>
</p>

<p align="center">
  <a href="https://github.com/ewgsta/weeb-cli/releases"><img src="https://img.shields.io/github/v/release/ewgsta/weeb-cli?style=flat-square" alt="Release"></a>
  <a href="https://github.com/ewgsta/weeb-cli/blob/main/LICENSE"><img src="https://img.shields.io/badge/license-CC%20BY--NC--ND%204.0-blue?style=flat-square" alt="License"></a>
  <a href="https://github.com/ewgsta/weeb-cli/stargazers"><img src="https://img.shields.io/github/stars/ewgsta/weeb-cli?style=flat-square" alt="Stars"></a>
</p>

<p align="center">
  <a href="#installation">Installation</a> •
  <a href="#features">Features</a> •
  <a href="#usage">Usage</a> •
  <a href="#sources">Sources</a> •
  <a href="README.md">Türkçe</a>
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

### Homebrew (macOS/Linux)
```bash
brew install ewgsta/tap/weeb-cli
```

### ~~Chocolatey (Windows)~~ *(pending approval)*

### Scoop (Windows)
```powershell
scoop bucket add weeb https://github.com/ewgsta/scoop-bucket.git
scoop install weeb-cli
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
| `Ctrl+C` | Go back / Exit |

---

## Sources

| Source | Language | Status |
|--------|----------|--------|
| Animecix | Turkish | ✅ Active |
| Turkanime | Turkish | ✅ Active |
| Anizle | Turkish | ✅ Active |
| HiAnime | English | ✅ Active |
| AllAnime | English | ✅ Active |

---

## Configuration

Config location: `~/.weeb-cli/weeb.db` (SQLite)

| Setting | Description | Default |
|---------|-------------|---------|
| `aria2_enabled` | Use Aria2 | `true` |
| `max_concurrent_downloads` | Concurrent downloads | `3` |
| `download_dir` | Download folder | `./weeb-downloads` |
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

### Planned
- [ ] MAL/AniList integration
- [ ] Anime recommendations
- [ ] Batch operations
- [ ] Watch statistics (graphs)
- [ ] Database backup/restore
- [ ] Theme support
- [ ] Keyboard shortcuts
- [ ] Subtitle downloads
- [ ] Torrent support (nyaa.si)
- [ ] Watch party

---

## License

This project is licensed under [CC BY-NC-ND 4.0](LICENSE).

---

<p align="center">
  <a href="https://weeb-cli.ewgsta.me">Website</a> •
  <a href="https://github.com/ewgsta/weeb-cli/issues">Report Issue</a>
</p>
