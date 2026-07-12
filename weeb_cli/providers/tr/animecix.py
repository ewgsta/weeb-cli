"""
Animecix provider for weeb-cli.

This provider supports animecix.tv, a Turkish anime streaming site.
Uses modern API endpoints with dynamic header management for stable operation.

Features:
- Dynamic header fetching with Playwright (cached for 1 hour)
- Comprehensive error handling and logging
- Support for series and movies
- Multiple season/episode handling
"""

import json
import time
from typing import List, Optional, Dict, Any
from urllib.parse import urlparse, parse_qs, quote

import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from weeb_cli.providers.base import (
    BaseProvider,
    AnimeResult,
    AnimeDetails,
    Episode,
    StreamLink
)
from weeb_cli.providers.registry import register_provider
from weeb_cli.providers.tr.animecix_helpers import (
    get_dynamic_headers,
    build_headers,
    clean_title_name,
    parse_episode_number,
    parse_season_number,
    retry_with_backoff
)
from weeb_cli.exceptions import ProviderError
from weeb_cli.services.logger import debug

# API endpoints
BASE_URL = "https://animecix.tv"
SEARCH_URL = f"{BASE_URL}/secure/search"
TITLES_URL = f"{BASE_URL}/secure/titles"
EPISODE_VIDEOS_URL = f"{BASE_URL}/secure/episode-videos-points"

# Video player domains
VIDEO_PLAYERS = ["tau-video.xyz", "sibnet.ru"]


def create_session() -> requests.Session:
    """
    Create a requests session with retry logic.
    
    Returns:
        Configured requests.Session with automatic retries.
    """
    session = requests.Session()
    
    # Configure retry strategy
    retry_strategy = Retry(
        total=3,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET", "OPTIONS"]
    )
    
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    
    return session


