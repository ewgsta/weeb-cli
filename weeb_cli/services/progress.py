import json
from pathlib import Path
from datetime import datetime

class ProgressTracker:
    def __init__(self):
        self.config_dir = Path.home() / ".weeb-cli"
        self.progress_file = self.config_dir / "progress.json"
        self.history_file = self.config_dir / "search_history.json"
        self._ensure_file()

    def _ensure_file(self):
        self.config_dir.mkdir(parents=True, exist_ok=True)
        if not self.progress_file.exists():
            with open(self.progress_file, 'w') as f:
                json.dump({}, f)
        if not self.history_file.exists():
            with open(self.history_file, 'w') as f:
                json.dump([], f)

    def load_progress(self):
        try:
            with open(self.progress_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}

    def save_progress(self, data):
        with open(self.progress_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)

    def get_anime_progress(self, slug):
        data = self.load_progress()
        return data.get(slug, {
            "last_watched": 0,
            "completed": [],
            "title": "",
            "total_episodes": 0,
            "last_watched_at": None
        })

    def mark_watched(self, slug, ep_number, title=None, total_episodes=None):
        data = self.load_progress()
        if slug not in data:
            data[slug] = {
                "last_watched": 0,
                "completed": [],
                "title": title or slug,
                "total_episodes": total_episodes or 0,
                "last_watched_at": None
            }
        
        completed_set = set(data[slug].get("completed", []))
        completed_set.add(ep_number)
        data[slug]["completed"] = sorted(list(completed_set))
        
        if ep_number > data[slug].get("last_watched", 0):
            data[slug]["last_watched"] = ep_number
        
        data[slug]["last_watched_at"] = datetime.now().isoformat()
        
        if title:
            data[slug]["title"] = title
        if total_episodes:
            data[slug]["total_episodes"] = total_episodes
             
        self.save_progress(data)

    def get_all_anime(self):
        return self.load_progress()

    def get_stats(self):
        data = self.load_progress()
        total_anime = len(data)
        total_episodes = sum(len(a.get("completed", [])) for a in data.values())
        total_hours = round(total_episodes * 24 / 60, 1)
        
        last_watched = None
        last_time = None
        for slug, info in data.items():
            watched_at = info.get("last_watched_at")
            if watched_at:
                if last_time is None or watched_at > last_time:
                    last_time = watched_at
                    last_watched = {"slug": slug, **info}
        
        return {
            "total_anime": total_anime,
            "total_episodes": total_episodes,
            "total_hours": total_hours,
            "last_watched": last_watched
        }

    def get_completed_anime(self):
        data = self.load_progress()
        completed = []
        for slug, info in data.items():
            total = info.get("total_episodes", 0)
            watched = len(info.get("completed", []))
            if total > 0 and watched >= total:
                completed.append({"slug": slug, **info})
        return completed

    def get_in_progress_anime(self):
        data = self.load_progress()
        in_progress = []
        for slug, info in data.items():
            total = info.get("total_episodes", 0)
            watched = len(info.get("completed", []))
            if watched > 0 and (total == 0 or watched < total):
                in_progress.append({"slug": slug, **info})
        return sorted(in_progress, key=lambda x: x.get("last_watched_at") or "", reverse=True)

    def add_search_history(self, query):
        try:
            with open(self.history_file, 'r', encoding='utf-8') as f:
                history = json.load(f)
        except:
            history = []
        
        if query in history:
            history.remove(query)
        history.insert(0, query)
        history = history[:10]
        
        with open(self.history_file, 'w', encoding='utf-8') as f:
            json.dump(history, f, ensure_ascii=False)

    def get_search_history(self):
        try:
            with open(self.history_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []

progress_tracker = ProgressTracker()
