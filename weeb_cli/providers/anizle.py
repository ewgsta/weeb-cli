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
    HAS_CURL_CFFI = False

BASE_URL = "https://anizm.pro"
API_BASE_URL = "https://anizle.org"
ANIME_LIST_URL = f"{BASE_URL}/getAnimeListForSearch"
PLAYER_BASE_URL = "https://anizmplayer.com"

_anime_database: List[Dict[str, Any]] = []
_database_loaded: bool = False
_session = None


def _get_session():
    global _session
    if _session is None:
        if HAS_CURL_CFFI:
            _session = curl_requests.Session(impersonate="chrome110")
        else:
            import requests
            _session = requests.Session()
    return _session


@register_provider("anizle", lang="tr", region="TR")
class AnizleProvider(BaseProvider):
    
    def __init__(self):
        super().__init__()
        self.headers.update({
            "Accept-Language": "tr-TR,tr;q=0.9,en-US;q=0.8,en;q=0.7",
        })
    
    def search(self, query: str) -> List[AnimeResult]:
        database = self._load_database()
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
                results.append((max_score, AnimeResult(
                    id=anime.get("info_slug", ""),
                    title=anime.get("info_title", ""),
                    cover=self._get_poster_url(anime.get("info_poster", "")),
                    year=int(anime.get("info_year")) if anime.get("info_year", "").isdigit() else None
                )))
        
        results.sort(key=lambda x: x[0], reverse=True)
        return [r[1] for r in results[:20]]
    
    def get_details(self, anime_id: str) -> Optional[AnimeDetails]:
        database = self._load_database()
        anime_data = None
        
        for anime in database:
            if anime.get("info_slug") == anime_id:
                anime_data = anime
                break
        
        if not anime_data:
            return AnimeDetails(
                id=anime_id,
                title=anime_id.replace("-", " ").title(),
                episodes=self.get_episodes(anime_id)
            )
        
        categories = []
        for cat in anime_data.get("categories", []):
            if isinstance(cat, dict) and "tag_title" in cat:
                categories.append(cat["tag_title"])
        
        episodes = self.get_episodes(anime_id)
        
        return AnimeDetails(
            id=anime_id,
            title=anime_data.get("info_title", ""),
            description=anime_data.get("info_summary"),
            cover=self._get_poster_url(anime_data.get("info_poster", "")),
            genres=categories,
            year=int(anime_data.get("info_year")) if anime_data.get("info_year", "").isdigit() else None,
            episodes=episodes,
            total_episodes=len(episodes)
        )
    
    def get_episodes(self, anime_id: str) -> List[Episode]:
        session = _get_session()
        url = f"{BASE_URL}/{anime_id}"
        
        try:
            response = session.get(url, headers=self.headers, timeout=30)
            html = response.text
        except Exception:
            return []
        
        if not html:
            return []
        
        episodes = []
        seen = set()
        
        pattern1 = r'href="/?([^"]+?-bolum[^"]*)"[^>]*data-order="(\d+)"[^>]*>([^<]+)'
        matches1 = re.findall(pattern1, html, re.IGNORECASE)
        
        for ep_slug, order, title in matches1:
            ep_slug = ep_slug.strip('/')
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
            ep_slug = ep_slug.strip('/')
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
            for future in as_completed(futures):
                try:
                    result = future.result(timeout=30)
                    if result:
                        streams.append(result)
                except Exception:
                    pass
        
        return streams
    
    def _load_database(self) -> List[Dict[str, Any]]:
        global _anime_database, _database_loaded
        
        if _database_loaded:
            return _anime_database
        
        try:
            session = _get_session()
            response = session.get(ANIME_LIST_URL, headers=self.headers, timeout=120)
            data = response.json()
            if isinstance(data, list):
                _anime_database = data
                _database_loaded = True
        except Exception:
            pass
        
        return _anime_database
    
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
        session = _get_session()
        url = f"{API_BASE_URL}/{episode_slug}"
        
        try:
            response = session.get(url, headers=self.headers, timeout=30)
            html = response.text
        except Exception:
            return []
        
        if not html:
            return []
        
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
        session = _get_session()
        
        try:
            response = session.get(
                translator_url,
                headers={
                    **self.headers,
                    "X-Requested-With": "XMLHttpRequest",
                    "Accept": "application/json",
                    "Referer": API_BASE_URL,
                },
                timeout=15
            )
            data = response.json()
            html = data.get("data", "")
            
            videos = []
            pattern = r'video="([^"]+)"[^>]*data-video-name="([^"]*)"'
            matches = re.findall(pattern, html)
            
            for video_url, video_name in matches:
                videos.append({"url": video_url, "name": video_name or "Player"})
            
            return videos
        except Exception:
            return []
    
    def _process_video(self, video_info: Dict[str, str]) -> Optional[StreamLink]:
        session = _get_session()
        
        try:
            video_url = video_info["url"]
            fansub = video_info["fansub"]
            name = video_info["name"]
            
            response = session.get(
                video_url,
                headers={
                    **self.headers,
                    "X-Requested-With": "XMLHttpRequest",
                    "Accept": "application/json",
                    "Referer": API_BASE_URL,
                },
                timeout=15
            )
            data = response.json()
            player_html = data.get("player", "")
            
            iframe_match = re.search(r'/player/(\d+)', player_html)
            if not iframe_match:
                return None
            
            player_id = iframe_match.group(1)
            
            player_response = session.get(
                f"{API_BASE_URL}/player/{player_id}",
                headers={**self.headers, "Referer": f"{API_BASE_URL}/"},
                timeout=15
            )
            
            fireplayer_id = self._extract_fireplayer_id(player_response.text)
            if not fireplayer_id:
                return None
            
            if HAS_CURL_CFFI:
                video_response = session.post(
                    f"{PLAYER_BASE_URL}/player/index.php?data={fireplayer_id}&do=getVideo",
                    headers={
                        **self.headers,
                        "Referer": f"{PLAYER_BASE_URL}/player/{fireplayer_id}",
                        "Origin": PLAYER_BASE_URL,
                    },
                    timeout=15
                )
            else:
                import requests
                video_response = requests.post(
                    f"{PLAYER_BASE_URL}/player/index.php?data={fireplayer_id}&do=getVideo",
                    headers={
                        **self.headers,
                        "Referer": f"{PLAYER_BASE_URL}/player/{fireplayer_id}",
                        "Origin": PLAYER_BASE_URL,
                    },
                    timeout=15
                )
            
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
    
    def _extract_fireplayer_id(self, html: str) -> Optional[str]:
        eval_match = re.search(
            r"eval\(function\(p,a,c,k,e,d\)\{.*?\}return p\}\('(.*?)',(\d+),(\d+),'([^']+)'\.split\('\|'\),0,\{\}\)\)",
            html, re.S
        )
        
        if eval_match:
            p = eval_match.group(1)
            a = int(eval_match.group(2))
            c = int(eval_match.group(3))
            k = eval_match.group(4).split('|')
            
            try:
                decoded = self._unpack_js(p, a, c, k)
                id_match = re.search(r'FirePlayer\s*\(\s*["\']([a-f0-9]{32})["\']', decoded)
                if id_match:
                    return id_match.group(1)
            except Exception:
                pass
        
        fp_direct = re.search(r'FirePlayer\s*\(["\']([a-f0-9]{32})["\']', html)
        if fp_direct:
            return fp_direct.group(1)
        
        return None
    
    def _unpack_js(self, p: str, a: int, c: int, k: List[str]) -> str:
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
