class WeebCLIError(Exception):
    def __init__(self, message: str = "", code: str = ""):
        self.message = message
        self.code = code
        super().__init__(f"{code}: {message}" if code else message)


class ProviderError(WeebCLIError):
    pass


class DownloadError(WeebCLIError):
    pass


class NetworkError(WeebCLIError):
    pass


class AuthenticationError(WeebCLIError):
    pass


class DatabaseError(WeebCLIError):
    pass


class ValidationError(WeebCLIError):
    pass


class DependencyError(WeebCLIError):
    pass
