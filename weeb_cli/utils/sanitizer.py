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
    if not url or len(url) < 10:
        return False
    
    if not url.startswith(('http://', 'https://')):
        return False
    
    try:
        from urllib.parse import urlparse
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except:
        return False