@register_provider("animecix", lang="tr", region="TR")
class AnimeCixProvider(BaseProvider):
    """
    Animecix.tv provider implementation.
    
    Supports searching, fetching details, and extracting streams from animecix.tv.
    Uses dynamic headers and modern API endpoints for stability.
    """
    
    def __init__(self):
        super().__init__()
        self.session = create_session()
        self.dynamic_headers = None
        debug("[AnimeCix] Provider initialized")
    
    def _get_headers(self, force_refresh: bool = False) -> Dict[str, str]:
        """
        Get headers for API requests.
        
        Args:
            force_refresh: Force refresh of dynamic headers.
        
        Returns:
            Complete headers dictionary.
        """
        if self.dynamic_headers is None or force_refresh:
            self.dynamic_headers = get_dynamic_headers(force_refresh)
            debug(f"[AnimeCix] Dynamic headers refreshed: {list(self.dynamic_headers.keys())}")
        
        return build_headers(self.dynamic_headers)
    
    def _request_json(self, url: str, params: Optional[Dict[str, Any]] = None, 
                     retry_count: int = 0) -> Optional[Dict[str, Any]]:
        """
        Make JSON API request with error handling.
        
        Args:
            url: Request URL.
            params: Query parameters.
            retry_count: Current retry attempt (internal).
        
        Returns:
            Parsed JSON response or None on failure.
        """
        try:
            force_refresh = (retry_count > 1)
            headers = self._get_headers(force_refresh=force_refresh)
            
            debug(f"[AnimeCix] GET {url} (retry={retry_count})")
            if params:
                debug(f"[AnimeCix] Params: {params}")
            
            resp = self.session.get(url, headers=headers, params=params, timeout=20)
            
            debug(f"[AnimeCix] Response: {resp.status_code}")
            
            # Handle authentication errors by refreshing headers
            if resp.status_code in (401, 403) and retry_count < 3:
                debug(f"[AnimeCix] Auth error, retrying (attempt {retry_count + 1}/3)")
                time.sleep(1)
                return self._request_json(url, params, retry_count + 1)
            
            resp.raise_for_status()
            
            data = resp.json()
            return data
            
        except requests.exceptions.JSONDecodeError as e:
            debug(f"[AnimeCix] JSON decode error: {e}")
            return None
        except requests.exceptions.RequestException as e:
            debug(f"[AnimeCix] Request error: {e}")
            return None
        except Exception as e:
            debug(f"[AnimeCix] Unexpected error: {e}")
            return None
    
    def search(self, query: str) -> List[AnimeResult]:
        """
        Search for anime by query string.
        
        Uses /secure/search/{query} endpoint.
        
        Args:
            query: Search query (anime title).
        
        Returns:
            List of anime search results.
        
        Raises:
            ProviderError: If search fails.
        """
        if not query or not query.strip():
            debug("[AnimeCix] Empty search query")
            return []
        
        debug(f"[AnimeCix] Searching for: {query}")
        
        # Clean and encode query
        query_clean = clean_title_name(query)
        url = f"{SEARCH_URL}/{quote(query_clean, safe='-')}"
        params = {"type": "", "limit": 20}
        
        data = self._request_json(url, params)
        
        if not data or "results" not in data:
            debug("[AnimeCix] No results found")
            return []
        
        results = []
        for item in data["results"]:
            anime_id = item.get("id")
            name = item.get("name")
            
            if not anime_id or not name:
                continue
            
            result = AnimeResult(
                id=str(anime_id),
                title=name,
                type=self._parse_type(item.get("title_type", "")),
                cover=item.get("poster"),
                year=item.get("year")
            )
            results.append(result)
        
        debug(f"[AnimeCix] Found {len(results)} results")
        return results
    
    def get_details(self, anime_id: str) -> Optional[AnimeDetails]:
        """
        Get detailed information for an anime.
        
        Uses /secure/titles/{id} endpoint to fetch full anime details.
        
        Args:
            anime_id: Unique anime identifier.
        
        Returns:
            Complete anime details with episodes.
        """
        try:
            title_id = int(anime_id)
        except (ValueError, TypeError):
            debug(f"[AnimeCix] Invalid anime_id: {anime_id}")
            return None
        
        debug(f"[AnimeCix] Fetching details for anime_id={title_id}")
        
        url = f"{TITLES_URL}/{title_id}"
        data = self._request_json(url, params={"titleId": title_id})
        
        if not data or "title" not in data:
            debug(f"[AnimeCix] No data returned for anime_id={title_id}")
            return None
        
        title = data["title"]
        
        # Extract basic info
        anime_name = title.get("name", "Unknown")
        description = title.get("description")
        poster = title.get("poster")
        year = title.get("year")
        anime_type = self._parse_type(title.get("type", ""))
        
        # Extract genres
        genres = [g.get("name", "") for g in title.get("genres", []) if g.get("name")]
        
        # Get episodes from seasons
        episodes = self._extract_episodes_from_title(title, title_id)
        
        debug(f"[AnimeCix] {anime_name}: {len(episodes)} episodes found")
        
        return AnimeDetails(
            id=anime_id,
            title=anime_name,
            description=description,
            cover=poster,
            genres=genres,
            year=year,
            status=title.get("status"),
            episodes=episodes,
            total_episodes=len(episodes)
        )
    
    def _extract_episodes_from_title(self, title: Dict[str, Any], title_id: int) -> List[Episode]:
        """
        Extract episode list from title data.
        
        Since /secure/titles endpoint doesn't include episode data,
        we need to fetch each season separately with seasonNumber parameter.
        
        Args:
            title: Title data from API.
            title_id: Title ID for fetching seasons.
        
        Returns:
            List of Episode objects with composite IDs including season/episode info.
        """
        episodes = []
        
        # Check anime type - use title_type as fallback since type can be null
        anime_type = title.get("type") or title.get("title_type") or ""
        anime_type = anime_type.lower() if anime_type else ""
        is_movie = "movie" in anime_type or "film" in anime_type
        
        # For movies, try videos endpoint
        if is_movie:
            videos = title.get("videos", [])
            if videos:
                debug(f"[AnimeCix] Movie detected, {len(videos)} video sources available")
                # For movies, create a single episode that represents the movie
                # Store all video sources in a special format for later stream extraction
                # Use title_id as episode ID with special marker
                episodes.append(Episode(
                    id=f"movie:{title_id}",  # Special format for movies
                    number=1,
                    title=title.get("name", "Movie"),
                    season=1,
                    url=None
                ))
                return episodes
            else:
                debug(f"[AnimeCix] Movie detected but no videos found")
                return []
        
        # For series, fetch each season with seasonNumber parameter
        seasons = title.get("seasons", [])
        season_count = title.get("season_count", len(seasons))
        
        if not seasons and season_count:
            debug(f"[AnimeCix] No seasons array, using season_count={season_count}")
            seasons = [{"number": i} for i in range(1, season_count + 1)]
        
        if not seasons:
            debug(f"[AnimeCix] No seasons found for title_id={title_id}")
            return []
        
        debug(f"[AnimeCix] Fetching {len(seasons)} seasons")
        
        # Fetch each season's episodes
        title_name = clean_title_name(title.get("name_romanji") or title.get("name", ""))
        
        for season in seasons:
            season_number = parse_season_number(season, 1)
            
            # Fetch season details with seasonNumber parameter
            season_episodes = self._fetch_season_episodes(title_id, season_number, title_name)
            episodes.extend(season_episodes)
        
        return episodes
    
    def _fetch_season_episodes(self, title_id: int, season_number: int, title_name: str) -> List[Episode]:
        """
        Fetch episodes for a specific season.
        
        Uses /secure/titles/{id}?seasonNumber={num}&titleName={name} endpoint.
        
        Args:
            title_id: Anime ID.
            season_number: Season number.
            title_name: URL-safe anime title name.
        
        Returns:
            List of Episode objects for this season with composite IDs.
        """
        params = {
            "titleId": title_id,
            "seasonNumber": season_number
        }
        
        if title_name:
            params["titleName"] = title_name
        
        url = f"{TITLES_URL}/{title_id}"
        data = self._request_json(url, params)
        
        if not data or "title" not in data:
            debug(f"[AnimeCix] Failed to fetch season {season_number} for title_id={title_id}")
            return []
        
        title = data["title"]
        episodes = []
        
        # Try to get episodes from season data
        seasons = title.get("seasons", [])
        
        for season in seasons:
            if parse_season_number(season, 0) != season_number:
                continue
            
            # Check episodePagination
            episode_pagination = season.get("episodePagination", {})
            episode_list = episode_pagination.get("data", [])
            
            debug(f"[AnimeCix] Season {season_number}: found {len(episode_list)} episodes")
            
            for ep_data in episode_list:
                ep_id = ep_data.get("id")
                ep_number = ep_data.get("episode_number")
                ep_name = ep_data.get("name", f"Episode {ep_number}")
                
                if ep_id and ep_number is not None:
                    # Create composite ID: "id:season:episode" for faster stream lookup
                    composite_id = f"{ep_id}:{season_number}:{ep_number}"
                    
                    episodes.append(Episode(
                        id=composite_id,
                        number=ep_number,
                        title=ep_name,
                        season=season_number,
                        url=None
                    ))
        
        return episodes
    
    def get_episodes(self, anime_id: str) -> List[Episode]:
        """
        Get list of available episodes for an anime.
        
        This method fetches full details and extracts episodes.
        Consider using get_details() directly for better performance.
        
        Args:
            anime_id: Unique anime identifier.
        
        Returns:
            List of Episode objects.
        """
        debug(f"[AnimeCix] Getting episodes for anime_id={anime_id}")
        
        details = self.get_details(anime_id)
        if details:
            return details.episodes
        
        return []
    
    def get_streams(self, anime_id: str, episode_id: str) -> List[StreamLink]:
        """
        Get stream URLs for a specific episode.
        
        Uses /secure/episode-videos-points endpoint to get video sources.
        
        Note: This method expects episode_id to be in format "id:season:episode"
        or will attempt to fetch details if plain ID is provided (slower).
        
        Args:
            anime_id: Unique anime identifier.
            episode_id: Episode identifier from get_episodes().
        
        Returns:
            List of StreamLink objects with different quality options.
        """
        debug(f"[AnimeCix] get_streams START: anime_id={anime_id}, episode_id={episode_id}")
        
        try:
            title_id = int(anime_id)
        except (ValueError, TypeError):
            debug(f"[AnimeCix] Invalid anime_id: {anime_id}")
            return []
        
        debug(f"[AnimeCix] Parsed title_id={title_id}")
        
        # Check if this is a movie (special format: "movie:{id}")
        if str(episode_id).startswith("movie:"):
            debug(f"[AnimeCix] Movie detected, fetching video sources directly")
            return self._get_movie_streams(title_id)
        
        # Try to parse composite ID first (format: "id:season:episode")
        ep_number = None
        season_number = None
        
        debug(f"[AnimeCix] Checking for composite ID...")
        
        if ":" in str(episode_id):
            parts = str(episode_id).split(":")
            debug(f"[AnimeCix] Composite ID parts: {parts}")
            
            if len(parts) >= 3:
                try:
                    ep_id, season_number, ep_number = int(parts[0]), int(parts[1]), int(parts[2])
                    debug(f"[AnimeCix] Parsed composite: ep_id={ep_id}, season={season_number}, episode={ep_number}")
                    # SUCCESS: We have season and episode numbers, skip to video fetch
                except ValueError as e:
                    debug(f"[AnimeCix] Failed to parse composite ID: {e}")
        
        if ep_number is None or season_number is None:
            debug(f"[AnimeCix] No composite ID, fetching details (SLOW PATH)...")
            details = self.get_details(anime_id)
            
            if not details or not details.episodes:
                debug(f"[AnimeCix] No details/episodes found")
                return []
            
            debug(f"[AnimeCix] Got {len(details.episodes)} episodes, searching for {episode_id}...")
            
            target_episode = None
            for ep in details.episodes:
                # Try exact match first
                if ep.id == episode_id:
                    target_episode = ep
                    break
                if ":" in ep.id:
                    ep_parts = ep.id.split(":")
                    if len(ep_parts) >= 1 and ep_parts[0] == str(episode_id):
                        target_episode = ep
                        break
            
            if not target_episode:
                debug(f"[AnimeCix] Episode {episode_id} not found in {len(details.episodes)} episodes")
                return []
            
            ep_number = target_episode.number
            season_number = target_episode.season
            debug(f"[AnimeCix] Found episode: S{season_number}E{ep_number}")
        
        debug(f"[AnimeCix] Resolved to S{season_number}E{ep_number}, fetching videos...")
        
        params = {
            "titleId": title_id,
            "episode": ep_number,
            "season": season_number
        }
        
        debug(f"[AnimeCix] Calling episode-videos-points API with params: {params}")
        data = self._request_json(EPISODE_VIDEOS_URL, params)
        
        if not data:
            debug(f"[AnimeCix] No data returned for episode videos")
            return []
        
        # Extract video sources
        videos = data.get("videos", [])
        if not videos:
            debug(f"[AnimeCix] No videos found in response")
            return []
        
        debug(f"[AnimeCix] Found {len(videos)} video sources")
        
        streams = []
        sources_tried = 0
        max_sources = 10  
        
        for idx, video in enumerate(videos, 1):
            if sources_tried >= max_sources:
                debug(f"[AnimeCix] Reached max sources limit ({max_sources})")
                break
            
            video_url = video.get("url")
            
            if not video_url:
                debug(f"[AnimeCix] Video {idx}: no URL, skipping")
                continue
            
            sources_tried += 1
            debug(f"[AnimeCix] Video {idx}: extracting from {video_url}")
            
            # Extract embed info from URL
            try:
                embed_streams = self._extract_embed_streams(video_url)
                debug(f"[AnimeCix] Video {idx}: got {len(embed_streams)} streams")
                
                if embed_streams:
                    streams.extend(embed_streams)
                    # Stop after first successful source (usually has all qualities)
                    debug(f"[AnimeCix] Got {len(embed_streams)} streams from source {idx}, stopping")
                    break
                    
            except Exception as e:
                debug(f"[AnimeCix] Video {idx}: error - {e}")
                continue
        
        # Sort by quality (highest first)
        streams.sort(key=self._quality_sort_key)
        
        debug(f"[AnimeCix] get_streams COMPLETE: {len(streams)} streams total")
        return streams
    
    def _get_movie_streams(self, title_id: int) -> List[StreamLink]:
        """
        Get stream URLs for a movie.
        
        Movies have video sources directly in the title endpoint.
        
        Args:
            title_id: Movie title ID.
        
        Returns:
            List of StreamLink objects.
        """
        debug(f"[AnimeCix] Fetching movie streams for title_id={title_id}")
        
        url = f"{TITLES_URL}/{title_id}"
        data = self._request_json(url, params={"titleId": title_id})
        
        if not data or "title" not in data:
            debug(f"[AnimeCix] No data returned for movie")
            return []
        
        title = data["title"]
        videos = title.get("videos", [])
        
        if not videos:
            debug(f"[AnimeCix] No videos found for movie")
            return []
        
        debug(f"[AnimeCix] Found {len(videos)} video sources for movie")
        
        # For movies, try first working video source
        streams = []
        sources_tried = 0
        max_sources = 10
        
        for idx, video in enumerate(videos, 1):
            if sources_tried >= max_sources:
                debug(f"[AnimeCix] Reached max sources limit ({max_sources})")
                break
            
            video_url = video.get("url")
            
            if not video_url:
                debug(f"[AnimeCix] Video {idx}: no URL, skipping")
                continue
            
            sources_tried += 1
            debug(f"[AnimeCix] Video {idx}: extracting from {video_url}")
            
            try:
                embed_streams = self._extract_embed_streams(video_url)
                debug(f"[AnimeCix] Video {idx}: got {len(embed_streams)} streams")
                
                if embed_streams:
                    streams.extend(embed_streams)
                    # Stop after first successful source
                    debug(f"[AnimeCix] Got {len(embed_streams)} streams from source {idx}, stopping")
                    break
                    
            except Exception as e:
                debug(f"[AnimeCix] Video {idx}: error - {e}")
                continue
        
        # Sort by quality
        streams.sort(key=self._quality_sort_key)
        
        debug(f"[AnimeCix] Movie streams complete: {len(streams)} streams total")
        return streams
    
    def _extract_embed_streams(self, embed_url: str) -> List[StreamLink]:
        """
        Extract stream URLs from embed page.
        
        Directly extracts embed ID from URL and calls video API.
        No redirect following or vid parameter needed.
        
        Args:
            embed_url: Embed page URL (e.g., https://tau-video.xyz/embed/{id}).
        
        Returns:
            List of StreamLink objects.
        """
        # Parse embed URL to extract embed ID
        parsed = urlparse(embed_url)
        path_parts = parsed.path.strip("/").split("/")
        
        # Extract embed ID from path
        embed_id = None
        if len(path_parts) >= 2 and path_parts[0] == "embed":
            embed_id = path_parts[1]
        elif len(path_parts) == 1:
            embed_id = path_parts[0]
        
        if not embed_id:
            debug(f"[AnimeCix] Could not extract embed_id from: {embed_url}")
            return []
        
        debug(f"[AnimeCix] Extracted embed_id: {embed_id}")
        
        api_url = f"https://{VIDEO_PLAYERS[0]}/api/video/{embed_id}"
        debug(f"[AnimeCix] Fetching video API: {api_url}")
        
        video_data = self._request_json(api_url)
        
        if not video_data:
            debug(f"[AnimeCix] No response from video API")
            return []
        
        if "urls" not in video_data:
            debug(f"[AnimeCix] No 'urls' key in video API response")
            return []
        
        # Extract streams
        streams = []
        for url_info in video_data["urls"]:
            stream_url = url_info.get("url")
            quality = url_info.get("label", "auto")
            
            if stream_url:
                streams.append(StreamLink(
                    url=stream_url,
                    quality=quality,
                    server="tau-video",
                    headers={"Referer": embed_url}
                ))
        
        debug(f"[AnimeCix] Extracted {len(streams)} streams from embed")
        return streams
    
    def _quality_sort_key(self, stream: StreamLink) -> int:
        """
        Sort key for stream quality (highest first).
        
        Args:
            stream: StreamLink object.
        
        Returns:
            Integer sort key (negative for descending order).
        """
        quality = stream.quality.lower().replace('p', '').strip()
        
        # Special cases
        if quality == "4k" or "2160" in quality:
            return -2160
        if quality == "auto":
            return 1  # Auto quality goes to end
        
        # Try to parse resolution
        try:
            return -int(quality)
        except ValueError:
            return 0
    
    def _parse_type(self, title_type: str) -> str:
        """
        Parse anime type from title_type string.
        
        Args:
            title_type: Type string from API.
        
        Returns:
            Normalized type: "movie", "ova", or "series".
        """
        title_type = (title_type or "").lower()
        
        if "movie" in title_type or "film" in title_type:
            return "movie"
        if "ova" in title_type:
            return "ova"
        if "special" in title_type:
            return "special"
        
        return "series"
