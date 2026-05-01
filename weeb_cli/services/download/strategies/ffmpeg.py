"""FFmpeg download strategy."""

import subprocess
import threading
from pathlib import Path

from weeb_cli.i18n import i18n
from weeb_cli.services.download.strategies.base import DownloadStrategy
from weeb_cli.services.download.context import DownloadContext
from weeb_cli.services.dependency_manager import dependency_manager
from weeb_cli.exceptions import DownloadError


class FFmpegStrategy(DownloadStrategy):
    """Download strategy using FFmpeg for HLS streams (fallback)."""
    
    def __init__(self):
        self._active_processes = {}
        self._lock = threading.Lock()
    
    def can_handle(self, url: str) -> bool:
        """FFmpeg handles HLS streams as fallback."""
        if not dependency_manager.check_dependency("ffmpeg"):
            return False
        return ".m3u8" in url
    
    def download(self, context: DownloadContext) -> None:
        """Download using FFmpeg."""
        ffmpeg = dependency_manager.check_dependency("ffmpeg")
        if not ffmpeg:
            raise DownloadError("FFmpeg not available", code="FFMPEG_NOT_FOUND")
        
        item = context.item
        if item:
            from weeb_cli.services.database import db
            db.update_queue_item(item["episode_id"], eta="...")
        
        cmd = [
            ffmpeg,
            "-i", context.url,
            "-c", "copy",
            "-bsf:a", "aac_adtstoasc",
            "-y",
            "-progress", "pipe:1",
            str(context.output_path)
        ]
        
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL,
            text=True,
            encoding='utf-8',
            errors='replace'
        )
        
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
            raise DownloadError("FFmpeg download failed", code="FFMPEG_FAILED")
    
    def _monitor_progress(self, process, item):
        """Monitor FFmpeg progress output."""
        if not item:
            process.wait()
            return
        
        from weeb_cli.services.database import db
        
        while True:
            line = process.stdout.readline()
            if not line and process.poll() is not None:
                break
            
            if line and "out_time=" in line:
                time_str = line.split("out_time=")[1].strip()
                eta_msg = i18n.t("downloads.ffmpeg_progress", time=time_str[:8])
                db.update_queue_item(item["episode_id"], eta=eta_msg)
    
    def get_priority(self) -> int:
        """FFmpeg has lower priority than yt-dlp for HLS."""
        return 20
