import re
import unicodedata
from pathlib import Path

def sanitize_filename(filename: str, max_length: int = 200) -> str:
    """
    Sanitize filename for safe filesystem usage.
    Prevents path traversal and ensures cross-platform compatibility.
    """
    if not filename or not isinstance(filename, str):
        return "untitled"
    
    # Remove path traversal attempts
    filename = filename.replace('..', '')
    filename = Path(filename).name  # Extract only filename, remove any path components
    
    # Normalize unicode characters
    filename = unicodedata.normalize('NFKD', filename)
    filename = filename.encode('ascii', 'ignore').decode('ascii')
    
    # Remove invalid characters for Windows/Linux/macOS
    # Windows: < > : " / \ | ? *
    # Also remove control characters (0x00-0x1F)
    filename = re.sub(r'[<>:"/\\|?*\x00-\x1F]', '', filename)
    
    # Replace multiple spaces with single space
    filename = re.sub(r'\s+', ' ', filename)
    
    # Remove leading/trailing spaces and dots (Windows compatibility)
    filename = filename.strip('. ')
    
    # Truncate to max length while preserving extension
    if len(filename) > max_length:
        name_parts = filename.rsplit('.', 1)
        if len(name_parts) == 2:
            name, ext = name_parts
            max_name_len = max_length - len(ext) - 1
            filename = name[:max_name_len] + '.' + ext
        else:
            filename = filename[:max_length]
    
    # Fallback if empty after sanitization
    if not filename or filename in ('.', '..'):
        filename = "untitled"
    
    # Reserved names on Windows
    reserved = {'CON', 'PRN', 'AUX', 'NUL', 'COM1', 'COM2', 'COM3', 'COM4', 
                'COM5', 'COM6', 'COM7', 'COM8', 'COM9', 'LPT1', 'LPT2', 
                'LPT3', 'LPT4', 'LPT5', 'LPT6', 'LPT7', 'LPT8', 'LPT9'}
    name_without_ext = filename.rsplit('.', 1)[0].upper()
    if name_without_ext in reserved:
        filename = f"_{filename}"
    
    return filename


def sanitize_path(path: str) -> Path:
    """Validate and resolve path safely."""
    p = Path(path)
    
    try:
        resolved = p.resolve()
        return resolved
    except (OSError, RuntimeError):
        raise ValueError(f"Invalid path: {path}")


def validate_url(url: str) -> bool:
    """Validate URL format."""
    if not url or len(url) < 10:
        return False
    
    if not url.startswith(('http://', 'https://')):
        return False
    
    try:
        from urllib.parse import urlparse
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False
