"""Aria2 download strategy."""

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


class Aria2Strategy(DownloadStrategy):
    """Download strategy using Aria2 for multi-connection downloads."""
    
    def __init__(self):
        self._active_processes = {}
        self._lock = threading.Lock()
    
    def can_handle(self, url: str) -> bool:
        """Aria2 handles non-HLS streams when available."""
        if not config.get(ConfigKey.ARIA2_ENABLED.value, True):
            return False
        if not dependency_manager.check_dependency("aria2"):
            return False
        return ".m3u8" not in url
    
    def download(self, context: DownloadContext) -> None:
        """Download using Aria2 with multi-connection support."""
        aria2 = dependency_manager.check_dependency("aria2")
        if not aria2:
            raise DownloadError("Aria2 not available", code="ARIA2_NOT_FOUND")
        
        path = Path(context.output_path)
        conn = config.get(ConfigKey.ARIA2_MAX_CONNECTIONS.value, 16)
        
        cmd = [
            aria2,
            context.url,
            "-d", str(path.parent),
            "-o", path.name,
            "-x", str(conn),
            "-s", str(conn),
            "-j", "1",
            "-c",
            "--summary-interval=2",
            "--console-log-level=warn"
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
            raise DownloadError("Aria2 download failed", code="ARIA2_FAILED")
    
    def _monitor_progress(self, process, item):
        """Monitor Aria2 progress output."""
        if not item:
            process.wait()
            return
        
        from weeb_cli.services.database import db
        
        while True:
            line = process.stdout.readline()
            if not line and process.poll() is not None:
                break
            
            if line and "ETA:" in line:
                try:
                    parts = line.split("ETA:")
                    eta_part = parts[1].split("]")[0].strip()
                    
                    match = re.search(r'\((\d+)%\)', line)
                    progress = int(match.group(1)) if match else None
                    
                    speed = None
                    speed_match = re.search(r'DL:([\d.]+[KMG]?i?B)', line)
                    if speed_match:
                        speed = speed_match.group(1) + "/s"
                    
                    updates = {}
                    if progress is not None:
                        updates["progress"] = progress
                    if eta_part:
                        updates["eta"] = eta_part
                    if speed:
                        updates["speed"] = speed
                    
                    if updates:
                        db.update_queue_item(item["episode_id"], **updates)
                except Exception:
                    pass
    
    def get_priority(self) -> int:
        """Aria2 has highest priority for non-HLS streams."""
        return 10
