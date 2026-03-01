from typing import List, Optional
from weeb_cli.config import config
from weeb_cli.providers import get_provider, get_default_provider, list_providers
from weeb_cli.providers.base import AnimeResult, AnimeDetails, Episode, StreamLink
from weeb_cli.exceptions import ProviderError
from weeb_cli.services.error_handler import handle_provider_error


class Scraper:
    
    def __init__(self) -> None:
        self._provider = None
        self._provider_name: Optional[str] = None
        self.last_error: Optional[str] = None
    
    @property
    def provider(self):
        current_source = config.get("scraping_source", "")
        
        if self._provider_name != current_source:
            self._provider_name = current_source
            self._provider = get_provider(current_source)
            
            if not self._provider:
                lang = config.get("language", "tr")
                default = get_default_provider(lang)
                if default:
                    self._provider = get_provider(default)
                    self._provider_name = default
        
        return self._provider
    
    def search(self, query: str) -> List[AnimeResult]:
        self.last_error = None
        if not self.provider:
            return []
        try:
            return self.provider.search(query)
        except ProviderError as e:
            self.last_error = e.code
            handle_provider_error(e, self._provider_name)
            return []
        except Exception as e:
            self.last_error = str(e)
            handle_provider_error(e, self._provider_name)
            return []
    
    def get_details(self, anime_id: str) -> Optional[AnimeDetails]:
        self.last_error = None
        if not self.provider:
            return None
        try:
            return self.provider.get_details(anime_id)
        except ProviderError as e:
            self.last_error = e.code
            handle_provider_error(e, self._provider_name)
            return None
        except Exception as e:
            self.last_error = str(e)
            handle_provider_error(e, self._provider_name)
            return None
    
    def get_episodes(self, anime_id: str) -> List[Episode]:
        self.last_error = None
        if not self.provider:
            return []
        try:
            return self.provider.get_episodes(anime_id)
        except ProviderError as e:
            self.last_error = e.code
            handle_provider_error(e, self._provider_name)
            return []
        except Exception as e:
            self.last_error = str(e)
            handle_provider_error(e, self._provider_name)
            return []
    
    def get_streams(self, anime_id: str, episode_id: str) -> List[StreamLink]:
        from weeb_cli.services.logger import debug
        
        self.last_error = None
        debug(f"[SCRAPER] get_streams called: anime_id={anime_id}, episode_id={episode_id}")
        debug(f"[SCRAPER] Current provider: {self._provider_name}")
        
        if not self.provider:
            debug("[SCRAPER] No provider available!")
            return []
        
        try:
            debug(f"[SCRAPER] Calling provider.get_streams()")
            result = self.provider.get_streams(anime_id, episode_id)
            debug(f"[SCRAPER] Provider returned {len(result) if result else 0} streams")
            return result
        except ProviderError as e:
            self.last_error = e.code
            handle_provider_error(e, self._provider_name)
            return []
        except Exception as e:
            self.last_error = str(e)
            handle_provider_error(e, self._provider_name)
            return []
    
    def get_available_sources(self) -> List[dict]:
        return list_providers()
    
    def get_sources_for_lang(self, lang: str) -> List[str]:
        from weeb_cli.providers import get_providers_for_lang
        return get_providers_for_lang(lang)


scraper: Scraper = Scraper()
