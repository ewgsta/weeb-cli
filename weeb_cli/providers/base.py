from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Tuple
from weeb_cli.exceptions import ProviderError
from weeb_cli.services.logger import debug


@dataclass
class AnimeResult:
    id: str
    title: str
    type: str = "series"
    cover: Optional[str] = None
    year: Optional[int] = None
    
    
@dataclass
class Episode:
    id: str
    number: int
    title: Optional[str] = None
    season: int = 1
    url: Optional[str] = None


@dataclass
class StreamLink:
    url: str
    quality: str = "auto"
    server: str = "default"
    headers: Dict[str, str] = field(default_factory=dict)
    subtitles: Optional[str] = None


@dataclass
class AnimeDetails:
    id: str
    title: str
    description: Optional[str] = None
    cover: Optional[str] = None
    genres: List[str] = field(default_factory=list)
    year: Optional[int] = None
    status: Optional[str] = None
    episodes: List[Episode] = field(default_factory=list)
    total_episodes: Optional[int] = None


class BaseProvider(ABC):
    
    name: str = "base"
    lang: str = "tr"
    region: str = "TR"
    
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/html, */*',
        }
    
    @abstractmethod
    def search(self, query: str) -> List[AnimeResult]:
        pass
    
    @abstractmethod
    def get_details(self, anime_id: str) -> Optional[AnimeDetails]:
        pass
    
    @abstractmethod
    def get_episodes(self, anime_id: str) -> List[Episode]:
        pass
    
    @abstractmethod
    def get_streams(self, anime_id: str, episode_id: str) -> List[StreamLink]:
        pass
    
    def _request(self, url: str, params: Optional[dict] = None, json_response: bool = True, max_retries: int = 3) -> Any:
        import requests
        import time
        import random
        
        for attempt in range(max_retries):
            try:
                response = requests.get(
                    url, 
                    headers=self.headers, 
                    params=params,
                    timeout=15
                )
                response.raise_for_status()
                
                if json_response:
                    return response.json()
                return response.text
                
            except requests.RequestException as e:
                debug(f"[HTTP] Request failed (attempt {attempt + 1}/{max_retries}): {url} - {e}")
                
                if attempt < max_retries - 1:
                    if isinstance(e, requests.HTTPError) and e.response.status_code in [404, 403, 401]:
                        debug(f"[HTTP] Permanent error, skipping retries")
                        return None
                    
                    delay = min(2 ** attempt, 10) + random.uniform(0, 1)
                    time.sleep(delay)
                    continue
                
                return None
