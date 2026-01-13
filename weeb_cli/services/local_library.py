import os
import re
from pathlib import Path
from typing import List, Dict, Optional
from weeb_cli.config import config
from weeb_cli.services.progress import progress_tracker

class LocalLibrary:
    def __init__(self):
        self.download_dir = Path(config.get("download_dir"))
    
    def refresh(self):
        self.download_dir = Path(config.get("download_dir"))
    
    def scan_library(self) -> List[Dict]:
        self.refresh()
        
        if not self.download_dir.exists():
            return []
        
        anime_list = []
        
        for anime_folder in self.download_dir.iterdir():
            if not anime_folder.is_dir():
                continue
            
            episodes = self._scan_anime_folder(anime_folder)
            if episodes:
                anime_list.append({
                    "title": anime_folder.name,
                    "path": str(anime_folder),
                    "episodes": episodes,
                    "episode_count": len(episodes)
                })
        
        return sorted(anime_list, key=lambda x: x["title"].lower())
    
    def _scan_anime_folder(self, folder: Path) -> List[Dict]:
        episodes = []
        video_extensions = {'.mp4', '.mkv', '.avi', '.webm', '.m4v'}
        
        for file in folder.iterdir():
            if file.is_file() and file.suffix.lower() in video_extensions:
                ep_num = self._extract_episode_number(file.name)
                episodes.append({
                    "filename": file.name,
                    "path": str(file),
                    "number": ep_num,
                    "size": file.stat().st_size
                })
        
        return sorted(episodes, key=lambda x: x["number"])
    
    def _extract_episode_number(self, filename: str) -> int:
        patterns = [
            r'S\d+B(\d+)',
            r'[Ee]p?(\d+)',
            r'[Bb]ölüm\s*(\d+)',
            r'[Ee]pisode\s*(\d+)',
            r'- (\d+)',
            r'\[(\d+)\]',
            r'(\d+)\.',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, filename, re.IGNORECASE)
            if match:
                return int(match.group(1))
        
        return 0
    
    def get_anime_progress(self, anime_title: str) -> Dict:
        slug = self._title_to_slug(anime_title)
        return progress_tracker.get_anime_progress(slug)
    
    def mark_episode_watched(self, anime_title: str, ep_number: int, total_episodes: int):
        slug = self._title_to_slug(anime_title)
        progress_tracker.mark_watched(slug, ep_number, title=anime_title, total_episodes=total_episodes)
    
    def _title_to_slug(self, title: str) -> str:
        slug = title.lower()
        slug = re.sub(r'[^a-z0-9\s-]', '', slug)
        slug = re.sub(r'\s+', '-', slug)
        return slug
    
    def get_next_episode(self, anime_title: str, episodes: List[Dict]) -> Optional[Dict]:
        progress = self.get_anime_progress(anime_title)
        last_watched = progress.get("last_watched", 0)
        
        for ep in episodes:
            if ep["number"] > last_watched:
                return ep
        
        return episodes[0] if episodes else None
    
    def format_size(self, size_bytes: int) -> str:
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024
        return f"{size_bytes:.1f} TB"

local_library = LocalLibrary()
