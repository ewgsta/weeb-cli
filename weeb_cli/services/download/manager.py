"""Download manager with strategy pattern."""

from typing import List
from pathlib import Path

from weeb_cli.services.download.context import DownloadContext
from weeb_cli.services.download.strategies import (
    DownloadStrategy,
    Aria2Strategy,
    YtdlpStrategy,
    FFmpegStrategy,
    GenericStrategy
)
from weeb_cli.services.logger import debug
from weeb_cli.exceptions import DownloadError


class DownloadManager:
    """Manages download operations using multiple strategies.
    
    Tries strategies in priority order until one succeeds.
    """
    
    def __init__(self):
        self.strategies: List[DownloadStrategy] = [
            Aria2Strategy(),
            YtdlpStrategy(),
            FFmpegStrategy(),
            GenericStrategy()
        ]
        self.strategies.sort(key=lambda s: s.get_priority())
    
    def download(self, url: str, output_path: str, item: dict = None) -> None:
        """Download a file using the best available strategy.
        
        Args:
            url: Stream URL to download.
            output_path: Path where file should be saved.
            item: Optional queue item metadata for progress tracking.
        
        Raises:
            DownloadError: If all strategies fail.
        """
        context = DownloadContext(
            url=url,
            output_path=output_path,
            item=item
        )
        
        last_error = None
        
        for strategy in self.strategies:
            if not strategy.can_handle(url):
                continue
            
            strategy_name = strategy.__class__.__name__
            debug(f"[DownloadManager] Trying {strategy_name} for {url[:80]}...")
            
            try:
                strategy.download(context)
                debug(f"[DownloadManager] Success with {strategy_name}")
                return
            except Exception as e:
                last_error = e
                debug(f"[DownloadManager] {strategy_name} failed: {e}")
                continue
        
        error_msg = f"All download strategies failed. Last error: {last_error}"
        raise DownloadError(error_msg, code="ALL_STRATEGIES_FAILED")
