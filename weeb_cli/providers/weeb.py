import json
from typing import List, Optional

from weeb_cli.providers.base import (
    AnimeDetails,
    AnimeResult,
    BaseProvider,
    Episode,
    StreamLink,
)
from weeb_cli.providers.registry import register_provider

BASE_URL = "https://anime-api.ewgsta.workers.dev"


@register_provider("weeb", lang="tr", region="TR")
class WeebProvider(BaseProvider):
    def __init__(self):
        super().__init__()
        self.headers.update({"Accept": "application/json"})

    def search(self, query: str) -> List[AnimeResult]:
        if not query or len(query) < 2:
            return []

        data = self._request(f"{BASE_URL}/search", params={"q": query})
        if not data or "data" not in data:
            return []

        results = []
        for item in data["data"]:
            results.append(
                AnimeResult(
                    id=item["slug"], title=item["name"], cover=item.get("first_image")
                )
            )
        return results

    def get_details(self, anime_id: str) -> Optional[AnimeDetails]:
        data = self._request(f"{BASE_URL}/animes/{anime_id}")
        if not data or "data" not in data:
            return None

        anime_data = data["data"]
        episodes = []

        for ep in anime_data.get("episodes", []):
            sources_json = json.dumps(ep.get("sources", []))
            ep_num = ep.get("episode_number", 0)
            episodes.append(
                Episode(
                    id=sources_json,
                    number=ep_num,
                    title=f"Bölüm {ep_num}",
                    season=anime_data.get("season_number", 1),
                )
            )

        return AnimeDetails(
            id=anime_id,
            title=anime_data.get("name", anime_id),
            description=anime_data.get("description"),
            cover=anime_data.get("first_image"),
            genres=anime_data.get("categories", []),
            episodes=episodes,
            total_episodes=len(episodes),
        )

    def get_episodes(self, anime_id: str) -> List[Episode]:
        details = self.get_details(anime_id)
        return details.episodes if details else []

    def get_streams(self, anime_id: str, episode_id: str) -> List[StreamLink]:
        try:
            sources = json.loads(episode_id)
            if isinstance(sources, list):
                streams = []
                for src in sources:
                    watch_url = src.get("watch_url", "")
                    if watch_url:
                        streams.append(
                            StreamLink(
                                url=f"{BASE_URL}{watch_url}",
                                quality="auto",
                                server=src.get("label", "default"),
                            )
                        )
                if streams:
                    return streams
        except (json.JSONDecodeError, ValueError, TypeError):
            pass

        data = self._request(f"{BASE_URL}/animes/{anime_id}")
        if not data or "data" not in data:
            return []

        anime_data = data["data"]
        for ep in anime_data.get("episodes", []):
            if str(ep.get("episode_number")) == str(episode_id):
                streams = []
                for src in ep.get("sources", []):
                    watch_url = src.get("watch_url", "")
                    if watch_url:
                        streams.append(
                            StreamLink(
                                url=f"{BASE_URL}{watch_url}",
                                quality="auto",
                                server=src.get("label", "default"),
                            )
                        )
                return streams

        return []
