import json
import re
import urllib.request
from urllib.parse import quote
from typing import List, Optional
from bs4 import BeautifulSoup

from weeb_cli.providers.base import (
    BaseProvider,
    AnimeResult,
    AnimeDetails,
    Episode,
    StreamLink
)
from weeb_cli.providers.registry import register_provider
from weeb_cli.providers.extractors.megacloud import extract_stream

BASE_URL = "https://hianime.to"
AJAX_URL = f"{BASE_URL}/ajax/v2"

HEADERS = {
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:122.0) Gecko/20100101 Firefox/122.0",
    "Referer": BASE_URL
}


def _http_get(url: str, headers: dict = None, timeout: int = 15) -> bytes:
    req = urllib.request.Request(url, headers=headers or HEADERS)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def _get_json(url: str, headers: dict = None) -> Optional[dict]:
    try:
        data = _http_get(url, headers)
        return json.loads(data)
    except Exception:
        return None


def _get_html(url: str, headers: dict = None) -> str:
    try:
        data = _http_get(url, headers)
        return data.decode('utf-8')
    except Exception:
        return ""


@register_provider("hianime", lang="en", region="US", disabled=True)
class HiAnimeProvider(BaseProvider):
    
    def __init__(self):
        super().__init__()
        self.headers = HEADERS.copy()
        
    def search(self, query: str) -> List[AnimeResult]:
        q = (query or "").strip()
        if not q:
            return []
        
        url = f"{BASE_URL}/search?keyword={quote(q)}"
        html = _get_html(url, self.headers)
        
        if not html:
            return []
        
        soup = BeautifulSoup(html, 'html.parser')
        results = []
        
        for item in soup.select('.flw-item'):
            try:
                title_el = item.select_one('.film-name .dynamic-name')
                if not title_el:
                    continue
                
                title = title_el.get_text(strip=True)
                alt_title = title_el.get('data-jname', '')
                href = title_el.get('href', '')
                anime_id = href.split('/')[-1].split('?')[0] if href else None
                
                if not anime_id or not title:
                    continue
                
                poster = item.select_one('.film-poster-img')
                cover = poster.get('data-src') if poster else None
                
                sub_el = item.select_one('.tick-sub')
                dub_el = item.select_one('.tick-dub')
                eps_el = item.select_one('.tick-eps')
                
                sub_count = sub_el.get_text(strip=True) if sub_el else "0"
                dub_count = dub_el.get_text(strip=True) if dub_el else "0"
                
                type_el = item.select_one('.fdi-item')
                anime_type = type_el.get_text(strip=True).lower() if type_el else "tv"
                
                duration_el = item.select_one('.fdi-duration')
                duration = duration_el.get_text(strip=True) if duration_el else ""
                
                results.append(AnimeResult(
                    id=anime_id,
                    title=title,
                    type=self._parse_type(anime_type),
                    cover=cover
                ))
            except Exception:
                continue
        
        return results
    
    def get_details(self, anime_id: str) -> Optional[AnimeDetails]:
        url = f"{BASE_URL}/{anime_id}"
        html = _get_html(url, self.headers)
        
        if not html:
            return None
        
        soup = BeautifulSoup(html, 'html.parser')
        
        title_el = soup.select_one('.anisc-detail .film-name')
        title = title_el.get_text(strip=True) if title_el else anime_id
        
        alt_title_el = soup.select_one('.film-name[data-jname]')
        alt_title = alt_title_el.get('data-jname') if alt_title_el else None
        
        desc_el = soup.select_one('.film-description .text')
        description = desc_el.get_text(strip=True) if desc_el else None
        
        poster_el = soup.select_one('.film-poster-img')
        cover = poster_el.get('src') if poster_el else None
        
        genres = []
        for genre_el in soup.select('.item-list a[href*="/genre/"]'):
            genres.append(genre_el.get_text(strip=True))
        
        episodes = self.get_episodes(anime_id)
        
        return AnimeDetails(
            id=anime_id,
            title=title,
            description=description,
            cover=cover,
            genres=genres,
            episodes=episodes,
            total_episodes=len(episodes)
        )
    
    def get_episodes(self, anime_id: str) -> List[Episode]:
        match = re.search(r'-(\d+)$', anime_id)
        if not match:
            return []
        
        show_id = match.group(1)
        url = f"{AJAX_URL}/episode/list/{show_id}"
        
        data = _get_json(url, self.headers)
        if not data or 'html' not in data:
            return []
        
        soup = BeautifulSoup(data['html'], 'html.parser')
        episodes = []
        
        for i, item in enumerate(soup.select('.ssl-item.ep-item')):
            try:
                href = item.get('href', '')
                ep_id = href.replace('/watch/', '').replace('?', '::') if href else None
                
                if not ep_id:
                    continue
                
                title = item.get('title', '')
                alt_title = item.select_one('.ep-name.e-dynamic-name')
                alt_title = alt_title.get('data-jname') if alt_title else None
                
                is_filler = 'ssl-item-filler' in item.get('class', [])
                ep_num = i + 1
                
                episodes.append(Episode(
                    id=ep_id,
                    number=ep_num,
                    title=title
                ))
            except Exception:
                continue
        
        return episodes
    
    def get_streams(self, anime_id: str, episode_id: str) -> List[StreamLink]:
        ep_num = episode_id.split('ep=')[-1] if 'ep=' in episode_id else episode_id.split('::')[-1]
        
        servers_url = f"{AJAX_URL}/episode/servers?episodeId={ep_num}"
        servers_data = _get_json(servers_url, self.headers)
        
        if not servers_data or 'html' not in servers_data:
            return []
        
        soup = BeautifulSoup(servers_data['html'], 'html.parser')
        
        servers = {"sub": [], "dub": []}
        
        for server_item in soup.select('.servers-sub .server-item'):
            try:
                server_id = server_item.get('data-id')
                server_index = server_item.get('data-server-id')
                server_name = server_item.select_one('a')
                server_name = server_name.get_text(strip=True).lower() if server_name else 'unknown'
                
                if server_id:
                    servers["sub"].append({
                        "id": int(server_id),
                        "index": int(server_index) if server_index else None,
                        "name": server_name,
                        "type": "sub"
                    })
            except Exception:
                continue
        
        for server_item in soup.select('.servers-dub .server-item'):
            try:
                server_id = server_item.get('data-id')
                server_index = server_item.get('data-server-id')
                server_name = server_item.select_one('a')
                server_name = server_name.get_text(strip=True).lower() if server_name else 'unknown'
                
                if server_id:
                    servers["dub"].append({
                        "id": int(server_id),
                        "index": int(server_index) if server_index else None,
                        "name": server_name,
                        "type": "dub"
                    })
            except Exception:
                continue
        
        streams = []
        
        for server_type in ["sub", "dub"]:
            for server in servers[server_type]:
                try:
                    stream_data = extract_stream(
                        server_id=server["id"],
                        episode_id=episode_id,
                        server_type=server_type,
                        server_name=server["name"]
                    )
                    
                    if stream_data and stream_data.get("file"):
                        streams.append(StreamLink(
                            url=stream_data["file"],
                            quality="auto",
                            server=f"{server['name']}-{server_type}",
                            headers={"Referer": "https://megacloud.tv"},
                            subtitles=self._get_subtitle_url(stream_data.get("tracks", []))
                        ))
                except Exception:
                    continue
        
        if not streams:
            for server_type in ["sub", "dub"]:
                for server in servers[server_type]:
                    streams.append(StreamLink(
                        url=f"embedded:{server['id']}:{episode_id}:{server_type}:{server['name']}",
                        quality="auto",
                        server=f"{server['name']}-{server_type} (embedded)",
                        headers={"Referer": BASE_URL}
                    ))
        
        return streams
    
    def _get_subtitle_url(self, tracks: List[dict]) -> Optional[str]:
        for track in tracks:
            if track.get('kind') in ['captions', 'subtitles']:
                label = track.get('label', '').lower()
                if 'english' in label:
                    return track.get('file')
        
        for track in tracks:
            if track.get('kind') in ['captions', 'subtitles']:
                return track.get('file')
        
        return None
    
    def _parse_type(self, type_str: str) -> str:
        type_str = (type_str or "").lower()
        if "movie" in type_str:
            return "movie"
        if "ova" in type_str:
            return "ova"
        if "ona" in type_str:
            return "ona"
        if "special" in type_str:
            return "special"
        return "series"
