"""Weeb CLI SDK - Programmatic API for Python applications.

This module provides a Python SDK for integrating Weeb CLI functionality
directly into your applications without spawning new processes or using
the CLI interface.

The SDK provides the same functionality as the `weeb-cli api` commands
but as native Python functions with proper type hints and error handling.

Example:
    Basic usage::

        from weeb_cli.sdk import WeebSDK
        
        # Initialize SDK
        sdk = WeebSDK()
        
        # Search for anime
        results = sdk.search("One Piece", provider="hianime")
        for anime in results:
            print(f"{anime.title} ({anime.year})")
        
        # Get episodes
        episodes = sdk.get_episodes(results[0].id, provider="hianime")
        
        # Get stream URLs
        streams = sdk.get_streams(
            anime_id=results[0].id,
            episode_id=episodes[0].id,
            provider="hianime"
        )
        
        # Download episode
        path = sdk.download_episode(
            anime_id=results[0].id,
            season=1,
            episode=1,
            provider="hianime",
            output_dir="./downloads"
        )

Features:
    - No subprocess overhead - direct Python API
    - Type-safe with full type hints
    - Automatic provider discovery
    - Headless mode (no database/TUI dependencies)
    - Same caching as CLI mode
    - Thread-safe operations

Classes:
    WeebSDK: Main SDK interface
    
Functions:
    list_providers: Quick access to provider list
    get_provider_info: Get metadata for a specific provider
"""

from typing import List, Optional, Dict, Any
from pathlib import Path

from weeb_cli.config import config
from weeb_cli.providers.base import AnimeResult, Episode, StreamLink, AnimeDetails
from weeb_cli.providers.registry import get_provider, list_providers as _list_providers
from weeb_cli.exceptions import ProviderError, WeebCLIError
from weeb_cli.services.logger import debug


