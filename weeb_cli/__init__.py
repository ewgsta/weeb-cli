"""Weeb CLI - Terminal-based anime streaming and downloading application.

Weeb CLI provides a browser-free, ad-free anime viewing experience with support
for multiple anime sources across different languages (Turkish, English, German, Polish).

Features:
    - Multi-source anime streaming and downloading
    - Integration with tracking services (AniList, MyAnimeList, Kitsu)
    - Local library management with external drive support
    - Advanced download queue with Aria2 and yt-dlp
    - Discord Rich Presence integration
    - Multi-language support (TR, EN, DE, PL)

Example:
    Basic usage::

        $ weeb-cli start
        $ weeb-cli api search "anime name"
        $ weeb-cli serve --port 8080

Attributes:
    __version__ (str): Current version of Weeb CLI.
"""

__version__ = "3.0.0"
