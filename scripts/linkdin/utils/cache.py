"""
Cache Management Module
Provides caching functionality for the application using various backends.
Enhanced with TTL, size limits, and cache statistics.
"""

import time
import json
import hashlib
import logging
from typing import Any, Optional, Dict, List, Union, Callable
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import threading
import pickle
import os

# Set up logging
logger = logging.getLogger(__name__)

class CacheBackend(Enum):
    """Enum for cache backends"""
    MEMORY = "memory"
    FILE = "file"
    REDIS = "redis"

@dataclass
class CacheConfig:
    """Configuration for cache settings"""
    backend: CacheBackend = CacheBackend.MEMORY
    ttl: int = 3600  # Time to live in seconds
    max_size: int = 1000  # Maximum number of items
    max_memory_mb: int = 100  # Maximum memory usage in MB
    file_path: str = "./cache"
    redis_url: str = "redis://localhost:6379/0"
    enable_compression: bool = False
    enable_serialization: bool = True

class CacheItem:
    """Cache item with metadata"""
    
    def __init__(self, key: str, value: Any, ttl: int = 3600):
        self.key = key
        self.value = value
        self.created_at = datetime.now()
        self.expires_at = self.created_at + timedelta(seconds=ttl)
        self.access_count = 0
        self.last_accessed = self.created_at
    
    def is_expired(self) -> bool:
        """Check if the cache item is expired."""
        return datetime.now() > self.expires_at
    
    def access(self):
        """Record access to the cache item."""
        self.access_count += 1
        self.last_accessed = datetime.now()
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert cache item to dictionary."""
        return {
            'key': self.key,
            'value': self.value,
            'created_at': self.created_at.isoformat(),
            'expires_at': self.expires_at.isoformat(),
            'access_count': self.access_count,
            'last_accessed': self.last_accessed.isoformat()
        }

class MemoryCache:
    """In-memory cache implementation"""
    
    def __init__(self, config: CacheConfig):
        self.config = config
        self.cache: Dict[str, CacheItem] = {}
        self.lock = threading.RLock()
        self.stats = {
            'hits': 0,
            'misses': 0,
            'evictions': 0,
            'size': 0
        }
        
        logger.info("MemoryCache initialized")
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        with self.lock:
            if key in self.cache:
                item = self.cache[key]
                if item.is_expired():
                    del self.cache[key]
                    self.stats['misses'] += 1
                    self.stats['size'] = len(self.cache)
                    return None
                
                item.access()
                self.stats['hits'] += 1
                return item.value
            else:
                self.stats['misses'] += 1
                return None
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Set value in cache."""
        try:
            with self.lock:
                if ttl is None:
                    ttl = self.config.ttl
                
                # Check size limit
                if len(self.cache) >= self.config.max_size:
                    self._evict_oldest()
                
                item = CacheItem(key, value, ttl)
                self.cache[key] = item
                self.stats['size'] = len(self.cache)
                
                logger.debug(f"Cached item: {key}")
                return True
                
        except Exception as e:
            logger.error(f"Error setting cache item {key}: {str(e)}")
            return False
    
    def delete(self, key: str) -> bool:
        """Delete value from cache."""
        with self.lock:
            if key in self.cache:
                del self.cache[key]
                self.stats['size'] = len(self.cache)
                logger.debug(f"Deleted cache item: {key}")
                return True
            return False
    
    def clear(self) -> bool:
        """Clear all cache items."""
        with self.lock:
            self.cache.clear()
            self.stats['size'] = 0
            logger.info("Cache cleared")
            return True
    
    def exists(self, key: str) -> bool:
        """Check if key exists in cache."""
        with self.lock:
            if key in self.cache:
                item = self.cache[key]
                if item.is_expired():
                    del self.cache[key]
                    self.stats['size'] = len(self.cache)
                    return False
                return True
            return False
    
    def _evict_oldest(self):
        """Evict oldest cache item."""
        if not self.cache:
            return
        
        oldest_key = min(self.cache.keys(), key=lambda k: self.cache[k].last_accessed)
        del self.cache[oldest_key]
        self.stats['evictions'] += 1
        logger.debug(f"Evicted oldest cache item: {oldest_key}")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        with self.lock:
            total_requests = self.stats['hits'] + self.stats['misses']
            hit_rate = self.stats['hits'] / total_requests if total_requests > 0 else 0
            
            return {
                'hits': self.stats['hits'],
                'misses': self.stats['misses'],
                'evictions': self.stats['evictions'],
                'size': self.stats['size'],
                'hit_rate': hit_rate,
                'max_size': self.config.max_size
            }

