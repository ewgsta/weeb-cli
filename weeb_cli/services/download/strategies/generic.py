"""Generic HTTP download strategy."""

import time
import requests

from weeb_cli.services.download.strategies.base import DownloadStrategy
from weeb_cli.services.download.context import DownloadContext
from weeb_cli.exceptions import DownloadError


class GenericStrategy(DownloadStrategy):
    """Generic HTTP download strategy (fallback for all URLs)."""
    
    def can_handle(self, url: str) -> bool:
        """Generic strategy handles any HTTP(S) URL."""
        return url.startswith(("http://", "https://"))
    
    def download(self, context: DownloadContext) -> None:
        """Download using requests library."""
        item = context.item
        if item:
            from weeb_cli.services.database import db
            db.update_queue_item(item["episode_id"], eta="...")
        
        headers = context.headers or {}
        
        try:
            with requests.get(context.url, stream=True, headers=headers) as r:
                r.raise_for_status()
                total = int(r.headers.get('content-length', 0))
                
                if total > 0:
                    self._download_with_progress(r, context.output_path, total, item)
                else:
                    self._download_without_progress(r, context.output_path)
        except requests.RequestException as e:
            raise DownloadError(f"HTTP download failed: {e}", code="HTTP_FAILED")
    
    def _download_with_progress(self, response, output_path, total, item):
        """Download with progress tracking."""
        downloaded = 0
        start_time = time.time()
        
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                downloaded += len(chunk)
                
                if item:
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
                        
                        from weeb_cli.services.database import db
                        db.update_queue_item(
                            item["episode_id"],
                            progress=progress,
                            eta=f"{int(eta_s)}s",
                            speed=speed_str
                        )
    
    def _download_without_progress(self, response, output_path):
        """Download without progress tracking."""
        with open(output_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
    
    def get_priority(self) -> int:
        """Generic strategy has lowest priority (last resort)."""
        return 100
