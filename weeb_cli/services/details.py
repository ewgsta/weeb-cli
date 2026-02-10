from typing import Optional, Dict
from weeb_cli.services.scraper import scraper


def get_details(anime_id: str) -> Optional[Dict]:
    details = scraper.get_details(anime_id)
    if not details:
        return None
    
    return {
        "id": details.id,
        "slug": details.id,
        "title": details.title,
        "name": details.title,
        "description": details.description,
        "synopsis": details.description,
        "cover": details.cover,
        "genres": details.genres,
        "year": details.year,
        "status": details.status,
        "total_episodes": details.total_episodes,
        "episodes": [
            {
                "id": ep.id,
                "number": ep.number,
                "ep_num": ep.number,
                "title": ep.title,
                "name": ep.title or f"Bölüm {ep.number}",
                "season": ep.season,
                "url": ep.url
            }
            for ep in details.episodes
        ]
    }
