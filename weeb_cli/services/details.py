from typing import Optional, Dict
from weeb_cli.services.scraper import scraper
from weeb_cli.services.cache import get_cache
from weeb_cli.config import config


def get_details(anime_id: str) -> Optional[Dict]:
    cache = get_cache()
    provider = config.get("scraping_source", "None")
    cache_key = f"details:{provider}:{anime_id}"
    
    cached = cache.get(cache_key, max_age=3600)
    if cached:
        return cached
    
    details = scraper.get_details(anime_id)
    if not details:
        return None
    
    result = {
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
    
    cache.set(cache_key, result)
    return result