class WeebSDK:
    """Main SDK interface for Weeb CLI functionality.
    
    Provides programmatic access to all Weeb CLI features including
    search, episode listing, stream extraction, and downloading.
    
    The SDK operates in headless mode by default, meaning it doesn't
    require database access or TUI dependencies. This makes it perfect
    for integration into other applications, scripts, or services.
    
    Attributes:
        headless (bool): Whether SDK is running in headless mode.
        default_provider (str): Default provider to use when not specified.
    
    Example:
        >>> sdk = WeebSDK(default_provider="hianime")
        >>> results = sdk.search("Naruto")
        >>> print(f"Found {len(results)} results")
    """
    
    def __init__(self, headless: bool = True, default_provider: Optional[str] = None):
        """Initialize Weeb CLI SDK.
        
        Args:
            headless: Run in headless mode (no database/TUI). Default: True.
            default_provider: Default provider name to use. If None, uses
                            'animecix' as fallback.
        
        Example:
            >>> sdk = WeebSDK()  # Headless with default provider
            >>> sdk = WeebSDK(default_provider="hianime")  # Custom default
            >>> sdk = WeebSDK(headless=False)  # With database access
        """
        self.headless = headless
        self.default_provider = default_provider or "animecix"
        
        if headless:
            config.set_headless(True)
            debug("[SDK] Initialized in headless mode")
    
    def list_providers(self) -> List[Dict[str, Any]]:
        """List all available anime providers.
        
        Returns:
            List of provider metadata dictionaries containing:
                - name (str): Provider identifier
                - lang (str): Language code (en, tr, de, pl)
                - region (str): Region code (US, TR, DE, PL)
                - class (str): Provider class name
                - disabled (bool): Whether provider is disabled
        
        Example:
            >>> sdk = WeebSDK()
            >>> providers = sdk.list_providers()
            >>> for p in providers:
            ...     print(f"{p['name']}: {p['lang']} ({p['region']})")
            animecix: tr (TR)
            hianime: en (US)
            aniworld: de (DE)
        """
        return _list_providers()
    
    def get_provider_info(self, provider_name: str) -> Optional[Dict[str, Any]]:
        """Get metadata for a specific provider.
        
        Args:
            provider_name: Provider identifier (e.g., 'animecix', 'hianime').
        
        Returns:
            Provider metadata dictionary, or None if not found.
        
        Example:
            >>> sdk = WeebSDK()
            >>> info = sdk.get_provider_info("hianime")
            >>> print(info['lang'])
            en
        """
        providers = self.list_providers()
        return next((p for p in providers if p['name'] == provider_name), None)
    
    def search(
        self, 
        query: str, 
        provider: Optional[str] = None
    ) -> List[AnimeResult]:
        """Search for anime by query string.
        
        Args:
            query: Search query (anime title or keywords).
            provider: Provider name to use. If None, uses default_provider.
        
        Returns:
            List of anime search results.
        
        Raises:
            ProviderError: If provider not found or search fails.
            WeebCLIError: For other errors.
        
        Example:
            >>> sdk = WeebSDK()
            >>> results = sdk.search("One Piece", provider="hianime")
            >>> for anime in results:
            ...     print(f"{anime.title} - {anime.year}")
            One Piece - 1999
        """
        provider_name = provider or self.default_provider
        provider_instance = get_provider(provider_name)
        
        if provider_instance is None:
            raise ProviderError(f"Provider not found or disabled: {provider_name}")
        
        debug(f"[SDK] Searching '{query}' on {provider_name}")
        return provider_instance.search(query)
    
    def get_details(
        self, 
        anime_id: str, 
        provider: Optional[str] = None
    ) -> Optional[AnimeDetails]:
        """Get detailed information for an anime.
        
        Args:
            anime_id: Unique anime identifier from search results.
            provider: Provider name to use. If None, uses default_provider.
        
        Returns:
            Complete anime details with episodes, or None if not found.
        
        Raises:
            ProviderError: If provider not found or fetch fails.
        
        Example:
            >>> sdk = WeebSDK()
            >>> details = sdk.get_details("anime-id", provider="hianime")
            >>> print(f"{details.title}: {details.description}")
            >>> print(f"Episodes: {len(details.episodes)}")
        """
        provider_name = provider or self.default_provider
        provider_instance = get_provider(provider_name)
        
        if provider_instance is None:
            raise ProviderError(f"Provider not found or disabled: {provider_name}")
        
        debug(f"[SDK] Fetching details for '{anime_id}' from {provider_name}")
        return provider_instance.get_details(anime_id)
    
    def get_episodes(
        self, 
        anime_id: str, 
        season: Optional[int] = None,
        provider: Optional[str] = None
    ) -> List[Episode]:
        """Get list of available episodes for an anime.
        
        Args:
            anime_id: Unique anime identifier.
            season: Filter by season number (optional).
            provider: Provider name to use. If None, uses default_provider.
        
        Returns:
            List of episodes with metadata.
        
        Raises:
            ProviderError: If provider not found or fetch fails.
        
        Example:
            >>> sdk = WeebSDK()
            >>> episodes = sdk.get_episodes("anime-id", season=1, provider="hianime")
            >>> for ep in episodes:
            ...     print(f"S{ep.season:02d}E{ep.number:02d}: {ep.title}")
            S01E01: First Episode
        """
        provider_name = provider or self.default_provider
        provider_instance = get_provider(provider_name)
        
        if provider_instance is None:
            raise ProviderError(f"Provider not found or disabled: {provider_name}")
        
        debug(f"[SDK] Fetching episodes for '{anime_id}' from {provider_name}")
        episodes = provider_instance.get_episodes(anime_id)
        
        # Filter by season if specified
        if season is not None:
            episodes = [ep for ep in episodes if ep.season == season]
        
        return episodes
    
    def get_streams(
        self, 
        anime_id: str, 
        episode_id: str,
        provider: Optional[str] = None
    ) -> List[StreamLink]:
        """Get stream URLs for a specific episode.
        
        Args:
            anime_id: Unique anime identifier.
            episode_id: Unique episode identifier.
            provider: Provider name to use. If None, uses default_provider.
        
        Returns:
            List of available stream links with quality options.
        
        Raises:
            ProviderError: If provider not found or extraction fails.
        
        Example:
            >>> sdk = WeebSDK()
            >>> streams = sdk.get_streams("anime-id", "ep-id", provider="hianime")
            >>> for stream in streams:
            ...     print(f"{stream.quality}: {stream.url}")
            1080p: https://...
        """
        provider_name = provider or self.default_provider
        provider_instance = get_provider(provider_name)
        
        if provider_instance is None:
            raise ProviderError(f"Provider not found or disabled: {provider_name}")
        
        debug(f"[SDK] Fetching streams for episode '{episode_id}' from {provider_name}")
        return provider_instance.get_streams(anime_id, episode_id)
    
    def download_episode(
        self,
        anime_id: str,
        season: int,
        episode: int,
        provider: Optional[str] = None,
        output_dir: str = ".",
        anime_title: Optional[str] = None
    ) -> Optional[str]:
        """Download an episode to local storage.
        
        Automatically selects the best quality stream and downloads it
        using the headless downloader (no database dependencies).
        
        Args:
            anime_id: Unique anime identifier.
            season: Season number.
            episode: Episode number.
            provider: Provider name to use. If None, uses default_provider.
            output_dir: Directory to save the file. Default: current directory.
            anime_title: Custom anime title for filename. If None, fetches
                        from provider.
        
        Returns:
            Path to downloaded file, or None if download failed.
        
        Raises:
            ProviderError: If provider not found or no streams available.
            WeebCLIError: If download fails.
        
        Example:
            >>> sdk = WeebSDK()
            >>> path = sdk.download_episode(
            ...     anime_id="anime-id",
            ...     season=1,
            ...     episode=1,
            ...     provider="hianime",
            ...     output_dir="./downloads"
            ... )
            >>> print(f"Downloaded to: {path}")
            Downloaded to: ./downloads/Anime Name - S01E01.mp4
        """
        from weeb_cli.services.headless_downloader import download_episode
        
        provider_name = provider or self.default_provider
        provider_instance = get_provider(provider_name)
        
        if provider_instance is None:
            raise ProviderError(f"Provider not found or disabled: {provider_name}")
        
        # Get episodes to find the target episode
        episodes = provider_instance.get_episodes(anime_id)
        target_episodes = [
            ep for ep in episodes 
            if ep.season == season and ep.number == episode
        ]
        
        if not target_episodes:
            raise WeebCLIError(
                f"Episode S{season:02d}E{episode:02d} not found",
                code="EPISODE_NOT_FOUND"
            )
        
        target_episode = target_episodes[0]
        
        # Get stream links
        stream_links = provider_instance.get_streams(anime_id, target_episode.id)
        if not stream_links:
            raise WeebCLIError(
                "No streams available for this episode",
                code="NO_STREAMS"
            )
        
        # Sort by quality (best first)
        def quality_score(quality: str) -> int:
            q = (quality or "").lower()
            if "4k" in q or "2160" in q:
                return 5
            if "1080" in q:
                return 4
            if "720" in q:
                return 3
            if "480" in q:
                return 2
            if "360" in q:
                return 1
            return 0
        
        stream_links.sort(key=lambda s: quality_score(s.quality), reverse=True)
        
        # Get anime title if not provided
        if anime_title is None:
            details = provider_instance.get_details(anime_id)
            anime_title = details.title if details else anime_id
        
        # Try each stream until one succeeds
        debug(f"[SDK] Downloading S{season:02d}E{episode:02d} of '{anime_title}'")
        for stream in stream_links:
            result = download_episode(
                stream_url=stream.url,
                series_title=anime_title,
                season=season,
                episode=episode,
                download_dir=output_dir,
            )
            if result:
                debug(f"[SDK] Download successful: {result}")
                return result
        
        raise WeebCLIError(
            "All stream download attempts failed",
            code="DOWNLOAD_FAILED"
        )
    
    def download_url(
        self,
        stream_url: str,
        title: str,
        season: int,
        episode: int,
        output_dir: str = "."
    ) -> Optional[str]:
        """Download a video from a direct stream URL.
        
        Useful when you already have a stream URL and just need to download it.
        
        Args:
            stream_url: Direct stream URL (HLS, MP4, etc.).
            title: Series title for filename.
            season: Season number.
            episode: Episode number.
            output_dir: Directory to save the file. Default: current directory.
        
        Returns:
            Path to downloaded file, or None if download failed.
        
        Example:
            >>> sdk = WeebSDK()
            >>> path = sdk.download_url(
            ...     stream_url="https://example.com/video.m3u8",
            ...     title="My Anime",
            ...     season=1,
            ...     episode=1,
            ...     output_dir="./downloads"
            ... )
        """
        from weeb_cli.services.headless_downloader import download_episode
        
        debug(f"[SDK] Downloading from URL: {stream_url}")
        return download_episode(
            stream_url=stream_url,
            series_title=title,
            season=season,
            episode=episode,
            download_dir=output_dir,
        )


# Convenience functions for quick access
def list_providers() -> List[Dict[str, Any]]:
    """Quick access to provider list without SDK instance.
    
    Returns:
        List of provider metadata dictionaries.
    
    Example:
        >>> from weeb_cli.sdk import list_providers
        >>> providers = list_providers()
        >>> print([p['name'] for p in providers])
        ['animecix', 'turkanime', 'hianime', ...]
    """
    return _list_providers()


def get_provider_info(provider_name: str) -> Optional[Dict[str, Any]]:
    """Quick access to provider info without SDK instance.
    
    Args:
        provider_name: Provider identifier.
    
    Returns:
        Provider metadata dictionary, or None if not found.
    
    Example:
        >>> from weeb_cli.sdk import get_provider_info
        >>> info = get_provider_info("hianime")
        >>> print(info['lang'])
        en
    """
    providers = list_providers()
    return next((p for p in providers if p['name'] == provider_name), None)
