from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Tuple


class ProviderError(Exception):
    def __init__(self, code: str, message: str = ""):
        self.code = code
        self.message = message
        super().__init__(f"{code}: {message}")


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
    
    def _request(self, url: str, params: dict = None, json_response: bool = True) -> Any:
        import requests
        
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
            
        except requests.RequestException:
            return None
