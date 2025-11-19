"""
Dashboard API for Sales Crew Application
Provides endpoints for usage analytics and dashboard data
"""

from fastapi import APIRouter, HTTPException
from typing import Dict
import logging

from services.usage_tracking_service import usage_tracker
from services.financial_analysis_service import FinancialAnalysisService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/dashboard", tags=["dashboard"])

@router.get("/metrics")
async def get_dashboard_metrics() -> Dict:
    """Get comprehensive dashboard metrics"""
    try:
        metrics = usage_tracker.get_dashboard_metrics()
        return {
            "status": "success",
            "data": metrics
        }
    except Exception as e:
        logger.error(f"Error fetching dashboard metrics: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch dashboard metrics")

@router.get("/analytics/{days}")
async def get_usage_analytics(days: int) -> Dict:
    """Get usage analytics for specified number of days"""
    try:
        if days <= 0 or days > 365:
            raise HTTPException(status_code=400, detail="Days must be between 1 and 365")
        
        analytics = usage_tracker.get_usage_analytics(days)
        return {
            "status": "success",
            "data": analytics
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching usage analytics: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch usage analytics")

@router.get("/financial-insights")
async def get_financial_insights() -> Dict:
    """Get financial insights and analysis summary"""
    try:
        # This would integrate with the financial analysis service
        # For now, return a placeholder structure
        return {
            "status": "success",
            "data": {
                "total_analyses": 0,  # Would be tracked by financial service
                "average_sentiment": "neutral",
                "top_industries": [],
                "recent_analyses": []
            }
        }
    except Exception as e:
        logger.error(f"Error fetching financial insights: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to fetch financial insights")

@router.post("/session/start")
async def start_session() -> Dict:
    """Start a new user session for tracking"""
    try:
        session_id = usage_tracker.start_session()
        return {
            "status": "success",
            "data": {
                "session_id": session_id
            }
        }
    except Exception as e:
        logger.error(f"Error starting session: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to start session")

@router.post("/search/track")
async def track_search(session_id: str, company_name: str, success: bool = True) -> Dict:
    """Track a search operation"""
    try:
        usage_tracker.track_search(session_id, company_name, {}, success)
        return {
            "status": "success",
            "message": "Search tracked successfully"
        }
    except Exception as e:
        logger.error(f"Error tracking search: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to track search")