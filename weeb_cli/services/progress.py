from datetime import datetime
from typing import Dict, List, Optional
from weeb_cli.services._base import LazyService


class ProgressTracker(LazyService):
    
    def get_anime_progress(self, slug: str) -> Dict:
        return self.db.get_progress(slug)

    def mark_watched(self, slug: str, ep_number: int, 
                     title: Optional[str] = None, 
                     total_episodes: Optional[int] = None) -> None:
        current = self.db.get_progress(slug)
        
        completed_set = set(current.get("completed", []))
        completed_set.add(ep_number)
        completed = sorted(list(completed_set))
        
        last_watched = max(current.get("last_watched", 0), ep_number)
        
        self.db.save_progress(
            slug,
            title or current.get("title", slug),
            last_watched,
            total_episodes or current.get("total_episodes", 0),
            completed,
            datetime.now().isoformat()
        )

    def get_all_anime(self) -> Dict:
        return self.db.get_all_progress()

    def get_stats(self) -> Dict:
        data = self.db.get_all_progress()
        total_anime = len(data)
        total_episodes = sum(len(a.get("completed", [])) for a in data.values())
        total_hours = round(total_episodes * 24 / 60, 1)
        
        last_watched = None
        last_time = None
        for slug, info in data.items():
            watched_at = info.get("last_watched_at")
            if watched_at and (last_time is None or watched_at > last_time):
                last_time = watched_at
                last_watched = {"slug": slug, **info}
        
        return {
            "total_anime": total_anime,
            "total_episodes": total_episodes,
            "total_hours": total_hours,
            "last_watched": last_watched
        }

    def get_completed_anime(self) -> List[Dict]:
        data = self.db.get_all_progress()
        completed = []
        for slug, info in data.items():
            total = info.get("total_episodes", 0)
            watched = len(info.get("completed", []))
            if total > 0 and watched >= total:
                completed.append({"slug": slug, **info})
        return completed

    def get_in_progress_anime(self) -> List[Dict]:
        data = self.db.get_all_progress()
        in_progress = []
        for slug, info in data.items():
            total = info.get("total_episodes", 0)
            watched = len(info.get("completed", []))
            if watched > 0 and (total == 0 or watched < total):
                in_progress.append({"slug": slug, **info})
        return sorted(in_progress, key=lambda x: x.get("last_watched_at") or "", reverse=True)

    def add_search_history(self, query: str) -> None:
        self.db.add_search_history(query)

    def get_search_history(self) -> List[str]:
        return self.db.get_search_history()


progress_tracker = ProgressTracker()

