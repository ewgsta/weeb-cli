"""Base provider interface and data classes for anime sources.

This module defines the abstract base class and data structures that all
anime providers must implement. It provides a consistent interface for
searching, fetching details, and extracting streams from various sources.

Data Classes:
    AnimeResult: Search result representation
    Episode: Episode information
    StreamLink: Stream URL with metadata
    AnimeDetails: Complete anime information

Base Class:
    BaseProvider: Abstract interface for all providers

Example:
    Implementing a provider::

        from weeb_cli.providers.base import BaseProvider, AnimeResult
        from weeb_cli.providers.registry import register_provider
        
        @register_provider("myprovider", lang="en", region="US")
        class MyProvider(BaseProvider):
            def search(self, query: str) -> List[AnimeResult]:
                # Implementation
                pass
            
            def get_details(self, anime_id: str) -> Optional[AnimeDetails]:
                # Implementation
                pass
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any

from weeb_cli.exceptions import ProviderError
from weeb_cli.services.logger import debug


@dataclass
class AnimeResult:
    """Search result for an anime.
    
    Represents a single anime in search results with basic information.
    
    Attributes:
        id: Unique identifier for the anime (provider-specific).
        title: Display title of the anime.
        type: Content type (e.g., 'series', 'movie', 'ova').
        cover: URL to cover/poster image.
        year: Release year.
    """
    id: str
    title: str
    type: str = "series"
    cover: Optional[str] = None
    year: Optional[int] = None
    
    
@dataclass
class Episode:
    """Episode information.
    
    Represents a single episode with metadata.
    
    Attributes:
        id: Unique identifier for the episode (provider-specific).
        number: Episode number within the season.
        title: Episode title (if available).
        season: Season number (default: 1).
        url: Direct URL to episode page (optional).
    """
    id: str
    number: int
    title: Optional[str] = None
    season: int = 1
    url: Optional[str] = None


@dataclass
class StreamLink:
    """Stream URL with metadata.
    
    Represents a playable stream with quality and server information.
    
    Attributes:
        url: Direct stream URL (HLS, MP4, etc.).
        quality: Quality label (e.g., '1080p', '720p', 'auto').
        server: Server/host name (e.g., 'megacloud', 'default').
        headers: HTTP headers required for playback.
        subtitles: URL to subtitle file (optional).
    """
    url: str
    quality: str = "auto"
    server: str = "default"
    headers: Dict[str, str] = field(default_factory=dict)
    subtitles: Optional[str] = None


@dataclass
class AnimeDetails:
    """Complete anime information.
    
    Represents full details of an anime including episodes.
    
    Attributes:
        id: Unique identifier for the anime.
        title: Display title.
        description: Synopsis/description text.
        cover: URL to cover/poster image.
        genres: List of genre tags.
        year: Release year.
        status: Airing status (e.g., 'ongoing', 'completed').
        episodes: List of available episodes.
        total_episodes: Total episode count (if known).
    """
    id: str
    title: str
    description: Optional[str] = None
    cover: Optional[str] = None
    genres: List[str] = field(default_factory=list)
    year: Optional[int] = None
    status: Optional[str] = None
    episodes: List[Episode] = field(default_factory=list)
    total_episodes: Optional[int] = None


class BaseProvider(ABC):
    """Abstract base class for anime providers.
    
    All anime source providers must inherit from this class and implement
    the abstract methods. Provides common functionality like HTTP requests
    with retry logic.
    
    Class Attributes:
        name: Provider identifier (set by @register_provider).
        lang: Language code (e.g., 'en', 'tr', 'de', 'pl').
        region: Region code (e.g., 'US', 'TR', 'DE', 'PL').
    
    Instance Attributes:
        headers: Default HTTP headers for requests.
    
    Example:
        Implementing a provider::

            @register_provider("myprovider", lang="en", region="US")
            class MyProvider(BaseProvider):
                def search(self, query: str) -> List[AnimeResult]:
                    results = self._request(f"{BASE_URL}/search?q={query}")
                    return [AnimeResult(id=r['id'], title=r['title']) 
                            for r in results]
    """
    
    name: str = "base"
    lang: str = "tr"
    region: str = "TR"
    
    def __init__(self) -> None:
        """Initialize provider with default headers."""
        self.headers: Dict[str, str] = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/html, */*',
        }
    
    @abstractmethod
    def search(self, query: str) -> List[AnimeResult]:
        """Search for anime by query string.
        
        Args:
            query: Search query (anime title or keywords).
        
        Returns:
            List of anime search results.
        
        Raises:
            ProviderError: If search fails.
        """
        pass
    
    @abstractmethod
    def get_details(self, anime_id: str) -> Optional[AnimeDetails]:
        """Get detailed information for an anime.
        
        Args:
            anime_id: Unique anime identifier from search results.
        
        Returns:
            Complete anime details, or None if not found.
        
        Raises:
            ProviderError: If fetching details fails.
        """
        pass
    
    @abstractmethod
    def get_episodes(self, anime_id: str) -> List[Episode]:
        """Get list of available episodes for an anime.
        
        Args:
            anime_id: Unique anime identifier.
        
        Returns:
            List of episodes with metadata.
        
        Raises:
            ProviderError: If fetching episodes fails.
        """
        pass
    
    @abstractmethod
    def get_streams(self, anime_id: str, episode_id: str) -> List[StreamLink]:
        """Get stream URLs for a specific episode.
        
        Args:
            anime_id: Unique anime identifier.
            episode_id: Unique episode identifier.
        
        Returns:
            List of available stream links with quality options.
        
        Raises:
            ProviderError: If extracting streams fails.
        """
        pass
    
    def _request(
        self, 
        url: str, 
        params: Optional[dict] = None, 
        json_response: bool = True, 
        max_retries: int = 3
    ) -> Any:
        """Make HTTP GET request with retry logic.
        
        Provides automatic retry with exponential backoff for transient errors.
        Skips retries for permanent errors (404, 403, 401).
        
        Args:
            url: Target URL.
            params: Query parameters.
            json_response: Whether to parse response as JSON.
            max_retries: Maximum number of retry attempts.
        
        Returns:
            Parsed JSON dict/list if json_response=True, otherwise raw text.
            Returns None if all retries fail.
        
        Example:
            >>> data = self._request("https://api.example.com/anime")
            >>> html = self._request("https://example.com", json_response=False)
        """
        import requests
        import time
        import random
        
        for attempt in range(max_retries):
            try:
                response = requests.get(
                    url, 
                    headers=self.headers, 
                    params=params,
                    timeout=15
                )
                response.raise_for_status()
                
                if json_response:
                    return response.json()
                return response.text
                
            except requests.RequestException as e:
                debug(f"[HTTP] Request failed (attempt {attempt + 1}/{max_retries}): {url} - {e}")
                
                if attempt < max_retries - 1:
                    # Skip retries for permanent errors
                    if isinstance(e, requests.HTTPError) and e.response.status_code in [404, 403, 401]:
                        debug(f"[HTTP] Permanent error, skipping retries")
                        return None
                    
                    # Exponential backoff with jitter
                    delay = min(2 ** attempt, 10) + random.uniform(0, 1)
                    time.sleep(delay)
                    continue
                
                return None
