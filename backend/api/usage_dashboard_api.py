# file: api/usage_dashboard_api.py

import os
import sys
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from fastapi import APIRouter, HTTPException

# Import the usage tracking service
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from services.usage_tracking_service import tracking_service

router = APIRouter(prefix="/api/usage", tags=["Usage Dashboard"])

@router.get("/summary")
async def get_usage_summary():
    """Get comprehensive usage summary"""
    try:
        summary = tracking_service.get_usage_summary()
        return {
            "success": True,
            "data": summary,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching usage summary: {str(e)}")

@router.get("/user/{user_id}/activity")
async def get_user_activity(user_id: str, hours: int = 24):
    """Get user activity for the specified time period"""
    try:
        if hours > 168:  # Limit to 1 week max
            hours = 168
            
        activities = tracking_service.get_user_activity(user_id, hours)
        return {
            "success": True,
            "data": {
                "user_id": user_id,
                "hours": hours,
                "activity_count": len(activities),
                "activities": activities
            },
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching user activity: {str(e)}")

@router.get("/searches/popular")
async def get_popular_searches(limit: int = 10):
    """Get most popular search queries"""
    try:
        if limit > 50:  # Limit to 50 max
            limit = 50
            
        popular_searches = tracking_service.get_popular_searches(limit)
        return {
            "success": True,
            "data": {
                "limit": limit,
                "popular_searches": popular_searches
            },
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching popular searches: {str(e)}")

@router.get("/health")
async def get_system_health():
    """Get system health metrics"""
    try:
        summary = tracking_service.get_usage_summary()
        health_data = summary.get("system_health", {})
        
        return {
            "success": True,
            "data": health_data,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching system health: {str(e)}")

@router.get("/metrics/performance")
async def get_performance_metrics():
    """Get detailed performance metrics"""
    try:
        summary = tracking_service.get_usage_summary()
        performance_data = summary.get("performance_metrics", {})
        
        return {
            "success": True,
            "data": performance_data,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching performance metrics: {str(e)}")

@router.get("/analytics/daily")
async def get_daily_analytics():
    """Get daily analytics breakdown"""
    try:
        # Calculate daily activity for the last 7 days
        now = datetime.now()
        daily_data = {}
        
        for i in range(7):
            date = (now - timedelta(days=i)).strftime("%Y-%m-%d")
            daily_data[date] = {
                "api_calls": 0,
                "searches": 0,
                "errors": 0
            }
        
        # Count activities by date
        for activity in tracking_service.metrics["user_activity"]:
            activity_date = datetime.fromisoformat(activity["timestamp"][:10])
            date_str = activity_date.strftime("%Y-%m-%d")
            if date_str in daily_data:
                daily_data[date_str]["api_calls"] += 1
        
        for search in tracking_service.metrics["search_queries"]:
            search_date = datetime.fromisoformat(search["timestamp"][:10])
            date_str = search_date.strftime("%Y-%m-%d")
            if date_str in daily_data:
                daily_data[date_str]["searches"] += 1
        
        for error in tracking_service.metrics["error_logs"]:
            error_date = datetime.fromisoformat(error["timestamp"][:10])
            date_str = error_date.strftime("%Y-%m-%d")
            if date_str in daily_data:
                daily_data[date_str]["errors"] += 1
        
        # Convert to list format for easier charting
        analytics_list = [
            {"date": date, **metrics} 
            for date, metrics in daily_data.items()
        ]
        analytics_list.reverse()  # Most recent first
        
        return {
            "success": True,
            "data": {
                "period": "7_days",
                "analytics": analytics_list
            },
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error fetching daily analytics: {str(e)}")

@router.post("/track/activity")
async def track_activity(activity_data: Dict):
    """Track custom activity (for frontend integration)"""
    try:
        # Validate required fields
        required_fields = ["user_id", "activity_type", "endpoint"]
        for field in required_fields:
            if field not in activity_data:
                raise HTTPException(status_code=400, detail=f"Missing required field: {field}")
        
        # Track the activity
        tracking_service.track_api_call(
            endpoint=activity_data["endpoint"],
            user_id=activity_data["user_id"]
        )
        
        return {
            "success": True,
            "message": "Activity tracked successfully",
            "timestamp": datetime.now().isoformat()
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error tracking activity: {str(e)}")

@router.delete("/reset")
async def reset_metrics():
    """Reset all usage metrics (admin only)"""
    try:
        tracking_service.reset_metrics()
        return {
            "success": True,
            "message": "Usage metrics reset successfully",
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error resetting metrics: {str(e)}")