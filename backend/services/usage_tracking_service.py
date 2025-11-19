# services/usage_tracking_service.py

import json
import time
from datetime import datetime, date
from typing import Dict, List, Optional
from pathlib import Path
import uuid

class UsageTrackingService:
    def __init__(self, storage_path: str = "/tmp/sales-crew/backend/data"):
        """
        Initialize usage tracking service
        
        Args:
            storage_path: Path to store usage data
        """
        self.storage_path = Path(storage_path)
        self.storage_path.mkdir(parents=True, exist_ok=True)
        
    def _get_daily_file_path(self) -> Path:
        """Get file path for current day's usage data"""
        today = date.today().isoformat()
        return self.storage_path / f"usage_{today}.json"
    
    def _load_daily_data(self) -> Dict:
        """Load usage data for current day"""
        file_path = self._get_daily_file_path()
        if file_path.exists():
            with open(file_path, 'r') as f:
                return json.load(f)
        return {"date": date.today().isoformat(), "sessions": []}
    
    def _save_daily_data(self, data: Dict) -> None:
        """Save usage data for current day"""
        file_path = self._get_daily_file_path()
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def track_search_session(
        self, 
        user_id: str,
        query: str,
        api_keys_used: Dict[str, bool],
        result_count: int = 0,
        error: Optional[str] = None
    ) -> str:
        """
        Track a search session
        
        Args:
            user_id: User identifier
            query: Search query
            api_keys_used: Dictionary indicating which APIs were used
            result_count: Number of results returned
            error: Error message if any
            
        Returns:
            Session ID
        """
        session_id = str(uuid.uuid4())
        
        session_data = {
            "session_id": session_id,
            "user_id": user_id,
            "timestamp": datetime.now().isoformat(),
            "query": query,
            "api_keys_used": api_keys_used,
            "result_count": result_count,
            "error": error,
            "duration": None  # Will be updated when session ends
        }
        
        data = self._load_daily_data()
        data["sessions"].append(session_data)
        self._save_daily_data(data)
        
        return session_id
    
    def end_search_session(self, session_id: str, result_count: int = 0) -> None:
        """Mark a search session as completed"""
        data = self._load_daily_data()
        
        for session in data["sessions"]:
            if session["session_id"] == session_id:
                session["result_count"] = result_count
                session["duration"] = time.time() - datetime.fromisoformat(session["timestamp"]).timestamp()
                break
        
        self._save_daily_data(data)
    
    def get_daily_usage_stats(self, target_date: Optional[date] = None) -> Dict:
        """Get usage statistics for a specific date"""
        if target_date is None:
            target_date = date.today()
        
        file_path = self.storage_path / f"usage_{target_date.isoformat()}.json"
        if not file_path.exists():
            return {
                "date": target_date.isoformat(),
                "total_searches": 0,
                "successful_searches": 0,
                "failed_searches": 0,
                "total_results": 0,
                "average_results": 0,
                "api_usage": {},
                "user_activity": {}
            }
        
        with open(file_path, 'r') as f:
            data = json.load(f)
        
        stats = {
            "date": target_date.isoformat(),
            "total_searches": len(data["sessions"]),
            "successful_searches": 0,
            "failed_searches": 0,
            "total_results": 0,
            "average_results": 0,
            "api_usage": {},
            "user_activity": {}
        }
        
        for session in data["sessions"]:
            # Track user activity
            user_id = session["user_id"]
            stats["user_activity"][user_id] = stats["user_activity"].get(user_id, 0) + 1
            
            # Track API usage
            for api_name, used in session["api_keys_used"].items():
                if used:
                    stats["api_usage"][api_name] = stats["api_usage"].get(api_name, 0) + 1
            
            # Track success/failure
            if session.get("error"):
                stats["failed_searches"] += 1
            else:
                stats["successful_searches"] += 1
                stats["total_results"] += session.get("result_count", 0)
        
        if stats["successful_searches"] > 0:
            stats["average_results"] = stats["total_results"] / stats["successful_searches"]
        
        return stats
    
    def get_usage_range_stats(self, start_date: date, end_date: date) -> Dict:
        """Get usage statistics for a date range"""
        current_date = start_date
        daily_stats = []
        
        while current_date <= end_date:
            stats = self.get_daily_usage_stats(current_date)
            daily_stats.append(stats)
            current_date = date(
                current_date.year,
                current_date.month,
                current_date.day + 1
            )
        
        # Aggregate stats
        aggregated = {
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
            "total_searches": sum(day["total_searches"] for day in daily_stats),
            "successful_searches": sum(day["successful_searches"] for day in daily_stats),
            "failed_searches": sum(day["failed_searches"] for day in daily_stats),
            "total_results": sum(day["total_results"] for day in daily_stats),
            "daily_average": {},
            "api_usage": {},
            "user_activity": {}
        }
        
        # Calculate daily averages
        if daily_stats:
            aggregated["daily_average"] = {
                "searches": aggregated["total_searches"] / len(daily_stats),
                "results": aggregated["total_results"] / len(daily_stats)
            }
        
        # Aggregate API usage and user activity
        for day in daily_stats:
            for api_name, count in day["api_usage"].items():
                aggregated["api_usage"][api_name] = aggregated["api_usage"].get(api_name, 0) + count
            
            for user_id, count in day["user_activity"].items():
                aggregated["user_activity"][user_id] = aggregated["user_activity"].get(user_id, 0) + count
        
        return aggregated

# Singleton instance
usage_tracker = UsageTrackingService()