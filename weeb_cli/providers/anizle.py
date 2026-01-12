import re
import json
from typing import List, Optional, Dict, Any
from difflib import SequenceMatcher
from concurrent.futures import ThreadPoolExecutor, as_completed

from weeb_cli.providers.base import (
    BaseProvider,
    AnimeResult,
    AnimeDetails,
    Episode,
    StreamLink
)
from weeb_cli.providers.registry import register_provider

try:
    from curl_cffi import requests as curl_requests
    HAS_CURL_CFFI = True
except ImportError:
    import requests as std_requests
    HAS_CURL_CFFI = False

BASE_URL = "https://anizm.pro"
API_BASE_URL = "https://anizle.org"
ANIME_LIST_URL = f"{BASE_URL}/getAnimeListForSearch"
PLAYER_BASE_URL = "https://anizmplayer.com"

_anime_database: List[Dict[str, Any]] = []
_database_loaded: bool = False
_session = None

DEFAULT_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
}


def _get_session():
    global _session
    if _session is None:
        if HAS_CURL_CFFI:
            _session = curl_requests.Session(impersonate="chrome110")
        else:
            _session = std_requests.Session()
    return _session


def _http_get(url: str, headers: Dict = None, timeout: int = 60):
    session = _get_session()
    h = {**DEFAULT_HEADERS}
    if headers:
        h.update(headers)
    
    try:
        return session.get(url, headers=h, timeout=timeout)
    except Exception:
        return None


def _http_post(url: str, headers: Dict = None, data: Dict = None, timeout: int = 60):
    session = _get_session()
    h = {**DEFAULT_HEADERS, "X-Requested-With": "XMLHttpRequest", "Accept": "application/json"}
    if headers:
        h.update(headers)
    
    try:
        return session.post(url, headers=h, data=data, timeout=timeout)
    except Exception:
        return None


