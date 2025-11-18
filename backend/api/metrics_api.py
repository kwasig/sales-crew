# metrics_api.py

from fastapi import FastAPI, Request, BackgroundTasks
from pydantic import BaseModel
import json
import uvicorn
import sys
import os
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import time
import asyncio
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
import uuid

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

# In-memory storage for metrics (in production, use a database)
metrics_data = {
    "total_searches": 0,
    "today_usage": 0,
    "recent_activity": [],
    "performance_stats": {
        "average_response_time": 0,
        "success_rate": 100,
        "total_errors": 0
    },
    "agent_usage": {
        "lead_generation": 0,
        "financial_analysis": 0
    }
}

class MetricsRequest(BaseModel):
    user_id: str
    action: str
    duration: float = 0
    success: bool = True

class MetricsAPI:
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
            allow_headers=["*", "x-sambanova-key", "x-exa-key"],
        )
        
    def setup_routes(self):
        @self.app.post("/track-usage")
        async def track_usage(request: Request):
            try:
                body = await request.json()
                user_id = body.get("user_id", "anonymous")
                action = body.get("action", "unknown")
                duration = body.get("duration", 0)
                success = body.get("success", True)

                # Update metrics
                metrics_data["total_searches"] += 1
                
                # Check if today's usage needs reset
                current_date = datetime.now().date()
                if not hasattr(metrics_data, 'last_reset_date'):
                    metrics_data['last_reset_date'] = current_date
                    metrics_data["today_usage"] = 0
                elif metrics_data['last_reset_date'] != current_date:
                    metrics_data['last_reset_date'] = current_date
                    metrics_data["today_usage"] = 0
                
                metrics_data["today_usage"] += 1
                
                # Add to recent activity
                activity_entry = {
                    "id": str(uuid.uuid4()),
                    "user_id": user_id,
                    "action": action,
                    "timestamp": datetime.now().isoformat(),
                    "duration": duration,
                    "success": success
                }
                metrics_data["recent_activity"].insert(0, activity_entry)
                
                # Keep only last 20 activities
                metrics_data["recent_activity"] = metrics_data["recent_activity"][:20]
                
                # Update agent usage
                if action == "lead_generation":
                    metrics_data["agent_usage"]["lead_generation"] += 1
                elif action == "financial_analysis":
                    metrics_data["agent_usage"]["financial_analysis"] += 1
                
                # Update performance stats
                if not success:
                    metrics_data["performance_stats"]["total_errors"] += 1
                
                total_requests = metrics_data["total_searches"]
                total_errors = metrics_data["performance_stats"]["total_errors"]
                metrics_data["performance_stats"]["success_rate"] = (
                    (total_requests - total_errors) / total_requests * 100 
                    if total_requests > 0 else 100
                )
                
                return JSONResponse(content={"status": "success"})
                
            except Exception as e:
                return JSONResponse(
                    status_code=500,
                    content={"error": str(e)}
                )

        @self.app.get("/usage-metrics")
        async def get_usage_metrics():
            try:
                # Calculate average response time from recent activities
                recent_activities = metrics_data["recent_activity"]
                if recent_activities:
                    total_duration = sum(activity["duration"] for activity in recent_activities if activity["duration"] > 0)
                    valid_activities = len([activity for activity in recent_activities if activity["duration"] > 0])
                    metrics_data["performance_stats"]["average_response_time"] = (
                        total_duration / valid_activities if valid_activities > 0 else 0
                    )
                
                return JSONResponse(content=metrics_data)
                
            except Exception as e:
                return JSONResponse(
                    status_code=500,
                    content={"error": str(e)}
                )

def create_app():
    api = MetricsAPI()
    return api.app

if __name__ == "__main__":
    app = create_app()
    uvicorn.run(app, host="127.0.0.1", port=8001)