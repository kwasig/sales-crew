# usage_api.py

from fastapi import APIRouter, Request
from datetime import datetime, timedelta
import json
import os
from pathlib import Path

router = APIRouter()

class UsageMetricsService:
    def __init__(self):
        self.metrics_dir = Path("usage_metrics")
        self.metrics_dir.mkdir(exist_ok=True)
    
    def log_usage(self, user_id: str, endpoint: str, duration: float, success: bool):
        """Log usage metrics for a user"""
        try:
            # Create user-specific metrics file
            user_file = self.metrics_dir / f"{user_id}.json"
            
            # Load existing metrics or create new
            if user_file.exists():
                with open(user_file, 'r') as f:
                    metrics = json.load(f)
            else:
                metrics = {
                    "user_id": user_id,
                    "total_requests": 0,
                    "successful_requests": 0,
                    "total_duration": 0,
                    "avg_response_time": 0,
                    "requests_by_endpoint": {},
                    "daily_usage": {},
                    "last_updated": datetime.now().isoformat()
                }
            
            # Update metrics
            today = datetime.now().strftime("%Y-%m-%d")
            metrics["total_requests"] += 1
            metrics["total_duration"] += duration
            metrics["avg_response_time"] = metrics["total_duration"] / metrics["total_requests"]
            
            if success:
                metrics["successful_requests"] += 1
            
            # Update endpoint-specific metrics
            if endpoint not in metrics["requests_by_endpoint"]:
                metrics["requests_by_endpoint"][endpoint] = {
                    "count": 0,
                    "total_duration": 0,
                    "successful": 0
                }
            metrics["requests_by_endpoint"][endpoint]["count"] += 1
            metrics["requests_by_endpoint"][endpoint]["total_duration"] += duration
            if success:
                metrics["requests_by_endpoint"][endpoint]["successful"] += 1
            
            # Update daily usage
            if today not in metrics["daily_usage"]:
                metrics["daily_usage"][today] = {
                    "requests": 0,
                    "duration": 0,
                    "successful": 0
                }
            metrics["daily_usage"][today]["requests"] += 1
            metrics["daily_usage"][today]["duration"] += duration
            if success:
                metrics["daily_usage"][today]["successful"] += 1
            
            metrics["last_updated"] = datetime.now().isoformat()
            
            # Save updated metrics
            with open(user_file, 'w') as f:
                json.dump(metrics, f, indent=2)
            
            return True
        except Exception as e:
            print(f"Error logging usage: {e}")
            return False
    
    def get_user_metrics(self, user_id: str):
        """Get usage metrics for a user"""
        try:
            user_file = self.metrics_dir / f"{user_id}.json"
            if not user_file.exists():
                return self._get_default_metrics(user_id)
            
            with open(user_file, 'r') as f:
                metrics = json.load(f)
            
            # Calculate additional derived metrics
            metrics["success_rate"] = (metrics["successful_requests"] / metrics["total_requests"]) * 100 if metrics["total_requests"] > 0 else 0
            
            # Get today's usage
            today = datetime.now().strftime("%Y-%m-%d")
            metrics["today_requests"] = metrics["daily_usage"].get(today, {"requests": 0})["requests"]
            
            return metrics
        except Exception as e:
            print(f"Error getting user metrics: {e}")
            return self._get_default_metrics(user_id)
    
    def _get_default_metrics(self, user_id: str):
        """Return default metrics structure for new users"""
        return {
            "user_id": user_id,
            "total_requests": 0,
            "successful_requests": 0,
            "total_duration": 0,
            "avg_response_time": 0,
            "success_rate": 0,
            "today_requests": 0,
            "requests_by_endpoint": {},
            "daily_usage": {},
            "last_updated": datetime.now().isoformat()
        }

# Global instance
usage_service = UsageMetricsService()

@router.get("/metrics/{user_id}")
async def get_metrics(user_id: str):
    """Get usage metrics for a specific user"""
    try:
        metrics = usage_service.get_user_metrics(user_id)
        return {"success": True, "data": metrics}
    except Exception as e:
        return {"success": False, "error": str(e)}

@router.get("/metrics/{user_id}/summary")
async def get_metrics_summary(user_id: str):
    """Get a summary of usage metrics for a specific user"""
    try:
        metrics = usage_service.get_user_metrics(user_id)
        summary = {
            "total_searches": metrics["total_requests"],
            "searches_today": metrics["today_requests"],
            "avg_response_time": round(metrics["avg_response_time"], 1),
            "success_rate": round(metrics["success_rate"], 1)
        }
        return {"success": True, "data": summary}
    except Exception as e:
        return {"success": False, "error": str(e)}

# Middleware function to log usage
async def log_usage_middleware(request: Request, call_next):
    """Middleware to log API usage"""
    start_time = datetime.now()
    
    # Process the request
    response = await call_next(request)
    
    # Calculate duration
    duration = (datetime.now() - start_time).total_seconds()
    
    # Extract user ID from request (you might need to adjust this based on your auth)
    user_id = request.headers.get("x-user-id", "anonymous")
    
    # Log the usage
    success = response.status_code < 400
    usage_service.log_usage(
        user_id=user_id,
        endpoint=request.url.path,
        duration=duration,
        success=success
    )
    
    return response