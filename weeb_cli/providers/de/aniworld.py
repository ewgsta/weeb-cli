import json, re, requests
from typing import List, Optional, Dict, Tuple
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from weeb_cli.providers.base import BaseProvider, AnimeResult, AnimeDetails, Episode, StreamLink
from weeb_cli.providers.registry import register_provider
from weeb_cli.services.logger import debug

BASE_URL = "https://aniworld.to"
AJAX_URL = "https://aniworld.to/ajax/search"
STREAM_BASE = "https://aniworld.to/anime/stream/"

@register_provider(name="aniworld", lang="de", region="DE")
class AniWorldProvider(BaseProvider):
    def __init__(self):
        super().__init__()
        self.session = requests.Session()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Referer": "https://aniworld.to/"
        }
        self._html_cache: Dict[str, str] = {}

    def _get(self, url, use_cache=False):
        if use_cache and url in self._html_cache:
            return self._html_cache[url]
        try:
            resp = self.session.get(url, headers=self.headers, timeout=10)
            resp.raise_for_status()
            html = resp.text
            if use_cache:
                self._html_cache[url] = html
            return html
        except Exception as e:
            debug(f"[AniWorld] GET Error: {e}"); return ""

    def _post(self, url, data):
        try:
            h = self.headers.copy(); h["X-Requested-With"] = "XMLHttpRequest"
            resp = self.session.post(url, data=data, headers=h, timeout=10)
            return resp.text
        except Exception as e:
            debug(f"[AniWorld] POST Error: {e}"); return ""

    def search(self, query: str) -> List[AnimeResult]:
        res = self._post(AJAX_URL, {"keyword": query})
        if not res: return []
        try:
            data = json.loads(res)
            results = []
            for item in data:
                link = item.get("link", "")
                if link.startswith("/anime/stream/"):
                    slug = link.replace("/anime/stream/", "").split("/")[0]
                    title = item.get("title", "").replace("<em>", "").replace("</em>", "")
                    results.append(AnimeResult(id=slug, title=title, type="series"))
            return results
        except: return []

    def get_details(self, anime_id: str) -> Optional[AnimeDetails]:
        slug = anime_id.split("/")[0]
        html = self._get(urljoin(STREAM_BASE, slug), use_cache=True)
        if not html: return None
        soup = BeautifulSoup(html, "html.parser")
        title_elem = soup.find("h1", itemprop="name")
        if title_elem:
            title_span = title_elem.find("span")
            title = title_span.text.strip() if title_span else title_elem.text.strip()
        else:
            title = slug
        season_matches = re.findall(r"staffel-(\d+)", html)
        unique_seasons = sorted(list(set(int(s) for s in season_matches)))
        if not unique_seasons: unique_seasons = [1]
        all_episodes = []
        for s_num in unique_seasons:
            s_html = self._get(f"{STREAM_BASE}{slug}/staffel-{s_num}", use_cache=True)
            ep_matches = re.findall(f"staffel-{s_num}/episode-(\\d+)", s_html)
            unique_eps = sorted(list(set(int(m) for m in ep_matches)))
            for e_num in unique_eps:
                all_episodes.append(Episode(
                    id=f"{slug}/staffel-{s_num}/episode-{e_num}",
                    number=e_num, title=f"Folge {e_num}" if s_num > 0 else f"Film {e_num}",
                    season=s_num
                ))
        return AnimeDetails(id=slug, title=title, description="", cover=None, total_episodes=len(all_episodes), episodes=all_episodes)

    def get_episodes(self, anime_id: str, season: int = 1) -> List[Episode]:
        slug = anime_id.split("/")[0]
        html = self._get(f"{STREAM_BASE}{slug}/staffel-{season}", use_cache=True)
        if not html: return []
        ep_matches = re.findall(f"staffel-{season}/episode-(\\d+)", html)
        unique_eps = sorted(list(set(int(m) for m in ep_matches)))
        return [Episode(id=f"{slug}/staffel-{season}/episode-{num}", number=num, title=f"Folge {num}" if season > 0 else f"Film {num}", season=season) for num in unique_eps]

    def _score_hoster(self, lang: str, quality: str, hoster: str) -> int:
        """Score hoster based on language, quality, and hoster preference (like bash version)"""
        lang_score = {"GerDub": 300, "GerSub": 200, "EngSub": 100}.get(lang, 0)
        qual_score = {"1080p": 5, "720p": 4, "480p": 3, "HD": 2}.get(quality, 1)
        h_lower = hoster.lower()
        if "vidmoly" in h_lower: hoster_score = 50
        elif "voe" in h_lower: hoster_score = 40
        elif "filemoon" in h_lower or "streamtape" in h_lower or "doodstream" in h_lower: hoster_score = 5
        else: hoster_score = 1
        return (lang_score * 10000) + (qual_score * 100) + hoster_score

    def _extract_quality(self, item_html: str) -> str:
        """Extract quality from hoster item HTML"""
        quality_match = re.search(r'\b(\d{3,4}p)\b', item_html)
        if quality_match: return quality_match.group(1)
        if "1080" in item_html: return "1080p"
        if "720" in item_html: return "720p"
        if "480" in item_html: return "480p"
        if "HD" in item_html.upper(): return "HD"
        return "N/A"

    def _extract_video_from_embed(self, embed_url: str, hoster_name: str) -> Optional[str]:
        """Extract video URL from embed page with fallback support"""
        from weeb_cli.providers.extractors.voe import extract_voe
        from weeb_cli.providers.extractors.filemoon import extract_filemoon
        from weeb_cli.providers.extractors.streamtape import extract_streamtape
        from weeb_cli.providers.extractors.vidoza import extract_vidoza
        from weeb_cli.providers.extractors.doodstream import extract_doodstream
        
        h_lower = hoster_name.lower()
        try:
            if "voe" in h_lower:
                return extract_voe(embed_url)
            elif "filemoon" in h_lower:
                return extract_filemoon(embed_url)
            elif "streamtape" in h_lower:
                return extract_streamtape(embed_url)
            elif "vidoza" in h_lower or "vidmoly" in h_lower:
                # Vidmoly extraction
                html = self._get(embed_url)
                if html:
                    # Try sources pattern
                    match = re.search(r'(?:sources|file):\s*["\']([^"\']*\.(?:m3u8|mp4)[^"\']*)', html)
                    if match: return match.group(1)
                    # Generic pattern
                    match = re.search(r'https?://[^"\']*\.(?:m3u8|mp4)[^"\']*', html)
                    if match: return match.group(0)
                return None
            elif "dood" in h_lower:
                return extract_doodstream(embed_url)
        except Exception as e:
            debug(f"[AniWorld] Extraction error for {hoster_name}: {e}")
        return None

    def get_streams(self, anime_id: str, episode_id: str) -> List[StreamLink]:
        html = self._get(urljoin(STREAM_BASE, episode_id))
        if not html: return []
        soup = BeautifulSoup(html, "html.parser")
        lang_map = {"1": "GerDub", "2": "GerSub", "3": "EngSub"}
        
        # Collect all hosters with metadata
        hosters = []
        hoster_items = soup.find_all("li", attrs={"data-link-target": True})
        for item in hoster_items:
            target = item.get("data-link-target", "")
            if not target.startswith("/redirect/"): continue
            
            redirect_id = target.replace("/redirect/", "")
            l_key = item.get("data-lang-key", "0")
            lang_name = lang_map.get(l_key, "N/A")
            
            # Extract hoster name
            h_name = "Unknown"
            icon = item.find("i", class_="icon")
            if icon:
                for cls in icon.get("class", []):
                    if cls != "icon": h_name = cls; break
            if h_name == "Unknown":
                h4 = item.find("h4")
                if h4: h_name = h4.text.strip()
            
            # Extract quality
            quality = self._extract_quality(str(item))
            
            # Calculate score
            score = self._score_hoster(lang_name, quality, h_name)
            
            hosters.append({
                "redirect_id": redirect_id,
                "target": target,
                "hoster": h_name,
                "language": lang_name,
                "quality": quality,
                "score": score
            })
        
        # Sort by score (highest first)
        hosters.sort(key=lambda x: x["score"], reverse=True)
        
        # Try each hoster with fallback
        streams = []
        for hoster_info in hosters:
            try:
                debug(f"[AniWorld] Trying {hoster_info['hoster']} [{hoster_info['language']}] [{hoster_info['quality']}]")
                resp = self.session.get(urljoin(BASE_URL, hoster_info["target"]), headers=self.headers, timeout=10, allow_redirects=True)
                embed_url = resp.url
                
                video_url = self._extract_video_from_embed(embed_url, hoster_info["hoster"])
                
                if video_url:
                    # Validate URL looks like actual video
                    if re.search(r'\.(m3u8|mp4|ts)(\?|#|$)', video_url) or '/hls/' in video_url or '/playlist' in video_url:
                        quality_label = f"[{hoster_info['language']}]"
                        if hoster_info['quality'] != "N/A":
                            quality_label += f" [{hoster_info['quality']}]"
                        streams.append(StreamLink(url=video_url, quality=quality_label, server=hoster_info["hoster"]))
                        debug(f"[AniWorld] Success: {hoster_info['hoster']}")
                    else:
                        debug(f"[AniWorld] Invalid video URL from {hoster_info['hoster']}: {video_url}")
                else:
                    debug(f"[AniWorld] Failed to extract from {hoster_info['hoster']}")
            except Exception as e:
                debug(f"[AniWorld] Error with {hoster_info['hoster']}: {e}")
                continue
        
        return streams
