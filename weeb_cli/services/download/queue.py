"""Download queue management."""

import time
import threading
import shutil
from pathlib import Path

from weeb_cli.config import config
from weeb_cli.constants import ConfigKey, DownloadStatus
from weeb_cli.services.download.manager import DownloadManager
from weeb_cli.utils.sanitizer import sanitize_filename
from weeb_cli.exceptions import DownloadError
from weeb_cli.services.logger import debug, error as log_error
from weeb_cli.i18n import i18n


class QueueManager:
    """Manages download queue with concurrent workers."""
    
    def __init__(self):
        self._db = None
        self.lock = threading.Lock()
        self.running = False
        self.worker_thread = None
        self.download_manager = DownloadManager()
    
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
        """Start processing the download queue."""
        if self.running:
            return
        self.running = True
        if self.worker_thread is None or not self.worker_thread.is_alive():
            self.worker_thread = threading.Thread(target=self._manage_queue, daemon=True)
            self.worker_thread.start()
    
    def stop_queue(self):
        """Stop processing the download queue."""
        self.running = False
    
    def is_running(self):
        """Check if queue is currently running."""
        return self.running and self.worker_thread is not None and self.worker_thread.is_alive()
    
    def has_incomplete_downloads(self):
        """Check if there are incomplete downloads."""
        return any(
            item["status"] in [DownloadStatus.PENDING.value, DownloadStatus.PROCESSING.value]
            for item in self.queue
        )
    
    def get_incomplete_count(self):
        """Get count of incomplete downloads."""
        return len([
            item for item in self.queue
            if item["status"] in [DownloadStatus.PENDING.value, DownloadStatus.PROCESSING.value]
        ])
    
    def get_pending_count(self):
        """Get count of pending downloads."""
        return len([item for item in self.queue if item["status"] == DownloadStatus.PENDING.value])
    
    def resume_incomplete(self):
        """Resume incomplete downloads."""
        for item in self.queue:
            if item["status"] == DownloadStatus.PROCESSING.value:
                self.db.update_queue_item(item["episode_id"], status=DownloadStatus.PENDING.value)
        self.start_queue()
    
    def cancel_incomplete(self):
        """Cancel all incomplete downloads."""
        self.db.clear_completed_queue()
        for item in self.queue:
            if item["status"] in [DownloadStatus.PENDING.value, DownloadStatus.PROCESSING.value]:
                self.db.update_queue_item(item["episode_id"], status=DownloadStatus.CANCELLED.value)
    
    def retry_failed(self):
        """Retry all failed downloads."""
        count = 0
        for item in self.queue:
            if item["status"] == DownloadStatus.FAILED.value:
                self.db.update_queue_item(
                    item["episode_id"],
                    status=DownloadStatus.PENDING.value,
                    progress=0,
                    error="",
                    eta="?"
                )
                count += 1
        if count > 0:
            self.start_queue()
        return count
    
    def get_failed_count(self):
        """Get count of failed downloads."""
        return len([item for item in self.queue if item["status"] == DownloadStatus.FAILED.value])
    
    def get_active_count(self):
        """Get count of active downloads."""
        return len([item for item in self.queue if item["status"] == DownloadStatus.PROCESSING.value])
    
    def is_downloading(self, slug, episode_id=None):
        """Check if anime/episode is currently downloading."""
        for item in self.queue:
            if item["slug"] == slug and item["status"] in [DownloadStatus.PENDING.value, DownloadStatus.PROCESSING.value]:
                if episode_id is None or item["episode_id"] == episode_id:
                    return True
        return False
    
    def add_to_queue(self, anime_title, episodes, slug):
        """Add episodes to download queue."""
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
                    "status": DownloadStatus.PENDING.value,
                    "added_at": time.time(),
                    "progress": 0,
                    "eta": "?"
                }
                if self.db.add_to_queue(item):
                    added += 1
        return added
    
    def clear_completed(self):
        """Clear completed downloads from queue."""
        self.db.clear_completed_queue()
    
    def _manage_queue(self):
        """Manage download queue with safety limits."""
        max_iterations = 86400
        iteration = 0
        
        while self.running and iteration < max_iterations:
            iteration += 1
            max_workers = config.get(ConfigKey.MAX_CONCURRENT_DOWNLOADS.value, 3)
            
            queue = self.queue
            active_count = len([x for x in queue if x["status"] == DownloadStatus.PROCESSING.value])
            pending = [x for x in queue if x["status"] == DownloadStatus.PENDING.value]
            
            if active_count < max_workers and pending:
                to_start = pending[0]
                self.db.update_queue_item(to_start["episode_id"], status=DownloadStatus.PROCESSING.value)
                
                t = threading.Thread(target=self._run_task, args=(to_start,), daemon=True)
                t.start()
            
            if not pending and active_count == 0:
                self.running = False
                break
            
            time.sleep(1)
        
        if iteration >= max_iterations:
            log_error("Download queue manager reached max iterations, stopping for safety")
    
    def _run_task(self, item):
        """Execute a download task with retry logic."""
        from weeb_cli.services.notifier import send_notification
        from weeb_cli.services.error_handler import handle_download_error
        
        max_retries = config.get(ConfigKey.DOWNLOAD_MAX_RETRIES.value, 3)
        base_delay = config.get(ConfigKey.DOWNLOAD_RETRY_DELAY.value, 10)
        
        debug(f"Starting download: {item['anime_title']} - Ep {item['episode_number']}")
        
        if not self._check_disk_space():
            error_msg = i18n.t("downloads.disk_full", free="<1GB")
            self.db.update_queue_item(item["episode_id"], status=DownloadStatus.FAILED.value, error=error_msg, eta="")
            send_notification(i18n.t("common.error"), f"{item['anime_title']}: {error_msg}")
            return
        
        for attempt in range(max_retries):
            try:
                if attempt > 0:
                    delay = self._calculate_backoff(attempt, base_delay)
                    debug(f"Retry attempt {attempt + 1}/{max_retries} after {delay}s")
                    retry_msg = i18n.t("downloads.retrying_status", attempt=attempt + 1, max=max_retries)
                    self.db.update_queue_item(item["episode_id"], eta=retry_msg)
                    time.sleep(delay)
                
                self._download_item(item)
                self.db.update_queue_item(
                    item["episode_id"],
                    status=DownloadStatus.COMPLETED.value,
                    progress=100,
                    eta="-",
                    retry_count=0
                )
                
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
                        debug("Permanent error detected, skipping retries")
                        break
                    continue
                
                self.db.update_queue_item(
                    item["episode_id"],
                    status=DownloadStatus.FAILED.value,
                    error=str(e),
                    eta="",
                    retry_count=attempt + 1
                )
                debug(f"Download failed after {max_retries} attempts: {item['anime_title']}")
    
    def _check_disk_space(self):
        """Check if there's enough disk space."""
        try:
            download_dir = config.get(ConfigKey.DOWNLOAD_DIR.value)
            total, used, free = shutil.disk_usage(download_dir)
            min_free_space = 1024 * 1024 * 1024
            
            if free < min_free_space:
                free_gb = free / (1024 * 1024 * 1024)
                debug(f"Insufficient disk space: {free_gb:.2f}GB free, need at least 1GB")
                return False
            return True
        except Exception as e:
            debug(f"Disk space check failed: {e}")
            return True
    
    def _calculate_backoff(self, attempt: int, base_delay: int) -> int:
        """Calculate exponential backoff with jitter."""
        import random
        delay = min(base_delay * (2 ** attempt), 300)
        jitter = random.uniform(0, delay * 0.1)
        return int(delay + jitter)
    
    def _classify_error(self, error: Exception) -> str:
        """Classify error as transient or permanent."""
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
        """Download a single item from the queue."""
        from weeb_cli.services.watch import get_streams
        from weeb_cli.services.scraper import scraper
        from weeb_cli.services.stream_validator import stream_validator
        
        download_dir = Path(config.get(ConfigKey.DOWNLOAD_DIR.value))
        safe_title = sanitize_filename(item["anime_title"])
        anime_dir = download_dir / safe_title
        anime_dir.mkdir(parents=True, exist_ok=True)
        
        ep_num = item["episode_number"]
        season = item.get("season", 1)
        filename = f"{safe_title} - S{season}E{ep_num}.mp4"
        output_path = anime_dir / filename
        
        stream_data = get_streams(item["slug"], item["episode_id"])
        
        if not stream_data:
            err_msg = i18n.t("downloads.stream_data_failed")
            if scraper.last_error:
                err_msg = f"{err_msg}: {scraper.last_error}"
            log_error(f"Download failed - {err_msg}")
            raise DownloadError(err_msg, code="NO_STREAM_DATA")
        
        if isinstance(stream_data, dict) and "data" in stream_data and "links" in stream_data["data"]:
            links = stream_data["data"]["links"]
            if not links:
                raise DownloadError(i18n.t("downloads.empty_stream_links"), code="EMPTY_STREAM_LINKS")
            
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
                raise DownloadError(i18n.t("downloads.no_valid_streams_found"), code="NO_VALID_STREAMS")
            
            debug(f"Found {len(valid_links)}/{len(links)} valid streams, trying each one...")
            
            valid_links.sort(key=self._link_quality_score, reverse=True)
            
            last_error = None
            for idx, link in enumerate(valid_links):
                stream_url = link.get("url")
                server_name = link.get("server", "unknown")
                
                if not stream_url:
                    continue
                
                debug(f"Trying source {idx + 1}/{len(valid_links)}: {server_name}")
                
                try:
                    self.download_manager.download(stream_url, str(output_path), item)
                    debug(f"Download successful with source: {server_name}")
                    return
                except Exception as e:
                    last_error = str(e)
                    log_error(f"Source {server_name} failed: {e}")
                    if idx < len(valid_links) - 1:
                        debug("Trying next source...")
                        continue
            
            raise DownloadError(f"All sources failed. Last error: {last_error}", code="ALL_SOURCES_FAILED")
        
        stream_url = self._extract_url(stream_data)
        
        if not stream_url:
            log_error(f"Download failed - {i18n.t('downloads.no_stream_url')}")
            raise DownloadError(i18n.t("downloads.no_stream_url"), code="NO_STREAM_URL")
        
        debug(f"Stream URL found: {stream_url[:80]}...")
        self.download_manager.download(stream_url, str(output_path), item)
    
    def _link_quality_score(self, link):
        """Calculate quality score for link sorting."""
        q = (link.get("quality") or "").lower()
        if "4k" in q or "2160" in q:
            return 5
        if "1080" in q:
            return 4
        if "720" in q:
            return 3
        if "480" in q:
            return 2
        if "360" in q:
            return 1
        return 0
    
    def _extract_url(self, data):
        """Extract URL from stream data."""
        urls = self._extract_all_urls(data)
        return urls[0][0] if urls else None
    
    def _extract_all_urls(self, data):
        """Extract all URLs from stream data with priority."""
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


queue_manager = QueueManager()
