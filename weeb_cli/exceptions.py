"""Custom exception hierarchy for Weeb CLI."""


class WeebCLIError(Exception):
    """Base exception for all Weeb CLI errors."""
    def __init__(self, message: str = "", code: str = ""):
        self.message = message
        self.code = code
        super().__init__(f"{code}: {message}" if code else message)


class ProviderError(WeebCLIError):
    """Raised when a provider operation fails."""
    pass


class DownloadError(WeebCLIError):
    """Raised when a download operation fails."""
    pass


class NetworkError(WeebCLIError):
    """Raised when a network operation fails."""
    pass


class AuthenticationError(WeebCLIError):
    """Raised when authentication fails."""
    pass


class DatabaseError(WeebCLIError):
    """Raised when a database operation fails."""
    pass


class ValidationError(WeebCLIError):
    """Raised when input validation fails."""
    pass


class DependencyError(WeebCLIError):
    """Raised when a required dependency is missing."""
    pass
