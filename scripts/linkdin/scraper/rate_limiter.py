"""
Rate Limiter Module
Handles rate limiting and request throttling to avoid being blocked by LinkedIn.
Enhanced with comprehensive logging and adaptive rate limiting.
"""

import time
import random
import logging
from typing import Dict, List, Optional, Any
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import threading
import queue

# Set up logging
logger = logging.getLogger(__name__)

class RateLimitStrategy(Enum):
    """Enum for rate limiting strategies"""
    FIXED = "fixed"
    RANDOM = "random"
    ADAPTIVE = "adaptive"
    EXPONENTIAL_BACKOFF = "exponential_backoff"

@dataclass
class RateLimitConfig:
    """Configuration for rate limiting"""
    min_delay: float = 2.0
    max_delay: float = 5.0
    strategy: RateLimitStrategy = RateLimitStrategy.RANDOM
    max_requests_per_minute: int = 20
    max_requests_per_hour: int = 500
    backoff_multiplier: float = 1.5
    max_backoff_delay: float = 60.0
    reset_interval: int = 3600  # Reset counters every hour

class RateLimiter:
    """
    Rate limiter for managing request frequency and avoiding detection.
    Enhanced with comprehensive logging and adaptive rate limiting.
    """
    
    def __init__(self, config: Optional[RateLimitConfig] = None):
        """
        Initialize the rate limiter.
        
        Args:
            config: RateLimitConfig object with rate limiting parameters
        """
        self.config = config or RateLimitConfig()
        self.request_times: List[datetime] = []
        self.last_request_time: Optional[datetime] = None
        self.consecutive_failures = 0
        self.current_delay = self.config.min_delay
        self.lock = threading.Lock()
        
        logger.info(f"Initialized RateLimiter with config: {self.config}")
        
        # Statistics tracking
        self.stats = {
            'total_requests': 0,
            'delayed_requests': 0,
            'total_delay_time': 0.0,
            'rate_limit_hits': 0,
            'adaptive_adjustments': 0
        }
    
    def wait_if_needed(self) -> float:
        """
        Wait if necessary to respect rate limits.
        
        Returns:
            Actual delay time in seconds
        """
        with self.lock:
            current_time = datetime.now()
            
            # Clean old request times
            self._clean_old_requests(current_time)
            
            # Check if we need to wait
            delay = self._calculate_delay(current_time)
            
            if delay > 0:
                logger.debug(f"Rate limiting: waiting {delay:.2f} seconds")
                time.sleep(delay)
                self.stats['delayed_requests'] += 1
                self.stats['total_delay_time'] += delay
            
            # Record this request
            self.request_times.append(current_time)
            self.last_request_time = current_time
            self.stats['total_requests'] += 1
            
            return delay
    
    def _clean_old_requests(self, current_time: datetime):
        """Remove request times older than the reset interval."""
        cutoff_time = current_time - timedelta(seconds=self.config.reset_interval)
        self.request_times = [req_time for req_time in self.request_times if req_time > cutoff_time]
    
    def _calculate_delay(self, current_time: datetime) -> float:
        """
        Calculate the delay needed before the next request.
        
        Args:
            current_time: Current timestamp
            
        Returns:
            Delay in seconds
        """
        # Check minute-based rate limit
        minute_ago = current_time - timedelta(minutes=1)
        recent_requests = [req_time for req_time in self.request_times if req_time > minute_ago]
        
        if len(recent_requests) >= self.config.max_requests_per_minute:
            logger.warning(f"Rate limit hit: {len(recent_requests)} requests in last minute")
            self.stats['rate_limit_hits'] += 1
            return 60.0  # Wait a full minute
        
        # Check hour-based rate limit
        hour_ago = current_time - timedelta(hours=1)
        hourly_requests = [req_time for req_time in self.request_times if req_time > hour_ago]
        
        if len(hourly_requests) >= self.config.max_requests_per_hour:
            logger.warning(f"Hourly rate limit hit: {len(hourly_requests)} requests in last hour")
            self.stats['rate_limit_hits'] += 1
            return 3600.0  # Wait a full hour
        
        # Calculate strategy-based delay
        if self.config.strategy == RateLimitStrategy.FIXED:
            return self._calculate_fixed_delay()
        elif self.config.strategy == RateLimitStrategy.RANDOM:
            return self._calculate_random_delay()
        elif self.config.strategy == RateLimitStrategy.ADAPTIVE:
            return self._calculate_adaptive_delay()
        elif self.config.strategy == RateLimitStrategy.EXPONENTIAL_BACKOFF:
            return self._calculate_exponential_backoff_delay()
        else:
            return self._calculate_random_delay()
    
    def _calculate_fixed_delay(self) -> float:
        """Calculate fixed delay between requests."""
        return self.config.min_delay
    
    def _calculate_random_delay(self) -> float:
        """Calculate random delay between min and max values."""
        return random.uniform(self.config.min_delay, self.config.max_delay)
    
    def _calculate_adaptive_delay(self) -> float:
        """
        Calculate adaptive delay based on recent request patterns.
        Increases delay if there are many recent requests.
        """
        current_time = datetime.now()
        recent_requests = [req_time for req_time in self.request_times 
                          if req_time > current_time - timedelta(minutes=5)]
        
        # Base delay
        base_delay = random.uniform(self.config.min_delay, self.config.max_delay)
        
        # Increase delay based on recent request frequency
        if len(recent_requests) > 10:
            multiplier = 1.5
        elif len(recent_requests) > 5:
            multiplier = 1.2
        else:
            multiplier = 1.0
        
        adaptive_delay = base_delay * multiplier
        
        # Update current delay for tracking
        if adaptive_delay != base_delay:
            self.stats['adaptive_adjustments'] += 1
            logger.debug(f"Adaptive delay adjustment: {base_delay:.2f} -> {adaptive_delay:.2f}")
        
        return min(adaptive_delay, self.config.max_backoff_delay)
    
    def _calculate_exponential_backoff_delay(self) -> float:
        """
        Calculate exponential backoff delay based on consecutive failures.
        """
        if self.consecutive_failures == 0:
            return random.uniform(self.config.min_delay, self.config.max_delay)
        
        # Calculate exponential backoff
        delay = self.config.min_delay * (self.config.backoff_multiplier ** self.consecutive_failures)
        delay = min(delay, self.config.max_backoff_delay)
        
        # Add some randomness to avoid thundering herd
        jitter = random.uniform(0.8, 1.2)
        delay *= jitter
        
        logger.debug(f"Exponential backoff delay: {delay:.2f} seconds (failures: {self.consecutive_failures})")
        return delay
    
    def record_success(self):
        """Record a successful request."""
        with self.lock:
            self.consecutive_failures = 0
            logger.debug("Recorded successful request")
    
    def record_failure(self):
        """Record a failed request."""
        with self.lock:
            self.consecutive_failures += 1
            logger.debug(f"Recorded failure (consecutive: {self.consecutive_failures})")
    
    def get_current_delay(self) -> float:
        """Get the current delay value."""
        return self.current_delay
    
    def get_request_frequency(self) -> Dict[str, float]:
        """
        Get current request frequency statistics.
        
        Returns:
            Dictionary with frequency statistics
        """
        current_time = datetime.now()
        
        with self.lock:
            # Requests per minute
            minute_ago = current_time - timedelta(minutes=1)
            recent_requests = [req_time for req_time in self.request_times if req_time > minute_ago]
            requests_per_minute = len(recent_requests)
            
            # Requests per hour
            hour_ago = current_time - timedelta(hours=1)
            hourly_requests = [req_time for req_time in self.request_times if req_time > hour_ago]
            requests_per_hour = len(hourly_requests)
            
            # Average delay
            avg_delay = (self.stats['total_delay_time'] / 
                        max(self.stats['delayed_requests'], 1))
            
            return {
                'requests_per_minute': requests_per_minute,
                'requests_per_hour': requests_per_hour,
                'consecutive_failures': self.consecutive_failures,
                'average_delay': avg_delay,
                'current_delay': self.current_delay
            }
    
    def get_statistics(self) -> Dict[str, Any]:
        """
        Get rate limiting statistics.
        
        Returns:
            Dictionary containing rate limiting statistics
        """
        frequency_stats = self.get_request_frequency()
        
        return {
            **self.stats,
            **frequency_stats,
            'config': {
                'min_delay': self.config.min_delay,
                'max_delay': self.config.max_delay,
                'strategy': self.config.strategy.value,
                'max_requests_per_minute': self.config.max_requests_per_minute,
                'max_requests_per_hour': self.config.max_requests_per_hour
            }
        }
    
    def reset_statistics(self):
        """Reset rate limiting statistics."""
        with self.lock:
            self.stats = {
                'total_requests': 0,
                'delayed_requests': 0,
                'total_delay_time': 0.0,
                'rate_limit_hits': 0,
                'adaptive_adjustments': 0
            }
            self.consecutive_failures = 0
            self.current_delay = self.config.min_delay
            logger.info("Rate limiting statistics reset")
    
    def update_config(self, new_config: RateLimitConfig):
        """
        Update rate limiting configuration.
        
        Args:
            new_config: New rate limiting configuration
        """
        with self.lock:
            self.config = new_config
            logger.info(f"Updated rate limiting configuration: {new_config}")
    
    def is_rate_limited(self) -> bool:
        """
        Check if currently rate limited.
        
        Returns:
            True if rate limited, False otherwise
        """
        current_time = datetime.now()
        
        with self.lock:
            # Check minute-based rate limit
            minute_ago = current_time - timedelta(minutes=1)
            recent_requests = [req_time for req_time in self.request_times if req_time > minute_ago]
            
            if len(recent_requests) >= self.config.max_requests_per_minute:
                return True
            
            # Check hour-based rate limit
            hour_ago = current_time - timedelta(hours=1)
            hourly_requests = [req_time for req_time in self.request_times if req_time > hour_ago]
            
            if len(hourly_requests) >= self.config.max_requests_per_hour:
                return True
            
            return False

