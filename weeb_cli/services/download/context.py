"""Download context and data structures."""

from dataclasses import dataclass
from typing import Optional, Dict


@dataclass
class DownloadContext:
    """Context information for a download operation.
    
    Attributes:
        url: Stream URL to download.
        output_path: Full path where file should be saved.
        headers: HTTP headers to use for the request.
        item: Queue item metadata (anime title, episode number, etc.).
    """
    
    url: str
    output_path: str
    headers: Optional[Dict[str, str]] = None
    item: Optional[dict] = None
