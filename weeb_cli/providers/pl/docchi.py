from typing import Any, Dict, List, Optional

from weeb_cli.providers.base import (
    AnimeDetails,
    AnimeResult,
    BaseProvider,
    Episode,
    StreamLink,
)
from weeb_cli.providers.registry import register_provider
from weeb_cli.services.logger import debug


@register_provider("docchi", lang="pl", region="PL")
class DocchiProvider(BaseProvider):
    BASE_URL = "https://api.docchi.pl/v1"

    def search(self, query: str) -> List[AnimeResult]:
        url = f"{self.BASE_URL}/series/list"
        data = self._request(url)

        if not data or not isinstance(data, list):
            return []

        results = []
        for item in data:
            title = item.get("title", "")
            if query.lower() in title.lower():
                results.append(
                    AnimeResult(
                        id=item.get("slug", ""),
                        title=title,
                        cover=item.get("image", ""),
                        year=None,
                    )
                )

        return results

    def get_details(self, anime_id: str) -> Optional[AnimeDetails]:
        url = f"{self.BASE_URL}/series/find/{anime_id}"
        data = self._request(url)

        if not data:
            return None

        episodes = self.get_episodes(anime_id)

        return AnimeDetails(
            id=anime_id,
            title=data.get("title", ""),
            description=data.get("description", ""),
            cover=data.get("image", ""),
            genres=data.get("genres", []),
            status=data.get("status", ""),
            episodes=episodes,
            total_episodes=len(episodes),
        )

    def get_episodes(self, anime_id: str) -> List[Episode]:
        url = f"{self.BASE_URL}/episodes/count/{anime_id}"
        data = self._request(url)

        if not data or not isinstance(data, list):
            return []

        episodes = []
        for i, item in enumerate(data, 1):
            episodes.append(Episode(id=str(i), number=i, title=f"Odcinek {i}"))

        return episodes

    def get_streams(self, anime_id: str, episode_id: str) -> List[StreamLink]:
        url = f"{self.BASE_URL}/episodes/find/{anime_id}/{episode_id}"
        debug(f"[DOCCHI] Requesting streams from: {url}")
        data = self._request(url)
        debug(f"[DOCCHI] API Response: {data}")

        if not data or not isinstance(data, list):
            debug(
                f"[DOCCHI] No valid data returned from API for {anime_id} ep {episode_id}"
            )
            return []

        streams = []
        for player in data:
            hosting = player.get("player_hosting", "unknown")
            translator = player.get("translator_title", "")
            player_url = player.get("player", "")

            if "mega.nz" in player_url:
                debug(f"[DOCCHI] Skipping MEGA link: {player_url}")
                continue

            if "ebd.cda.pl" in player_url:
                parts = player_url.split("/")
                if len(parts) >= 5:
                    video_id = parts[-1]
                    player_url = f"https://www.cda.pl/video/{video_id}"

            server_name = f"{hosting} ({translator})" if translator else hosting
            debug(f"[DOCCHI] Found player: {server_name} -> {player_url}")

            if player_url:
                streams.append(
                    StreamLink(url=player_url, quality="auto", server=server_name)
                )

        debug(f"[DOCCHI] Returning {len(streams)} streams")
        return streams
