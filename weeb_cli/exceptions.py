"""Custom exceptions for Weeb CLI.

This module defines the exception hierarchy for error handling throughout
the application. All exceptions inherit from WeebCLIError base class.

Exception Hierarchy:
    WeebCLIError (base)
    ├── ProviderError: Anime provider-related errors
    ├── DownloadError: Download operation failures
    ├── NetworkError: Network connectivity issues
    ├── AuthenticationError: Tracker authentication failures
    ├── DatabaseError: Database operation errors
    ├── ValidationError: Input validation failures
    └── DependencyError: External dependency issues

Example:
    Raising exceptions::

        from weeb_cli.exceptions import ProviderError, DownloadError
        
        raise ProviderError("Failed to fetch anime", code="PROVIDER_001")
        raise DownloadError("Insufficient disk space", code="DISK_FULL")
    
    Catching exceptions::

        try:
            provider.search("anime")
        except ProviderError as e:
            print(f"Provider error: {e.message} ({e.code})")
        except WeebCLIError as e:
            print(f"General error: {e}")
"""


class WeebCLIError(Exception):
    """Base exception for all Weeb CLI errors.
    
    Provides structured error handling with optional error codes for
    better error tracking and debugging.
    
    Attributes:
        message (str): Human-readable error message.
        code (str): Optional error code for categorization.
    """
    
    def __init__(self, message: str = "", code: str = "") -> None:
        """Initialize exception with message and optional code.
        
        Args:
            message: Descriptive error message.
            code: Optional error code (e.g., 'PROVIDER_001').
        """
        self.message = message
        self.code = code
        super().__init__(f"{code}: {message}" if code else message)


class ProviderError(WeebCLIError):
    """Exception raised for anime provider-related errors.
    
    Used when providers fail to search, fetch details, or extract streams.
    """
    pass


class DownloadError(WeebCLIError):
    """Exception raised for download operation failures.
    
    Used when downloads fail due to network issues, disk space, or
    invalid stream URLs.
    """
    pass


class NetworkError(WeebCLIError):
    """Exception raised for network connectivity issues.
    
    Used when HTTP requests fail or network is unavailable.
    """
    pass


class AuthenticationError(WeebCLIError):
    """Exception raised for tracker authentication failures.
    
    Used when OAuth flows fail or credentials are invalid.
    """
    pass


class DatabaseError(WeebCLIError):
    """Exception raised for database operation errors.
    
    Used when SQLite operations fail or database is corrupted.
    """
    pass


class ValidationError(WeebCLIError):
    """Exception raised for input validation failures.
    
    Used when user input or configuration values are invalid.
    """
    pass


class DependencyError(WeebCLIError):
    """Exception raised for external dependency issues.
    
    Used when required tools (FFmpeg, MPV, Aria2) are missing or fail.
    """
    pass
