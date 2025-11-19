# api/analytics_api.py

from fastapi import FastAPI, Request, Depends
from pydantic import BaseModel
import json
import uvicorn
import sys
import os
from datetime import date, datetime, timedelta
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from services.usage_tracking_service import usage_tracker

class DateRangeRequest(BaseModel):
    start_date: Optional[str] = None
    end_date: Optional[str] = None

class AnalyticsAPI:
    def __init__(self):
        self.app = FastAPI()
        self.setup_cors()
        self.setup_routes()

    def setup_cors(self):
        # Get allowed origins from environment variable or use default
        allowed_origins = os.getenv('ALLOWED_ORIGINS', '*').split(',')
        
        # If no specific origins are set, default to allowing all
        if not allowed_origins or (len(allowed_origins) == 1 and allowed_origins[0] == '*'):
            allowed_origins = ["*"]
        else:
            # Add localhost for development
            allowed_origins.extend(["http://localhost:5173", "http://localhost:5174"])

        self.app.add_middleware(
            CORSMiddleware,
            allow_origins=allowed_origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        

    def setup_routes(self):
        @self.app.get("/analytics/daily")
        async def get_daily_analytics(target_date: Optional[str] = None):
            """Get analytics for a specific date"""
            try:
                if target_date:
                    target_date_obj = date.fromisoformat(target_date)
                else:
                    target_date_obj = date.today()
                
                stats = usage_tracker.get_daily_usage_stats(target_date_obj)
                return JSONResponse(content=stats)
                
            except ValueError as e:
                return JSONResponse(
                    status_code=400,
                    content={"error": f"Invalid date format: {str(e)}"}
                )
            except Exception as e:
                return JSONResponse(
                    status_code=500,
                    content={"error": str(e)}
                )

        @self.app.post("/analytics/range")
        async def get_range_analytics(request: DateRangeRequest):
            """Get analytics for a date range"""
            try:
                # Default to last 7 days if no dates provided
                if not request.start_date or not request.end_date:
                    end_date = date.today()
                    start_date = end_date - timedelta(days=7)
                else:
                    start_date = date.fromisoformat(request.start_date)
                    end_date = date.fromisoformat(request.end_date)
                
                # Validate date range
                if start_date > end_date:
                    return JSONResponse(
                        status_code=400,
                        content={"error": "Start date cannot be after end date"}
                    )
                
                stats = usage_tracker.get_usage_range_stats(start_date, end_date)
                return JSONResponse(content=stats)
                
            except ValueError as e:
                return JSONResponse(
                    status_code=400,
                    content={"error": f"Invalid date format: {str(e)}"}
                )
            except Exception as e:
                return JSONResponse(
                    status_code=500,
                    content={"error": str(e)}
                )

        @self.app.get("/analytics/health")
        async def health_check():
            """Health check endpoint"""
            return {"status": "healthy", "service": "Analytics API"}

def create_app():
    api = AnalyticsAPI()
    return api.app

if __name__ == "__main__":
    app = create_app()
    uvicorn.run(app, host="127.0.0.1", port=8002)