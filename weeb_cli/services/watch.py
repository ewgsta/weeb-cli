from weeb_cli.services.scraper import scraper

def get_streams(anime_id, episode_id):
    """Stream linklerini getir - dict döndürür"""
    streams = scraper.get_streams(anime_id, episode_id)
    if not streams:
        return None
    
    # Eski format uyumluluğu
    return {
        "data": {
            "links": [
                {
                    "url": s.url,
                    "quality": s.quality,
                    "server": s.server
                }
                for s in streams
            ]
        }
    }
