"""Download manager with strategy pattern."""

import time as _time
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
from weeb_cli.services.telemetry import get_tracer, get_metrics, record_exception


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
        tracer = get_tracer()
        m = get_metrics()
        start = _time.monotonic()

        with tracer.start_as_current_span("download", attributes={
            "weeb.download.url_prefix": url[:80],
            "weeb.download.output": output_path,
        }) as span:
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
                    duration = _time.monotonic() - start
                    span.set_attribute("weeb.download.strategy", strategy_name)
                    m.download_duration.record(duration, {"weeb.download.strategy": strategy_name, "weeb.download.status": "success"})
                    m.download_status.add(1, {"status": "success"})
                    return
                except Exception as e:
                    last_error = e
                    debug(f"[DownloadManager] {strategy_name} failed: {e}")
                    continue

            duration = _time.monotonic() - start
            m.download_duration.record(duration, {"weeb.download.status": "failed"})
            m.download_status.add(1, {"status": "failed"})

            error_msg = f"All download strategies failed. Last error: {last_error}"
            err = DownloadError(error_msg, code="ALL_STRATEGIES_FAILED")
            record_exception(span, err)
            raise err
