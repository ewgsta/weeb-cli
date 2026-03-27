# Installation

Weeb CLI can be installed through multiple methods depending on your platform and preferences.

## PyPI (Universal)

The easiest way to install Weeb CLI is through pip:

```bash
pip install weeb-cli
```

To upgrade to the latest version:

```bash
pip install --upgrade weeb-cli
```

## Arch Linux (AUR)

For Arch Linux users, Weeb CLI is available in the AUR:

```bash
yay -S weeb-cli
```

Or using any other AUR helper:

```bash
paru -S weeb-cli
```

## Portable Executables

Pre-built portable executables are available for Windows, macOS, and Linux from the [Releases](https://github.com/ewgsta/weeb-cli/releases) page.

1. Download the appropriate file for your platform
2. Extract the archive
3. Run the executable

## Developer Installation

For development or contributing to the project:

```bash
# Clone the repository
git clone https://github.com/ewgsta/weeb-cli.git
cd weeb-cli

# Install in editable mode
pip install -e .

# Install development dependencies
pip install -r requirements.txt
```

## Dependencies

Weeb CLI will automatically download and install the following dependencies on first run:

- **FFmpeg**: Video processing and conversion
- **MPV**: Media player for streaming
- **Aria2**: Fast multi-connection downloads
- **yt-dlp**: Stream extraction and downloading

These tools are downloaded to `~/.weeb-cli/bin/` and managed automatically.

## Verification

After installation, verify that Weeb CLI is installed correctly:

```bash
weeb-cli --version
```

You should see the version number displayed.

## Next Steps

- [Quick Start Guide](quickstart.md): Get started with Weeb CLI
- [Configuration](configuration.md): Configure your preferences
