"""Base download strategy interface."""

from abc import ABC, abstractmethod
from weeb_cli.services.download.context import DownloadContext


class DownloadStrategy(ABC):
    """Abstract base class for download strategies.
    
    Each strategy implements a specific download method (Aria2, yt-dlp, etc.)
    and can determine if it's capable of handling a given URL.
    """
    
    @abstractmethod
    def can_handle(self, url: str) -> bool:
        """Check if this strategy can handle the given URL.
        
        Args:
            url: Stream URL to check.
        
        Returns:
            True if this strategy can download from this URL.
        """
        pass
    
    @abstractmethod
    def download(self, context: DownloadContext) -> None:
        """Execute the download operation.
        
        Args:
            context: Download context with URL, output path, and metadata.
        
        Raises:
            DownloadError: If download fails.
        """
        pass
    
    @abstractmethod
    def get_priority(self) -> int:
        """Get strategy priority (lower number = higher priority).
        
        Returns:
            Priority value (0-100, where 0 is highest priority).
        """
        pass
