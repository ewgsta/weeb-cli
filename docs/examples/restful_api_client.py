#!/usr/bin/env python3
"""Example RESTful API client for weeb-cli.

This script demonstrates how to interact with the weeb-cli RESTful API server.
"""
import requests
from typing import List, Dict, Optional


class WeebCLIClient:
    """Client for weeb-cli RESTful API."""
    
    def __init__(self, base_url: str = "http://localhost:8080"):
        """Initialize client with base URL.
        
        Args:
            base_url: Base URL of the weeb-cli RESTful API server
        """
        self.base_url = base_url.rstrip("/")
        self.session = requests.Session()
    
    def health_check(self) -> Dict:
        """Check if the server is running.
        
        Returns:
            Health status dictionary
        """
        response = self.session.get(f"{self.base_url}/health")
        response.raise_for_status()
        return response.json()
    
    def list_providers(self) -> Dict:
        """List all available providers.
        
        Returns:
            Dictionary with providers list
        """
        response = self.session.get(f"{self.base_url}/api/providers")
        response.raise_for_status()
        return response.json()
    
    def search(self, query: str, provider: Optional[str] = None) -> List[Dict]:
        """Search for anime.
        
        Args:
            query: Search query
            provider: Provider name (optional)
        
        Returns:
            List of anime results
        """
        params = {"q": query}
        if provider:
            params["provider"] = provider
        
        response = self.session.get(f"{self.base_url}/api/search", params=params)
        response.raise_for_status()
        data = response.json()
        return data.get("results", [])
    
    def get_anime_details(self, anime_id: str, provider: Optional[str] = None) -> Dict:
        """Get anime details.
        
        Args:
            anime_id: Anime ID
            provider: Provider name (optional)
        
        Returns:
            Anime details dictionary
        """
        params = {}
        if provider:
            params["provider"] = provider
        
        response = self.session.get(
            f"{self.base_url}/api/anime/{anime_id}",
            params=params
        )
        response.raise_for_status()
        data = response.json()
        return data.get("anime", {})
    
    def get_episodes(
        self,
        anime_id: str,
        season: Optional[int] = None,
        provider: Optional[str] = None
    ) -> List[Dict]:
        """Get anime episodes.
        
        Args:
            anime_id: Anime ID
            season: Season number (optional)
            provider: Provider name (optional)
        
        Returns:
            List of episodes
        """
        params = {}
        if season:
            params["season"] = season
        if provider:
            params["provider"] = provider
        
        response = self.session.get(
            f"{self.base_url}/api/anime/{anime_id}/episodes",
            params=params
        )
        response.raise_for_status()
        data = response.json()
        return data.get("episodes", [])
    
    def get_streams(
        self,
        anime_id: str,
        episode_id: str,
        provider: Optional[str] = None,
        sort: str = "desc"
    ) -> List[Dict]:
        """Get episode streams.
        
        Args:
            anime_id: Anime ID
            episode_id: Episode ID
            provider: Provider name (optional)
            sort: Sort order ('asc' or 'desc')
        
        Returns:
            List of streams
        """
        params = {"sort": sort}
        if provider:
            params["provider"] = provider
        
        response = self.session.get(
            f"{self.base_url}/api/anime/{anime_id}/episodes/{episode_id}/streams",
            params=params
        )
        response.raise_for_status()
        data = response.json()
        return data.get("streams", [])


def main():
    """Example usage of the WeebCLIClient."""
    # Initialize client
    client = WeebCLIClient("http://localhost:8080")
    
    # Health check
    print("=== Health Check ===")
    health = client.health_check()
    print(f"Status: {health['status']}")
    print(f"Providers: {', '.join(health['providers'])}")
    print()
    
    # List providers
    print("=== Available Providers ===")
    providers_data = client.list_providers()
    for provider in providers_data["providers"]:
        print(f"- {provider['name']} ({provider['lang']}/{provider['region']})")
    print()
    
    # Search anime
    print("=== Search Results ===")
    query = "naruto"
    results = client.search(query, provider="animecix")
    print(f"Found {len(results)} results for '{query}':")
    for i, anime in enumerate(results[:5], 1):
        print(f"{i}. {anime['title']} ({anime['year']}) - ID: {anime['id']}")
    print()
    
    if not results:
        print("No results found. Exiting.")
        return
    
    # Get anime details
    print("=== Anime Details ===")
    anime_id = results[0]["id"]
    details = client.get_anime_details(anime_id, provider="animecix")
    print(f"Title: {details['title']}")
    print(f"Type: {details['type']}")
    print(f"Year: {details['year']}")
    print(f"Status: {details.get('status', 'N/A')}")
    if details.get('genres'):
        print(f"Genres: {', '.join(details['genres'])}")
    print()
    
    # Get episodes
    print("=== Episodes (Season 1) ===")
    episodes = client.get_episodes(anime_id, season=1, provider="animecix")
    print(f"Found {len(episodes)} episodes:")
    for ep in episodes[:5]:
        title = ep.get('title') or f"Episode {ep['number']}"
        print(f"- S{ep['season']:02d}E{ep['number']:02d}: {title}")
    print()
    
    if not episodes:
        print("No episodes found. Exiting.")
        return
    
    # Get streams for first episode
    print("=== Streams (First Episode) ===")
    episode_id = episodes[0]["id"]
    streams = client.get_streams(anime_id, episode_id, provider="animecix")
    print(f"Found {len(streams)} streams:")
    for stream in streams:
        print(f"- Quality: {stream['quality']}")
        print(f"  Server: {stream['server']}")
        print(f"  URL: {stream['url'][:60]}...")
        if stream.get('subtitles'):
            print(f"  Subtitles: {stream['subtitles']}")
    print()


if __name__ == "__main__":
    try:
        main()
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to weeb-cli RESTful API server.")
        print("Make sure the server is running: weeb-cli serve restful")
    except requests.exceptions.HTTPError as e:
        print(f"HTTP Error: {e}")
    except KeyboardInterrupt:
        print("\nInterrupted by user.")
