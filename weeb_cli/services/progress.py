import json
import os
from pathlib import Path
from rich.console import Console
from weeb_cli.config import config

console = Console()

class ProgressTracker:
    def __init__(self):
        self.config_dir = Path.home() / ".weeb-cli"
        self.progress_file = self.config_dir / "progress.json"
        self._ensure_file()

    def _ensure_file(self):
        if not self.progress_file.exists():
            self.progress_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.progress_file, 'w') as f:
                json.dump({}, f)

    def load_progress(self):
        try:
            with open(self.progress_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}

    def save_progress(self, data):
        with open(self.progress_file, 'w') as f:
            json.dump(data, f, indent=2)

    def get_anime_progress(self, slug):
        data = self.load_progress()
        return data.get(slug, {
            "last_watched": 0,
            "completed": []
        })

    def mark_watched(self, slug, ep_number):
        data = self.load_progress()
        if slug not in data:
            data[slug] = {"last_watched": 0, "completed": []}
        
        # Add to completed list
        completed_set = set(data[slug].get("completed", []))
        completed_set.add(ep_number)
        data[slug]["completed"] = list(completed_set)
        
        # Update last watched if greater
        if ep_number > data[slug].get("last_watched", 0):
             data[slug]["last_watched"] = ep_number
             
        self.save_progress(data)

    def get_next_episode(self, slug):
        prog = self.get_anime_progress(slug)
        last = prog.get("last_watched", 0)
        # If last is 0, start at 1. If 6, next is 7.
        # But we should check if 7 is completed? (maybe skipped around)
        # For simplicity, next is last + 1.
        return last + 1

progress_tracker = ProgressTracker()
