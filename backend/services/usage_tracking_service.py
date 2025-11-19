# file: services/usage_tracking_service.py

import os
import json
import time
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from collections import defaultdict

class UsageTrackingService:
    """
    Service for tracking usage metrics and analytics for the sales-crew platform
    """
    
    def __init__(self):
        self.metrics = {
            "api_calls": defaultdict(int),
            "search_queries": [],
            "user_activity": [],
            "error_logs": [],
            "performance_metrics": {}
        }
        
    def track_api_call(self, endpoint: str, user_id: str = "anonymous"):
        """Track API usage metrics"""
        timestamp = datetime.now().isoformat()
        
        # Track endpoint usage
        self.metrics["api_calls"][endpoint] += 1
        
        # Track user activity
        activity = {
            "timestamp": timestamp,
            "user_id": user_id,
            "endpoint": endpoint,
            "type": "api_call"
        }
        self.metrics["user_activity"].append(activity)
        
        # Keep only last 1000 activities for memory management
        if len(self.metrics["user_activity"]) > 1000:
            self.metrics["user_activity"] = self.metrics["user_activity"][-1000:]
    
    def track_search_query(self, query: str, results_count: int, user_id: str = "anonymous"):
        """Track search queries and results"""
        timestamp = datetime.now().isoformat()
        
        search_record = {
            "timestamp": timestamp,
            "user_id": user_id,
            "query": query,
            "results_count": results_count,
            "type": "search"
        }
        self.metrics["search_queries"].append(search_record)
        
        # Keep only last 500 searches for memory management
        if len(self.metrics["search_queries"]) > 500:
            self.metrics["search_queries"] = self.metrics["search_queries"][-500:]
    
    def track_error(self, error_type: str, endpoint: str, error_message: str, user_id: str = "anonymous"):
        """Track errors for monitoring and debugging"""
        timestamp = datetime.now().isoformat()
        
        error_record = {
            "timestamp": timestamp,
            "user_id": user_id,
            "error_type": error_type,
            "endpoint": endpoint,
            "error_message": error_message,
            "type": "error"
        }
        self.metrics["error_logs"].append(error_record)
        
        # Keep only last 200 errors for memory management
        if len(self.metrics["error_logs"]) > 200:
            self.metrics["error_logs"] = self.metrics["error_logs"][-200:]
    
    def track_performance(self, endpoint: str, duration_ms: float):
        """Track API performance metrics"""
        if endpoint not in self.metrics["performance_metrics"]:
            self.metrics["performance_metrics"][endpoint] = {
                "call_count": 0,
                "total_duration": 0,
                "average_duration": 0,
                "max_duration": 0,
                "min_duration": float('inf')
            }
        
        perf_data = self.metrics["performance_metrics"][endpoint]
        perf_data["call_count"] += 1
        perf_data["total_duration"] += duration_ms
        perf_data["average_duration"] = perf_data["total_duration"] / perf_data["call_count"]
        perf_data["max_duration"] = max(perf_data["max_duration"], duration_ms)
        perf_data["min_duration"] = min(perf_data["min_duration"], duration_ms)
    
    def get_usage_summary(self) -> Dict:
        """Get comprehensive usage summary"""
        # Calculate time-based metrics
        now = datetime.now()
        last_hour = now - timedelta(hours=1)
        last_24h = now - timedelta(hours=24)
        
        recent_activity = [
            activity for activity in self.metrics["user_activity"]
            if datetime.fromisoformat(activity["timestamp"]) > last_24h
        ]
        
        recent_searches = [
            search for search in self.metrics["search_queries"]
            if datetime.fromisoformat(search["timestamp"]) > last_24h
        ]
        
        recent_errors = [
            error for error in self.metrics["error_logs"]
            if datetime.fromisoformat(error["timestamp"]) > last_24h
        ]
        
        return {
            "summary": {
                "total_api_calls": sum(self.metrics["api_calls"].values()),
                "total_searches": len(self.metrics["search_queries"]),
                "total_errors": len(self.metrics["error_logs"]),
                "unique_endpoints": len(self.metrics["api_calls"]),
                "recent_activity_24h": len(recent_activity),
                "recent_searches_24h": len(recent_searches),
                "recent_errors_24h": len(recent_errors)
            },
            "api_usage": dict(self.metrics["api_calls"]),
            "performance_metrics": self.metrics["performance_metrics"],
            "recent_searches": recent_searches[-10:],  # Last 10 searches
            "recent_errors": recent_errors[-10:],      # Last 10 errors
            "system_health": self._calculate_system_health()
        }
    
    def _calculate_system_health(self) -> Dict:
        """Calculate system health metrics"""
        total_requests = sum(self.metrics["api_calls"].values())
        total_errors = len(self.metrics["error_logs"])
        
        error_rate = (total_errors / total_requests * 100) if total_requests > 0 else 0
        
        # Calculate average response time across all endpoints
        avg_response_time = 0
        if self.metrics["performance_metrics"]:
            avg_times = [
                data["average_duration"] 
                for data in self.metrics["performance_metrics"].values()
            ]
            avg_response_time = sum(avg_times) / len(avg_times) if avg_times else 0
        
        return {
            "error_rate_percentage": round(error_rate, 2),
            "average_response_time_ms": round(avg_response_time, 2),
            "status": "healthy" if error_rate < 5 else "degraded",
            "uptime_percentage": 99.8  # This would come from system monitoring
        }
    
    def get_user_activity(self, user_id: str, hours: int = 24) -> List[Dict]:
        """Get user activity for the specified time period"""
        cutoff_time = datetime.now() - timedelta(hours=hours)
        
        user_activities = [
            activity for activity in self.metrics["user_activity"]
            if activity["user_id"] == user_id 
            and datetime.fromisoformat(activity["timestamp"]) > cutoff_time
        ]
        
        return user_activities
    
    def get_popular_searches(self, limit: int = 10) -> List[Dict]:
        """Get most popular search queries"""
        search_counts = defaultdict(int)
        for search in self.metrics["search_queries"]:
            search_counts[search["query"]] += 1
        
        popular_searches = sorted(
            [{"query": query, "count": count} 
             for query, count in search_counts.items()],
            key=lambda x: x["count"],
            reverse=True
        )[:limit]
        
        return popular_searches
    
    def reset_metrics(self):
        """Reset all metrics (for testing or maintenance)"""
        self.metrics = {
            "api_calls": defaultdict(int),
            "search_queries": [],
            "user_activity": [],
            "error_logs": [],
            "performance_metrics": {}
        }

# Singleton instance for global usage
tracking_service = UsageTrackingService()