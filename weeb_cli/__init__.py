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
    - Python SDK for programmatic access

Example:
    CLI usage::

        $ weeb-cli start
        $ weeb-cli api search "anime name"
        $ weeb-cli serve --port 8080
    
    SDK usage::

        from weeb_cli import WeebSDK
        
        sdk = WeebSDK(default_provider="hianime")
        results = sdk.search("One Piece")
        episodes = sdk.get_episodes(results[0].id)

Attributes:
    __version__ (str): Current version of Weeb CLI.
"""

__version__ = "2.16.0"

# SDK exports for easy import
from weeb_cli.sdk import WeebSDK, list_providers, get_provider_info

__all__ = [
    "__version__",
    "WeebSDK",
    "list_providers",
    "get_provider_info",
]
