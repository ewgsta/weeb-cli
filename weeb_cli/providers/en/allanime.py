import json
import re
import urllib.request
from urllib.parse import quote, urlencode
from typing import List, Optional

from weeb_cli.providers.base import (
    BaseProvider,
    AnimeResult,
    AnimeDetails,
    Episode,
    StreamLink
)
from weeb_cli.providers.registry import register_provider

API_URL = "https://api.allanime.day/api"
REFERER = "https://allmanga.to"

HEADERS = {
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/121.0",
    "Referer": REFERER
}

DECODE_MAP = {
    '79': 'A', '7a': 'B', '7b': 'C', '7c': 'D', '7d': 'E', '7e': 'F', '7f': 'G',
    '70': 'H', '71': 'I', '72': 'J', '73': 'K', '74': 'L', '75': 'M', '76': 'N',
    '77': 'O', '68': 'P', '69': 'Q', '6a': 'R', '6b': 'S', '6c': 'T', '6d': 'U',
    '6e': 'V', '6f': 'W', '60': 'X', '61': 'Y', '62': 'Z', '59': 'a', '5a': 'b',
    '5b': 'c', '5c': 'd', '5d': 'e', '5e': 'f', '5f': 'g', '50': 'h', '51': 'i',
    '52': 'j', '53': 'k', '54': 'l', '55': 'm', '56': 'n', '57': 'o', '48': 'p',
    '49': 'q', '4a': 'r', '4b': 's', '4c': 't', '4d': 'u', '4e': 'v', '4f': 'w',
    '40': 'x', '41': 'y', '42': 'z', '08': '0', '09': '1', '0a': '2', '0b': '3',
    '0c': '4', '0d': '5', '0e': '6', '0f': '7', '00': '8', '01': '9', '15': '-',
    '16': '.', '67': '_', '46': '~', '02': ':', '17': '/', '07': '?', '1b': '#',
    '63': '[', '65': ']', '78': '@', '19': '!', '1c': '$', '1e': '&', '10': '(',
    '11': ')', '12': '*', '13': '+', '14': ',', '03': ';', '05': '=', '1d': '%'
}


def _decode_provider_id(encoded: str) -> str:
    result = []
    i = 0
    while i < len(encoded):
        pair = encoded[i:i+2]
        if pair in DECODE_MAP:
            result.append(DECODE_MAP[pair])
        i += 2
    decoded = ''.join(result)
    return decoded.replace('/clock', '/clock.json')


def _http_get(url: str, headers: dict = None, timeout: int = 15) -> bytes:
    req = urllib.request.Request(url, headers=headers or HEADERS)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read()


def _get_json(url: str, headers: dict = None, timeout: int = 15):
    try:
        data = _http_get(url, headers, timeout)
        return json.loads(data)
    except Exception:
        return None


def _graphql_request(query: str, variables: dict) -> dict:
    params = {
        'variables': json.dumps(variables),
        'query': query
    }
    url = f"{API_URL}?{urlencode(params)}"
    return _get_json(url, HEADERS)


