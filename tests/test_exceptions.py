"""Tests for custom exceptions."""
import pytest
from weeb_cli.exceptions import (
    WeebCLIError,
    ProviderError,
    DownloadError,
    NetworkError,
    AuthenticationError
)


class TestExceptions:
    """Test custom exception hierarchy."""
    
    def test_base_exception(self):
        """Test base exception."""
        exc = WeebCLIError("Test message", "TEST_CODE")
        assert str(exc) == "TEST_CODE: Test message"
        assert exc.message == "Test message"
        assert exc.code == "TEST_CODE"
    
    def test_exception_without_code(self):
        """Test exception without error code."""
        exc = WeebCLIError("Test message")
        assert str(exc) == "Test message"
    
    def test_provider_error(self):
        """Test provider error."""
        exc = ProviderError("Provider failed", "PROVIDER_ERROR")
        assert isinstance(exc, WeebCLIError)
    
    def test_download_error(self):
        """Test download error."""
        exc = DownloadError("Download failed", "DOWNLOAD_ERROR")
        assert isinstance(exc, WeebCLIError)
    
    def test_network_error(self):
        """Test network error."""
        exc = NetworkError("Network failed", "NETWORK_ERROR")
        assert isinstance(exc, WeebCLIError)
    
    def test_authentication_error(self):
        """Test authentication error."""
        exc = AuthenticationError("Auth failed", "AUTH_ERROR")
        assert isinstance(exc, WeebCLIError)
