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
        self.active_downloads = 0
        self.lock = threading.Lock()
        self._load_queue()
        
        self.worker_thread = threading.Thread(target=self._manage_queue, daemon=True)
        self.worker_thread.start()

    def _load_queue(self):
        if self.queue_file.exists():
            try:
                with open(self.queue_file, 'r', encoding='utf-8') as f:
                    self.queue = json.load(f)
                    for item in self.queue:
                        if item["status"] == "processing":
                            item["status"] = "pending"
            except:
                self.queue = []

    def _save_queue(self):
        with self.lock:
             with open(self.queue_file, 'w', encoding='utf-8') as f:
                json.dump(self.queue, f, indent=2, ensure_ascii=False)

    def add_to_queue(self, anime_title, episodes, slug):
        with self.lock:
            for ep in episodes:
                item = {
                    "anime_title": anime_title,
                    "episode_number": ep.get("number") or ep.get("ep_num"),
                    "episode_id": ep.get("id"),
                    "slug": slug,
                    "status": "pending",
                    "added_at": time.time(),
                    "progress": 0,
                    "eta": "?"
                }
                if not any(x['episode_id'] == item['episode_id'] for x in self.queue):
                    self.queue.append(item)
        self._save_queue()

    def _sanitize_filename(self, name):
        return re.sub(r'[<>:"/\\|?*]', '', name).strip()

    def _manage_queue(self):
        while True:
            max_workers = config.get("max_concurrent_downloads", 3)
            
            with self.lock:
                active_count = len([x for x in self.queue if x["status"] == "processing"])
                pending = [x for x in self.queue if x["status"] == "pending"]

            if active_count < max_workers and pending:
                to_start = pending[0]
                to_start["status"] = "processing"
                self._save_queue()
                
                t = threading.Thread(target=self._run_task, args=(to_start,))
                t.start()
            
            time.sleep(1)

    def _run_task(self, item):
        try:
            self._download_item(item)
            item["status"] = "completed"
            item["progress"] = 100
            item["eta"] = "-"
        except Exception as e:
            item["status"] = "failed"
            item["error"] = str(e)
            item["eta"] = "Error"
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
                self._download_ytdlp(stream_url, output_path, item)
            else:
                self._download_ffmpeg(stream_url, output_path, item)
        else:
            if config.get("aria2_enabled") and dependency_manager.check_dependency("aria2"):
                self._download_aria2(stream_url, output_path, item)
            else:
                self._download_generic(stream_url, output_path, item)

    def _extract_url(self, data):
        if isinstance(data, dict):
             node = data
             for _ in range(3):
                 if "data" in node and isinstance(node["data"], (dict, list)):
                     node = node["data"]
                 else: break
             
             sources = node if isinstance(node, list) else node.get("links") or node.get("sources")
             if sources and isinstance(sources, list) and len(sources) > 0:
                 return sources[0].get("url")
             elif isinstance(node, dict) and "url" in node:
                 return node["url"]
        return None

    def _download_aria2(self, url, path, item):
        aria2 = dependency_manager.check_dependency("aria2")
        conn = config.get("aria2_max_connections", 16)
        cmd = [
            aria2, 
            url, 
            "-d", str(path.parent), 
            "-o", path.name,
            "-x", str(conn),
            "-s", str(conn),
            "-j", "1",
            "--summary-interval=2",
            "--console-log-level=warn" 
        ]
        
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='utf-8', errors='replace')
        
        while True:
            line = process.stdout.readline()
            if not line and process.poll() is not None:
                break
            if line:
                 if "ETA:" in line:
                     try:
                         parts = line.split("ETA:")
                         eta_part = parts[1].split("]")[0]
                         item["eta"] = eta_part.strip()
                         
                         match = re.search(r'\((\d+)%\)', line)
                         if match:
                              item["progress"] = int(match.group(1))
                     except: pass
        
        if process.returncode != 0:
            raise Exception("Aria2 failed")

    def _download_ytdlp(self, url, path, item):
        ytdlp = dependency_manager.check_dependency("yt-dlp")
        fmt = config.get("ytdlp_format", "best")
        cmd = [
            ytdlp, 
            "-f", fmt,
            "-o", str(path),
            "--no-part", 
            "--newline",
            url
        ]
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding='utf-8', errors='replace')
        while True:
            line = process.stdout.readline()
            if not line and process.poll() is not None:
                break
            if line:
                if "[download]" in line and "%" in line:
                    try:
                        p_str = line.split("%")[0].split()[-1]
                        item["progress"] = float(p_str)
                        if "ETA" in line:
                            item["eta"] = line.split("ETA")[-1].strip()
                    except: pass
        if process.returncode != 0:
             raise Exception("yt-dlp failed")

    def _download_ffmpeg(self, url, path, item):
        item["eta"] = "N/A"
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

    def _download_generic(self, url, path, item):
        import requests
        item["eta"] = "..."
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            total = int(r.headers.get('content-length', 0))
            if total > 0:
                downloaded = 0
                start_time = time.time()
                with open(path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
                        downloaded += len(chunk)
                        item["progress"] = int((downloaded / total) * 100)
                        
                        elapsed = time.time() - start_time
                        if elapsed > 0:
                            speed = downloaded / elapsed
                            remaining = total - downloaded
                            eta_s = remaining / speed
                            item["eta"] = f"{int(eta_s)}s"
            else:
                 with open(path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)

queue_manager = QueueManager()
