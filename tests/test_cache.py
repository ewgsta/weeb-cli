"""Tests for cache manager."""
import pytest
import time
from weeb_cli.services.cache import CacheManager, cached


class TestCacheManager:
    """Test cache manager functionality."""
    
    def test_set_and_get(self, temp_dir):
        """Test basic set and get operations."""
        cache = CacheManager(temp_dir / "cache")
        
        cache.set("test_key", "test_value")
        result = cache.get("test_key")
        
        assert result == "test_value"
    
    def test_expiration(self, temp_dir):
        """Test cache expiration."""
        cache = CacheManager(temp_dir / "cache")
        
        cache.set("test_key", "test_value")
        
        assert cache.get("test_key", max_age=10) == "test_value"
        
        time.sleep(0.1)
        assert cache.get("test_key", max_age=0) is None
    
    def test_delete(self, temp_dir):
        """Test cache deletion."""
        cache = CacheManager(temp_dir / "cache")
        
        cache.set("test_key", "test_value")
        cache.delete("test_key")
        
        assert cache.get("test_key") is None
    
    def test_clear(self, temp_dir):
        """Test clearing all cache."""
        cache = CacheManager(temp_dir / "cache")
        
        cache.set("key1", "value1")
        cache.set("key2", "value2")
        cache.clear()
        
        assert cache.get("key1") is None
        assert cache.get("key2") is None
    
    def test_complex_values(self, temp_dir):
        """Test caching complex data structures."""
        cache = CacheManager(temp_dir / "cache")
        
        data = {
            "list": [1, 2, 3],
            "dict": {"nested": "value"},
            "tuple": (1, 2, 3)
        }
        
        cache.set("complex", data)
        result = cache.get("complex")
        
        assert result == data


class TestCachedDecorator:
    """Test cached decorator."""
    
    def test_function_caching(self, temp_dir):
        """Test that function results are cached."""
        cache = CacheManager(temp_dir / "cache")
        call_count = 0
        
        @cached(max_age=10, cache_manager=cache)
        def expensive_function(x):
            nonlocal call_count
            call_count += 1
            return x * 2
        
        result1 = expensive_function(5)
        assert result1 == 10
        assert call_count == 1
        
        result2 = expensive_function(5)
        assert result2 == 10
        assert call_count == 1
        
        result3 = expensive_function(10)
        assert result3 == 20
        assert call_count == 2