class AdaptiveRateLimiter(RateLimiter):
    """
    Enhanced rate limiter with machine learning-based adaptive behavior.
    """
    
    def __init__(self, config: Optional[RateLimitConfig] = None):
        """Initialize the adaptive rate limiter."""
        super().__init__(config)
        self.success_history: List[float] = []
        self.failure_history: List[float] = []
        self.performance_window = 100  # Number of requests to consider for adaptation
        
        logger.info("Initialized AdaptiveRateLimiter")
    
    def _calculate_adaptive_delay(self) -> float:
        """
        Enhanced adaptive delay calculation using historical performance.
        """
        current_time = datetime.now()
        
        # Get recent request history
        recent_requests = [req_time for req_time in self.request_times 
                          if req_time > current_time - timedelta(minutes=10)]
        
        # Base delay from parent class
        base_delay = super()._calculate_adaptive_delay()
        
        # Adjust based on success/failure patterns
        if len(self.success_history) > 10:
            recent_success_rate = sum(self.success_history[-10:]) / 10
            
            if recent_success_rate > 0.9:  # High success rate
                # Can be more aggressive
                multiplier = 0.8
            elif recent_success_rate > 0.7:  # Good success rate
                multiplier = 1.0
            else:  # Low success rate
                # Be more conservative
                multiplier = 1.5
            
            adaptive_delay = base_delay * multiplier
            logger.debug(f"Adaptive delay: {base_delay:.2f} * {multiplier:.2f} = {adaptive_delay:.2f}")
            
            return min(adaptive_delay, self.config.max_backoff_delay)
        
        return base_delay
    
    def record_success(self):
        """Record a successful request with timestamp."""
        super().record_success()
        self.success_history.append(1.0)
        self.failure_history.append(0.0)
        self._trim_history()
    
    def record_failure(self):
        """Record a failed request with timestamp."""
        super().record_failure()
        self.success_history.append(0.0)
        self.failure_history.append(1.0)
        self._trim_history()
    
    def _trim_history(self):
        """Keep only recent history within the performance window."""
        if len(self.success_history) > self.performance_window:
            self.success_history = self.success_history[-self.performance_window:]
            self.failure_history = self.failure_history[-self.performance_window:]

# Usage example
if __name__ == "__main__":
    # Set up logging
    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Example usage
    config = RateLimitConfig(
        min_delay=1.0,
        max_delay=3.0,
        strategy=RateLimitStrategy.ADAPTIVE,
        max_requests_per_minute=15,
        max_requests_per_hour=300
    )
    
    rate_limiter = AdaptiveRateLimiter(config)
    
    # Simulate some requests
    for i in range(10):
        delay = rate_limiter.wait_if_needed()
        print(f"Request {i + 1}: waited {delay:.2f} seconds")
        
        # Simulate some failures
        if i % 3 == 0:
            rate_limiter.record_failure()
        else:
            rate_limiter.record_success()
        
        time.sleep(0.1)  # Small delay for demonstration
    
    # Print statistics
    stats = rate_limiter.get_statistics()
    print(f"\nRate limiting statistics: {stats}")
    
    # Print frequency info
    frequency = rate_limiter.get_request_frequency()
    print(f"Request frequency: {frequency}")
