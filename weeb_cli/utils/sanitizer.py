import re
import unicodedata
from pathlib import Path


def sanitize_filename(name: str, max_length: int = 200) -> str:
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
    p = Path(path)
    
    try:
        resolved = p.resolve()
        return resolved
    except (OSError, RuntimeError):
        raise ValueError(f"Invalid path: {path}")


def validate_url(url: str) -> bool:
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
