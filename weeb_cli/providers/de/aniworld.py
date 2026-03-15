import json, re, requests
from typing import List, Optional
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

    def _get(self, url):
        try:
            resp = self.session.get(url, headers=self.headers, timeout=10)
            resp.raise_for_status()
            return resp.text
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
        html = self._get(urljoin(STREAM_BASE, slug))
        if not html: return None
        soup = BeautifulSoup(html, "html.parser")
        title = soup.find("h1", itemprop="name").text.strip() if soup.find("h1", itemprop="name") else slug
        season_matches = re.findall(r"staffel-(\d+)", html)
        unique_seasons = sorted(list(set(int(s) for s in season_matches)))
        if not unique_seasons: unique_seasons = [1]
        all_episodes = []
        for s_num in unique_seasons:
            s_html = self._get(f"{STREAM_BASE}{slug}/staffel-{s_num}")
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
        html = self._get(f"{STREAM_BASE}{slug}/staffel-{season}")
        if not html: return []
        ep_matches = re.findall(f"staffel-{season}/episode-(\\d+)", html)
        unique_eps = sorted(list(set(int(m) for m in ep_matches)))
        return [Episode(id=f"{slug}/staffel-{season}/episode-{num}", number=num, title=f"Folge {num}" if season > 0 else f"Film {num}", season=season) for num in unique_eps]

    def get_streams(self, anime_id: str, episode_id: str) -> List[StreamLink]:
        from weeb_cli.providers.extractors.voe import extract_voe
        from weeb_cli.providers.extractors.filemoon import extract_filemoon
        from weeb_cli.providers.extractors.streamtape import extract_streamtape
        from weeb_cli.providers.extractors.vidoza import extract_vidoza
        from weeb_cli.providers.extractors.doodstream import extract_doodstream
        html = self._get(urljoin(STREAM_BASE, episode_id))
        if not html: return []
        soup = BeautifulSoup(html, "html.parser")
        lang_map = {"1": "GerDub", "2": "GerSub", "3": "EngSub"}
        streams = []
        hoster_items = soup.find_all("li", attrs={"data-link-target": True})
        for item in hoster_items:
            target = item["data-link-target"]
            if not target.startswith("/redirect/"): continue
            l_key = item.get("data-lang-key", "0")
            lang_name = lang_map.get(l_key, "N/A")
            h_name = "Unknown"
            icon = item.find("i", class_="icon")
            if icon:
                for cls in icon.get("class", []):
                    if cls != "icon": h_name = cls; break
            if h_name == "Unknown" and item.find("h4"): h_name = item.find("h4").text.strip()
            try:
                resp = self.session.get(urljoin(BASE_URL, target), headers=self.headers, timeout=10, allow_redirects=True)
                e_url = resp.url
                v_url = None; h_low = h_name.lower()
                if "voe" in h_low: v_url = extract_voe(e_url)
                elif "filemoon" in h_low: v_url = extract_filemoon(e_url)
                elif "streamtape" in h_low: v_url = extract_streamtape(e_url)
                elif "vidoza" in h_low: v_url = extract_vidoza(e_url)
                elif "dood" in h_low: v_url = extract_doodstream(e_url)
                f_url = v_url or e_url
                if f_url: streams.append(StreamLink(url=f_url, quality=f"[{lang_name}]", server=h_name))
            except: continue
        return streams
