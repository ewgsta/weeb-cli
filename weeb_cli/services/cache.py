import pickle
import time
import hashlib
from pathlib import Path
from typing import Any, Optional, Callable, Dict
from functools import wraps


class CacheManager:
    
    def __init__(self, cache_dir: Path) -> None:
        self.cache_dir: Path = cache_dir
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self._memory_cache: Dict[str, tuple] = {}
    
    def _get_cache_key(self, key: str) -> str:
        return hashlib.md5(key.encode()).hexdigest()
    
    def get(self, key: str, max_age: int = 3600) -> Optional[Any]:
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
        self._memory_cache[key] = (value, time.time())
        
        cache_key = self._get_cache_key(key)
        cache_file = self.cache_dir / f"{cache_key}.cache"
        
        try:
            with open(cache_file, 'wb') as f:
                pickle.dump(value, f)
        except (pickle.PickleError, OSError):
            pass
    
    def delete(self, key: str) -> None:
        self._memory_cache.pop(key, None)
        
        cache_key = self._get_cache_key(key)
        cache_file = self.cache_dir / f"{cache_key}.cache"
        cache_file.unlink(missing_ok=True)
    
    def clear(self) -> None:
        self._memory_cache.clear()
        
        for cache_file in self.cache_dir.glob("*.cache"):
            cache_file.unlink(missing_ok=True)
    
    def clear_pattern(self, pattern: str) -> int:
        removed = 0
        keys_to_remove = [k for k in self._memory_cache.keys() if pattern in k]
        for key in keys_to_remove:
            del self._memory_cache[key]
            removed += 1
        
        for cache_file in self.cache_dir.glob("*.cache"):
            try:
                with open(cache_file, 'rb') as f:
                    value = pickle.load(f)
            except:
                continue
        
        return removed
    
    def invalidate_provider(self, provider_name: str) -> int:
        removed = 0
        patterns = [f"search:{provider_name}:", f"details:{provider_name}:"]
        
        for pattern in patterns:
            keys_to_remove = [k for k in list(self._memory_cache.keys()) if k.startswith(pattern)]
            for key in keys_to_remove:
                del self._memory_cache[key]
                removed += 1
        
        for cache_file in self.cache_dir.glob("*.cache"):
            cache_file.unlink(missing_ok=True)
        
        return removed
    
    def cleanup(self, max_age: int = 86400) -> int:
        removed = 0
        cutoff = time.time() - max_age
        
        keys_to_remove = []
        for key, (value, timestamp) in list(self._memory_cache.items()):
            if timestamp < cutoff:
                keys_to_remove.append(key)
        
        for key in keys_to_remove:
            del self._memory_cache[key]
            removed += 1
        
        for cache_file in self.cache_dir.glob("*.cache"):
            if cache_file.stat().st_mtime < cutoff:
                cache_file.unlink(missing_ok=True)
                removed += 1
        
        return removed
    
    def get_stats(self) -> Dict[str, Any]:
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
    global _global_cache
    if _global_cache is None:
        from weeb_cli.config import CONFIG_DIR
        _global_cache = CacheManager(CONFIG_DIR / "cache")
    return _global_cache


def get_cache() -> CacheManager:
    return _get_global_cache()