class FileCache:
    """File-based cache implementation"""
    
    def __init__(self, config: CacheConfig):
        self.config = config
        self.cache_dir = Path(config.file_path)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
        self.lock = threading.RLock()
        self.stats = {
            'hits': 0,
            'misses': 0,
            'evictions': 0,
            'size': 0
        }
        
        # Clean expired items on startup
        self._clean_expired()
        
        logger.info(f"FileCache initialized at {self.cache_dir}")
    
    def _get_file_path(self, key: str) -> Path:
        """Get file path for cache key."""
        key_hash = hashlib.md5(key.encode()).hexdigest()
        return self.cache_dir / f"{key_hash}.cache"
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        try:
            file_path = self._get_file_path(key)
            
            if not file_path.exists():
                self.stats['misses'] += 1
                return None
            
            with open(file_path, 'rb') as f:
                item_data = pickle.load(f)
            
            item = CacheItem(
                item_data['key'],
                item_data['value'],
                item_data.get('ttl', self.config.ttl)
            )
            item.created_at = datetime.fromisoformat(item_data['created_at'])
            item.expires_at = datetime.fromisoformat(item_data['expires_at'])
            item.access_count = item_data.get('access_count', 0)
            item.last_accessed = datetime.fromisoformat(item_data.get('last_accessed', item_data['created_at']))
            
            if item.is_expired():
                file_path.unlink()
                self.stats['misses'] += 1
                return None
            
            item.access()
            self.stats['hits'] += 1
            
            # Update access info
            self._save_item(item)
            
            return item.value
            
        except Exception as e:
            logger.error(f"Error getting cache item {key}: {str(e)}")
            self.stats['misses'] += 1
            return None
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Set value in cache."""
        try:
            if ttl is None:
                ttl = self.config.ttl
            
            item = CacheItem(key, value, ttl)
            self._save_item(item)
            
            # Check size limit
            self._enforce_size_limit()
            
            logger.debug(f"Cached item: {key}")
            return True
            
        except Exception as e:
            logger.error(f"Error setting cache item {key}: {str(e)}")
            return False
    
    def delete(self, key: str) -> bool:
        """Delete value from cache."""
        try:
            file_path = self._get_file_path(key)
            if file_path.exists():
                file_path.unlink()
                logger.debug(f"Deleted cache item: {key}")
                return True
            return False
        except Exception as e:
            logger.error(f"Error deleting cache item {key}: {str(e)}")
            return False
    
    def clear(self) -> bool:
        """Clear all cache items."""
        try:
            for file_path in self.cache_dir.glob("*.cache"):
                file_path.unlink()
            logger.info("Cache cleared")
            return True
        except Exception as e:
            logger.error(f"Error clearing cache: {str(e)}")
            return False
    
    def exists(self, key: str) -> bool:
        """Check if key exists in cache."""
        file_path = self._get_file_path(key)
        return file_path.exists() and not self._is_expired(file_path)
    
    def _save_item(self, item: CacheItem):
        """Save cache item to file."""
        file_path = self._get_file_path(item.key)
        
        item_data = {
            'key': item.key,
            'value': item.value,
            'created_at': item.created_at.isoformat(),
            'expires_at': item.expires_at.isoformat(),
            'access_count': item.access_count,
            'last_accessed': item.last_accessed.isoformat(),
            'ttl': (item.expires_at - item.created_at).total_seconds()
        }
        
        with open(file_path, 'wb') as f:
            pickle.dump(item_data, f)
    
    def _is_expired(self, file_path: Path) -> bool:
        """Check if cache file is expired."""
        try:
            with open(file_path, 'rb') as f:
                item_data = pickle.load(f)
            
            expires_at = datetime.fromisoformat(item_data['expires_at'])
            return datetime.now() > expires_at
        except:
            return True
    
    def _clean_expired(self):
        """Clean expired cache items."""
        try:
            expired_count = 0
            for file_path in self.cache_dir.glob("*.cache"):
                if self._is_expired(file_path):
                    file_path.unlink()
                    expired_count += 1
            
            if expired_count > 0:
                logger.info(f"Cleaned {expired_count} expired cache items")
        except Exception as e:
            logger.error(f"Error cleaning expired cache items: {str(e)}")
    
    def _enforce_size_limit(self):
        """Enforce cache size limit."""
        try:
            cache_files = list(self.cache_dir.glob("*.cache"))
            
            if len(cache_files) > self.config.max_size:
                # Sort by last accessed time
                file_times = []
                for file_path in cache_files:
                    try:
                        with open(file_path, 'rb') as f:
                            item_data = pickle.load(f)
                        last_accessed = datetime.fromisoformat(item_data.get('last_accessed', item_data['created_at']))
                        file_times.append((file_path, last_accessed))
                    except:
                        file_times.append((file_path, datetime.min))
                
                # Remove oldest files
                file_times.sort(key=lambda x: x[1])
                files_to_remove = file_times[:len(cache_files) - self.config.max_size]
                
                for file_path, _ in files_to_remove:
                    file_path.unlink()
                    self.stats['evictions'] += 1
                
                logger.debug(f"Evicted {len(files_to_remove)} cache items")
        except Exception as e:
            logger.error(f"Error enforcing size limit: {str(e)}")
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        try:
            cache_files = list(self.cache_dir.glob("*.cache"))
            self.stats['size'] = len(cache_files)
            
            total_requests = self.stats['hits'] + self.stats['misses']
            hit_rate = self.stats['hits'] / total_requests if total_requests > 0 else 0
            
            return {
                'hits': self.stats['hits'],
                'misses': self.stats['misses'],
                'evictions': self.stats['evictions'],
                'size': self.stats['size'],
                'hit_rate': hit_rate,
                'max_size': self.config.max_size,
                'cache_dir': str(self.cache_dir)
            }
        except Exception as e:
            logger.error(f"Error getting cache stats: {str(e)}")
            return {}

class CacheManager:
    """
    Cache manager for handling different cache backends.
    """
    
    def __init__(self, config: Optional[CacheConfig] = None):
        """
        Initialize cache manager.
        
        Args:
            config: Cache configuration
        """
        self.config = config or CacheConfig()
        self.cache = self._create_cache_backend()
        
        logger.info(f"CacheManager initialized with {self.config.backend.value} backend")
    
    def _create_cache_backend(self):
        """Create cache backend based on configuration."""
        if self.config.backend == CacheBackend.MEMORY:
            return MemoryCache(self.config)
        elif self.config.backend == CacheBackend.FILE:
            return FileCache(self.config)
        elif self.config.backend == CacheBackend.REDIS:
            # Redis implementation would go here
            logger.warning("Redis backend not implemented, falling back to memory")
            return MemoryCache(self.config)
        else:
            logger.warning(f"Unknown cache backend: {self.config.backend}, using memory")
            return MemoryCache(self.config)
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        return self.cache.get(key)
    
    def set(self, key: str, value: Any, ttl: Optional[int] = None) -> bool:
        """Set value in cache."""
        return self.cache.set(key, value, ttl)
    
    def delete(self, key: str) -> bool:
        """Delete value from cache."""
        return self.cache.delete(key)
    
    def clear(self) -> bool:
        """Clear all cache items."""
        return self.cache.clear()
    
    def exists(self, key: str) -> bool:
        """Check if key exists in cache."""
        return self.cache.exists(key)
    
    def get_or_set(self, key: str, factory: Callable[[], Any], ttl: Optional[int] = None) -> Any:
        """
        Get value from cache or set it using factory function.
        
        Args:
            key: Cache key
            factory: Function to generate value if not in cache
            ttl: Time to live in seconds
            
        Returns:
            Cached or generated value
        """
        value = self.get(key)
        if value is None:
            value = factory()
            self.set(key, value, ttl)
        return value
    
    def get_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        return self.cache.get_stats()
    
    def update_config(self, new_config: CacheConfig):
        """Update cache configuration."""
        self.config = new_config
        self.cache = self._create_cache_backend()

# Global cache manager instance
cache_manager = CacheManager()

def get_cache() -> CacheManager:
    """Get global cache manager instance."""
    return cache_manager

def cache_result(ttl: int = 3600, key_func: Optional[Callable] = None):
    """
    Decorator to cache function results.
    
    Args:
        ttl: Time to live in seconds
        key_func: Function to generate cache key from arguments
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Generate cache key
            if key_func:
                cache_key = key_func(*args, **kwargs)
            else:
                # Default key generation
                key_parts = [func.__name__]
                key_parts.extend([str(arg) for arg in args])
                key_parts.extend([f"{k}={v}" for k, v in sorted(kwargs.items())])
                cache_key = hashlib.md5('|'.join(key_parts).encode()).hexdigest()
            
            # Try to get from cache
            result = cache_manager.get(cache_key)
            if result is not None:
                logger.debug(f"Cache hit for {func.__name__}")
                return result
            
            # Execute function and cache result
            result = func(*args, **kwargs)
            cache_manager.set(cache_key, result, ttl)
            logger.debug(f"Cached result for {func.__name__}")
            
            return result
        
        return wrapper
    return decorator

# Usage example
if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Example usage
    config = CacheConfig(
        backend=CacheBackend.MEMORY,
        ttl=60,
        max_size=100
    )
    
    cache = CacheManager(config)
    
    # Basic operations
    cache.set("key1", "value1", 30)
    value = cache.get("key1")
    print(f"Retrieved value: {value}")
    
    # Test expiration
    cache.set("key2", "value2", 1)
    time.sleep(2)
    expired_value = cache.get("key2")
    print(f"Expired value: {expired_value}")
    
    # Test decorator
    @cache_result(ttl=60)
    def expensive_function(x, y):
        time.sleep(0.1)  # Simulate expensive operation
        return x + y
    
    # First call - will execute function
    result1 = expensive_function(1, 2)
    print(f"First call result: {result1}")
    
    # Second call - will use cache
    result2 = expensive_function(1, 2)
    print(f"Second call result: {result2}")
    
    # Get stats
    stats = cache.get_stats()
    print(f"Cache stats: {stats}")
