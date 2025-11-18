#!/usr/bin/env python3
"""
Main entry point for the Sales Agent Crew backend.
This file combines all API services into a single application.
"""

import uvicorn
from api.lead_generation_api import create_app as create_lead_app
from api.financial_analysis_api import create_app as create_finance_app
from api.metrics_api import create_app as create_metrics_app
from fastapi import FastAPI
import asyncio
import threading
import time

# Create main FastAPI app
app = FastAPI(title="Sales Agent Crew API", version="1.0.0")

# Mount individual API apps
app.mount("/api/leads", create_lead_app())
app.mount("/api/finance", create_finance_app())
app.mount("/api/metrics", create_metrics_app())

@app.get("/")
async def root():
    return {
        "message": "Sales Agent Crew API",
        "version": "1.0.0",
        "endpoints": {
            "lead_generation": "/api/leads/generate-leads",
            "financial_analysis": "/api/finance/financial-analysis",
            "metrics": "/api/metrics/usage-metrics"
        }
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "Sales Agent Crew API"}

def run_metrics_server():
    """Run metrics API on a separate port"""
    from api.metrics_api import create_app
    metrics_app = create_app()
    uvicorn.run(metrics_app, host="127.0.0.1", port=8001, log_level="info")

def run_finance_server():
    """Run finance API on a separate port"""
    from api.financial_analysis_api import create_app
    finance_app = create_app()
    uvicorn.run(finance_app, host="127.0.0.1", port=8002, log_level="info")

def run_lead_server():
    """Run lead generation API on a separate port"""
    from api.lead_generation_api import create_app
    lead_app = create_app()
    uvicorn.run(lead_app, host="127.0.0.1", port=8003, log_level="info")

if __name__ == "__main__":
    # Start individual servers in separate threads
    import threading
    
    # Start metrics server
    metrics_thread = threading.Thread(target=run_metrics_server)
    metrics_thread.daemon = True
    metrics_thread.start()
    
    # Start finance server
    finance_thread = threading.Thread(target=run_finance_server)
    finance_thread.daemon = True
    finance_thread.start()
    
    # Start lead server
    lead_thread = threading.Thread(target=run_lead_server)
    lead_thread.daemon = True
    lead_thread.start()
    
    # Give servers time to start
    time.sleep(2)
    
    # Start main app
    print("Starting Sales Agent Crew API servers...")
    print("Metrics API: http://127.0.0.1:8001")
    print("Finance API: http://127.0.0.1:8002")
    print("Lead API: http://127.0.0.1:8003")
    print("Main API: http://127.0.0.1:8000")
    
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")