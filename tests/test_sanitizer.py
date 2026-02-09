"""Tests for sanitizer utilities."""
import pytest
from weeb_cli.utils.sanitizer import sanitize_filename, validate_url


class TestSanitizeFilename:
    """Test filename sanitization."""
    
    def test_basic_sanitization(self):
        """Test basic character removal."""
        assert sanitize_filename("test<>file") == "testfile"
        assert sanitize_filename('test"file') == "testfile"
        assert sanitize_filename("test|file") == "testfile"
    
    def test_path_traversal_prevention(self):
        """Test path traversal attack prevention."""
        assert ".." not in sanitize_filename("../../../etc/passwd")
        assert ".." not in sanitize_filename("test..file")
    
    def test_empty_input(self):
        """Test empty input handling."""
        assert sanitize_filename("") == "unnamed"
        assert sanitize_filename("   ") == "unnamed"
    
    def test_unicode_handling(self):
        """Test unicode character handling."""
        result = sanitize_filename("Anime - 第1話")
        assert result  # Should not be empty
        assert len(result) > 0
    
    def test_length_limiting(self):
        """Test filename length limiting."""
        long_name = "a" * 300
        result = sanitize_filename(long_name, max_length=200)
        assert len(result) <= 200
    
    def test_windows_reserved_chars(self):
        """Test Windows reserved character removal."""
        assert sanitize_filename("file:name") == "filename"
        assert sanitize_filename("file*name") == "filename"
        assert sanitize_filename("file?name") == "filename"
    
    def test_leading_trailing_dots(self):
        """Test removal of leading/trailing dots and spaces."""
        assert sanitize_filename("...file...") == "file"
        assert sanitize_filename("  file  ") == "file"


class TestValidateUrl:
    """Test URL validation."""
    
    def test_valid_urls(self):
        """Test valid URL patterns."""
        assert validate_url("https://example.com")
        assert validate_url("http://example.com")
        assert validate_url("https://example.com/path")
        assert validate_url("https://example.com:8080")
    
    def test_invalid_urls(self):
        """Test invalid URL patterns."""
        assert not validate_url("")
        assert not validate_url("not a url")
        assert not validate_url("ftp://example.com")
        assert not validate_url("javascript:alert(1)")
    
    def test_localhost(self):
        """Test localhost URLs."""
        assert validate_url("http://localhost")
        assert validate_url("http://localhost:8080")
