import pytest
from weeb_cli.exceptions import (
    WeebCLIError,
    ProviderError,
    DownloadError,
    NetworkError,
    AuthenticationError
)


class TestExceptions:
    def test_base_exception(self):
        exc = WeebCLIError("Test message", "TEST_CODE")
        assert str(exc) == "TEST_CODE: Test message"
        assert exc.message == "Test message"
        assert exc.code == "TEST_CODE"
    
    def test_exception_without_code(self):
        exc = WeebCLIError("Test message")
        assert str(exc) == "Test message"
    
    def test_provider_error(self):
        exc = ProviderError("Provider failed", "PROVIDER_ERROR")
        assert isinstance(exc, WeebCLIError)
    
    def test_download_error(self):
        exc = DownloadError("Download failed", "DOWNLOAD_ERROR")
        assert isinstance(exc, WeebCLIError)
    
    def test_network_error(self):
        exc = NetworkError("Network failed", "NETWORK_ERROR")
        assert isinstance(exc, WeebCLIError)
    
    def test_authentication_error(self):
        exc = AuthenticationError("Auth failed", "AUTH_ERROR")
        assert isinstance(exc, WeebCLIError)
