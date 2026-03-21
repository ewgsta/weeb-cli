import json
import re
from typing import List, Optional

from weeb_cli.providers.base import (
    BaseProvider,
    AnimeResult,
    AnimeDetails,
    Episode,
    StreamLink,
)


class ExampleProvider(BaseProvider):

    def __init__(self):
        super().__init__()
        self.headers.update({
            "Referer": "https://example-anime-site.com/",
        })
        self.base_url = "https://example-anime-site.com/api"

    def search(self, query: str) -> List[AnimeResult]:
        # In a real plugin, you would make an HTTP request here:
        # data = self._request(f"{self.base_url}/search?q={query}")

        return [
            AnimeResult(
                id="example-1",
                title=f"Example Anime: {query}",
                type="series",
            ),
            AnimeResult(
                id="example-2",
                title=f"Another Anime: {query}",
                type="movie",
            ),
        ]

    def get_details(self, anime_id: str) -> Optional[AnimeDetails]:
        episodes = self.get_episodes(anime_id)

        return AnimeDetails(
            id=anime_id,
            title=f"Example Anime ({anime_id})",
            description="This is an example anime description.",
            genres=["Action", "Adventure"],
            year=2025,
            status="Ongoing",
            episodes=episodes,
            total_episodes=len(episodes),
        )

    def get_episodes(self, anime_id: str) -> List[Episode]:
        return [
            Episode(id=f"{anime_id}-ep-{i}", number=i, title=f"Episode {i}")
            for i in range(1, 13)
        ]

    def get_streams(self, anime_id: str, episode_id: str) -> List[StreamLink]:
        # In a real plugin, you would parse video embed pages
        # and extract actual stream URLs here.

        return [
            StreamLink(
                url="https://example.com/stream/1080p.m3u8",
                quality="1080p",
                server="example-cdn",
            ),
            StreamLink(
                url="https://example.com/stream/720p.m3u8",
                quality="720p",
                server="example-cdn",
            ),
        ]
