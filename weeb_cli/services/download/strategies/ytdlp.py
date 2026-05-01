"""yt-dlp download strategy."""

import re
import subprocess
import threading
from pathlib import Path

from weeb_cli.config import config
from weeb_cli.constants import ConfigKey
from weeb_cli.services.download.strategies.base import DownloadStrategy
from weeb_cli.services.download.context import DownloadContext
from weeb_cli.services.dependency_manager import dependency_manager
from weeb_cli.exceptions import DownloadError


class YtdlpStrategy(DownloadStrategy):
    """Download strategy using yt-dlp for HLS streams."""
    
    def __init__(self):
        self._active_processes = {}
        self._lock = threading.Lock()
    
    def can_handle(self, url: str) -> bool:
        """yt-dlp handles HLS streams when available."""
        if not config.get(ConfigKey.YTDLP_ENABLED.value, True):
            return False
        if not dependency_manager.check_dependency("yt-dlp"):
            return False
        return ".m3u8" in url
    
    def download(self, context: DownloadContext) -> None:
        """Download using yt-dlp."""
        ytdlp = dependency_manager.check_dependency("yt-dlp")
        if not ytdlp:
            raise DownloadError("yt-dlp not available", code="YTDLP_NOT_FOUND")
        
        fmt = config.get(ConfigKey.YTDLP_FORMAT.value, "best")
        
        cmd = [
            ytdlp,
            "-f", fmt,
            "-o", str(context.output_path),
            "--no-part",
            "--newline",
            context.url
        ]
        
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            encoding='utf-8',
            errors='replace'
        )
        
        item = context.item
        if item:
            with self._lock:
                self._active_processes[item["episode_id"]] = process
        
        try:
            self._monitor_progress(process, item)
        finally:
            if item:
                with self._lock:
                    self._active_processes.pop(item["episode_id"], None)
        
        if process.returncode != 0:
            raise DownloadError("yt-dlp download failed", code="YTDLP_FAILED")
    
    def _monitor_progress(self, process, item):
        """Monitor yt-dlp progress output."""
        if not item:
            process.wait()
            return
        
        from weeb_cli.services.database import db
        
        while True:
            line = process.stdout.readline()
            if not line and process.poll() is not None:
                break
            
            if line and "[download]" in line and "%" in line:
                try:
                    p_str = line.split("%")[0].split()[-1]
                    progress = float(p_str)
                    eta = line.split("ETA")[-1].strip() if "ETA" in line else None
                    
                    speed = None
                    speed_match = re.search(r'at\s+([\d.]+[KMG]?i?B/s)', line)
                    if speed_match:
                        speed = speed_match.group(1)
                    
                    updates = {"progress": progress}
                    if eta:
                        updates["eta"] = eta
                    if speed:
                        updates["speed"] = speed
                    
                    db.update_queue_item(item["episode_id"], **updates)
                except Exception:
                    pass
    
    def get_priority(self) -> int:
        """yt-dlp has highest priority for HLS streams."""
        return 10
