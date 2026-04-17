"""Caching system for Weeb CLI.

This module provides a two-tier caching system with both memory and file-based
storage. Supports TTL (time-to-live) for automatic cache expiration.

The cache system is used throughout the application to reduce redundant
API calls and improve performance.

Classes:
    CacheManager: Main cache manager with memory and file storage
    
Functions:
    cached: Decorator for automatic function result caching
    get_cache: Get global cache instance

Example:
    Using cache manager::

        from weeb_cli.services.cache import get_cache
        
        cache = get_cache()
        
        # Store value
        cache.set("search:animecix:naruto", results)
        
        # Retrieve value (max 1 hour old)
        results = cache.get("search:animecix:naruto", max_age=3600)
        
        # Clear specific pattern
        cache.clear_pattern("search:animecix:")
    
    Using decorator::

        from weeb_cli.services.cache import cached
        
        @cached(max_age=1800)  # 30 minutes
        def expensive_operation(param):
            # This result will be cached
            return compute_result(param)
"""

import json
import time
import hashlib
from pathlib import Path
from typing import Any, Optional, Callable, Dict, Tuple
from functools import wraps


class CacheManager:
    """Two-tier cache manager with memory and file storage.
    
    Provides fast memory cache with persistent file backup. Automatically
    handles cache expiration based on TTL (time-to-live).
    
    Attributes:
        cache_dir: Directory for cache file storage.
        _memory_cache: In-memory cache dictionary.
    """
    
    def __init__(self, cache_dir: Path) -> None:
        """Initialize cache manager.
        
        Args:
            cache_dir: Directory path for storing cache files.
        """
        self.cache_dir: Path = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self._memory_cache: Dict[str, Tuple[Any, float]] = {}
    
    def _get_cache_key(self, key: str) -> str:
        """Generate SHA256 hash for cache key.
        
        Args:
            key: Original cache key.
        
        Returns:
            Hexadecimal hash string.
        """
        return hashlib.sha256(key.encode()).hexdigest()
    
    def get(self, key: str, max_age: int = 3600) -> Optional[Any]:
        """Retrieve cached value if not expired.
        
        Checks memory cache first, then file cache. Automatically removes
        expired entries.
        
        Args:
            key: Cache key.
            max_age: Maximum age in seconds (default: 1 hour).
        
        Returns:
            Cached value if found and not expired, otherwise None.
        
        Example:
            >>> cache.get("search:naruto", max_age=1800)
            [{'id': '1', 'title': 'Naruto'}]
        """
        # Check memory cache
        if key in self._memory_cache:
            value, timestamp = self._memory_cache[key]
            if time.time() - timestamp < max_age:
                return value
            else:
                del self._memory_cache[key]
        
        # Check file cache
        cache_key = self._get_cache_key(key)
        cache_file = self.cache_dir / f"{cache_key}.cache"
        
        if cache_file.exists():
            age = time.time() - cache_file.stat().st_mtime
            if age < max_age:
                try:
                    with open(cache_file, 'r', encoding='utf-8') as f:
                        value = json.load(f)
                        self._memory_cache[key] = (value, time.time())
                        return value
                except (json.JSONDecodeError, UnicodeDecodeError, OSError):
                    cache_file.unlink(missing_ok=True)
        
        return None
    
    def set(self, key: str, value: Any) -> None:
        """Store value in cache.
        
        Stores in both memory and file cache for persistence.
        
        Args:
            key: Cache key.
            value: Value to cache (must be JSON-serializable).
        
        Example:
            >>> cache.set("search:naruto", results)
        """
        self._memory_cache[key] = (value, time.time())
        
        cache_key = self._get_cache_key(key)
        cache_file = self.cache_dir / f"{cache_key}.cache"
        
        try:
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(value, f, ensure_ascii=False, default=str)
        except (OSError, TypeError):
            pass
    
    def delete(self, key: str) -> None:
        """Delete cached value.
        
        Removes from both memory and file cache.
        
        Args:
            key: Cache key to delete.
        """
        self._memory_cache.pop(key, None)
        
        cache_key = self._get_cache_key(key)
        cache_file = self.cache_dir / f"{cache_key}.cache"
        cache_file.unlink(missing_ok=True)
    
    def clear(self) -> None:
        """Clear all cached values.
        
        Removes all entries from memory and deletes all cache files.
        """
        self._memory_cache.clear()
        
        for cache_file in self.cache_dir.glob("*.cache"):
            cache_file.unlink(missing_ok=True)
    
    def clear_pattern(self, pattern: str) -> int:
        """Clear cached values matching a pattern.
        
        Args:
            pattern: String pattern to match in cache keys.
        
        Returns:
            Number of entries removed.
        
        Example:
            >>> count = cache.clear_pattern("search:animecix:")
            >>> print(f"Removed {count} entries")
        """
        removed = 0
        keys_to_remove = [k for k in self._memory_cache.keys() if pattern in k]
        for key in keys_to_remove:
            del self._memory_cache[key]
            cache_key = self._get_cache_key(key)
            cache_file = self.cache_dir / f"{cache_key}.cache"
            cache_file.unlink(missing_ok=True)
            removed += 1
        
        return removed
    
    def invalidate_provider(self, provider_name: str) -> int:
        """Invalidate all cache entries for a provider.
        
        Clears search and details cache for the specified provider.
        
        Args:
            provider_name: Provider identifier.
        
        Returns:
            Number of entries removed.
        
        Example:
            >>> cache.invalidate_provider("animecix")
        """
        removed = 0
        patterns = [f"search:{provider_name}:", f"details:{provider_name}:"]
        
        for pattern in patterns:
            keys_to_remove = [k for k in list(self._memory_cache.keys()) if k.startswith(pattern)]
            for key in keys_to_remove:
                del self._memory_cache[key]
                removed += 1
        
        # Clear all file cache (conservative approach)
        for cache_file in self.cache_dir.glob("*.cache"):
            cache_file.unlink(missing_ok=True)
        
        return removed
    
    def cleanup(self, max_age: int = 86400) -> int:
        """Remove expired cache entries.
        
        Removes entries older than max_age from both memory and file cache.
        
        Args:
            max_age: Maximum age in seconds (default: 24 hours).
        
        Returns:
            Number of entries removed.
        
        Example:
            >>> # Remove entries older than 1 hour
            >>> count = cache.cleanup(max_age=3600)
        """
        removed = 0
        cutoff = time.time() - max_age
        
        # Clean memory cache
        keys_to_remove = []
        for key, (value, timestamp) in list(self._memory_cache.items()):
            if timestamp < cutoff:
                keys_to_remove.append(key)
        
        for key in keys_to_remove:
            del self._memory_cache[key]
            removed += 1
        
        # Clean file cache
        for cache_file in self.cache_dir.glob("*.cache"):
            if cache_file.stat().st_mtime < cutoff:
                cache_file.unlink(missing_ok=True)
                removed += 1
        
        return removed
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics.
        
        Returns:
            Dictionary with cache statistics:
                - memory_entries: Number of in-memory entries
                - file_entries: Number of file cache entries
                - total_size_bytes: Total file cache size in bytes
                - total_size_mb: Total file cache size in MB
        
        Example:
            >>> stats = cache.get_stats()
            >>> print(f"Cache size: {stats['total_size_mb']} MB")
        """
        memory_count = len(self._memory_cache)
        file_count = len(list(self.cache_dir.glob("*.cache")))
        
        total_size = 0
        for cache_file in self.cache_dir.glob("*.cache"):
            total_size += cache_file.stat().st_size
        
        return {
            "memory_entries": memory_count,
            "file_entries": file_count,
            "total_size_bytes": total_size,
            "total_size_mb": round(total_size / (1024 * 1024), 2)
        }


def cached(max_age: int = 3600, cache_manager: Optional[CacheManager] = None):
    """Decorator for automatic function result caching.
    
    Caches function results based on arguments. Cache key is generated
    from function name and arguments.
    
    Args:
        max_age: Cache TTL in seconds (default: 1 hour).
        cache_manager: Optional custom cache manager instance.
    
    Returns:
        Decorator function.
    
    Example:
        >>> @cached(max_age=1800)
        ... def fetch_anime_details(anime_id):
        ...     # Expensive operation
        ...     return api.get_details(anime_id)
        
        >>> # First call: executes function
        >>> details = fetch_anime_details("123")
        
        >>> # Second call within 30 min: returns cached result
        >>> details = fetch_anime_details("123")
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Generate cache key from function name and arguments
            key_parts = [func.__name__]
            key_parts.extend(str(arg) for arg in args)
            key_parts.extend(f"{k}={v}" for k, v in sorted(kwargs.items()))
            cache_key = ":".join(key_parts)
            
            cm = cache_manager or _get_global_cache()
            
            # Try to get from cache
            result = cm.get(cache_key, max_age)
            if result is not None:
                return result
            
            # Execute function and cache result
            result = func(*args, **kwargs)
            cm.set(cache_key, result)
            return result
        
        return wrapper
    return decorator


_global_cache: Optional[CacheManager] = None


def _get_global_cache() -> CacheManager:
    """Get or create global cache instance.
    
    Returns:
        Global CacheManager instance.
    """
    global _global_cache
    if _global_cache is None:
        from weeb_cli.config import CONFIG_DIR
        _global_cache = CacheManager(CONFIG_DIR / "cache")
    return _global_cache


def get_cache() -> CacheManager:
    """Get global cache instance.
    
    Returns:
        Global CacheManager instance for application-wide use.
    
    Example:
        >>> from weeb_cli.services.cache import get_cache
        >>> cache = get_cache()
        >>> cache.set("key", "value")
    """
    return _get_global_cache()
