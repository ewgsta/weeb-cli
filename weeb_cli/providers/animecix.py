import json
import time
import urllib.request
from urllib.parse import urlparse, parse_qs, quote, urlsplit, urlunsplit
from typing import List, Optional

from weeb_cli.providers.base import (
    BaseProvider,
    AnimeResult,
    AnimeDetails,
    Episode,
    StreamLink
)
from weeb_cli.providers.registry import register_provider

BASE_URL = "https://animecix.tv/"
ALT_URL = "https://mangacix.net/"
VIDEO_PLAYERS = ["tau-video.xyz", "sibnet"]

HEADERS = {
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}


def _http_get(url: str, timeout: int = 15) -> bytes:
    sp = urlsplit(url)
    safe_path = quote(sp.path, safe="/:%@")
    safe_url = urlunsplit((sp.scheme, sp.netloc, safe_path, sp.query, sp.fragment))
    
    req = urllib.request.Request(safe_url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def _get_json(url: str, timeout: int = 15):
    try:
        data = _http_get(url, timeout)
        return json.loads(data)
    except Exception:
        return None


@register_provider("animecix", lang="tr", region="TR")
class AnimeCixProvider(BaseProvider):
    
    def __init__(self):
        super().__init__()
        
    def search(self, query: str) -> List[AnimeResult]:
        q = (query or "").strip().replace(" ", "-")
        q_enc = quote(q, safe="-")
        url = f"{BASE_URL}secure/search/{q_enc}?type=&limit=20"
        
        data = _get_json(url)
        if not data or "results" not in data:
            return []
        
        results = []
        for item in data["results"]:
            name = item.get("name")
            _id = item.get("id")
            if name and _id:
                results.append(AnimeResult(
                    id=str(_id),
                    title=str(name),
                    type=self._parse_type(item.get("title_type", ""))
                ))
        
        return results
    
    def get_details(self, anime_id: str) -> Optional[AnimeDetails]:
        try:
            safe_id = int(anime_id)
        except (ValueError, TypeError):
            return None
        
        url = f"{ALT_URL}secure/related-videos?episode=1&season=1&titleId={safe_id}&videoId=637113"
        data = _get_json(url)
        
        title_data = None
        if data and "videos" in data:
            videos = data.get("videos") or []
            if videos:
                title_data = videos[0].get("title")
        
        episodes = self.get_episodes(anime_id)
        
        if not episodes:
            movie_url = self._get_movie_url(safe_id)
            if movie_url:
                title_name = title_data.get("name", "Film") if title_data else "Film"
                episodes = [Episode(
                    id=movie_url,
                    number=1,
                    title=title_name,
                    url=movie_url
                )]
        
        if not title_data:
            return AnimeDetails(
                id=anime_id,
                title=anime_id,
                episodes=episodes,
                total_episodes=len(episodes)
            )
        
        return AnimeDetails(
            id=anime_id,
            title=title_data.get("name", ""),
            description=title_data.get("description"),
            cover=title_data.get("poster"),
            genres=[g.get("name", "") for g in title_data.get("genres", [])],
            year=title_data.get("year"),
            episodes=episodes,
            total_episodes=len(episodes)
        )
    
    def _get_movie_url(self, title_id: int) -> Optional[str]:
        url = f"{ALT_URL}secure/titles/{title_id}"
        data = _get_json(url)
        
        if not data or "title" not in data:
            return None
        
        title = data["title"]
        videos = title.get("videos") or []
        
        if videos:
            return videos[0].get("url")
        
        return None
    
    def get_episodes(self, anime_id: str) -> List[Episode]:
        try:
            safe_id = int(anime_id)
        except (ValueError, TypeError):
            return []
        
        seasons = self._get_seasons(safe_id)
        if not seasons:
            seasons = [0]
        
        episodes = []
        seen = set()
        
        for sidx in seasons:
            url = f"{ALT_URL}secure/related-videos?episode=1&season={sidx+1}&titleId={safe_id}&videoId=637113"
            data = _get_json(url)
            
            if not data or "videos" not in data:
                continue
            
            for v in data["videos"]:
                name = v.get("name")
                ep_url = v.get("url")
                
                if not name or not ep_url:
                    continue
                if name in seen:
                    continue
                
                seen.add(name)
                ep_num = self._parse_episode_number(name, len(episodes) + 1)
                
                episodes.append(Episode(
                    id=ep_url,
                    number=ep_num,
                    title=name,
                    season=sidx + 1,
                    url=ep_url
                ))
        
        return episodes
    
    def get_streams(self, anime_id: str, episode_id: str) -> List[StreamLink]:
        embed_path = episode_id.lstrip("/")
        
        if embed_path.startswith("http"):
            full_url = embed_path
        else:
            full_url = f"{BASE_URL}{quote(embed_path, safe='/:?=&')}"
        
        try:
            req = urllib.request.Request(full_url, headers=HEADERS)
            resp = urllib.request.urlopen(req, timeout=15)
            final_url = resp.geturl()
            
            time.sleep(1)
            
            p = urlparse(final_url)
            parts = p.path.strip("/").split("/")
            
            embed_id = None
            if len(parts) >= 2:
                if parts[0] == "embed":
                    embed_id = parts[1]
                else:
                    embed_id = parts[0]
            elif len(parts) == 1 and parts[0]:
                embed_id = parts[0]
            
            qs = parse_qs(p.query)
            vid = (qs.get("vid") or [None])[0]
            
            if not embed_id or not vid:
                return []
            
            api_url = f"https://{VIDEO_PLAYERS[0]}/api/video/{embed_id}?vid={vid}"
            video_data = _get_json(api_url)
            
            if not video_data or "urls" not in video_data:
                return []
            
            streams = []
            for u in video_data["urls"]:
                label = u.get("label")
                url = u.get("url")
                if url:
                    streams.append(StreamLink(
                        url=url,
                        quality=label or "auto",
                        server="tau-video"
                    ))
            
            return streams
            
        except Exception:
            return []
    
    def _get_seasons(self, title_id: int) -> List[int]:
        try:
            safe_id = int(title_id)
        except (ValueError, TypeError):
            return [0]
        
        url = f"{ALT_URL}secure/related-videos?episode=1&season=1&titleId={safe_id}&videoId=637113"
        data = _get_json(url)
        
        if not data or "videos" not in data:
            return [0]
        
        videos = data.get("videos") or []
        if not videos:
            return [0]
        
        title = (videos[0] or {}).get("title") or {}
        seasons = title.get("seasons") or []
        
        if seasons:
            return list(range(len(seasons)))
        return [0]
    
    def _parse_type(self, title_type: str) -> str:
        title_type = (title_type or "").lower()
        if "movie" in title_type or "film" in title_type:
            return "movie"
        if "ova" in title_type:
            return "ova"
        return "series"
    
    def _parse_episode_number(self, name: str, fallback: int) -> int:
        import re
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
