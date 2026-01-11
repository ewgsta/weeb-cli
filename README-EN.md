<div align="center">
  <img src="https://raw.githubusercontent.com/ewgsta/weeb-cli/refs/heads/main/weeb_landing/logo/256x256.webp" alt="Weeb CLI Logo" width="200" height="200" />
  <h1>Weeb CLI</h1>
  <p>
    <b>No browser, no ads, no distractions. Just you and a unique anime watching experience.</b>
  </p>

  <p>
    <a href="./README.md">Türkçe Oku</a>
  </p>

  <p>
    <a href="https://pypi.org/project/weeb-cli/">
      <img src="https://img.shields.io/pypi/v/weeb-cli?style=flat-square&color=blue" alt="PyPI Version" />
    </a>
    <a href="https://aur.archlinux.org/packages/weeb-cli">
      <img src="https://img.shields.io/aur/version/weeb-cli?style=flat-square&color=magenta" alt="AUR Version" />
    </a>
    <img src="https://img.shields.io/github/license/ewgsta/weeb-cli?style=flat-square" alt="License" />
    <img src="https://img.shields.io/badge/platform-win%20%7C%20linux%20%7C%20macos-lightgrey?style=flat-square" alt="Platform" />
  </p>
</div>

Weeb CLI is a powerful, cross-platform command-line tool designed for anime enthusiasts. Stream, download, and track your favorite anime series directly from your terminal with a beautiful and interactive UI.

---

## Features

- **Advanced Search**: Quickly find anime with fuzzy search and detailed metadata.
- **Seamless Streaming**: Watch episodes instantly using **MPV** with high-quality streaming support (HLS/MP4).
- **Smart Downloader**: 
  - Integrated with **Aria2** for high-speed multi-connection downloads.
  - **yt-dlp** support for complex streams.
  - Queue system with concurrent download management.
  - Smart file naming (e.g., `Anime Name - S1E1.mp4`).
- **Watch History**: Automatically tracks your progress. Resumes where you left off (`●` indicator) and marks completed episodes (`✓`).
- **Multi-language**: Full support for HiAnime, All Anime (English) and TurkAnime, Anizle, Animecix, Weeb (Local Source) (Turkish) interfaces.
- **Auto-Dependency**: Automatically detects and installs necessary tools (MPV, FFmpeg, Aria2, yt-dlp) if missing.

## Installation

### PyPI (Universal)
```bash
pip install weeb-cli
```

### AUR (Arch Linux)
```bash
yay -S weeb-cli
```

### Homebrew (macOS/Linux)
```bash
brew tap ewgsta/tap
brew install weeb-cli
```

### Scoop (Windows)
```bash
scoop bucket add weeb-cli https://github.com/ewgsta/scoop-bucket
scoop install weeb-cli
```

### Chocolatey (Windows)
```bash
choco install weeb-cli
```

---

## Usage

Simply run the tool from your terminal:

```bash
weeb-cli
```

Or use specific commands:

```bash
weeb start       # Launch the main interactive menu
weeb search      # Go directly to search
```

### Controls
- **Arrow Keys**: Navigate menus.
- **Enter**: Select option.
- **Ctrl+C**: Go back / Exit.

---

## Roadmap & To-Do

- [x] Core Search & Details
- [x] Streaming with MPV
- [x] Local Watch History & Progress Tracking
- [x] Download Manager (Aria2/yt-dlp integration)
- [x] Interactive Settings Menu
- [ ] **Anilist / MAL Integration** (Sync your lists)
- [ ] **Torrent Support** (Streaming & Downloading via Webtorrent)
- [ ] **Custom Themes** (Change CLI colors)
- [ ] **Notification System** (New episode alerts)
- [ ] **Batch Download** (Download entire seasons with one click)
- [ ] **Discord RPC** (Show what you're watching)

---

## Configuration

Configuration is stored in `~/.weeb-cli/config.json`. You can modify settings directly via the **Settings** menu in the app.

| Setting | Description | Default |
|---------|-------------|---------|
| `aria2_enabled` | Use Aria2 for faster downloads | `true` |
| `max_concurrent_downloads` | Number of simultaneous downloads | `3` |
| `download_dir` | Directory to save downloads | `./weeb-downloads` |

---

## License

This project is licensed under the Creative Commons Attribution-NonCommercial-NoDerivatives 4.0 International License (CC BY-NC-ND 4.0).
See the [LICENSE](LICENSE) file for details.
