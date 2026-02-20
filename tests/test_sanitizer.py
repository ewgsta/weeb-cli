import pytest
from weeb_cli.utils.sanitizer import sanitize_filename, validate_url


class TestSanitizeFilename:
    def test_basic_sanitization(self):
        assert sanitize_filename("test<>file") == "testfile"
        assert sanitize_filename('test"file') == "testfile"
        assert sanitize_filename("test|file") == "testfile"
    
    def test_path_traversal_prevention(self):
        assert ".." not in sanitize_filename("../../../etc/passwd")
        assert ".." not in sanitize_filename("test..file")
    
    def test_empty_input(self):
        assert sanitize_filename("") == "unnamed"
        assert sanitize_filename("   ") == "unnamed"
    
    def test_unicode_handling(self):
        result = sanitize_filename("Anime - 第1話")
        assert result
        assert len(result) > 0
    
    def test_length_limiting(self):
        long_name = "a" * 300
        result = sanitize_filename(long_name, max_length=200)
        assert len(result) <= 200
    
    def test_windows_reserved_chars(self):
        assert sanitize_filename("file:name") == "filename"
        assert sanitize_filename("file*name") == "filename"
        assert sanitize_filename("file?name") == "filename"
    
    def test_leading_trailing_dots(self):
        assert sanitize_filename("...file...") == "file"
        assert sanitize_filename("  file  ") == "file"


class TestValidateUrl:
    def test_valid_urls(self):
        assert validate_url("https://example.com")
        assert validate_url("http://example.com")
        assert validate_url("https://example.com/path")
        assert validate_url("https://example.com:8080")
    
    def test_invalid_urls(self):
        assert not validate_url("")
        assert not validate_url("not a url")
        assert not validate_url("ftp://example.com")
        assert not validate_url("javascript:alert(1)")
    
    def test_localhost(self):
        assert validate_url("http://localhost")
        assert validate_url("http://localhost:8080")
