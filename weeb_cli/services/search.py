from typing import List, Dict
from weeb_cli.services.scraper import scraper


def search(query: str) -> List[Dict]:
    results = scraper.search(query)
    return [
        {
            "id": r.id,
            "title": r.title,
            "name": r.title,
            "slug": r.id,
            "type": r.type,
            "cover": r.cover,
            "year": r.year
        }
        for r in results
    ]

