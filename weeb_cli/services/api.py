import requests
from weeb_cli.config import config

class WeebClient:
    def __init__(self):
        pass

    @property
    def base_url(self):
        return config.get("api_url")

    def _get(self, endpoint, params=None):
        try:
            url = f"{self.base_url}{endpoint}"
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException:
            return None

    def search(self, query):
        source = config.get("scraping_source") or "local"
        if source == "weeb": source = "local"
        
        return self._get("/api/v1/anime/search", params={"query": query, "source": source})

    def get_details(self, slug):
        source = config.get("scraping_source") or "local"
        if source == "weeb": source = "local"
        return self._get(f"/api/v1/anime/detail/{slug}", params={"source": source})

    def get_streams(self, slug, episode):
        source = config.get("scraping_source") or "local"
        if source == "weeb": source = "local"
        return self._get(f"/api/v1/anime/watch/{slug}/{episode}", params={"source": source})

api_client = WeebClient()
