"""
Base Provider - Tüm kaynakların implement etmesi gereken interface

Her provider şu metodları implement etmeli:
- search(query) -> List[AnimeResult]
- get_details(anime_id) -> AnimeDetails
- get_episodes(anime_id) -> List[Episode]
- get_streams(anime_id, episode_id) -> List[StreamLink]
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any


@dataclass
class AnimeResult:
    """Arama sonucu"""
    id: str
    title: str
    type: str = "series"  # series, movie, ova
    cover: Optional[str] = None
    year: Optional[int] = None
    
    
@dataclass
class Episode:
    """Bölüm bilgisi"""
    id: str
    number: int
    title: Optional[str] = None
    season: int = 1
    url: Optional[str] = None


@dataclass
class StreamLink:
    """Stream linki"""
    url: str
    quality: str = "auto"
    server: str = "default"
    headers: Dict[str, str] = field(default_factory=dict)
    subtitles: Optional[str] = None


@dataclass
class AnimeDetails:
    """Anime detayları"""
    id: str
    title: str
    description: Optional[str] = None
    cover: Optional[str] = None
    genres: List[str] = field(default_factory=list)
    year: Optional[int] = None
    status: Optional[str] = None  # ongoing, completed
    episodes: List[Episode] = field(default_factory=list)
    total_episodes: Optional[int] = None


class BaseProvider(ABC):
    """
    Abstract base class for all anime providers.
    
    Her yeni kaynak bu class'tan türemeli ve
    tüm abstract metodları implement etmeli.
    """
    
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
        """
        Anime ara
        
        Args:
            query: Arama terimi
            
        Returns:
            AnimeResult listesi
        """
        pass
    
    @abstractmethod
    def get_details(self, anime_id: str) -> Optional[AnimeDetails]:
        """
        Anime detaylarını getir
        
        Args:
            anime_id: Anime ID
            
        Returns:
            AnimeDetails veya None
        """
        pass
    
    @abstractmethod
    def get_episodes(self, anime_id: str) -> List[Episode]:
        """
        Bölüm listesini getir
        
        Args:
            anime_id: Anime ID
            
        Returns:
            Episode listesi
        """
        pass
    
    @abstractmethod
    def get_streams(self, anime_id: str, episode_id: str) -> List[StreamLink]:
        """
        Stream linklerini getir
        
        Args:
            anime_id: Anime ID
            episode_id: Bölüm ID
            
        Returns:
            StreamLink listesi
        """
        pass
    
    def _request(self, url: str, params: dict = None, json_response: bool = True) -> Any:
        """
        HTTP GET request helper
        
        Args:
            url: Request URL
            params: Query parameters
            json_response: JSON olarak parse et
            
        Returns:
            Response data veya None
        """
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
