"""AniSkip integration for automatic OP/ED skipping.

This module integrates with the AniSkip API to automatically skip
anime openings and endings during playback.

The service fetches skip timestamps from AniSkip based on MAL ID
and episode number, then provides them to the player for automatic seeking.

Example:
    Basic usage::

        from weeb_cli.services.aniskip import aniskip_service
        
        # Get skip times for an anime episode
        skip_times = aniskip_service.get_skip_times("One Piece", 1)
        
        if skip_times:
            print(f"OP: {skip_times['op']}")
            print(f"ED: {skip_times['ed']}")
"""

import requests
from typing import Optional, Dict, Tuple
from weeb_cli.services.logger import debug as log_debug, error as log_error
from weeb_cli.services.cache import cache


class AniSkipService:
    """Service for fetching anime skip timestamps from AniSkip API.
    
    Provides automatic OP/ED skip functionality by querying MyAnimeList
    for anime IDs and AniSkip API for timestamp data.
    
    Attributes:
        MAL_SEARCH_URL: MyAnimeList search endpoint
        ANISKIP_API_URL: AniSkip API base URL
    """
    
    MAL_SEARCH_URL = "https://myanimelist.net/search/prefix.json"
    ANISKIP_API_URL = "https://api.aniskip.com/v1/skip-times"
    
    def __init__(self):
        self._enabled = False
        self._headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Gecko/20100101 Firefox/109.0",
            "Content-Type": "application/json",
        }
    
    def is_enabled(self) -> bool:
        """Check if AniSkip is enabled in config."""
        return self._enabled
    
    def set_enabled(self, enabled: bool) -> None:
        """Enable or disable AniSkip functionality."""
        self._enabled = enabled
        log_debug(f"[AniSkip] {'Enabled' if enabled else 'Disabled'}")
    
    def get_mal_id(self, anime_name: str) -> Optional[int]:
        """Get MyAnimeList ID for an anime by name.
        
        Args:
            anime_name: Name of the anime to search for.
        
        Returns:
            MAL ID if found, None otherwise.
        """
        cache_key = f"mal_id:{anime_name}"
        cached = cache.get(cache_key)
        if cached:
            log_debug(f"[AniSkip] MAL ID from cache: {cached}")
            return cached
        
        try:
            response = requests.get(
                self.MAL_SEARCH_URL,
                params={"type": "anime", "keyword": anime_name},
                headers=self._headers,
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            
            anime_category = next(
                (cat for cat in data.get("categories", []) if cat.get("type") == "anime"),
                None
            )
            
            if not anime_category or not anime_category.get("items"):
                log_error(f"[AniSkip] No anime found on MAL for: {anime_name}")
                return None
            
            mal_id = anime_category["items"][0]["id"]
            cache.set(cache_key, mal_id, ttl=86400 * 7)  # Cache for 7 days
            log_debug(f"[AniSkip] Found MAL ID {mal_id} for {anime_name}")
            return mal_id
            
        except Exception as e:
            log_error(f"[AniSkip] Failed to get MAL ID: {e}")
            return None
    
    def get_skip_times(
        self, 
        anime_name: str, 
        episode: int
    ) -> Optional[Dict[str, Tuple[float, float]]]:
        """Get skip timestamps for an anime episode.
        
        Args:
            anime_name: Name of the anime.
            episode: Episode number.
        
        Returns:
            Dictionary with 'op' and 'ed' keys containing (start, end) tuples,
            or None if no skip times found.
        """
        if not self._enabled:
            return None
        
        cache_key = f"skip_times:{anime_name}:{episode}"
        cached = cache.get(cache_key)
        if cached:
            log_debug(f"[AniSkip] Skip times from cache")
            return cached
        
        mal_id = self.get_mal_id(anime_name)
        if not mal_id:
            return None
        
        try:
            url = f"{self.ANISKIP_API_URL}/{mal_id}/{episode}"
            response = requests.get(
                url,
                params={"types": ["op", "ed"]},
                headers=self._headers,
                timeout=10
            )
            response.raise_for_status()
            data = response.json()
            
            if not data.get("found"):
                log_debug(f"[AniSkip] No skip times found for {anime_name} EP{episode}")
                return None
            
            skip_times = {}
            for result in data.get("results", []):
                skip_type = result.get("skip_type")
                interval = result.get("interval", {})
                start = interval.get("start_time")
                end = interval.get("end_time")
                
                if skip_type and start is not None and end is not None:
                    skip_times[skip_type] = (start, end)
            
            if not skip_times:
                return None
            
            cache.set(cache_key, skip_times, ttl=86400 * 30)  # Cache for 30 days
            log_debug(f"[AniSkip] Found skip times: {skip_times}")
            return skip_times
            
        except Exception as e:
            log_error(f"[AniSkip] Failed to get skip times: {e}")
            return None


# Global instance
aniskip_service = AniSkipService()
