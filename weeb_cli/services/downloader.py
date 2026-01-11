import os
import json
import re
import threading
import time
import subprocess
from pathlib import Path
from rich.console import Console
from weeb_cli.config import config
from weeb_cli.services.dependency_manager import dependency_manager

console = Console()

class QueueManager:
    def __init__(self):
        self.config_dir = Path.home() / ".weeb-cli"
        self.queue_file = self.config_dir / "download_queue.json"
        self.queue = []
        self._load_queue()
        
        self.worker_thread = threading.Thread(target=self._process_queue, daemon=True)
        self.worker_thread.start()

    def _load_queue(self):
        if self.queue_file.exists():
            try:
                with open(self.queue_file, 'r', encoding='utf-8') as f:
                    self.queue = json.load(f)
            except:
                self.queue = []

    def _save_queue(self):
        with open(self.queue_file, 'w', encoding='utf-8') as f:
            json.dump(self.queue, f, indent=2, ensure_ascii=False)

    def add_to_queue(self, anime_title, episodes, slug):
        for ep in episodes:
            item = {
                "anime_title": anime_title,
                "episode_number": ep.get("number") or ep.get("ep_num"),
                "episode_id": ep.get("id"),
                "slug": slug,
                "status": "pending",
                "added_at": time.time()
            }
            if not any(x['episode_id'] == item['episode_id'] for x in self.queue):
                self.queue.append(item)
        self._save_queue()

    def _sanitize_filename(self, name):
        return re.sub(r'[<>:"/\\|?*]', '', name).strip()

    def _process_queue(self):
        while True:
            pending = [item for item in self.queue if item["status"] == "pending"]
            if not pending:
                time.sleep(2)
                continue

            item = pending[0]
            item["status"] = "processing"
            self._save_queue() 
            
            try:
                self._download_item(item)
                item["status"] = "completed"
            except Exception as e:
                item["status"] = "failed"
                item["error"] = str(e)
            
            self._save_queue()
            
    def _download_item(self, item):
        from weeb_cli.services.watch import get_streams
        
        download_dir = Path(config.get("download_dir"))
        safe_title = self._sanitize_filename(item["anime_title"])
        anime_dir = download_dir / safe_title
        anime_dir.mkdir(parents=True, exist_ok=True)
        ep_num = item["episode_number"]
        filename = f"{safe_title} - S1B{ep_num}.mp4" 
        output_path = anime_dir / filename

        stream_data = get_streams(item["slug"], item["episode_id"])
        if not stream_data: 
            raise Exception("No stream data")

        stream_url = self._extract_url(stream_data)
        if not stream_url:
            raise Exception("No stream URL")

        is_hls = ".m3u8" in stream_url
        
        if is_hls:
            if config.get("ytdlp_enabled") and dependency_manager.check_dependency("yt-dlp"):
                self._download_ytdlp(stream_url, output_path)
            else:
                self._download_ffmpeg(stream_url, output_path)
        else:
            if config.get("aria2_enabled") and dependency_manager.check_dependency("aria2"):
                self._download_aria2(stream_url, output_path)
            else:
                self._download_generic(stream_url, output_path)

    def _extract_url(self, data):
        if isinstance(data, dict):
             node = data
             for _ in range(3):
                 if "data" in node and isinstance(node["data"], (dict, list)):
                     node = node["data"]
                 else: break
             
             sources = node if isinstance(node, list) else node.get("sources") or node.get("links")
             if sources and isinstance(sources, list) and len(sources) > 0:
                 return sources[0].get("url")
             elif isinstance(node, dict) and "url" in node:
                 return node["url"]
        return None

    def _download_aria2(self, url, path):
        aria2 = dependency_manager.check_dependency("aria2")
        conn = config.get("aria2_max_connections", 16)
        cmd = [
            aria2, 
            url, 
            "-d", str(path.parent), 
            "-o", path.name,
            "-x", str(conn),
            "-s", str(conn),
            "-j", "1"
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) 

    def _download_ytdlp(self, url, path):
        ytdlp = dependency_manager.check_dependency("yt-dlp")
        fmt = config.get("ytdlp_format", "best")
        cmd = [
            ytdlp, 
            "-f", fmt,
            "-o", str(path),
            "--no-part", 
            url
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def _download_ffmpeg(self, url, path):
        ffmpeg = dependency_manager.check_dependency("ffmpeg")
        cmd = [
            ffmpeg,
            "-i", url,
            "-c", "copy",
            "-bsf:a", "aac_adtstoasc",
            str(path),
            "-y"
        ]
        subprocess.run(cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

    def _download_generic(self, url, path):
        import requests
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(path, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)

queue_manager = QueueManager()
