from weeb_cli.services.scraper import scraper

def search(query):
    """Anime ara - AnimeResult listesi döndürür"""
    results = scraper.search(query)
    # Eski format uyumluluğu için dict'e çevir
    return [
        {
            "id": r.id,
            "title": r.title,
            "name": r.title,  # eski uyumluluk
            "slug": r.id,     # eski uyumluluk
            "type": r.type,
            "cover": r.cover,
            "year": r.year
        }
        for r in results
    ]
