"""Utility functions for sanitizing user input and filenames."""
import re
import unicodedata
from pathlib import Path


def sanitize_filename(name: str, max_length: int = 200) -> str:
    """
    Sanitize a filename to be safe for all operating systems.
    
    Args:
        name: The filename to sanitize
        max_length: Maximum length of the filename (default: 200)
    
    Returns:
        A safe filename string
    """
    if not name:
        return "unnamed"
    
    name = unicodedata.normalize('NFKD', name)
    
    name = re.sub(r'[<>:"/\\|?*\x00-\x1f]', '', name)
    
    name = name.replace('..', '')
    
    name = name.strip('. ')
    
    if not name:
        return "unnamed"
    
    if len(name) > max_length:
        name = name[:max_length]
    
    return name


def sanitize_path(path: str) -> Path:
    """
    Sanitize a full path to prevent directory traversal.
    
    Args:
        path: The path to sanitize
    
    Returns:
        A safe Path object
    """
    p = Path(path)
    
    try:
        resolved = p.resolve()
        return resolved
    except (OSError, RuntimeError):
        raise ValueError(f"Invalid path: {path}")


def validate_url(url: str) -> bool:
    """
    Validate if a URL is safe to use.
    
    Args:
        url: The URL to validate
    
    Returns:
        True if valid, False otherwise
    """
    if not url:
        return False
    
    url_pattern = re.compile(
        r'^https?://'
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'
        r'localhost|'
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
        r'(?::\d+)?'
        r'(?:/?|[/?]\S+)$', re.IGNORECASE
    )
    
    return bool(url_pattern.match(url))
