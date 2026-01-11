import requests
from rich.console import Console
from weeb_cli.config import config

console = Console()

class WeebClient:
    def __init__(self):
        pass

    @property
    def base_url(self):
        if config.get("dev_mode", False):
            return config.get("api_url")
        return "https://weeb-api.ewgsta.me"

    def _get(self, endpoint, params=None):
        try:
            url = f"{self.base_url}{endpoint}"
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            console.print(f"[red]Error: {e}[/red]")
            return None

    def search(self, query):
        source = config.get("scraping_source")
        if source == "weeb": source = "local"
        
        return self._get("/api/v1/anime/search", params={"query": query, "source": source})

    def get_details(self, slug):
        source = config.get("scraping_source")
        if source == "weeb": source = "local"
        return self._get(f"/api/v1/anime/detail/{slug}", params={"source": source})

    def get_streams(self, slug, episode):
        source = config.get("scraping_source")
        if source == "weeb": source = "local"
        return self._get(f"/api/v1/anime/watch/{slug}/{episode}", params={"source": source})

    def get_sources(self):
        return self._get("/api/v1/sources/")

api_client = WeebClient()
