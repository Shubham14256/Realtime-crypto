"""
Rate limiting and advanced middleware for the cryptocurrency server
"""

from datetime import datetime, timedelta, timezone
from typing import Dict, List
from collections import deque
import time

class RateLimiter:
    """Token bucket rate limiter"""
    
    def __init__(self, requests_per_minute: int = 60):
        self.requests_per_minute = requests_per_minute
        self.requests: Dict[str, deque] = {}
        self.cleanup_interval = 300  # seconds
        self.last_cleanup = time.time()
    
    def is_allowed(self, client_id: str) -> tuple[bool, Dict]:
        """Check if request is allowed for client"""
        now = time.time()
        
        # Cleanup old entries periodically
        if now - self.last_cleanup > self.cleanup_interval:
            self._cleanup_old_entries(now)
            self.last_cleanup = now
        
        # Initialize client if needed
        if client_id not in self.requests:
            self.requests[client_id] = deque()
        
        # Remove old requests outside the window
        minute_ago = now - 60
        while self.requests[client_id] and self.requests[client_id][0] < minute_ago:
            self.requests[client_id].popleft()
        
        # Check if limit exceeded
        if len(self.requests[client_id]) >= self.requests_per_minute:
            return False, self._get_retry_after(client_id)
        
        # Add current request
        self.requests[client_id].append(now)
        
        return True, {
            "limit": self.requests_per_minute,
            "remaining": self.requests_per_minute - len(self.requests[client_id]),
            "reset": int(now + 60)
        }
    
    def _cleanup_old_entries(self, now: float):
        """Remove old entries to save memory"""
        keys_to_delete = []
        for client_id, requests in self.requests.items():
            minute_ago = now - 60
            while requests and requests[0] < minute_ago:
                requests.popleft()
            if not requests:
                keys_to_delete.append(client_id)
        
        for key in keys_to_delete:
            del self.requests[key]
    
    def _get_retry_after(self, client_id: str) -> Dict:
        """Calculate retry-after time"""
        if self.requests[client_id]:
            oldest = self.requests[client_id][0]
            retry_after = int(oldest + 60 - time.time()) + 1
            return {
                "error": "Rate limit exceeded",
                "retry_after": max(1, retry_after),
                "limit": self.requests_per_minute
            }
        return {"error": "Rate limit exceeded"}


class PerformanceMonitor:
    """Monitor and track API performance metrics"""
    
    def __init__(self, window_size: int = 100):
        self.window_size = window_size
        self.endpoint_metrics: Dict[str, Dict] = {}
        self.response_times: Dict[str, deque] = {}
    
    def record_request(self, endpoint: str, response_time: float, status_code: int):
        """Record request metrics"""
        if endpoint not in self.endpoint_metrics:
            self.endpoint_metrics[endpoint] = {
                "total_requests": 0,
                "success_count": 0,
                "error_count": 0,
                "avg_response_time": 0,
                "min_response_time": float('inf'),
                "max_response_time": 0,
                "last_updated": None
            }
            self.response_times[endpoint] = deque(maxlen=self.window_size)
        
        metrics = self.endpoint_metrics[endpoint]
        metrics["total_requests"] += 1
        
        if 200 <= status_code < 300:
            metrics["success_count"] += 1
        else:
            metrics["error_count"] += 1
        
        # Track response times
        self.response_times[endpoint].append(response_time)
        
        # Calculate statistics
        times = list(self.response_times[endpoint])
        metrics["avg_response_time"] = sum(times) / len(times) if times else 0
        metrics["min_response_time"] = min(times) if times else 0
        metrics["max_response_time"] = max(times) if times else 0
        metrics["last_updated"] = datetime.now(timezone.utc).isoformat()
    
    def get_metrics(self, endpoint: str = None) -> Dict:
        """Get performance metrics"""
        if endpoint:
            return self.endpoint_metrics.get(endpoint, {})
        return self.endpoint_metrics
    
    def get_health_score(self) -> Dict:
        """Calculate overall health score (0-100)"""
        if not self.endpoint_metrics:
            return {"health_score": 100, "status": "healthy"}
        
        total_requests = sum(m["total_requests"] for m in self.endpoint_metrics.values())
        total_errors = sum(m["error_count"] for m in self.endpoint_metrics.values())
        
        if total_requests == 0:
            return {"health_score": 100, "status": "healthy"}
        
        success_rate = (total_requests - total_errors) / total_requests * 100
        health_score = success_rate
        
        if health_score >= 95:
            status = "healthy"
        elif health_score >= 80:
            status = "degraded"
        else:
            status = "unhealthy"
        
        return {
            "health_score": round(health_score, 2),
            "status": status,
            "total_requests": total_requests,
            "total_errors": total_errors,
            "success_rate": round(success_rate, 2)
        }


class CacheAnalytics:
    """Analyze cache performance"""
    
    def __init__(self):
        self.hit_count = 0
        self.miss_count = 0
        self.total_saved_ms = 0.0
    
    def record_hit(self, saved_ms: float = 100):
        """Record cache hit"""
        self.hit_count += 1
        self.total_saved_ms += saved_ms
    
    def record_miss(self):
        """Record cache miss"""
        self.miss_count += 1
    
    def get_stats(self) -> Dict:
        """Get cache statistics"""
        total = self.hit_count + self.miss_count
        hit_rate = (self.hit_count / total * 100) if total > 0 else 0
        
        return {
            "hits": self.hit_count,
            "misses": self.miss_count,
            "total": total,
            "hit_rate": round(hit_rate, 2),
            "total_time_saved_ms": round(self.total_saved_ms, 2),
            "avg_time_saved_per_hit_ms": round(self.total_saved_ms / self.hit_count, 2) if self.hit_count > 0 else 0
        }
