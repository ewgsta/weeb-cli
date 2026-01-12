"""
AnimeCix Provider - Türkçe anime kaynağı

Website: https://animecix.tv/
API: JSON tabanlı, Cloudflare korumasız
"""

import time
import requests
from urllib.parse import urlparse, parse_qs
from typing import List, Optional

from weeb_cli.providers.base import (
    BaseProvider, 
    AnimeResult, 
    AnimeDetails, 
    Episode, 
    StreamLink
)
from weeb_cli.providers.registry import register_provider


@register_provider("animecix", lang="tr", region="TR")
class AnimeCixProvider(BaseProvider):
    """AnimeCix scraper implementation"""
    
    def __init__(self):
        super().__init__()
        self.base_url = "https://animecix.tv"
        self.api_url = "https://mangacix.net"
        self.video_host = "tau-video.xyz"
        
    def search(self, query: str) -> List[AnimeResult]:
        """Anime ara"""
        url = f"{self.base_url}/secure/search/{query}"
        params = {"type": "", "limit": "20"}
        
        data = self._request(url, params)
        if not data or "results" not in data:
            return []
        
        results = []
        for item in data["results"]:
            results.append(AnimeResult(
                id=str(item.get("id", "")),
                title=item.get("name", ""),
                type=self._parse_type(item.get("title_type", "")),
                cover=item.get("poster"),
                year=item.get("year")
            ))
        
        return results
    
    def get_details(self, anime_id: str) -> Optional[AnimeDetails]:
        """Anime detaylarını getir"""
        url = f"{self.api_url}/secure/titles/{anime_id}"
        data = self._request(url)
        
        if not data or "title" not in data:
            return None
        
        title_data = data["title"]
        episodes = self.get_episodes(anime_id)
        
        return AnimeDetails(
            id=anime_id,
            title=title_data.get("name", ""),
            description=title_data.get("description"),
            cover=title_data.get("poster"),
            genres=[g.get("name", "") for g in title_data.get("genres", [])],
            year=title_data.get("year"),
            status=self._parse_status(title_data.get("status")),
            episodes=episodes,
            total_episodes=len(episodes)
        )
    
    def get_episodes(self, anime_id: str) -> List[Episode]:
        """Bölüm listesini getir"""
        seasons = self._get_seasons(anime_id)
        episodes = []
        seen = set()
        
        for season_idx in seasons:
            season_eps = self._get_season_episodes(anime_id, season_idx + 1)
            
            for ep in season_eps:
                ep_name = ep.get("name", "")
                if ep_name not in seen:
                    seen.add(ep_name)
                    
                    # Episode number'ı parse et
                    ep_num = self._parse_episode_number(ep_name, len(episodes) + 1)
                    
                    episodes.append(Episode(
                        id=ep.get("url", ""),
                        number=ep_num,
                        title=ep_name,
                        season=season_idx + 1,
                        url=ep.get("url")
                    ))
        
        return episodes
    
    def get_streams(self, anime_id: str, episode_id: str) -> List[StreamLink]:
        """Stream linklerini getir"""
        # episode_id aslında URL path
        stream_url = f"{self.base_url}{episode_id}"
        
        try:
            response = requests.get(
                stream_url, 
                headers=self.headers, 
                allow_redirects=True,
                timeout=15
            )
            response.raise_for_status()
            
            # Redirect sonrası URL'den embed bilgilerini çıkar
            time.sleep(2)  # Rate limit için bekle
            
            final_url = response.url
            parsed = urlparse(final_url)
            
            # /embed/{embed_id}?vid={vid} formatı
            path_parts = parsed.path.split('/')
            if len(path_parts) < 3:
                return []
                
            embed_id = path_parts[2]
            query_params = parse_qs(parsed.query)
            vid = query_params.get('vid', [None])[0]
            
            if not embed_id or not vid:
                return []
            
            # Video API'den stream URL'lerini al
            api_url = f"https://{self.video_host}/api/video/{embed_id}"
            video_data = self._request(api_url, {"vid": vid})
            
            if not video_data or "urls" not in video_data:
                return []
            
            streams = []
            for item in video_data["urls"]:
                url = item.get("url")
                if url:
                    streams.append(StreamLink(
                        url=url,
                        quality=item.get("label", "auto"),
                        server="tau-video"
                    ))
            
            return streams
            
        except requests.RequestException:
            return []
    
    def get_subtitles(self, anime_id: str, season: int, episode_idx: int) -> Optional[str]:
        """Altyazı URL'si getir"""
        url = f"{self.api_url}/secure/related-videos"
        params = {
            "episode": "1",
            "season": str(season),
            "titleId": anime_id,
            "videoId": "637113"
        }
        
        data = self._request(url, params)
        if not data or "videos" not in data:
            return None
        
        videos = data["videos"]
        if episode_idx >= len(videos):
            return None
        
        captions = videos[episode_idx].get("captions", [])
        
        # Türkçe altyazı tercih et
        for cap in captions:
            if cap.get("language") == "tr":
                return cap.get("url")
        
        # Yoksa ilk altyazıyı döndür
        return captions[0].get("url") if captions else None
    
    # Private helper methods
    
    def _get_seasons(self, anime_id: str) -> List[int]:
        """Sezon listesini getir"""
        url = f"{self.api_url}/secure/related-videos"
        params = {
            "episode": "1",
            "season": "1", 
            "titleId": anime_id,
            "videoId": "637113"
        }
        
        data = self._request(url, params)
        if not data or "videos" not in data:
            return [0]
        
        videos = data["videos"]
        if not videos:
            return [0]
        
        seasons = videos[0].get("title", {}).get("seasons", [])
        if isinstance(seasons, list) and seasons:
            return list(range(len(seasons)))
        
        return [0]
    
    def _get_season_episodes(self, anime_id: str, season: int) -> List[dict]:
        """Belirli sezonun bölümlerini getir"""
        url = f"{self.api_url}/secure/related-videos"
        params = {
            "episode": "1",
            "season": str(season),
            "titleId": anime_id,
            "videoId": "637113"
        }
        
        data = self._request(url, params)
        if not data or "videos" not in data:
            return []
        
        return data["videos"]
    
    def _parse_type(self, title_type: str) -> str:
        """Anime tipini normalize et"""
        title_type = (title_type or "").lower()
        if "movie" in title_type or "film" in title_type:
            return "movie"
        if "ova" in title_type:
            return "ova"
        if "special" in title_type:
            return "special"
        return "series"
    
    def _parse_status(self, status: str) -> str:
        """Durumu normalize et"""
        status = (status or "").lower()
        if "ongoing" in status or "devam" in status:
            return "ongoing"
        return "completed"
    
    def _parse_episode_number(self, name: str, fallback: int) -> int:
        """Bölüm adından numara çıkar"""
        import re
        
        # "Bölüm 5", "Episode 5", "5. Bölüm" gibi formatları yakala
        patterns = [
            r'(?:bölüm|episode|ep)\s*(\d+)',
            r'(\d+)\.\s*(?:bölüm|episode)',
            r'^(\d+)$'
        ]
        
        name_lower = name.lower()
        for pattern in patterns:
            match = re.search(pattern, name_lower)
            if match:
                return int(match.group(1))
        
        return fallback
