import pytest
from weeb_cli.utils.sanitizer import sanitize_filename


class TestSanitizerSecurity:
    """Security tests for filename sanitization."""
    
    def test_path_traversal_prevention(self):
        """Test that path traversal attempts are blocked."""
        assert sanitize_filename("../../etc/passwd") == "etcpasswd"
        assert sanitize_filename("..\\..\\windows\\system32") == "windowssystem32"
        assert sanitize_filename("../../../root") == "root"
    
    def test_windows_reserved_names(self):
        """Test Windows reserved filenames are handled."""
        assert sanitize_filename("CON") == "_CON"
        assert sanitize_filename("PRN.txt") == "_PRN.txt"
        assert sanitize_filename("AUX") == "_AUX"
        assert sanitize_filename("NUL.log") == "_NUL.log"
    
    def test_invalid_characters_removed(self):
        """Test that invalid filesystem characters are removed."""
        assert sanitize_filename("file<name>") == "filename"
        assert sanitize_filename('file:name"test') == "filenametest"
        assert sanitize_filename("file|name?") == "filename"
        assert sanitize_filename("file*name") == "filename"
    
    def test_control_characters_removed(self):
        """Test control characters are removed."""
        assert sanitize_filename("file\x00name") == "filename"
        assert sanitize_filename("file\x1fname") == "filename"
    
    def test_empty_and_invalid_inputs(self):
        """Test handling of empty and invalid inputs."""
        assert sanitize_filename("") == "untitled"
        assert sanitize_filename("   ") == "untitled"
        assert sanitize_filename(".") == "untitled"
        assert sanitize_filename("..") == "untitled"
        assert sanitize_filename(None) == "untitled"
    
    def test_length_truncation(self):
        """Test that long filenames are truncated."""
        long_name = "a" * 300
        result = sanitize_filename(long_name)
        assert len(result) <= 200
    
    def test_extension_preservation(self):
        """Test that file extensions are preserved during truncation."""
        long_name = "a" * 300 + ".mp4"
        result = sanitize_filename(long_name)
        assert result.endswith(".mp4")
        assert len(result) <= 200