@register_provider("allanime", lang="en", region="US")
class AllAnimeProvider(BaseProvider):
    
    def __init__(self):
        super().__init__()
        self.mode = "sub"
        self.headers = HEADERS.copy()
        
    def search(self, query: str) -> List[AnimeResult]:
        q = (query or "").strip()
        if not q:
            return []
        
        gql = '''query($search: SearchInput $limit: Int $page: Int $translationType: VaildTranslationTypeEnumType $countryOrigin: VaildCountryOriginEnumType) {
            shows(search: $search limit: $limit page: $page translationType: $translationType countryOrigin: $countryOrigin) {
                edges {
                    _id
                    name
                    availableEpisodes
                    __typename
                }
            }
        }'''
        
        variables = {
            "search": {
                "allowAdult": False,
                "allowUnknown": False,
                "query": q
            },
            "limit": 40,
            "page": 1,
            "translationType": self.mode,
            "countryOrigin": "ALL"
        }
        
        data = _graphql_request(gql, variables)
        if not data or 'data' not in data:
            return []
        
        shows = data.get('data', {}).get('shows', {}).get('edges', [])
        results = []
        
        for show in shows:
            anime_id = show.get('_id')
            name = show.get('name')
            episodes = show.get('availableEpisodes', {})
            
            if not anime_id or not name:
                continue
            
            ep_count = episodes.get(self.mode, 0)
            if ep_count == 0:
                continue
            
            results.append(AnimeResult(
                id=anime_id,
                title=name,
                type="series"
            ))
        
        return results
    
    def get_details(self, anime_id: str) -> Optional[AnimeDetails]:
        gql = '''query ($showId: String!) {
            show(_id: $showId) {
                _id
                name
                description
                thumbnail
                availableEpisodesDetail
            }
        }'''
        
        variables = {"showId": anime_id}
        data = _graphql_request(gql, variables)
        
        if not data or 'data' not in data:
            return None
        
        show = data.get('data', {}).get('show', {})
        
        if not show:
            return None
        
        title = show.get('name', anime_id.replace('-', ' ').title())
        description = show.get('description')
        thumbnail = show.get('thumbnail')
        
        ep_detail = show.get('availableEpisodesDetail', {})
        ep_list = ep_detail.get(self.mode, [])
        
        episodes = []
        for i, ep_num in enumerate(sorted(ep_list, key=lambda x: float(x) if x.replace('.', '').isdigit() else 0)):
            episodes.append(Episode(
                id=f"{anime_id}::ep={ep_num}",
                number=i + 1,
                title=f"Episode {ep_num}"
            ))
        
        return AnimeDetails(
            id=anime_id,
            title=title,
            description=description,
            cover=thumbnail,
            episodes=episodes,
            total_episodes=len(episodes)
        )
    
    def get_episodes(self, anime_id: str) -> List[Episode]:
        gql = '''query ($showId: String!) {
            show(_id: $showId) {
                _id
                availableEpisodesDetail
            }
        }'''
        
        variables = {"showId": anime_id}
        data = _graphql_request(gql, variables)
        
        if not data or 'data' not in data:
            return []
        
        show = data.get('data', {}).get('show', {})
        ep_detail = show.get('availableEpisodesDetail', {})
        ep_list = ep_detail.get(self.mode, [])
        
        episodes = []
        for i, ep_num in enumerate(sorted(ep_list, key=lambda x: float(x) if x.replace('.', '').isdigit() else 0)):
            episodes.append(Episode(
                id=f"{anime_id}::ep={ep_num}",
                number=i + 1,
                title=f"Episode {ep_num}"
            ))
        
        return episodes
    
    def get_streams(self, anime_id: str, episode_id: str) -> List[StreamLink]:
        from weeb_cli.services.logger import debug, error
        
        debug(f"[ALLANIME] get_streams: anime_id={anime_id}, episode_id={episode_id}")
        
        if '::ep=' in episode_id:
            parts = episode_id.split('::ep=')
            show_id = parts[0]
            ep_no = parts[1]
        else:
            show_id = anime_id
            ep_no = episode_id
        
        debug(f"[ALLANIME] Parsed: show_id={show_id}, ep_no={ep_no}, mode={self.mode}")
        
        gql = '''query ($showId: String!, $translationType: VaildTranslationTypeEnumType!, $episodeString: String!) {
            episode(showId: $showId translationType: $translationType episodeString: $episodeString) {
                episodeString
                sourceUrls
            }
        }'''
        
        variables = {
            "showId": show_id,
            "translationType": self.mode,
            "episodeString": ep_no
        }
        
        debug(f"[ALLANIME] GraphQL variables: {variables}")
        
        data = _graphql_request(gql, variables)
        
        debug(f"[ALLANIME] GraphQL response: {data}")
        
        if not data or 'data' not in data:
            error(f"[ALLANIME] No data in response")
            return []
        
        episode = data.get('data', {}).get('episode', {})
        source_urls = episode.get('sourceUrls', [])
        
        streams = []
        
        for source in source_urls:
            try:
                source_url = source.get('sourceUrl', '')
                source_name = source.get('sourceName', 'unknown')
                
                if not source_url or not source_url.startswith('--'):
                    continue
                
                encoded = source_url[2:]
                decoded_path = _decode_provider_id(encoded)
                
                if not decoded_path:
                    continue
                
                full_url = f"https://allanime.day{decoded_path}"
                
                stream_data = _get_json(full_url, self.headers)
                if not stream_data:
                    continue
                
                links = stream_data.get('links', [])
                for link in links:
                    link_url = link.get('link')
                    resolution = link.get('resolutionStr', 'auto')
                    
                    if link_url:
                        streams.append(StreamLink(
                            url=link_url,
                            quality=resolution,
                            server=source_name.lower(),
                            headers={"Referer": REFERER}
                        ))
            except Exception:
                continue
        
        return streams
    
    def set_mode(self, mode: str):
        if mode in ['sub', 'dub']:
            self.mode = mode
