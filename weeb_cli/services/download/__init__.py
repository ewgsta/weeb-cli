"""Download service with strategy-based architecture.

This package provides a modular download system with multiple strategies
for different download methods (Aria2, yt-dlp, FFmpeg, generic HTTP).
"""

from weeb_cli.services.download.manager import DownloadManager
from weeb_cli.services.download.queue import QueueManager, queue_manager

__all__ = ['DownloadManager', 'QueueManager', 'queue_manager']
