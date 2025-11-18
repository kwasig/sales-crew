# metrics_api.py

from fastapi import FastAPI, Request
from pydantic import BaseModel
import json
import uvicorn
import sys
import os
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import time
import asyncio
from datetime import datetime, timedelta

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

class MetricsRequest(BaseModel):
    user_id: str
    start_date: str = None
    end_date: str = None

class MetricsAPI:
    def __init__(self):
        self.app = FastAPI()
        self.setup_cors()
        self.setup_routes()
        self.metrics_data = {}

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
            allow_headers=["*", "x-sambanova-key", "x-exa-key"],
        )
        

    def setup_routes(self):
        @self.app.get("/metrics/usage")
        async def get_usage_metrics(user_id: str):
            """Get usage metrics for a specific user"""
            try:
                # In a real implementation, this would query a database
                # For now, we'll return mock data based on user_id
                
                # Generate mock usage data
                metrics = {
                    "user_id": user_id,
                    "total_searches": 15,
                    "total_companies_found": 127,
                    "average_response_time": 3.2,
                    "last_search_date": datetime.now().isoformat(),
                    "searches_this_week": 5,
                    "searches_this_month": 15,
                    "most_common_industry": "Technology",
                    "most_common_geography": "United States",
                    "success_rate": 0.87,
                    "api_calls_today": 8,
                    "api_calls_this_month": 45
                }
                
                return JSONResponse(content=metrics)
                
            except Exception as e:
                return JSONResponse(
                    status_code=500,
                    content={"error": f"Failed to get usage metrics: {str(e)}"}
                )

        @self.app.get("/metrics/performance")
        async def get_performance_metrics():
            """Get system performance metrics"""
            try:
                # Mock performance data
                performance = {
                    "system_status": "Healthy",
                    "uptime": "99.8%",
                    "average_response_time": 2.1,
                    "active_agents": 4,
                    "total_agents": 5,
                    "memory_usage": "65%",
                    "cpu_usage": "42%",
                    "disk_usage": "78%",
                    "requests_per_minute": 12,
                    "error_rate": 0.02,
                    "last_updated": datetime.now().isoformat()
                }
                
                return JSONResponse(content=performance)
                
            except Exception as e:
                return JSONResponse(
                    status_code=500,
                    content={"error": f"Failed to get performance metrics: {str(e)}"}
                )

        @self.app.get("/metrics/quality")
        async def get_quality_metrics(user_id: str):
            """Get quality metrics for generated content"""
            try:
                # Mock quality metrics
                quality = {
                    "user_id": user_id,
                    "average_relevance_score": 4.2,
                    "email_personalization_quality": 4.5,
                    "market_analysis_accuracy": 4.1,
                    "financial_insights_depth": 3.9,
                    "overall_satisfaction": 4.3,
                    "total_ratings": 12,
                    "positive_feedback_count": 10,
                    "suggestions_for_improvement": [
                        "More detailed financial analysis",
                        "Better contact information accuracy"
                    ]
                }
                
                return JSONResponse(content=quality)
                
            except Exception as e:
                return JSONResponse(
                    status_code=500,
                    content={"error": f"Failed to get quality metrics: {str(e)}"}
                )

        @self.app.post("/metrics/log-search")
        async def log_search(request: Request):
            """Log a search for metrics tracking"""
            try:
                body = await request.json()
                
                # Extract search data
                user_id = body.get("user_id")
                query = body.get("query")
                results_count = body.get("results_count", 0)
                execution_time = body.get("execution_time", 0)
                
                # In a real implementation, this would store in a database
                # For now, we'll just return success
                
                log_entry = {
                    "user_id": user_id,
                    "query": query,
                    "results_count": results_count,
                    "execution_time": execution_time,
                    "timestamp": datetime.now().isoformat()
                }
                
                # Store in memory (in production, use a database)
                if user_id not in self.metrics_data:
                    self.metrics_data[user_id] = []
                self.metrics_data[user_id].append(log_entry)
                
                # Keep only last 1000 entries per user to prevent memory issues
                if len(self.metrics_data[user_id]) > 1000:
                    self.metrics_data[user_id] = self.metrics_data[user_id][-1000:]
                
                return JSONResponse(content={"status": "success", "logged": True})
                
            except Exception as e:
                return JSONResponse(
                    status_code=500,
                    content={"error": f"Failed to log search: {str(e)}"}
                )

def create_app():
    api = MetricsAPI()
    return api.app

if __name__ == "__main__":
    app = create_app()
    uvicorn.run(app, host="127.0.0.1", port=8001)