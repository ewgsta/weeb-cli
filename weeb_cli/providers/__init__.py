"""Anime source providers for Weeb CLI.

This package implements a pluggable provider system for fetching anime content
from various sources across different languages and regions.

Architecture:
    - Base provider interface (BaseProvider) defines standard methods
    - Language-organized structure (tr/, en/, de/, pl/)
    - Registry pattern for dynamic provider discovery
    - Stream extractors for various hosting services

Supported Providers:
    Turkish: Animecix, Turkanime, Anizle, Weeb
    English: HiAnime, AllAnime
    German: AniWorld
    Polish: Docchi

Example:
    Using a provider::

        from weeb_cli.providers import get_provider
        
        provider = get_provider("animecix")
        results = provider.search("One Piece")
        details = provider.get_details(results[0].id)
        streams = provider.get_streams(details.id, episode_id)

Modules:
    base: Abstract base provider interface and data classes
    registry: Provider registration and discovery system
    extractors: Stream URL extractors for various hosting services
    tr/: Turkish anime providers
    en/: English anime providers
    de/: German anime providers
    pl/: Polish anime providers
"""

from .registry import (
    get_provider,
    get_providers_for_lang,
    list_providers,
    get_default_provider,
    register_provider
)

__all__ = [
    "get_provider",
    "get_providers_for_lang",
    "list_providers",
    "get_default_provider",
    "register_provider"
]