def _strip_html(text: str) -> str:
    if not text:
        return ""
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'&[a-zA-Z]+;', ' ', text)
    text = re.sub(r'&#\d+;', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def _load_database() -> List[Dict[str, Any]]:
    global _anime_database, _database_loaded
    
    if _database_loaded:
        return _anime_database
    
    try:
        response = _http_get(ANIME_LIST_URL, timeout=120)
        if response and response.status_code == 200:
            data = response.json()
            if isinstance(data, list):
                _anime_database = data
                _database_loaded = True
    except Exception:
        pass
    
    return _anime_database


def _unpack_js(p: str, a: int, c: int, k: List[str]) -> str:
    def e(c: int, a: int) -> str:
        first = '' if c < a else e(c // a, a)
        c = c % a
        if c > 35:
            second = chr(c + 29)
        elif c > 9:
            second = chr(c + 87)
        else:
            second = str(c)
        return first + second
    
    d = {}
    temp_c = c
    while temp_c:
        temp_c -= 1
        key = e(temp_c, a)
        d[key] = k[temp_c] if temp_c < len(k) and k[temp_c] else key
    
    def replace_func(match):
        return d.get(match.group(0), match.group(0))
    
    return re.sub(r'\b\w+\b', replace_func, p)


def _extract_fireplayer_id(player_html: str) -> Optional[str]:
    eval_match = re.search(
        r"eval\(function\(p,a,c,k,e,d\)\{.*?\}return p\}\('(.*?)',(\d+),(\d+),'([^']+)'\.split\('\|'\),0,\{\}\)\)",
        player_html, re.S
    )
    
    if eval_match:
        p = eval_match.group(1)
        a = int(eval_match.group(2))
        c = int(eval_match.group(3))
        k = eval_match.group(4).split('|')
        
        try:
            decoded = _unpack_js(p, a, c, k)
            id_match = re.search(r'FirePlayer\s*\(\s*["\']([a-f0-9]{32})["\']', decoded)
            if id_match:
                return id_match.group(1)
        except Exception:
            pass
    
    fp_direct = re.search(r'FirePlayer\s*\(["\']([a-f0-9]{32})["\']', player_html)
    if fp_direct:
        return fp_direct.group(1)
    
    return None


@register_provider("anizle", lang="tr", region="TR")
class AnizleProvider(BaseProvider):
    
    def __init__(self):
        super().__init__()
    
    def search(self, query: str) -> List[AnimeResult]:
        database = _load_database()
        if not database:
            return []
        
        results = []
        for anime in database:
            scores = [
                self._similarity(query, anime.get("info_title", "")),
                self._similarity(query, anime.get("info_titleoriginal", "")),
                self._similarity(query, anime.get("info_titleenglish", "")),
            ]
            max_score = max(scores)
            
            if max_score > 0.3:
                year_str = anime.get("info_year", "")
                year = int(year_str) if year_str and str(year_str).isdigit() else None
                
                results.append((max_score, AnimeResult(
                    id=anime.get("info_slug", ""),
                    title=anime.get("info_title", ""),
                    cover=self._get_poster_url(anime.get("info_poster", "")),
                    year=year
                )))
        
        results.sort(key=lambda x: x[0], reverse=True)
        return [r[1] for r in results[:20]]
    
    def get_details(self, anime_id: str) -> Optional[AnimeDetails]:
        database = _load_database()
        anime_data = None
        
        for anime in database:
            if anime.get("info_slug") == anime_id:
                anime_data = anime
                break
        
        episodes = self.get_episodes(anime_id)
        
        if not anime_data:
            return AnimeDetails(
                id=anime_id,
                title=anime_id.replace("-", " ").title(),
                episodes=episodes,
                total_episodes=len(episodes)
            )
        
        categories = []
        for cat in anime_data.get("categories", []):
            if isinstance(cat, dict) and "tag_title" in cat:
                categories.append(cat["tag_title"])
        
        year_str = anime_data.get("info_year", "")
        year = int(year_str) if year_str and str(year_str).isdigit() else None
        
        description = _strip_html(anime_data.get("info_summary", ""))
        
        return AnimeDetails(
            id=anime_id,
            title=anime_data.get("info_title", ""),
            description=description,
            cover=self._get_poster_url(anime_data.get("info_poster", "")),
            genres=categories,
            year=year,
            episodes=episodes,
            total_episodes=len(episodes)
        )
    
    def get_episodes(self, anime_id: str) -> List[Episode]:
        url = f"{BASE_URL}/{anime_id}"
        response = _http_get(url)
        
        if not response or response.status_code != 200:
            return []
        
        html = response.text
        episodes = []
        seen = set()
        
        pattern1 = r'href="/?([^"]+?-bolum[^"]*)"[^>]*data-order="(\d+)"[^>]*>([^<]+)'
        matches1 = re.findall(pattern1, html, re.IGNORECASE)
        
        for ep_slug, order, title in matches1:
            ep_slug = ep_slug.strip('/').replace('https://anizm.pro/', '').replace('https://anizle.org/', '')
            try:
                order_num = int(order)
                if order_num not in seen:
                    seen.add(order_num)
                    episodes.append(Episode(
                        id=ep_slug,
                        number=order_num,
                        title=title.strip()
                    ))
            except ValueError:
                pass
        
        pattern2 = r'href="/?([^"]+?-(\d+)-bolum[^"]*)"[^>]*>([^<]*)'
        matches2 = re.findall(pattern2, html, re.IGNORECASE)
        
        for ep_slug, ep_num, title in matches2:
            ep_slug = ep_slug.strip('/').replace('https://anizm.pro/', '').replace('https://anizle.org/', '')
            try:
                order_num = int(ep_num)
                if order_num not in seen:
                    seen.add(order_num)
                    final_title = title.strip() if title.strip() else f"{ep_num}. Bölüm"
                    episodes.append(Episode(
                        id=ep_slug,
                        number=order_num,
                        title=final_title
                    ))
            except ValueError:
                pass
        
        episodes.sort(key=lambda x: x.number)
        return episodes
    
    def get_streams(self, anime_id: str, episode_id: str) -> List[StreamLink]:
        translators = self._get_translators(episode_id)
        if not translators:
            return []
        
        all_videos = []
        for tr in translators:
            videos = self._get_translator_videos(tr["url"])
            for v in videos:
                all_videos.append({
                    "url": v["url"],
                    "name": v["name"],
                    "fansub": tr["name"]
                })
        
        if not all_videos:
            return []
        
        streams = []
        with ThreadPoolExecutor(max_workers=4) as executor:
            futures = {executor.submit(self._process_video, v): v for v in all_videos[:8]}
            for future in as_completed(futures, timeout=60):
                try:
                    result = future.result(timeout=30)
                    if result:
                        streams.append(result)
                except Exception:
                    pass
        
        return streams
    
    def _similarity(self, query: str, text: str) -> float:
        if not text:
            return 0.0
        q = query.lower()
        t = text.lower()
        if q == t:
            return 1.0
        if q in t:
            return 0.9
        return SequenceMatcher(None, q, t).ratio()
    
    def _get_poster_url(self, poster: str) -> str:
        if not poster:
            return ""
        if poster.startswith("http"):
            return poster
        return f"https://anizm.pro/uploads/img/{poster}"
    
    def _get_translators(self, episode_slug: str) -> List[Dict[str, str]]:
        clean_slug = episode_slug.lstrip("/")
        url = f"{API_BASE_URL}/{clean_slug}"
        
        response = _http_get(url)
        if not response or response.status_code != 200:
            return []
        
        html = response.text
        translators = []
        pattern = r'translator="([^"]+)"[^>]*data-fansub-name="([^"]*)"'
        matches = re.findall(pattern, html)
        
        seen = set()
        for tr_url, fansub in matches:
            if tr_url not in seen:
                seen.add(tr_url)
                translators.append({"url": tr_url, "name": fansub or "Fansub"})
        
        return translators
    
    def _get_translator_videos(self, translator_url: str) -> List[Dict[str, str]]:
        response = _http_get(
            translator_url,
            headers={
                "X-Requested-With": "XMLHttpRequest",
                "Accept": "application/json",
                "Referer": API_BASE_URL,
            }
        )
        
        if not response or response.status_code != 200:
            return []
        
        try:
            data = response.json()
            html = data.get("data", "")
            
            videos = []
            pattern = r'video="([^"]+)"[^>]*data-video-name="([^"]*)"'
            matches = re.findall(pattern, html)
            
            for video_url, video_name in matches:
                videos.append({"url": video_url, "name": video_name or "Player"})
            
            if not videos:
                pattern2 = r'data-video-name="([^"]*)"[^>]*video="([^"]+)"'
                matches2 = re.findall(pattern2, html)
                for video_name, video_url in matches2:
                    videos.append({"url": video_url, "name": video_name or "Player"})
            
            return videos
        except Exception:
            return []
    
    def _process_video(self, video_info: Dict[str, str]) -> Optional[StreamLink]:
        try:
            video_url = video_info["url"]
            fansub = video_info["fansub"]
            name = video_info["name"]
            
            response = _http_get(
                video_url,
                headers={
                    "X-Requested-With": "XMLHttpRequest",
                    "Accept": "application/json",
                    "Referer": API_BASE_URL,
                }
            )
            
            if not response or response.status_code != 200:
                return None
            
            data = response.json()
            player_html = data.get("player", "")
            
            iframe_match = re.search(r'/player/(\d+)', player_html)
            if not iframe_match:
                return None
            
            player_id = iframe_match.group(1)
            
            player_response = _http_get(
                f"{API_BASE_URL}/player/{player_id}",
                headers={"Referer": f"{API_BASE_URL}/"}
            )
            
            if not player_response or player_response.status_code != 200:
                return None
            
            fireplayer_id = _extract_fireplayer_id(player_response.text)
            if not fireplayer_id:
                return None
            
            video_response = _http_post(
                f"{PLAYER_BASE_URL}/player/index.php?data={fireplayer_id}&do=getVideo",
                headers={
                    "Referer": f"{PLAYER_BASE_URL}/player/{fireplayer_id}",
                    "Origin": PLAYER_BASE_URL,
                }
            )
            
            if not video_response or video_response.status_code != 200:
                return None
            
            video_data = video_response.json()
            
            if video_data.get("securedLink"):
                return StreamLink(
                    url=video_data["securedLink"],
                    quality="auto",
                    server=f"{fansub} - {name}"
                )
            
            if video_data.get("videoSource"):
                return StreamLink(
                    url=video_data["videoSource"],
                    quality="auto",
                    server=f"{fansub} - {name}"
                )
            
            return None
            
        except Exception:
            return None
