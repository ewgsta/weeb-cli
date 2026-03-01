import os
import re
import threading
import time
import subprocess
from pathlib import Path
from rich.console import Console
from weeb_cli.config import config
from weeb_cli.services.dependency_manager import dependency_manager
from weeb_cli.utils.sanitizer import sanitize_filename
from weeb_cli.exceptions import DownloadError

console = Console()

class QueueManager:
    def __init__(self):
        self._db = None
        self.lock = threading.Lock()
        self.running = False
        self.worker_thread = None
    
    @property
    def db(self):
        if self._db is None:
            from weeb_cli.services.database import db
            self._db = db
        return self._db
    
    @property
    def queue(self):
        return self.db.get_queue()

    def start_queue(self):
        if self.running:
            return
        self.running = True
        if self.worker_thread is None or not self.worker_thread.is_alive():
            self.worker_thread = threading.Thread(target=self._manage_queue, daemon=True)
            self.worker_thread.start()

    def stop_queue(self):
        self.running = False

    def is_running(self):
        return self.running and self.worker_thread is not None and self.worker_thread.is_alive()

    def has_incomplete_downloads(self):
        return any(item["status"] in ["pending", "processing"] for item in self.queue)

    def get_incomplete_count(self):
        return len([item for item in self.queue if item["status"] in ["pending", "processing"]])

    def get_pending_count(self):
        return len([item for item in self.queue if item["status"] == "pending"])

    def resume_incomplete(self):
        for item in self.queue:
            if item["status"] == "processing":
                self.db.update_queue_item(item["episode_id"], status="pending")
        self.start_queue()

    def cancel_incomplete(self):
        self.db.clear_completed_queue()
        for item in self.queue:
            if item["status"] in ["pending", "processing"]:
                self.db.update_queue_item(item["episode_id"], status="cancelled")

    def retry_failed(self):
        count = 0
        for item in self.queue:
            if item["status"] == "failed":
                self.db.update_queue_item(item["episode_id"], status="pending", progress=0, error="", eta="?")
                count += 1
        if count > 0:
            self.start_queue()
        return count

    def get_failed_count(self):
        return len([item for item in self.queue if item["status"] == "failed"])

    def get_active_count(self):
        return len([item for item in self.queue if item["status"] == "processing"])

    def is_downloading(self, slug, episode_id=None):
        for item in self.queue:
            if item["slug"] == slug and item["status"] in ["pending", "processing"]:
                if episode_id is None or item["episode_id"] == episode_id:
                    return True
        return False

    def add_to_queue(self, anime_title, episodes, slug):
        added = 0
        with self.lock:
            for ep in episodes:
                ep_id = ep.get("id")
                if self.is_downloading(slug, ep_id):
                    continue
                
                item = {
                    "anime_title": anime_title,
                    "episode_number": ep.get("number") or ep.get("ep_num"),
                    "episode_id": ep_id,
                    "slug": slug,
                    "season": ep.get("season", 1),
                    "status": "pending",
                    "added_at": time.time(),
                    "progress": 0,
                    "eta": "?"
                }
                if self.db.add_to_queue(item):
                    added += 1
        return added

    def _sanitize_filename(self, name):
        """Sanitize filename for safe file system operations."""
        return sanitize_filename(name)

    def _manage_queue(self):
        while self.running:
            max_workers = config.get("max_concurrent_downloads", 3)
            
            queue = self.queue
            active_count = len([x for x in queue if x["status"] == "processing"])
            pending = [x for x in queue if x["status"] == "pending"]

            if active_count < max_workers and pending:
                to_start = pending[0]
                self.db.update_queue_item(to_start["episode_id"], status="processing")
                
                t = threading.Thread(target=self._run_task, args=(to_start,))
                t.start()
            
            if not pending and active_count == 0:
                self.running = False
                break
            
            time.sleep(1)

    def _run_task(self, item):
        from weeb_cli.services.notifier import send_notification
        from weeb_cli.services.logger import debug
        from weeb_cli.services.error_handler import handle_download_error
        from weeb_cli.i18n import i18n
        
        max_retries = config.get("download_max_retries", 3)
        base_delay = config.get("download_retry_delay", 10)
        
        debug(f"Starting download: {item['anime_title']} - Ep {item['episode_number']}")
        
        try:
            import shutil
            download_dir = config.get("download_dir")
            total, used, free = shutil.disk_usage(download_dir)
            
            if free < 500 * 1024 * 1024:
                error_msg = i18n.t("downloads.disk_full", "Yetersiz disk alanı!")
                self.db.update_queue_item(item["episode_id"], status="failed", error=error_msg, eta="")
                send_notification(i18n.t("common.error"), f"{item['anime_title']}: {error_msg}")
                return
        except Exception as e:
            handle_download_error(e, item['anime_title'], item['episode_number'])

        for attempt in range(max_retries):
            try:
                if attempt > 0:
                    delay = self._calculate_backoff(attempt, base_delay)
                    debug(f"Retry attempt {attempt + 1}/{max_retries} after {delay}s")
                    self._update_progress(item, eta=f"Yeniden deneniyor ({attempt + 1}/{max_retries})...")
                    time.sleep(delay)
                
                self._download_item(item)
                self.db.update_queue_item(item["episode_id"], status="completed", progress=100, eta="-", retry_count=0)
                
                debug(f"Download completed: {item['anime_title']} - Ep {item['episode_number']}")
                
                title = i18n.t("downloads.notification_title", "Weeb CLI")
                msg = i18n.t("downloads.notification_complete", anime=item['anime_title'], episode=item['episode_number'])
                send_notification(title, msg)
                return
                
            except Exception as e:
                error_type = self._classify_error(e)
                handle_download_error(e, item['anime_title'], item['episode_number'])
                
                if attempt < max_retries - 1:
                    if error_type == "permanent":
                        debug(f"Permanent error detected, skipping retries")
                        break
                    continue
                
                self.db.update_queue_item(
                    item["episode_id"], 
                    status="failed", 
                    error=str(e), 
                    eta="",
                    retry_count=attempt + 1
                )
                debug(f"Download failed after {max_retries} attempts: {item['anime_title']}")
    
    def _calculate_backoff(self, attempt: int, base_delay: int) -> int:
        import random
        delay = min(base_delay * (2 ** attempt), 300)
        jitter = random.uniform(0, delay * 0.1)
        return int(delay + jitter)
    
    def _classify_error(self, error: Exception) -> str:
        error_str = str(error).lower()
        
        permanent_errors = [
            "404", "not found", "forbidden", "unauthorized",
            "invalid", "no streams", "no such file"
        ]
        
        for err in permanent_errors:
            if err in error_str:
                return "permanent"
        
        return "transient"

    def _download_item(self, item):
        from weeb_cli.services.watch import get_streams
        from weeb_cli.services.scraper import scraper
        from weeb_cli.services.logger import debug, error as log_error
        from weeb_cli.services.stream_validator import stream_validator
        
        download_dir = Path(config.get("download_dir"))
        safe_title = self._sanitize_filename(item["anime_title"])
        anime_dir = download_dir / safe_title
        anime_dir.mkdir(parents=True, exist_ok=True)

        ep_num = item["episode_number"]
        season = item.get("season", 1)
        filename = f"{safe_title} - S{season}B{ep_num}.mp4" 
        output_path = anime_dir / filename

        stream_data = get_streams(item["slug"], item["episode_id"])
        
        if not stream_data:
            err_msg = "Stream verisi alınamadı"
            if scraper.last_error:
                err_msg = f"{err_msg}: {scraper.last_error}"
            log_error(f"Download failed - {err_msg}")
            raise DownloadError(err_msg, code="NO_STREAM_DATA")

        if isinstance(stream_data, dict) and "data" in stream_data and "links" in stream_data["data"]:
            links = stream_data["data"]["links"]
            if not links:
                raise DownloadError("Stream links boş", code="EMPTY_STREAM_LINKS")
            
            debug(f"Found {len(links)} stream sources, validating...")
            
            valid_links = []
            for link in links:
                stream_url = link.get("url")
                if stream_url:
                    is_valid, error = stream_validator.validate_url(stream_url, timeout=3)
                    if is_valid:
                        valid_links.append(link)
                        debug(f"Valid: {link.get('server', 'unknown')}")
                    else:
                        debug(f"Invalid: {link.get('server', 'unknown')} - {error}")
            
            if not valid_links:
                raise DownloadError("Geçerli stream bulunamadı", code="NO_VALID_STREAMS")
            
            debug(f"Found {len(valid_links)}/{len(links)} valid streams, trying each one...")
            
            last_error = None
            for idx, link in enumerate(valid_links):
                stream_url = link.get("url")
                server_name = link.get("server", "unknown")
                
                if not stream_url:
                    continue
                
                debug(f"Trying source {idx + 1}/{len(valid_links)}: {server_name} - {stream_url[:80]}...")
                
                try:
                    self._try_download(stream_url, output_path, item)
                    debug(f"Download successful with source: {server_name}")
                    return
                    
                except Exception as e:
                    last_error = str(e)
                    log_error(f"Source {server_name} failed: {e}")
                    if idx < len(valid_links) - 1:
                        debug(f"Trying next source...")
                        continue
            
            raise DownloadError(f"Tüm kaynaklar başarısız. Son hata: {last_error}", code="ALL_SOURCES_FAILED")

        stream_url = self._extract_url(stream_data)
        
        debug(f"Extracted stream URL: {stream_url}")
        
        if not stream_url:
            log_error(f"Download failed - Stream URL bulunamadı. Data: {stream_data}")
            raise DownloadError("Stream URL bulunamadı", code="NO_STREAM_URL")

        debug(f"Stream URL found: {stream_url[:80]}...")
        
        self._try_download(stream_url, output_path, item)

    def _extract_all_urls(self, data):
        """Extract all available stream URLs with their server names."""
        PRIORITY = ["ALUCARD", "AMATERASU", "SIBNET", "MP4UPLOAD", "UQLOAD"]
        
        results = []
        
        if isinstance(data, dict):
            node = data
            for _ in range(3):
                if "data" in node and isinstance(node["data"], (dict, list)):
                    node = node["data"]
                else:
                    break
             
            sources = node if isinstance(node, list) else node.get("links") or node.get("sources")
            if sources and isinstance(sources, list) and len(sources) > 0:
                def get_priority(s):
                    server = (s.get("server") or "").upper()
                    for i, p in enumerate(PRIORITY):
                        if p in server:
                            return i
                    return 999
                
                sorted_sources = sorted(sources, key=get_priority)
                
                for src in sorted_sources:
                    url = src.get("url")
                    server = src.get("server", "unknown")
                    if url:
                        results.append((url, server))
                        
            elif isinstance(node, dict) and "url" in node:
                results.append((node["url"], node.get("server", "unknown")))
        
        return results
    
    def _try_download(self, stream_url, output_path, item):
        """Try to download from a stream URL."""
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
        PRIORITY = ["ALUCARD", "AMATERASU", "SIBNET", "MP4UPLOAD", "UQLOAD"]
        
        if isinstance(data, dict):
            node = data
            for _ in range(3):
                if "data" in node and isinstance(node["data"], (dict, list)):
                    node = node["data"]
                else:
                    break
             
            sources = node if isinstance(node, list) else node.get("links") or node.get("sources")
            if sources and isinstance(sources, list) and len(sources) > 0:
                def get_priority(s):
                    server = (s.get("server") or "").upper()
                    for i, p in enumerate(PRIORITY):
                        if p in server:
                            return i
                    return 999
                
                sorted_sources = sorted(sources, key=get_priority)
                
                for src in sorted_sources:
                    url = src.get("url")
                    if url:
                        return url
                        
            elif isinstance(node, dict) and "url" in node:
                return node["url"]
        return None

    def _update_progress(self, item, progress=None, eta=None, speed=None):
        updates = {}
        if progress is not None:
            updates["progress"] = progress
        if eta is not None:
            updates["eta"] = eta
        if speed is not None:
            updates["speed"] = speed
        if updates:
            self.db.update_queue_item(item["episode_id"], **updates)

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
            "-c",
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
                        
                        match = re.search(r'\((\d+)%\)', line)
                        progress = int(match.group(1)) if match else None
                        
                        speed = None
                        speed_match = re.search(r'DL:([\d.]+[KMG]?i?B)', line)
                        if speed_match:
                            speed = speed_match.group(1) + "/s"
                        
                        self._update_progress(item, progress=progress, eta=eta_part.strip(), speed=speed)
                    except:
                        pass
        
        if process.returncode != 0:
            raise DownloadError("Aria2 download failed", code="ARIA2_FAILED")

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
                        progress = float(p_str)
                        eta = line.split("ETA")[-1].strip() if "ETA" in line else None
                        
                        speed = None
                        speed_match = re.search(r'at\s+([\d.]+[KMG]?i?B/s)', line)
                        if speed_match:
                            speed = speed_match.group(1)
                        
                        self._update_progress(item, progress=progress, eta=eta, speed=speed)
                    except:
                        pass
        if process.returncode != 0:
            raise DownloadError("yt-dlp download failed", code="YTDLP_FAILED")

    def _download_ffmpeg(self, url, path, item):
        self._update_progress(item, eta="")
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
        self._update_progress(item, eta="...")
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
                        progress = int((downloaded / total) * 100)
                        
                        elapsed = time.time() - start_time
                        if elapsed > 0:
                            speed_bytes = downloaded / elapsed
                            remaining = total - downloaded
                            eta_s = remaining / speed_bytes if speed_bytes > 0 else 0
                            
                            if speed_bytes >= 1024 * 1024:
                                speed_str = f"{speed_bytes / (1024*1024):.1f}MB/s"
                            elif speed_bytes >= 1024:
                                speed_str = f"{speed_bytes / 1024:.1f}KB/s"
                            else:
                                speed_str = f"{speed_bytes:.0f}B/s"
                            
                            self._update_progress(item, progress=progress, eta=f"{int(eta_s)}s", speed=speed_str)
            else:
                with open(path, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)

    def clear_completed(self):
        self.db.clear_completed_queue()

queue_manager = QueueManager()
