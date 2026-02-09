"""Simple file-based cache manager for Weeb CLI."""
import pickle
import time
import hashlib
from pathlib import Path
from typing import Any, Optional, Callable
from functools import wraps


class CacheManager:
    """Simple file-based cache with TTL support."""
    
    def __init__(self, cache_dir: Path):
        """
        Initialize cache manager.
        
        Args:
            cache_dir: Directory to store cache files
        """
        self.cache_dir = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self._memory_cache = {}
    
    def _get_cache_key(self, key: str) -> str:
        """Generate a safe cache key from input."""
        return hashlib.md5(key.encode()).hexdigest()
    
    def get(self, key: str, max_age: int = 3600) -> Optional[Any]:
        """
        Get value from cache if not expired.
        
        Args:
            key: Cache key
            max_age: Maximum age in seconds (default: 1 hour)
        
        Returns:
            Cached value or None if expired/not found
        """
        if key in self._memory_cache:
            value, timestamp = self._memory_cache[key]
            if time.time() - timestamp < max_age:
                return value
            else:
                del self._memory_cache[key]
        
        cache_key = self._get_cache_key(key)
        cache_file = self.cache_dir / f"{cache_key}.cache"
        
        if cache_file.exists():
            age = time.time() - cache_file.stat().st_mtime
            if age < max_age:
                try:
                    with open(cache_file, 'rb') as f:
                        value = pickle.load(f)
                        self._memory_cache[key] = (value, time.time())
                        return value
                except (pickle.PickleError, EOFError):
                    cache_file.unlink(missing_ok=True)
        
        return None
    
    def set(self, key: str, value: Any) -> None:
        """
        Store value in cache.
        
        Args:
            key: Cache key
            value: Value to cache
        """
        self._memory_cache[key] = (value, time.time())
        
        cache_key = self._get_cache_key(key)
        cache_file = self.cache_dir / f"{cache_key}.cache"
        
        try:
            with open(cache_file, 'wb') as f:
                pickle.dump(value, f)
        except (pickle.PickleError, OSError):
            pass  # Fail silently for cache writes
    
    def delete(self, key: str) -> None:
        """
        Delete value from cache.
        
        Args:
            key: Cache key
        """
        self._memory_cache.pop(key, None)
        
        cache_key = self._get_cache_key(key)
        cache_file = self.cache_dir / f"{cache_key}.cache"
        cache_file.unlink(missing_ok=True)
    
    def clear(self) -> None:
        """Clear all cache."""
        self._memory_cache.clear()
        
        for cache_file in self.cache_dir.glob("*.cache"):
            cache_file.unlink(missing_ok=True)
    
    def cleanup(self, max_age: int = 86400) -> int:
        """
        Remove expired cache files.
        
        Args:
            max_age: Maximum age in seconds (default: 24 hours)
        
        Returns:
            Number of files removed
        """
        removed = 0
        cutoff = time.time() - max_age
        
        for cache_file in self.cache_dir.glob("*.cache"):
            if cache_file.stat().st_mtime < cutoff:
                cache_file.unlink(missing_ok=True)
                removed += 1
        
        return removed


def cached(max_age: int = 3600, cache_manager: Optional[CacheManager] = None):
    """
    Decorator to cache function results.
    
    Args:
        max_age: Cache TTL in seconds
        cache_manager: CacheManager instance (uses global if None)
    
    Example:
        @cached(max_age=1800)
        def expensive_function(arg1, arg2):
            pass
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            key_parts = [func.__name__]
            key_parts.extend(str(arg) for arg in args)
            key_parts.extend(f"{k}={v}" for k, v in sorted(kwargs.items()))
            cache_key = ":".join(key_parts)
            
            cm = cache_manager or _get_global_cache()
            
            result = cm.get(cache_key, max_age)
            if result is not None:
                return result
            
            result = func(*args, **kwargs)
            cm.set(cache_key, result)
            return result
        
        return wrapper
    return decorator


_global_cache = None


def _get_global_cache() -> CacheManager:
    """Get or create global cache instance."""
    global _global_cache
    if _global_cache is None:
        from weeb_cli.config import CONFIG_DIR
        _global_cache = CacheManager(CONFIG_DIR / "cache")
    return _global_cache


def get_cache() -> CacheManager:
    """Get global cache instance."""
    return _get_global_cache()
